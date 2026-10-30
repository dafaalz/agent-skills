#!/usr/bin/env python3
"""
Trusted Verification Receipt Executor (run_receipt.py)
Executes a verification command as a subprocess, captures stdout/stderr,
computes cryptographic digests, parses test results, and writes an execution-bound
verification-receipt.json and receipt-hash.txt.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import shlex
import shutil
import subprocess
import sys


EMPTY_SHA = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"

FORBIDDEN_DUMMY_COMMANDS = {
    "true", ":", "exit 0", "echo pass", "echo ok",
    "sleep 0", "test 1 -eq 1", "/usr/bin/true", "/bin/true",
}
ALLOWED_EXECUTABLES = {"python3", "python", "git", "shasum", "wc", "grep"}
ALLOWED_PYTHON_FLAGS = {"--all", "--json", "--strict", "--self-test"}
FORBIDDEN_PYTHON_INLINE_FLAGS = {"-c", "-m", "-e", "-O", "-W"}
FORBIDDEN_SHELL_META = {";", "&", "|", "$", "`"}
EXPECTED_RULE_IDS = {
    "line_budget",
    "frontmatter",
    "punctuation",
    "pseudo_labels",
    "anti_slop",
    "completion_criteria",
    "references",
    "r13_anti_patterns",
    "r9_fuzzy_criteria",
}
EXCLUDE_SPECS = [":!*.agents", ":!*advisor_prompt.txt"]


def compute_sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def compute_file_sha256(path: Path) -> str:
    return compute_sha256(path.read_bytes())


def parse_linter_json(stdout_text: str) -> dict | None:
    try:
        json_start = stdout_text.find("{\n")
        if json_start != -1:
            json_str = stdout_text[json_start:]
            return json.loads(json_str)
    except Exception:
        pass
    return None


def get_git_info(cwd: Path) -> tuple[str, str, str, str, int, bool]:
    try:
        commit = subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            cwd=cwd,
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
        tree = subprocess.check_output(
            ["git", "rev-parse", "HEAD^{tree}"],
            cwd=cwd,
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
        status_out = subprocess.check_output(
            ["git", "status", "--porcelain", "--", ".", ":(exclude).agents", ":(exclude)advisor_prompt.txt"],
            cwd=cwd,
            text=True,
            stderr=subprocess.DEVNULL,
        )
        status_sha = compute_sha256(status_out.encode("utf-8"))
        diff_proc = subprocess.run(
            ["git", "diff", "--exit-code", "--", ".", ":(exclude).agents", ":(exclude)advisor_prompt.txt"],
            cwd=cwd,
            capture_output=True,
        )
        diff_sha = compute_sha256(diff_proc.stdout)
        diff_exit = diff_proc.returncode
        worktree_clean = (status_sha == EMPTY_SHA and diff_sha == EMPTY_SHA and diff_exit == 0)
        return commit, tree, status_sha, diff_sha, diff_exit, worktree_clean
    except Exception:
        return "unknown", "unknown", "unknown", "unknown", 1, False


def verify_receipt(receipt_file: Path, hash_file: Path, stdout_file: Path, lc_file: Path) -> int:
    if not receipt_file.is_file():
        print(f"VERIFY FAILED: receipt file not found: {receipt_file}", file=sys.stderr)
        return 1
    if not hash_file.is_file():
        print(f"VERIFY FAILED: hash file not found: {hash_file}", file=sys.stderr)
        return 1

    actual_receipt_hash = compute_file_sha256(receipt_file)
    expected_hash_parts = hash_file.read_text().strip().split(None, 1)
    if not expected_hash_parts:
        print(f"VERIFY FAILED: hash file empty: {hash_file}", file=sys.stderr)
        return 1
    expected_hash = expected_hash_parts[0]
    expected_filename = expected_hash_parts[1].strip() if len(expected_hash_parts) > 1 else ""
    if expected_filename and not expected_filename.endswith("verification-receipt.json"):
        print(f"VERIFY FAILED: hash file specifies invalid target filename: {expected_filename}", file=sys.stderr)
        return 1

    if actual_receipt_hash != expected_hash:
        print(
            f"VERIFY FAILED: receipt hash mismatch (actual {actual_receipt_hash} != recorded {expected_hash})",
            file=sys.stderr,
        )
        return 1

    try:
        receipt = json.loads(receipt_file.read_text())
    except Exception as exc:
        print(f"VERIFY FAILED: corrupt JSON in {receipt_file}: {exc}", file=sys.stderr)
        return 1

    # Schema Validation
    iso_pattern = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})$")
    sha64_pattern = re.compile(r"^[0-9a-f]{64}$")
    sha40_pattern = re.compile(r"^[0-9a-f]{40}$")

    for tf in ["start_time_iso8601", "end_time_iso8601"]:
        val = receipt.get(tf, "")
        if not iso_pattern.match(val):
            print(f"VERIFY FAILED: timestamp {tf} is not valid ISO-8601 with timezone: '{val}'", file=sys.stderr)
            return 1

    for hf in ["stdout_sha256", "stderr_sha256", "worktree_status_sha256", "worktree_diff_sha256"]:
        val = receipt.get(hf, "")
        if not sha64_pattern.match(val):
            print(f"VERIFY FAILED: hash field {hf} is not a valid 64-hex SHA-256: '{val}'", file=sys.stderr)
            return 1

    for gf in ["git_commit", "git_tree"]:
        val = receipt.get(gf, "")
        if not sha40_pattern.match(val):
            print(f"VERIFY FAILED: git field {gf} is not a valid 40-hex SHA-1: '{val}'", file=sys.stderr)
            return 1

    # Check exit code
    if receipt.get("exit_code") != 0:
        print(f"VERIFY FAILED: recorded exit code is non-zero: {receipt.get('exit_code')}", file=sys.stderr)
        return 1

    # Check dummy commands
    cmd = receipt.get("command", "").strip()
    if cmd in FORBIDDEN_DUMMY_COMMANDS:
        print(f"VERIFY FAILED: forbidden dummy command detected: '{cmd}'", file=sys.stderr)
        return 1

    # Check committed blob & disk linter SHA-256
    commit_sha = receipt.get("git_commit")
    cwd = Path.cwd()
    linter_path = Path("skills/review-a-skill/scripts/lint_skill.py")
    actual_linter_sha = compute_file_sha256(linter_path) if linter_path.is_file() else None
    if commit_sha:
        try:
            committed_linter_blob = subprocess.check_output(
                ["git", "cat-file", "-p", f"{commit_sha}:skills/review-a-skill/scripts/lint_skill.py"],
                cwd=cwd,
                stderr=subprocess.DEVNULL,
            )
            committed_linter_sha = compute_sha256(committed_linter_blob)
            if committed_linter_sha != receipt.get("linter_sha256"):
                print(
                    f"VERIFY FAILED: committed linter blob SHA-256 ({committed_linter_sha}) != receipt linter_sha256 ({receipt.get('linter_sha256')})",
                    file=sys.stderr,
                )
                return 1
            if committed_linter_sha != actual_linter_sha:
                print(
                    f"VERIFY FAILED: disk linter SHA-256 ({actual_linter_sha}) != committed linter blob SHA-256 ({committed_linter_sha})",
                    file=sys.stderr,
                )
                return 1
        except Exception as exc:
            print(f"VERIFY FAILED: failed reading committed linter blob from {commit_sha}: {exc}", file=sys.stderr)
            return 1

    # Check git tree cross-check against commit
    if commit_sha:
        try:
            expected_tree = subprocess.check_output(
                ["git", "rev-parse", f"{commit_sha}^{{tree}}"],
                cwd=cwd,
                text=True,
                stderr=subprocess.DEVNULL,
            ).strip()
            if receipt.get("git_tree") != expected_tree:
                print(
                    f"VERIFY FAILED: git tree divergence (commit tree {expected_tree} != receipt tree {receipt.get('git_tree')})",
                    file=sys.stderr,
                )
                return 1
        except Exception as exc:
            print(f"VERIFY FAILED: unable to rev-parse commit {commit_sha}: {exc}", file=sys.stderr)
            return 1

    # Live Working Tree Re-evaluation (F2 invariant)
    live_status_proc = subprocess.run(
        ["git", "status", "--porcelain", "--", ".", ":(exclude).agents", ":(exclude)advisor_prompt.txt"],
        cwd=cwd,
        capture_output=True,
        text=True,
    )
    live_status_sha = compute_sha256(live_status_proc.stdout.encode("utf-8"))
    live_diff_proc = subprocess.run(
        ["git", "diff", "--exit-code", "--", ".", ":(exclude).agents", ":(exclude)advisor_prompt.txt"],
        cwd=cwd,
        capture_output=True,
    )
    live_diff_sha = compute_sha256(live_diff_proc.stdout)
    live_diff_exit = live_diff_proc.returncode

    if live_status_sha != EMPTY_SHA or live_diff_sha != EMPTY_SHA or live_diff_exit != 0:
        print(
            f"VERIFY FAILED: live worktree is dirty! status_sha: {live_status_sha}, diff_exit: {live_diff_exit}",
            file=sys.stderr,
        )
        return 1

    if receipt.get("worktree_clean"):
        if (
            receipt.get("worktree_status_sha256") != EMPTY_SHA
            or receipt.get("worktree_diff_sha256") != EMPTY_SHA
            or receipt.get("worktree_diff_exit") != 0
        ):
            print(
                f"VERIFY FAILED: recorded worktree_clean inconsistent with recorded status/diff hashes",
                file=sys.stderr,
            )
            return 1
        if live_status_sha != receipt.get("worktree_status_sha256") or live_diff_sha != receipt.get("worktree_diff_sha256"):
            print("VERIFY FAILED: recorded worktree hashes do not match live worktree hashes", file=sys.stderr)
            return 1

    # Rules Schema and Counters Validation (S3, S4)
    rules = receipt.get("rules", [])
    if len(rules) != 9:
        print(f"VERIFY FAILED: rules array length {len(rules)} != 9", file=sys.stderr)
        return 1

    rule_ids = {r.get("id") for r in rules}
    if rule_ids != EXPECTED_RULE_IDS:
        print(f"VERIFY FAILED: rule IDs {rule_ids} != expected set {EXPECTED_RULE_IDS}", file=sys.stderr)
        return 1

    rules_exec = set(receipt.get("rules_executed", []))
    if rules_exec != EXPECTED_RULE_IDS:
        print(f"VERIFY FAILED: rules_executed {rules_exec} != expected set {EXPECTED_RULE_IDS}", file=sys.stderr)
        return 1

    for r in rules:
        if r.get("failed", 0) != 0:
            print(f"VERIFY FAILED: rule '{r.get('id')}' has failed count {r.get('failed')}", file=sys.stderr)
            return 1
        if r.get("checked", 0) != 35:
            print(f"VERIFY FAILED: rule '{r.get('id')}' has checked count {r.get('checked')} != 35", file=sys.stderr)
            return 1

    # Captured Log Re-read & Verification (F3)
    if not stdout_file.is_file():
        print(f"VERIFY FAILED: captured stdout file not found: {stdout_file}", file=sys.stderr)
        return 1
    actual_stdout_hash = compute_file_sha256(stdout_file)
    if actual_stdout_hash != receipt.get("stdout_sha256"):
        print(
            f"VERIFY FAILED: stdout hash mismatch (actual {actual_stdout_hash} != receipt {receipt.get('stdout_sha256')})",
            file=sys.stderr,
        )
        return 1

    # Line Counts Cross-Check into --verify (F4)
    if not lc_file.is_file():
        print(f"VERIFY FAILED: line-counts file not found: {lc_file}", file=sys.stderr)
        return 1
    actual_lc_sha = compute_file_sha256(lc_file)
    if "line_counts_sha256" in receipt and actual_lc_sha != receipt.get("line_counts_sha256"):
        print(
            f"VERIFY FAILED: line_counts_sha256 mismatch (actual {actual_lc_sha} != receipt {receipt.get('line_counts_sha256')})",
            file=sys.stderr,
        )
        return 1

    # Parse line-counts.txt and verify equality with receipt["line_counts"]
    parsed_counts: dict[str, int] = {}
    for line in lc_file.read_text().splitlines():
        parts = line.strip().split()
        if len(parts) == 2 and parts[1].endswith("/SKILL.md"):
            sk_name = parts[1].split("/")[1]
            try:
                parsed_counts[sk_name] = int(parts[0])
            except ValueError:
                pass

    receipt_line_counts = receipt.get("line_counts", {})
    if len(receipt_line_counts) != 35 or len(parsed_counts) != 35:
        print(f"VERIFY FAILED: line counts count mismatch (receipt {len(receipt_line_counts)}, parsed {len(parsed_counts)} != 35)", file=sys.stderr)
        return 1

    for sk_name, count in parsed_counts.items():
        if receipt_line_counts.get(sk_name) != count:
            print(f"VERIFY FAILED: line count divergence for {sk_name}: receipt {receipt_line_counts.get(sk_name)} != parsed {count}", file=sys.stderr)
            return 1
        if count > 250:
            print(f"VERIFY FAILED: skill {sk_name} exceeds line budget: {count} > 250", file=sys.stderr)
            return 1

    print("=" * 70)
    print("VERIFY INVARIANT AUDIT:")
    print(f"[PASS] receipt-hash.txt filename matches verification-receipt.json ({expected_filename})")
    print(f"[PASS] sha256(verification-receipt.json) == expected ({actual_receipt_hash})")
    print(f"[PASS] recorded exit_code == 0")
    print(f"[PASS] command is not dummy ({cmd})")
    print(f"[PASS] linter_sha256 committed blob matches disk and receipt ({actual_linter_sha})")
    print(f"[PASS] git rev-parse <git_commit>^{{tree}} == git_tree ({receipt.get('git_tree')})")
    print(f"[PASS] live worktree re-check is clean (status_sha == EMPTY_SHA, diff_exit == 0)")
    print(f"[PASS] worktree_clean <=> EMPTY_SHA ({EMPTY_SHA})")
    print(f"[PASS] rules array exactly matches expected 9 rule IDs with 0 failures across 35 skills")
    print(f"[PASS] rules_executed set matches rules array IDs")
    print(f"[PASS] stdout_sha256 matches captured log at {stdout_file} ({actual_stdout_hash})")
    print(f"[PASS] line_counts cross-checked against line-counts.txt (35 targets verified <= 250, sha: {actual_lc_sha[:16]}...)")
    print("=" * 70)
    print(f"RECEIPT VERIFIED: {receipt_file} (hash: {actual_receipt_hash}, exit_code: 0)")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Trusted Verification Receipt Executor")
    parser.add_argument("--claim", help="Assertion claim text for receipt")
    parser.add_argument("--command", help="Command line to execute")
    parser.add_argument("--argv", help="Command argv array as JSON string")
    parser.add_argument("--out", default=".agents/state/verification-before-completion/verification-receipt.json", help="Path to write receipt JSON")
    parser.add_argument("--hash-out", default=".agents/state/verification-before-completion/receipt-hash.txt", help="Path to write receipt hash")
    parser.add_argument("--stdout-out", default=".agents/state/verification-before-completion/last-stdout.log", help="Path to write stdout log")
    parser.add_argument("--stderr-out", default=".agents/state/verification-before-completion/last-stderr.log", help="Path to write stderr log")
    parser.add_argument("--line-counts-file", default=".agents/state/verification-before-completion/line-counts.txt", help="Path to line counts file")
    parser.add_argument("--verify", action="store_true", help="Verify existing receipt integrity")
    parser.add_argument("--allow-noop", action="store_true", help="Allow no-op command")

    args = parser.parse_args()

    receipt_path = Path(args.out)
    hash_path = Path(args.hash_out)
    stdout_path = Path(args.stdout_out)
    stderr_path = Path(args.stderr_out)
    lc_path = Path(args.line_counts_file)

    if args.verify:
        return verify_receipt(receipt_path, hash_path, stdout_path, lc_path)

    if not args.command and not args.argv:
        print("Error: Either --command or --argv must be provided.", file=sys.stderr)
        return 1

    if args.argv:
        argv = json.loads(args.argv)
        cmd_str = " ".join(shlex.quote(a) for a in argv)
    else:
        cmd_str = args.command.strip()
        argv = shlex.split(cmd_str)

    if not argv:
        print("Error: Empty command cannot be executed.", file=sys.stderr)
        return 1

    # Executable allowlist enforcement
    base_exe = Path(argv[0]).name
    if base_exe not in ALLOWED_EXECUTABLES:
        print(f"Error: Executable '{base_exe}' is not in the trusted allowlist {ALLOWED_EXECUTABLES}.", file=sys.stderr)
        return 1

    resolved_exe = shutil.which(argv[0]) or argv[0]

    # Subcommand allowlist & argument security
    if base_exe in {"python3", "python"}:
        if len(argv) < 2:
            print("Error: python invocation requires a script path.", file=sys.stderr)
            return 1
        for a in argv[1:]:
            if a in FORBIDDEN_PYTHON_INLINE_FLAGS:
                print(f"Error: Inline execution flag '{a}' is forbidden. Only script paths under the workspace are permitted.", file=sys.stderr)
                return 1
        script_file = Path(argv[1])
        if not script_file.is_file() or not script_file.name.endswith(".py"):
            print(f"Error: python script target '{argv[1]}' must be an existing .py file.", file=sys.stderr)
            return 1
        for a in argv[2:]:
            if a.startswith("-") and a not in ALLOWED_PYTHON_FLAGS:
                print(f"Error: Forbidden or unknown argument '{a}' passed to python. Permitted: {ALLOWED_PYTHON_FLAGS}", file=sys.stderr)
                return 1

    # Shell metacharacter check
    for arg in argv:
        for char in FORBIDDEN_SHELL_META:
            if char in arg:
                print(f"Error: Forbidden shell metacharacter '{char}' detected in argument '{arg}'.", file=sys.stderr)
                return 1

    if not args.allow_noop and cmd_str in FORBIDDEN_DUMMY_COMMANDS:
        print(f"Error: Forbidden dummy command '{cmd_str}' rejected by executor.", file=sys.stderr)
        return 1

    receipt_path.parent.mkdir(parents=True, exist_ok=True)
    hash_path.parent.mkdir(parents=True, exist_ok=True)
    stdout_path.parent.mkdir(parents=True, exist_ok=True)
    stderr_path.parent.mkdir(parents=True, exist_ok=True)

    cwd = Path.cwd()
    commit, tree, status_sha, diff_sha, diff_exit, worktree_clean = get_git_info(cwd)

    linter_path = Path("skills/review-a-skill/scripts/lint_skill.py")
    linter_sha = compute_file_sha256(linter_path) if linter_path.is_file() else None

    start_iso = datetime.now(timezone.utc).isoformat()
    proc = subprocess.run(argv, capture_output=True)
    end_iso = datetime.now(timezone.utc).isoformat()

    stdout_path.write_bytes(proc.stdout)
    stderr_path.write_bytes(proc.stderr)

    stdout_hash = compute_sha256(proc.stdout)
    stderr_hash = compute_sha256(proc.stderr)

    stdout_text = proc.stdout.decode("utf-8", errors="replace")
    linter_data = parse_linter_json(stdout_text)

    line_counts = {}
    if linter_data:
        passed_count = linter_data.get("targets_passed", 0)
        failed_count = linter_data.get("targets_failed", 0)
        rules = linter_data.get("rules", [])
        rules_executed = linter_data.get("rules_executed", [])
        line_counts = linter_data.get("line_counts", {})
    else:
        lint_match = re.search(r"Summary:\s*(\d+)\s*targets checked\.\s*(\d+)\s*errors", stdout_text)
        if lint_match:
            total = int(lint_match.group(1))
            errors = int(lint_match.group(2))
            passed_count, failed_count = total - errors, errors
        elif proc.returncode == 0:
            passed_count, failed_count = 1, 0
        else:
            passed_count, failed_count = 0, 1
        rules = []
        rules_executed = []

    lc_sha = compute_file_sha256(lc_path) if lc_path.is_file() else None

    claim_text = args.claim or (
        f"argv={argv} exited {proc.returncode}; "
        f"{passed_count} targets passed; "
        f"rules length {len(rules)} with failed {failed_count}; "
        f"worktree_clean {worktree_clean}; "
        f"git_tree {tree}"
    )

    receipt_payload = {
        "claim": claim_text,
        "command": cmd_str,
        "argv": argv,
        "argv0_resolved": resolved_exe,
        "cwd": str(cwd),
        "git_commit": commit,
        "git_tree": tree,
        "worktree_clean": worktree_clean,
        "worktree_diff_exit": diff_exit,
        "worktree_status_sha256": status_sha,
        "worktree_diff_sha256": diff_sha,
        "linter_sha256": linter_sha,
        "line_counts_sha256": lc_sha,
        "rules": rules,
        "rules_executed": rules_executed,
        "line_counts": line_counts,
        "stdout_capture_path": str(stdout_path.as_posix()),
        "start_time_iso8601": start_iso,
        "end_time_iso8601": end_iso,
        "exit_code": proc.returncode,
        "stdout_sha256": stdout_hash,
        "stderr_sha256": stderr_hash,
        "test_count_passed": passed_count,
        "test_count_failed": failed_count,
    }

    receipt_json_bytes = (json.dumps(receipt_payload, indent=2) + "\n").encode("utf-8")
    receipt_path.write_bytes(receipt_json_bytes)

    receipt_sha = compute_sha256(receipt_json_bytes)
    hash_path.write_text(f"{receipt_sha}  {receipt_path.as_posix()}\n")

    print(f"EXECUTED: {cmd_str}")
    print(f"EXIT CODE: {proc.returncode} (passed: {passed_count}, failed: {failed_count})")
    print(f"STDOUT SHA256: {stdout_hash}")
    print(f"RECEIPT WRITTEN: {receipt_path} (hash: {receipt_sha})")

    # Mirror child process stdout to terminal
    sys.stdout.buffer.write(proc.stdout)
    sys.stderr.buffer.write(proc.stderr)

    return proc.returncode


if __name__ == "__main__":
    sys.exit(main())
