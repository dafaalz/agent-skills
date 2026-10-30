#!/usr/bin/env python3
"""
T3 Adversarial Call Path Dispatcher (Operational Integrity Guardrail)
Location: ~/Library/Application Support/t3/bin/t3_dispatch.py

PURPOSE:
Enforces operational discipline, pre-flight contract boundaries, and anti-friction guardrails
for autonomous agents executing under T3 Code / Antigravity.
NOTE: This is an operational reliability and anti-friction guardrail, NOT a kernel-level
host security sandbox.
"""
import sys
import os
import shlex
import re
import json
import hashlib
import subprocess
import fnmatch
import fcntl
from pathlib import Path

# De-collided Exit Codes (70-89: exactly 20 codes)
EC_SHELL_META = 70
EC_EMPTY_CMD = 71
EC_DENIED_BINARY = 72
EC_GIT_BYPASS_FLAGS = 73
EC_GIT_FORBIDDEN_SUB = 74
EC_DESTRUCTIVE_APPROVAL = 75
EC_SECRET_PATH_ACCESS = 76
EC_ENV_DUMP = 77
EC_ROUTER_CIRCUIT_OPEN = 78
EC_FILE_OUTSIDE_TARGETS = 79
EC_CONTROL_ARTIFACT_TAMPER = 80
EC_WORKTREE_CONFLICT = 81
EC_MANIFEST_HASH_MISMATCH = 82
EC_MODEL_UNAVAILABLE = 83
EC_BRIEF_INVALID_SESSION = 84
EC_BRIEF_TRAVERSAL = 85
EC_BRIEF_MISSING_ANCHOR = 86
EC_BRIEF_UNAUTHORIZED_TOOL = 87
EC_BRIEF_SYMLINK = 88
EC_LOOP_BUDGET_EXCEEDED = 89

SHELL_META = [";", "&&", "||", "&", "`", "$(", "|", ">", "<", "\n", "\r"]

# Binaries prohibited from raw invocation
DENY_BINARIES = {
    "bash", "sh", "zsh", "ksh", "csh", "eval", "exec", "command", "builtin", "source", ".",
    "python", "python3", "perl", "ruby", "osascript", "find", "xargs",
    "chflags", "chmod", "chown", "install", "dd", "ln", "mv", "cp", "tee", "truncate",
    "awk", "busybox", "nohup", "nice", "timeout", "watch", "script",
    "screen", "tmux", "socat", "nc", "ssh", "curl", "wget", "security"
}

# Operational boundaries for PHP Artisan (Non-security task scope guardrail)
ALLOWED_PHP_ARTISAN = {
    ("test",),
    ("route:list",),
    ("about",),
    ("config:show",),
    ("model:show",),
    ("migrate", "--pretend")
}

# Operational boundaries for NPM Scripts
ALLOWED_NPM_RUN = {"build", "lint", "test"}

# Safe non-destructive Git subcommands
ALLOWED_GIT_SAFE = {"status", "diff", "log", "add", "checkout", "branch", "commit"}

# Token-gated destructive Git operations (Requires HMAC token signed by human and bound to exact command)
TOKEN_GATED_GIT_SUBCOMMANDS = {"push", "reset"}

# Flag-level destructive operations & config override injections (EC 73)
DESTRUCTIVE_GIT_FLAGS = {
    # Worktree discard / force / branch reset & delete
    "--discard-changes",
    "--amend",
    "-D",
    "-d",
    "--delete",
    "--move",
    "-c",
    "-C",
    "--copy",
    "-fd",
    "-fdx",
    "-f",
    "--force",
    "--no-verify",
    "--bare",
    "--paginate",
    "--show-signature",
    "--include",
    # Arbitrary commit input / editor bypass / template / signing
    "-F",
    "--file",
    "-t",
    "--template",
    "--fixup",
    "--squash",
    "--reset-author",
    "-S",
    "--gpg-sign",
    # Diff arbitrary file read / arbitrary file write
    "--no-index",
    "--ext-diff",
}

# Dangerous git configuration keys / options in arguments (normalized check)
DANGEROUS_CONFIG_PATTERNS = [
    "fsmonitor",
    "sshcommand",
    "credential.helper",
    "diff.external",
    "diff.",
    "textconv",
    "filter.",
    "merge.",
    "attributesfile",
    "excludesfile",
    "include.path",
    "includeif",
    "difffilter",
    "core.pager",
    "core.editor",
    "alias.",
    "commit.template",
    "sequence.editor",
    "submodule.recurse",
    "pager.",
    "askpass",
    "gpg.program",
    "insteadof",
    "pushinsteadof",
    "--ext-diff",
    "--no-index",
    "--output",
    "--gpg-sign",
    "--git-dir",
    "--work-tree",
    "--paginate",
    "--show-signature",
    "--include",
]

# Prohibited Git subcommands (EC 74)
DENY_GIT_SUBCOMMANDS = {
    "remote", "clone", "fetch", "tag", "config", "worktree",
    "update-ref", "reflog", "alias", "filter-branch",
    "clean", "gc", "prune", "replace", "stash", "restore", "switch"
}

DENY_ENV_PREFIX_REGEX = re.compile(r'(?:^|\s)GIT_[A-Za-z0-9_]*=')

DENY_READ_CMDS = {"env", "printenv", "set", "export"}

T3_ROOT = Path.home() / "Library/Application Support/t3"

SECRET_PATHS = (
    ".env", "id_rsa", ".pem", ".key",
    "aws/credentials", ".netrc", ".git-credentials", ".ssh",
    ".config/gh", ".docker/config", ".npmrc", ".pypirc",
    "config/database.php", "config/app.php", "config/secrets.yml",
    "wp-config.php", "app/etc/env.php",
    str(Path.home() / ".gitconfig"),
    str(Path.home() / ".config/git/config"),
    str(T3_ROOT / "tokens"),
    str(T3_ROOT / "sessions"),
    str(T3_ROOT / "ledgers")
)


def get_repo_root() -> Path:
    try:
        # Harden rev-parse by scrubbing environment and overriding git hooks (R-1)
        safe_env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
        safe_env["GIT_CONFIG_NOSYSTEM"] = "1"
        safe_env["GIT_CONFIG_GLOBAL"] = "/dev/null"
        safe_env["GIT_ATTR_NOSYSTEM"] = "1"
        res = subprocess.run(
            ["git", "-c", "core.hooksPath=/dev/null", "rev-parse", "--show-toplevel"],
            capture_output=True,
            text=True,
            check=True,
            env=safe_env
        )
        out = res.stdout.strip()
        if out:
            return Path(out).resolve()
    except Exception:
        pass
    cur = Path.cwd().resolve()
    for p in [cur] + list(cur.parents):
        if (p / ".git").exists():
            return p
    return cur


def is_path_in_targets(candidate_path: str, allowed_targets: list) -> bool:
    # Fail-closed: An unmanifested operation or missing targets must never pass (S-2)
    if not allowed_targets:
        return False

    repo_root = get_repo_root()

    try:
        cand_p = Path(candidate_path).expanduser()
        if cand_p.is_absolute():
            cand_resolved = cand_p.resolve()
        else:
            cand_resolved = (Path.cwd().resolve() / cand_p).resolve()
    except Exception:
        cand_resolved = Path(candidate_path).absolute()

    for t in allowed_targets:
        try:
            tp = Path(t).expanduser()
            if tp.is_absolute():
                t_resolved = tp.resolve()
            else:
                t_resolved = (repo_root / tp).resolve()
        except Exception:
            t_resolved = (repo_root / str(t)).resolve()

        # Component-wise exact resolved match
        if cand_resolved == t_resolved:
            return True

        # If target is explicitly a directory, allow directory containment
        if str(t).endswith("/") or (t_resolved.exists() and t_resolved.is_dir()):
            if t_resolved in cand_resolved.parents:
                return True

        # Relative component-wise comparison against repo_root (S-3)
        try:
            cand_rel = cand_resolved.relative_to(repo_root)
            t_rel = t_resolved.relative_to(repo_root)
            if cand_rel == t_rel:
                return True
            if str(t).endswith("/") and cand_rel.parts[:len(t_rel.parts)] == t_rel.parts:
                return True
        except (ValueError, Exception):
            pass

    return False

def normalize_backup_path(raw_path: str) -> str:
    """
    Normalizes paths by stripping lockfiles (~$), prefix tildes (~), trailing dots,
    and iterative backup extensions (.bak, .orig, .swp, ~, .old, .tmp, .save, .backup). (C-R18-1)
    Note on ~user (C-R18-2): Tildes at the start of path segments are stripped defensively
    as potential backup markers; POSIX ~user home directory expansion is intentionally
    not evaluated here in favor of strict, safe-direction path matching.
    Note on ~+ / ~- (C-R18-3): Shell directory stack tokens (~+, ~-) are not expanded
    by Python's Path.expanduser() and remain unexpanded literals.
    """
    s = raw_path.strip().rstrip(".")
    parts = s.split("/")
    clean_parts = []
    for part in parts:
        # Iterative prefix strip for ~$ and ~ (C-R19-1)
        p_changed = True
        while p_changed:
            p_changed = False
            if part.startswith("~$"):
                part = part[2:]
                p_changed = True
            elif part.startswith("~") and len(part) > 1:
                part = part[1:]
                p_changed = True
        clean_parts.append(part)
    s = "/".join(clean_parts).rstrip(".")

    ext_list = (".bak", ".orig", ".swp", "~", ".old", ".tmp", ".save", ".backup")
    changed = True
    while changed:
        changed = False
        s = s.rstrip(".")
        for ext in ext_list:
            if s.endswith(ext):
                s = s[:-len(ext)].rstrip(".")
                changed = True
                break
    return s

def is_secret_path(p: str) -> bool:
    clean_p = p.strip()
    # Strip git pathspec magic prefixes like :(glob)path, :(attr:...)path, :!path, :^path, :/path, :path (S-N1)
    if clean_p.startswith(":(") and ")" in clean_p:
        clean_p = clean_p.split(")", 1)[1].strip()
    elif clean_p.startswith((":!", ":^", ":/")):
        clean_p = clean_p[2:].strip()
    elif clean_p.startswith(":"):
        clean_p = clean_p.lstrip(":").strip()
    elif ":" in clean_p:
        clean_p = clean_p.split(":")[-1]

    if clean_p.startswith("--"):
        clean_p = clean_p.lstrip("-").strip()
    clean_lower = clean_p.lower()

    stripped_p = normalize_backup_path(clean_lower)
    candidates = [clean_lower]
    if stripped_p != clean_lower:
        candidates.append(stripped_p)

    for cand in candidates:
        for sec in SECRET_PATHS:
            s_low = sec.lower()
            if cand == s_low:
                return True
            if cand.endswith("/" + s_low) or cand.startswith(s_low + "/") or ("/" + s_low + "/") in cand:
                return True
            base_name = cand.split("/")[-1]
            if base_name == s_low or base_name.startswith(s_low + "."):
                return True
            if s_low.startswith(".") and cand.endswith(s_low) and (" " not in cand):
                return True
            # Glob matching (fnmatch) for wildcard pathspecs (e.g. config/*.php, *.env) (S-N1)
            if ("*" in cand or "?" in cand or "[" in cand) and cand not in {"*", ".*", "**"}:
                if fnmatch.fnmatch(s_low, cand) or fnmatch.fnmatch(s_low.split("/")[-1], cand):
                    return True
                if "/" in s_low and fnmatch.fnmatch(s_low, "*/" + cand.lstrip("/")):
                    return True

    try:
        # Note on Home configs (C-R20-3): ~/.gitconfig and ~/.config/git/config rely on
        # Path.expanduser().resolve() equality matching against SECRET_PATHS. Write mutations
        # are intercepted with EC 80 priority in validate_file_tool() via is_control_path().
        resolved = Path(clean_p).expanduser().resolve()
        rp_lower = str(resolved).lower()
        res_candidates = [rp_lower]
        stripped_rp = normalize_backup_path(rp_lower)
        if stripped_rp != rp_lower:
            res_candidates.append(stripped_rp)

        for rc in res_candidates:
            for sec in SECRET_PATHS:
                s_low = sec.lower()
                if rc == s_low or rc.endswith("/" + s_low) or ("/" + s_low + "/") in rc:
                    return True
    except Exception:
        pass
    return False

def is_control_path(p: str) -> bool:
    try:
        resolved = Path(p).expanduser().resolve()
    except Exception:
        resolved = Path(p).absolute()

    t3_root = T3_ROOT.resolve()
    if resolved == t3_root or t3_root in resolved.parents:
        return True

    # User global git configs (S-7)
    user_gitconfig = (Path.home() / ".gitconfig").resolve()
    user_gitdir = (Path.home() / ".config/git").resolve()
    if resolved == user_gitconfig or resolved == user_gitdir or user_gitdir in resolved.parents:
        return True

    # Check path parts
    parts = set(resolved.parts)
    if any(ctrl_dir in parts for ctrl_dir in {".git", ".github", "node_modules", ".agents"}):
        return True

    # Specifically protect agent verification receipts and state ledgers (.agents/state/)
    str_resolved = str(resolved).lower()
    if ".agents/state" in str_resolved or "/.agents/state" in str_resolved:
        return True

    # Check exact basename (S-5: precise matching, no over-broad substring matches)
    basename = resolved.name.lower()
    exact_control_files = {
        "task-manifest.json", "t3_dispatch.py", "t3_acp_gateway.py",
        "t3_approval.py", "t3-brief-lint.py", "t3_router.py", "t3_worktree_queue.py",
        "trusted_root_hashes.json", "enforcement-evidence.json", ".pinned_last_hash",
        "package.json", ".gitattributes", ".gitignore",
        "verification-receipt.json", "receipt-hash.txt", "iteration_counter.json"
    }
    if basename in exact_control_files:
        return True

    if basename.startswith("test_") and "tests" in parts:
        return True

    return False

# Hard execution-loop budget cap per session to prevent unbudgeted agent loops
MAX_SESSION_ITERATIONS = 250

def check_iteration_budget(session_id: str, max_iterations: int = MAX_SESSION_ITERATIONS):
    """
    Enforces a hard numeric iteration limit per session using atomic file locking (fcntl.flock).
    Trips fail-closed (EC 89) if total dispatched tool calls exceed max_iterations.
    """
    if not session_id or session_id == "default":
        return
    budget_file = T3_ROOT / f"sessions/{session_id}/iteration_counter.json"
    budget_file.parent.mkdir(parents=True, exist_ok=True)
    with open(budget_file, "a+") as f:
        fcntl.flock(f.fileno(), fcntl.LOCK_EX)
        try:
            f.seek(0)
            content = f.read().strip()
            count = 0
            if content:
                try:
                    count = json.loads(content).get("iteration_count", 0)
                except Exception:
                    count = 0
            count += 1
            if count > max_iterations:
                sys.stderr.write(f"[DISPATCH DENIED 89] Hard execution-loop budget exceeded: {count} > {max_iterations}\n")
                sys.exit(EC_LOOP_BUDGET_EXCEEDED)
            f.seek(0)
            f.truncate()
            f.write(json.dumps({"iteration_count": count, "max_iterations": max_iterations}) + "\n")
            f.flush()
            os.fsync(f.fileno())
        finally:
            fcntl.flock(f.fileno(), fcntl.LOCK_UN)

def check_approval_token(session_id: str, action: str) -> bool:
    approval_bin = T3_ROOT / "bin/t3_approval.py"
    if not approval_bin.exists():
        return False
    res = subprocess.run([sys.executable, str(approval_bin), "verify", session_id, action], capture_output=True)
    return res.returncode == 0

def verify_runtime_attestation():
    trusted_file = T3_ROOT / "ledgers/trusted_root_hashes.json"
    if not trusted_file.exists():
        sys.stderr.write("[DISPATCH DENIED 80] Missing trusted root attestation ledger: FAIL-CLOSED.\n")
        sys.exit(EC_CONTROL_ARTIFACT_TAMPER)
    try:
        with open(trusted_file, "r") as f:
            trusted_data = json.load(f)
        hashes = trusted_data.get("bin_hashes", {})
        if not hashes:
            sys.stderr.write("[DISPATCH DENIED 80] Empty trusted root attestation ledger: FAIL-CLOSED.\n")
            sys.exit(EC_CONTROL_ARTIFACT_TAMPER)
        for fname, exp_hash in hashes.items():
            fpath = T3_ROOT / "bin" / fname
            if not fpath.exists():
                sys.stderr.write(f"[DISPATCH DENIED 80] Control binary missing: {fname}\n")
                sys.exit(EC_CONTROL_ARTIFACT_TAMPER)
            cur_hash = hashlib.sha256(fpath.read_bytes()).hexdigest()
            if cur_hash != exp_hash:
                sys.stderr.write(f"[DISPATCH DENIED 80] Control binary runtime integrity violation: {fname}\n")
                sys.exit(EC_CONTROL_ARTIFACT_TAMPER)
    except Exception as e:
        sys.stderr.write(f"[DISPATCH DENIED 80] Attestation root check failure: {e}\n")
        sys.exit(EC_CONTROL_ARTIFACT_TAMPER)

def check_config_file_hygiene(cfg_path: Path):
    if not cfg_path.exists():
        return
    prohibited_sections = {
        "filter", "diff", "merge", "include", "includeif",
        "pager", "gpg", "url", "credential", "alias", "transfer", "protocol"
    }
    prohibited_keys = [
        "textconv", "diff.", "filter.", "merge.", "include.path", "includeif",
        "sshcommand", "fsmonitor", "pager.", "gpg.program", "credential.helper",
        "insteadof", "pushinsteadof", "uploadpack", "receivepack", "askpass"
    ]
    try:
        raw = cfg_path.read_text(encoding="utf-8", errors="replace").lower()
        for line in raw.splitlines():
            line = line.strip()
            if not line or line.startswith("#") or line.startswith(";"):
                continue
            if line.startswith("["):
                sec_name = line.strip("[] ").lower()
                if any(p in sec_name for p in prohibited_sections):
                    sys.stderr.write(f"[DISPATCH DENIED 73] Prohibited INI section in {cfg_path}: [{sec_name}]\n")
                    sys.exit(EC_GIT_BYPASS_FLAGS)
            else:
                for pat in prohibited_keys:
                    if pat in line:
                        sys.stderr.write(f"[DISPATCH DENIED 73] Prohibited config entry in {cfg_path}: {line}\n")
                        sys.exit(EC_GIT_BYPASS_FLAGS)
    except Exception as e:
        sys.stderr.write(f"[DISPATCH DENIED 73] Failed reading git config at {cfg_path}: {e}\n")
        sys.exit(EC_GIT_BYPASS_FLAGS)

def check_git_repo_hygiene():
    cur = Path.cwd()
    git_dir = None
    common_dir = None

    for p in [cur] + list(cur.parents):
        cand = p / ".git"
        if cand.is_dir():
            git_dir = cand
            common_dir = cand
            break
        elif cand.is_file():
            # Worktree or submodule pointer
            try:
                line = cand.read_text(encoding="utf-8").strip()
                if line.startswith("gitdir:"):
                    raw_path = line[7:].strip()
                    wt_gitdir = Path(raw_path)
                    if not wt_gitdir.is_absolute():
                        wt_gitdir = (cand.parent / wt_gitdir).resolve()
                    git_dir = wt_gitdir
                    commondir_file = wt_gitdir / "commondir"
                    if commondir_file.exists():
                        c_raw = commondir_file.read_text(encoding="utf-8").strip()
                        c_path = Path(c_raw)
                        if not c_path.is_absolute():
                            common_dir = (wt_gitdir / c_path).resolve()
                        else:
                            common_dir = c_path
                    else:
                        common_dir = wt_gitdir
                    break
            except Exception as e:
                sys.stderr.write(f"[DISPATCH DENIED 73] Failed resolving .git worktree pointer: {e}\n")
                sys.exit(EC_GIT_BYPASS_FLAGS)

    configs_to_check = set()
    if git_dir:
        configs_to_check.add(git_dir / "config")
        configs_to_check.add(git_dir / "config.worktree")
    if common_dir and common_dir != git_dir:
        configs_to_check.add(common_dir / "config")

    # Check user global git configs (S-7)
    configs_to_check.add(Path.home() / ".gitconfig")
    configs_to_check.add(Path.home() / ".config/git/config")

    for cfg in configs_to_check:
        check_config_file_hygiene(cfg)

    # Check .git/info/attributes
    info_attrs_files = set()
    if git_dir:
        info_attrs_files.add(git_dir / "info/attributes")
    if common_dir:
        info_attrs_files.add(common_dir / "info/attributes")

    for ia in info_attrs_files:
        if ia.exists():
            try:
                c = ia.read_text(encoding="utf-8", errors="replace").lower()
                for pat in ["diff=", "filter=", "merge=", "textconv"]:
                    if pat in c:
                        sys.stderr.write(f"[DISPATCH DENIED 73] {ia} contains unapproved driver pattern: {pat}\n")
                        sys.exit(EC_GIT_BYPASS_FLAGS)
            except Exception as e:
                sys.stderr.write(f"[DISPATCH DENIED 73] Failed reading attributes at {ia}: {e}\n")
                sys.exit(EC_GIT_BYPASS_FLAGS)

    # Recursive scan for all in-tree .gitattributes (F-2)
    try:
        for attr_file in Path.cwd().rglob(".gitattributes"):
            if ".git" in attr_file.parts:
                continue
            try:
                c = attr_file.read_text(encoding="utf-8", errors="replace").lower()
                for pat in ["diff=", "filter=", "merge=", "textconv"]:
                    if pat in c:
                        sys.stderr.write(f"[DISPATCH DENIED 73] In-tree {attr_file} contains unapproved driver pattern: {pat}\n")
                        sys.exit(EC_GIT_BYPASS_FLAGS)
            except Exception as e:
                sys.stderr.write(f"[DISPATCH DENIED 73] Failed reading in-tree attributes at {attr_file}: {e}\n")
                sys.exit(EC_GIT_BYPASS_FLAGS)
    except Exception as e:
        sys.stderr.write(f"[DISPATCH DENIED 73] Failed recursive .gitattributes search: {e}\n")
        sys.exit(EC_GIT_BYPASS_FLAGS)

def validate_command(cmd_str: str, session_id: str = "default", allowed_targets: list = None) -> list:
    verify_runtime_attestation()
    check_iteration_budget(session_id)

    if not cmd_str or not cmd_str.strip():
        sys.stderr.write("[DISPATCH DENIED 71] Empty command.\n")
        sys.exit(EC_EMPTY_CMD)

    raw_clean = cmd_str.strip()

    # 1. Environment override prefixes check (EC 73)
    if DENY_ENV_PREFIX_REGEX.search(raw_clean):
        sys.stderr.write("[DISPATCH DENIED 73] Git environment override prohibited.\n")
        sys.exit(EC_GIT_BYPASS_FLAGS)

    # Scrub GIT_ environment variables if present
    for k in list(os.environ.keys()):
        if k.startswith("GIT_"):
            del os.environ[k]

    # 2. Parse argv via shlex safely
    try:
        argv = shlex.split(raw_clean)
    except Exception as e:
        sys.stderr.write(f"[DISPATCH DENIED 70] Shlex parsing failure: {e}\n")
        sys.exit(EC_SHELL_META)

    if not argv:
        sys.stderr.write("[DISPATCH DENIED 71] Empty parsed argv.\n")
        sys.exit(EC_EMPTY_CMD)

    bin_name = os.path.basename(argv[0])

    # 3. Denied binary check (EC 72)
    if bin_name in DENY_BINARIES:
        sys.stderr.write(f"[DISPATCH DENIED 72] Denied binary or interpreter class: {bin_name}\n")
        sys.exit(EC_DENIED_BINARY)

    # 4. PHP Interpreter Subcommand Guardrail (EC 72)
    if bin_name == "php":
        if len(argv) < 3 or argv[1] != "artisan":
            sys.stderr.write("[DISPATCH DENIED 72] Raw php or unapproved script execution prohibited.\n")
            sys.exit(EC_DENIED_BINARY)
        sub_tuple = tuple(argv[2:])
        matched = False
        for allowed in ALLOWED_PHP_ARTISAN:
            if len(sub_tuple) >= len(allowed) and sub_tuple[:len(allowed)] == allowed:
                matched = True
                break
        if not matched:
            sys.stderr.write(f"[DISPATCH DENIED 72] PHP artisan subcommand '{' '.join(argv[2:4])}' not on operational allowlist.\n")
            sys.exit(EC_DENIED_BINARY)

    # 5. Node & NPM Operational Guardrail (EC 72)
    if bin_name == "node":
        if len(argv) < 2 or os.path.basename(argv[1]) != "oxlint":
            sys.stderr.write("[DISPATCH DENIED 72] Raw node interpreter or unapproved script prohibited.\n")
            sys.exit(EC_DENIED_BINARY)
    elif bin_name == "npm":
        if len(argv) < 3 or argv[1] != "run" or argv[2] not in ALLOWED_NPM_RUN:
            sys.stderr.write(f"[DISPATCH DENIED 72] NPM script '{' '.join(argv[1:])}' not on operational allowlist.\n")
            sys.exit(EC_DENIED_BINARY)

    # 6. Direct Environment Variable Dump Command Rejection (EC 77)
    if bin_name in DENY_READ_CMDS:
        sys.stderr.write(f"[DISPATCH DENIED 77] Environment dump command prohibited: {bin_name}\n")
        sys.exit(EC_ENV_DUMP)

    # 7. Check for dangerous chaining metacharacters (EC 70)
    for ch in SHELL_META:
        if ch in raw_clean:
            sys.stderr.write(f"[DISPATCH DENIED 70] Shell metacharacter or chaining detected: {ch}\n")
            sys.exit(EC_SHELL_META)

    # Determine Git subcommand and all commit message token indices (R-2 & C-2)
    git_sub = None
    commit_msg_indices: set = set()
    if bin_name == "git":
        all_known_git = ALLOWED_GIT_SAFE | TOKEN_GATED_GIT_SUBCOMMANDS | DENY_GIT_SUBCOMMANDS
        for a in argv[1:]:
            if not a.startswith("-") and a in all_known_git:
                git_sub = a
                break
        if not git_sub:
            for a in argv[1:]:
                if not a.startswith("-"):
                    git_sub = a
                    break

        if git_sub == "commit":
            try:
                sub_idx = argv.index("commit")
            except ValueError:
                sub_idx = 0
            skip_c = False
            for idx in range(sub_idx + 1, len(argv)):
                if skip_c:
                    skip_c = False
                    continue
                tok = argv[idx]
                if tok in {"-m", "--message"}:
                    if idx + 1 < len(argv):
                        commit_msg_indices.add(idx + 1)
                        skip_c = True
                elif tok.startswith("--message="):
                    commit_msg_indices.add(idx)

    # 8. Check ALL arguments for secret paths (EC 76) & control path mutation (EC 80)
    for idx, arg in enumerate(argv[1:], start=1):
        if bin_name == "git" and git_sub == "commit" and idx in commit_msg_indices:
            # Commit message strings are exempt from secret/control path name collision check (C-2)
            continue

        if is_secret_path(arg):
            sys.stderr.write(f"[DISPATCH DENIED 76] Secret path access prohibited in argument: {arg}\n")
            sys.exit(EC_SECRET_PATH_ACCESS)
        if is_control_path(arg):
            sys.stderr.write(f"[DISPATCH DENIED 80] Tampering with control path in command prohibited: {arg}\n")
            sys.exit(EC_CONTROL_ARTIFACT_TAMPER)

    # 9. Granular Git Invariant, Flag-Level, Combined-Form, and Destructive Checks
    if bin_name == "git":
        check_git_repo_hygiene()
        # Scan every argument token in argv[1:] EXCEPT commit message values (F-1 & C-2 Remediation)
        for idx, a in enumerate(argv[1:], start=1):
            if git_sub == "commit" and idx in commit_msg_indices:
                # Commit message values are checked inside sub == "commit", not in the global flag scanner
                continue

            a_lower = a.lower().strip()

            # A. Combined-form single-token prefixes rejection (S-1 & Cos-N2 Remediation)
            if len(a) > 2 and (a.startswith("-c") or a.startswith("-C") or a.startswith("-B") or a.startswith("-S") or a.startswith("-F")):
                sys.stderr.write(f"[DISPATCH DENIED 73] Prohibited single-token short Git flag: {a}\n")
                sys.exit(EC_GIT_BYPASS_FLAGS)

            # Check for exotic pathspec magic prefixes (S-N1 Residual Closed)
            if a.startswith(":(") or a.startswith(":!") or a.startswith(":^") or a.startswith(":/"):
                sys.stderr.write(f"[DISPATCH DENIED 74] Git pathspec magic prefix prohibited: {a}\n")
                sys.exit(EC_GIT_FORBIDDEN_SUB)

            combined_long_prefixes = (
                "--exec-path", "--config-env", "--git-dir", "--work-tree",
                "--namespace", "--attr-source", "--output", "--gpg-sign",
                "--super-prefix", "--literal-pathspecs", "--glob-pathspecs",
                "--noglob-pathspecs", "--icase-pathspecs"
            )
            for lpref in combined_long_prefixes:
                if a == lpref or a.startswith(lpref + "="):
                    sys.stderr.write(f"[DISPATCH DENIED 73] Prohibited Git redirection/override option: {a}\n")
                    sys.exit(EC_GIT_BYPASS_FLAGS)

            # B. Destructive and bypass flags
            for flg in DESTRUCTIVE_GIT_FLAGS:
                if a == flg or a.startswith(flg + "="):
                    sys.stderr.write(f"[DISPATCH DENIED 73] Destructive or bypass Git flag prohibited: {a}\n")
                    sys.exit(EC_GIT_BYPASS_FLAGS)

            # C. Normalized config-driven execution patterns (S-2 & S-3 Remediation)
            for pat in DANGEROUS_CONFIG_PATTERNS:
                if pat in a_lower:
                    sys.stderr.write(f"[DISPATCH DENIED 73] Dangerous Git config/helper pattern prohibited: {a}\n")
                    sys.exit(EC_GIT_BYPASS_FLAGS)

        subcommands = [a for a in argv[1:] if not a.startswith("-")]
        if not subcommands and not git_sub:
            sys.stderr.write("[DISPATCH DENIED 74] Git missing subcommand.\n")
            sys.exit(EC_GIT_FORBIDDEN_SUB)

        sub = git_sub if git_sub else subcommands[0]

        # Explicitly denied dangerous subcommands (EC 74)
        if sub in DENY_GIT_SUBCOMMANDS:
            sys.stderr.write(f"[DISPATCH DENIED 74] Git dangerous subcommand prohibited: {sub}\n")
            sys.exit(EC_GIT_FORBIDDEN_SUB)

        # Enforcing configs neutralizing hooks, editors, pagers, textconv, filters, includes
        enforcing_configs = [
            "-c", "core.hooksPath=/dev/null",
            "-c", "core.editor=true",
            "-c", "core.pager=cat",
            "-c", "pager.status=cat",
            "-c", "pager.diff=cat",
            "-c", "pager.log=cat",
            "-c", "pager.branch=cat",
            "-c", "pager.show=cat",
            "-c", "diff.external=",
            "-c", "core.fsmonitor=",
            "-c", "credential.helper=",
            "-c", "core.sshCommand=true",
            "-c", "commit.gpgSign=false",
            "-c", "gpg.program=true",
            "-c", "core.askPass=true",
            "-c", "core.attributesFile=/dev/null",
            "-c", "core.excludesFile=/dev/null",
            "-c", "commit.template=",
            "-c", "sequence.editor=true",
            "-c", "interactive.diffFilter=cat",
            "-c", "submodule.recurse=false",
            "-c", "diff.textconv=",
            "-c", "merge.driver=",
            "-c", "filter.lfs.smudge=",
            "-c", "filter.lfs.clean=",
            "-c", "filter.lfs.process=",
            "-c", "filter.lfs.required=false",
            "-c", "include.path=",
        ]

        # Flag-level protection on checkout, branch, commit, add, diff, log
        if sub == "checkout":
            rest = argv[argv.index("checkout") + 1:]
            for a in rest:
                if a in {".", "..", "--", "HEAD", "-B"} or a.startswith("-f") or a == "--force" or a.startswith("-B"):
                    sys.stderr.write(f"[DISPATCH DENIED 74] Destructive worktree discard or branch reset via git checkout prohibited: {a}\n")
                    sys.exit(EC_GIT_FORBIDDEN_SUB)
            if any(a == "--" for a in rest):
                sys.stderr.write("[DISPATCH DENIED 74] Worktree checkout with pathspec delimiter prohibited.\n")
                sys.exit(EC_GIT_FORBIDDEN_SUB)

            non_flag_args = [a for a in rest if not a.startswith("-")]
            flag_args = [a for a in rest if a.startswith("-")]

            if any(f != "-b" for f in flag_args):
                sys.stderr.write(f"[DISPATCH DENIED 74] Unauthorized checkout flag: {flag_args}\n")
                sys.exit(EC_GIT_FORBIDDEN_SUB)

            if len(non_flag_args) != 1:
                sys.stderr.write(f"[DISPATCH DENIED 74] Checkout requires exactly 1 branch target, got: {non_flag_args}\n")
                sys.exit(EC_GIT_FORBIDDEN_SUB)

            target = non_flag_args[0]
            # Discriminate file on disk or traversal from valid branch name
            common_file_exts = (".md", ".py", ".json", ".txt", ".js", ".ts", ".php", ".yml", ".yaml", ".sh", ".html", ".css", ".lock", ".go", ".rs")
            if os.path.exists(target) or ".." in target or target.startswith("/") or target.startswith("./") or target.endswith(common_file_exts):
                sys.stderr.write(f"[DISPATCH DENIED 74] Pathspec checkout prohibited. Branch navigation only: {target}\n")
                sys.exit(EC_GIT_FORBIDDEN_SUB)

            # Valid branch name grammar: alphanumeric, _, -, ., / (e.g. release/1.0, v1.2.3, feature-auth)
            if not re.match(r"^[a-zA-Z0-9_\-\.\/]+$", target) or target.endswith(".git") or "//" in target:
                sys.stderr.write(f"[DISPATCH DENIED 74] Invalid branch naming characters in checkout: {target}\n")
                sys.exit(EC_GIT_FORBIDDEN_SUB)

        elif sub == "branch":
            rest = argv[argv.index("branch") + 1:]
            for a in rest:
                if a in {"-d", "-D", "-m", "-M", "-f", "--force", "--delete", "--move", "-c", "-C"}:
                    sys.stderr.write(f"[DISPATCH DENIED 74] Branch mutation flag prohibited: {a}\n")
                    sys.exit(EC_GIT_FORBIDDEN_SUB)

        elif sub == "commit":
            rest = argv[argv.index("commit") + 1:]
            prohibited_commit_flags = {
                "-a", "--all", "--include", "-i", "-p", "--patch",
                "-e", "--edit", "--interactive", "-o", "--only",
                "--pathspec-from-file", "--pathspec-file-nul"
            }

            has_msg = False
            msg_vals = []
            pathspecs = []
            after_double_dash = False
            skip_cmsg = False

            for i, a in enumerate(rest):
                if skip_cmsg:
                    skip_cmsg = False
                    continue
                if after_double_dash:
                    pathspecs.append(a)
                    continue
                if a == "--":
                    after_double_dash = True
                    continue
                if a in {"-m", "--message"}:
                    if i + 1 < len(rest):
                        has_msg = True
                        msg_vals.append(rest[i + 1])
                        skip_cmsg = True
                    continue
                if a.startswith("--message="):
                    has_msg = True
                    msg_vals.append(a.split("=", 1)[1])
                    continue
                if a.startswith("-m") and len(a) > 2:
                    has_msg = True
                    msg_vals.append(a[2:])
                    continue

                # Flag checks: only for tokens outside message values (C-1 Remediation)
                if (a in prohibited_commit_flags or
                    a == "-a" or
                    a.startswith("-a=") or
                    a == "--all" or
                    a.startswith("--all=") or
                    a.startswith("--include=") or
                    a.startswith("-o=") or
                    a.startswith("--pathspec-from-file=")):
                    sys.stderr.write(f"[DISPATCH DENIED 74] Blanket staging, interactive, or unmanifest flag prohibited on git commit: {a}\n")
                    sys.exit(EC_GIT_FORBIDDEN_SUB)

                if not a.startswith("-"):
                    pathspecs.append(a)

            if not has_msg:
                sys.stderr.write("[DISPATCH DENIED 74] git commit requires explicit -m message; editor spawning prohibited.\n")
                sys.exit(EC_GIT_FORBIDDEN_SUB)

            # Validate any commit pathspecs against manifest targets (S-1)
            if pathspecs:
                for p in pathspecs:
                    if is_control_path(p):
                        sys.stderr.write(f"[DISPATCH DENIED 80] Tampering with control path in commit prohibited: {p}\n")
                        sys.exit(EC_CONTROL_ARTIFACT_TAMPER)
                    if is_secret_path(p):
                        sys.stderr.write(f"[DISPATCH DENIED 76] Secret path access prohibited in commit pathspec: {p}\n")
                        sys.exit(EC_SECRET_PATH_ACCESS)
                    if not is_path_in_targets(p, allowed_targets):
                        sys.stderr.write(f"[DISPATCH DENIED 79] Commit pathspec '{p}' outside manifest target scope: {allowed_targets}\n")
                        sys.exit(EC_FILE_OUTSIDE_TARGETS)

        elif sub == "add":
            rest = argv[argv.index("add") + 1:]
            # Disallow blanket staging, update, patch, and interactive flags (S-2)
            prohibited_add_flags = {
                ".", "-A", "--all", "*", "..",
                "-u", "--update",
                "-p", "--patch",
                "-i", "--interactive",
                "-e", "--edit"
            }
            for a in rest:
                if a in prohibited_add_flags or a.startswith("-u") or a.startswith("-p") or a.startswith("-i"):
                    sys.stderr.write(f"[DISPATCH DENIED 74] Blanket, update, or interactive git add flag prohibited: {a}\n")
                    sys.exit(EC_GIT_FORBIDDEN_SUB)

            explicit_files = [a for a in rest if not a.startswith("-")]
            if not explicit_files:
                sys.stderr.write("[DISPATCH DENIED 74] git add requires explicit target file path.\n")
                sys.exit(EC_GIT_FORBIDDEN_SUB)

            for a in explicit_files:
                if is_control_path(a):
                    sys.stderr.write(f"[DISPATCH DENIED 80] Staging control path prohibited: {a}\n")
                    sys.exit(EC_CONTROL_ARTIFACT_TAMPER)

            # Enforce manifest scope on explicit files (component-wise resolved path, fail-closed on missing targets S-2)
            for a in explicit_files:
                if not is_path_in_targets(a, allowed_targets):
                    sys.stderr.write(f"[DISPATCH DENIED 79] Staged file '{a}' outside manifest target scope: {allowed_targets}\n")
                    sys.exit(EC_FILE_OUTSIDE_TARGETS)

        # In diff, log, show: inject --no-ext-diff and --no-textconv
        extra_subcommand_flags = []
        if sub in {"diff", "log"}:
            extra_subcommand_flags = ["--no-ext-diff", "--no-textconv"]

        if sub == "log":
            rest = argv[argv.index("log") + 1:]
            for i, a in enumerate(rest):
                a_lower = a.lower()
                if a_lower == "--show-signature":
                    sys.stderr.write(f"[DISPATCH DENIED 73] Signature inspection spawner prohibited: {a}\n")
                    sys.exit(EC_GIT_BYPASS_FLAGS)

                if a in {"--format", "--pretty"}:
                    if i + 1 < len(rest) and "%g" in rest[i + 1].lower():
                        sys.stderr.write(f"[DISPATCH DENIED 73] Signature inspection spawner prohibited in format argument: {rest[i + 1]}\n")
                        sys.exit(EC_GIT_BYPASS_FLAGS)

                if a_lower.startswith("--format=") or a_lower.startswith("--pretty=") or a_lower.startswith("--format:") or a_lower.startswith("--pretty:"):
                    if "%g" in a_lower:
                        sys.stderr.write(f"[DISPATCH DENIED 73] Signature inspection spawner prohibited: {a}\n")
                        sys.exit(EC_GIT_BYPASS_FLAGS)

        # Precise argv reconstruction: locate actual subcommand index (S-2)
        sub_idx = argv.index(sub)
        global_flags = argv[1:sub_idx]
        sub_and_args = argv[sub_idx:]
        safe_sub_and_args = [sub_and_args[0]] + extra_subcommand_flags + sub_and_args[1:]

        # Token-gated destructive git operations (EC 75)
        if sub in TOKEN_GATED_GIT_SUBCOMMANDS:
            if not check_approval_token(session_id, raw_clean):
                sys.stderr.write(f"[DISPATCH BLOCKED 75] '{raw_clean}' requires valid human approval token bound to exact command.\n")
                sys.exit(EC_DESTRUCTIVE_APPROVAL)
            safe_argv = [argv[0]] + enforcing_configs + global_flags + safe_sub_and_args
            return safe_argv

        # Safe non-destructive git commands (Allowed)
        if sub in ALLOWED_GIT_SAFE:
            safe_argv = [argv[0]] + enforcing_configs + global_flags + safe_sub_and_args
            return safe_argv

        # Any other unlisted git subcommand -> EC 74
        sys.stderr.write(f"[DISPATCH DENIED 74] Git subcommand prohibited on operational allowlist: {sub}\n")
        sys.exit(EC_GIT_FORBIDDEN_SUB)

    return argv

def validate_file_tool(tool_name: str, file_path: str, allowed_targets: list = None):
    verify_runtime_attestation()
    p = Path(file_path)

    # 1. Symlink rejection at runtime (EC 80)
    if p.is_symlink():
        sys.stderr.write(f"[DISPATCH DENIED 80] Symlink target rejected: {file_path}\n")
        sys.exit(EC_CONTROL_ARTIFACT_TAMPER)

    # 2. T3 internal control artifacts (ledgers, tokens) are always EC 80
    t3_root_str = str(T3_ROOT.resolve()).lower()
    try:
        rp_str = str(p.expanduser().resolve()).lower()
    except Exception:
        rp_str = str(p.absolute()).lower()
    if t3_root_str in rp_str:
        sys.stderr.write(f"[DISPATCH DENIED 80] Control artifact access prohibited: {file_path}\n")
        sys.exit(EC_CONTROL_ARTIFACT_TAMPER)

    # 3. Mutation tools strictly block all control paths (EC 80)
    if tool_name in ["edit_file", "create_file", "fs/write_text_file"]:
        if is_control_path(file_path):
            sys.stderr.write(f"[DISPATCH DENIED 80] Tampering with control artifact prohibited: {file_path}\n")
            sys.exit(EC_CONTROL_ARTIFACT_TAMPER)

    # 4. Secret path protection for reads and mutations (EC 76)
    if is_secret_path(file_path):
        sys.stderr.write(f"[DISPATCH DENIED 76] Access to secret path prohibited: {file_path}\n")
        sys.exit(EC_SECRET_PATH_ACCESS)

    # 5. Fallback control path check for read tools
    if is_control_path(file_path):
        sys.stderr.write(f"[DISPATCH DENIED 80] Tampering with control artifact prohibited: {file_path}\n")
        sys.exit(EC_CONTROL_ARTIFACT_TAMPER)

    # 4. Enforce Task Target Scope for mutation tools (EC 79, fail-closed on missing targets S-2)
    if tool_name in ["edit_file", "create_file", "fs/write_text_file"]:
        if not is_path_in_targets(file_path, allowed_targets):
            sys.stderr.write(f"[DISPATCH DENIED 79] Target '{file_path}' outside manifest scope: {allowed_targets}\n")
            sys.exit(EC_FILE_OUTSIDE_TARGETS)

def validate_network_tool(tool_name: str, payload: str, allowed_hosts: list = None, allowed_keywords: list = None):
    verify_runtime_attestation()
    if tool_name == "read_url_content":
        match = re.search(r"https?://([^/]+)", payload)
        if not match:
            sys.stderr.write("[DISPATCH DENIED 76] Invalid URL schema.\n")
            sys.exit(EC_SECRET_PATH_ACCESS)
        host = match.group(1).lower()
        if allowed_hosts and host not in [h.lower() for h in allowed_hosts]:
            sys.stderr.write(f"[DISPATCH DENIED 76] Host '{host}' not on egress allowlist.\n")
            sys.exit(EC_SECRET_PATH_ACCESS)
    elif tool_name == "search_web":
        if any(secret in payload.lower() for secret in [".env", "id_rsa", "secret_key", "token"]):
            sys.stderr.write("[DISPATCH DENIED 76] Search query references sensitive token or secret.\n")
            sys.exit(EC_SECRET_PATH_ACCESS)
        if allowed_keywords:
            tokens = payload.lower().split()
            if not any(t in [k.lower() for k in allowed_keywords] for t in tokens):
                sys.stderr.write(f"[DISPATCH DENIED 76] Search query outside manifest allowed_keywords.\n")
                sys.exit(EC_SECRET_PATH_ACCESS)

def verify_manifest_hash(manifest_path: str, expected_sha256: str):
    p = Path(manifest_path)
    if not p.exists():
        sys.stderr.write(f"[DISPATCH DENIED 82] Manifest missing from {manifest_path}\n")
        sys.exit(EC_MANIFEST_HASH_MISMATCH)
    curr_sha = hashlib.sha256(p.read_bytes()).hexdigest()
    if curr_sha != expected_sha256:
        sys.stderr.write(f"[DISPATCH DENIED 82] Manifest SHA256 mismatch. Expected {expected_sha256}, got {curr_sha}\n")
        sys.exit(EC_MANIFEST_HASH_MISMATCH)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="T3 Dispatcher")
    parser.add_argument("--tool", default=None)
    parser.add_argument("--payload", default="")
    parser.add_argument("--targets", default="")
    parser.add_argument("--session", default="default")
    parser.add_argument("--hash", default=None)
    parser.add_argument("pos_args", nargs="*", default=[])
    parsed_args = parser.parse_args()

    if parsed_args.tool:
        tool = parsed_args.tool
        payload = parsed_args.payload
        targets = parsed_args.targets.split(",") if parsed_args.targets else None
        sess_id = parsed_args.session
        exp_hash = parsed_args.hash
    elif len(parsed_args.pos_args) >= 2:
        tool = parsed_args.pos_args[0]
        payload = parsed_args.pos_args[1]
        targets = parsed_args.pos_args[2].split(",") if len(parsed_args.pos_args) > 2 and parsed_args.pos_args[2] else None
        exp_hash = parsed_args.pos_args[3] if len(parsed_args.pos_args) > 3 and parsed_args.pos_args[3] else None
        sess_id = parsed_args.pos_args[4] if len(parsed_args.pos_args) > 4 and parsed_args.pos_args[4] else "default"
    else:
        sys.exit(1)

    if exp_hash:
        manifest_p = str(T3_ROOT / f"sessions/{sess_id}/task-manifest.json")
        verify_manifest_hash(manifest_p, exp_hash)

    if tool in {"run_command", "terminal/create"}:
        argv = validate_command(payload, session_id=sess_id, allowed_targets=targets)
        print(f"[DISPATCH ALLOWED] argv={argv}")
        sys.exit(0)
    elif tool in {"view_file", "edit_file", "create_file", "fs/read_text_file", "fs/write_text_file"}:
        validate_file_tool(tool, payload, targets)
        print(f"[DISPATCH ALLOWED] tool={tool} path={payload}")
        sys.exit(0)
    elif tool in {"read_url_content", "search_web"}:
        validate_network_tool(tool, payload, allowed_hosts=["api.github.com"], allowed_keywords=["blade", "pest", "tailwind"])
        print(f"[DISPATCH ALLOWED] tool={tool} payload={payload}")
        sys.exit(0)
    else:
        sys.stderr.write(f"[DISPATCH DENIED] Unknown tool: {tool}\n")
        sys.exit(1)
