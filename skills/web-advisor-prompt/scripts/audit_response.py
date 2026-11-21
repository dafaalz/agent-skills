#!/usr/bin/env python3
"""Audit external advisor responses against local repository bounds, macOS BSD shell rules, and stub checks."""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

FENCE_OPEN_RE = re.compile(r"^\s*(`{3,}|~{3,})\s*([A-Za-z0-9_+-]*)\s*$")
URL_STRIP_RE = re.compile(r"[a-z][a-z0-9+.-]*://\S+", re.IGNORECASE)
IPV4_RE = re.compile(r"^\d+\.\d+\.\d+\.\d+$")

EXTENSIONLESS_FILES = (
    "Makefile",
    "Dockerfile",
    "Containerfile",
    "Gemfile",
    "Rakefile",
    "Procfile",
    "Justfile",
    "Brewfile",
    "Vagrantfile",
)

DOTTED_CITATION_RE = re.compile(r"`?([A-Za-z0-9_./-]+\.[A-Za-z0-9]+):(\d+)(?:-(\d+))?`?")
SLASHED_CITATION_RE = re.compile(r"`?([A-Za-z0-9_./-]+/[A-Za-z0-9_.-]+):(\d+)(?:-(\d+))?`?")
EXTLESS_CITATION_RE = re.compile(
    r"`?((?:[A-Za-z0-9_.-]+/)*(?:" + "|".join(EXTENSIONLESS_FILES) + r")):(\d+)(?:-(\d+))?`?"
)

NON_FILE_TLDS = (
    ".com",
    ".org",
    ".net",
    ".io",
    ".dev",
    ".local",
    ".internal",
    ".app",
    ".ai",
    ".edu",
    ".gov",
    ".localhost",
)

SHELL_LANGS = {"", "sh", "bash", "zsh", "shell", "console"}

GNU_PATTERNS: tuple[tuple[re.Pattern[str], str], ...] = (
    (
        re.compile(r"\bsed\s+(?:-[^i\s]+\s+)*-i(?!\s*(?:''|\"\"|\.[A-Za-z0-9_-]+))(?=\s)"),
        "GNU sed -i without BSD backup extension argument",
    ),
    (
        re.compile(r"\bsed\s+-[a-zA-Z]+i\b"),
        "Combined sed -i flag fails BSD backup extension syntax",
    ),
    (
        re.compile(r"\bsed\s+(?:[^\n]*\s)?-r\b"),
        "GNU sed -r flag unsupported on BSD sed (use -E)",
    ),
    (
        re.compile(r"\bgrep\s+-[A-Za-z]*P"),
        "GNU grep -P PCRE flag unsupported on macOS BSD grep",
    ),
    (
        re.compile(r"\bdate\s+(?:-[A-Za-z]+\s+)*(?:-d|--date)\b"),
        "GNU date -d flag unsupported on BSD date",
    ),
    (
        re.compile(r"\bstat\s+(?:-[A-Za-z]+\s+)*(?:-c|--format)\b"),
        "GNU stat -c flag unsupported on BSD stat (use -f)",
    ),
    (
        re.compile(r"\bfind\b[^\n]*\s-printf\b"),
        "GNU find -printf action unsupported on BSD find",
    ),
    (
        re.compile(r"\bawk\b[^\n]*\b(?:gensub|strftime)\s*\("),
        "GNU gawk extension unsupported on macOS BSD awk",
    ),
)

STUB_PATTERNS: tuple[re.Pattern[str], ...] = (
    re.compile(r"(?://|#|/\*)\s*rest of\b", re.IGNORECASE),
    re.compile(r"(?://|#|/\*)\s*(?:existing code|unchanged|omitted)\b", re.IGNORECASE),
    re.compile(r"\b(?:TODO|FIXME)\s*:\s*implement\b", re.IGNORECASE),
    re.compile(r"^\s*raise\s+NotImplementedError\b"),
)
ELLIPSIS_LINE_RE = re.compile(r"^\s*(?://|#|/\*|\*)?\s*\.\.\.\s*(?:\*/|;)?\s*$")


def format_ref(rel_path: str, start_line: int, end_line: int) -> str:
    if end_line == start_line:
        return f"{rel_path}:{start_line}"
    return f"{rel_path}:{start_line}-{end_line}"


def extract_prose_citations(line: str) -> list[tuple[str, int, int]]:
    cleaned = URL_STRIP_RE.sub("", line)
    matches: list[tuple[str, int, int]] = []
    seen: set[tuple[str, int, int]] = set()
    for regex in (DOTTED_CITATION_RE, SLASHED_CITATION_RE, EXTLESS_CITATION_RE):
        for match in regex.finditer(cleaned):
            rel_path = match.group(1)
            if IPV4_RE.match(rel_path) or rel_path.lower().endswith(NON_FILE_TLDS):
                continue
            start_line = int(match.group(2))
            end_line = int(match.group(3)) if match.group(3) else start_line
            key = (rel_path, start_line, end_line)
            if key not in seen:
                seen.add(key)
                matches.append(key)
    return matches


def audit_response(response_path: Path, repo_root: Path) -> tuple[dict[str, object], dict[str, object]]:
    text = response_path.read_text(encoding="utf-8", errors="replace")
    root_resolved = repo_root.resolve()
    findings: list[dict[str, str]] = []
    seen_citations: set[tuple[str, int, int]] = set()
    line_count_cache: dict[Path, int] = {}

    in_fence = False
    fence_char = ""
    fence_len = 0
    fence_lang = ""

    for line_no, raw_line in enumerate(text.splitlines(), start=1):
        stripped = raw_line.strip()

        if not in_fence:
            open_match = FENCE_OPEN_RE.match(raw_line)
            if open_match:
                in_fence = True
                fence_char = open_match.group(1)[0]
                fence_len = len(open_match.group(1))
                fence_lang = open_match.group(2).lower()
                continue

            for rel_path, start_line, end_line in extract_prose_citations(raw_line):
                key = (rel_path, start_line, end_line)
                if key in seen_citations:
                    continue
                seen_citations.add(key)
                ref_str = format_ref(rel_path, start_line, end_line)

                target = (root_resolved / rel_path).resolve()
                if not target.is_relative_to(root_resolved):
                    findings.append(
                        {
                            "type": "citation",
                            "ref": ref_str,
                            "file": rel_path,
                            "status": "HALLUCINATED_LINE",
                            "reason": "Citation path escapes repository root",
                        }
                    )
                    continue

                if not target.is_file():
                    findings.append(
                        {
                            "type": "citation",
                            "ref": ref_str,
                            "file": rel_path,
                            "status": "HALLUCINATED_LINE",
                            "reason": "Referenced file does not exist on disk",
                        }
                    )
                    continue

                if target not in line_count_cache:
                    line_count_cache[target] = len(
                        target.read_text(encoding="utf-8", errors="replace").splitlines()
                    )
                total_lines = line_count_cache[target]

                if start_line < 1 or end_line < start_line or end_line > total_lines:
                    findings.append(
                        {
                            "type": "citation",
                            "ref": ref_str,
                            "file": rel_path,
                            "status": "HALLUCINATED_LINE",
                            "reason": f"Line range out of bounds (file has {total_lines} lines)",
                        }
                    )
                else:
                    norm_rel = target.relative_to(root_resolved).as_posix()
                    findings.append(
                        {
                            "type": "citation",
                            "ref": format_ref(norm_rel, start_line, end_line),
                            "file": norm_rel,
                            "status": "VERIFIED",
                            "reason": f"Verified within 1..{total_lines}",
                        }
                    )
        else:
            if stripped and set(stripped) == {fence_char} and len(stripped) >= fence_len:
                in_fence = False
                fence_char = ""
                fence_len = 0
                fence_lang = ""
                continue

            if fence_lang in SHELL_LANGS and not stripped.startswith("#"):
                for pattern, message in GNU_PATTERNS:
                    if pattern.search(raw_line):
                        findings.append(
                            {
                                "type": "cli_compatibility",
                                "ref": f"response:{line_no}",
                                "file": str(response_path),
                                "status": "PLATFORM_INVALID",
                                "reason": message,
                            }
                        )

            for stub_re in STUB_PATTERNS:
                if stub_re.search(raw_line):
                    findings.append(
                        {
                            "type": "completeness",
                            "ref": f"response:{line_no}",
                            "file": str(response_path),
                            "status": "INCOMPLETE_STUB",
                            "reason": "Truncated placeholder or unimplemented stub detected",
                        }
                    )
            if fence_lang not in {"yaml", "yml"} and ELLIPSIS_LINE_RE.match(raw_line):
                findings.append(
                    {
                        "type": "completeness",
                        "ref": f"response:{line_no}",
                        "file": str(response_path),
                        "status": "INCOMPLETE_STUB",
                        "reason": "Standalone ellipsis line detected inside code block",
                    }
                )

    verified = [f for f in findings if f["status"] == "VERIFIED"]
    unverified = [f for f in findings if f["status"] != "VERIFIED"]
    status_counts: dict[str, int] = {}
    for item in findings:
        status_counts[item["status"]] = status_counts.get(item["status"], 0) + 1

    verified_files = sorted({item["file"] for item in verified})
    audit_report: dict[str, object] = {
        "response_file": str(response_path),
        "repo_root": str(root_resolved),
        "total_checks": len(findings),
        "verified_count": len(verified),
        "unverified_count": len(unverified),
        "status_counts": status_counts,
        "findings": findings,
    }
    verified_manifest: dict[str, object] = {
        "response_file": str(response_path),
        "verified_files": verified_files,
        "verified_citations": [item["ref"] for item in verified],
    }
    return audit_report, verified_manifest


def capture_clipboard_to_file(dest: Path) -> None:
    env = os.environ.copy()
    env["LC_ALL"] = "en_US.UTF-8"
    env["LANG"] = "en_US.UTF-8"
    content = subprocess.run(["pbpaste"], capture_output=True, check=True, env=env).stdout
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(content)


def run_self_test() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "src").mkdir(parents=True)
        (root / "src" / "app.py").write_text("a = 1\nb = 2\nc = 3\nd = 4\n", encoding="utf-8")
        (root / "Makefile").write_text("all:\n\techo ok\n", encoding="utf-8")

        # 1. Clean response fixture
        clean_md = root / "clean.md"
        clean_md.write_text(
            "Verified issue at `src/app.py:2-4` and `Makefile:1`.\n"
            "Do not run grep -P or sed -i without backup arg on macOS.\n"
            "```bash\n"
            "sed -i '' 's/a/b/' src/app.py\n"
            'sed -i "" "s/a/b/" src/app.py\n'
            "readlink -f src/app.py\n"
            "```\n",
            encoding="utf-8",
        )
        clean_report, clean_manifest = audit_response(clean_md, root)
        assert clean_report["unverified_count"] == 0, f"Unexpected failures: {clean_report}"
        assert clean_report["verified_count"] == 2
        assert clean_manifest["verified_citations"] == ["src/app.py:2-4", "Makefile:1"]

        # 2. Adversarial defective response fixture
        bad_md = root / "bad.md"
        bad_md.write_text(
            "Check `src/app.py:1-99` and `../../../../etc/passwd:1` and `src/missing.py:1`.\n"
            "```bash\n"
            "grep -rnP 'foo' src/\n"
            "sed -i 's/a/b/' src/app.py\n"
            "```\n"
            "```python\n"
            "def run():\n"
            "    # rest of implementation\n"
            "    raise NotImplementedError()\n"
            "```\n",
            encoding="utf-8",
        )
        bad_report, _ = audit_response(bad_md, root)
        counts = bad_report["status_counts"]
        assert isinstance(counts, dict)
        assert counts.get("HALLUCINATED_LINE") == 3, f"Expected 3 hallucinated lines: {counts}"
        assert counts.get("PLATFORM_INVALID") == 2, f"Expected 2 platform errors: {counts}"
        assert counts.get("INCOMPLETE_STUB") == 2, f"Expected 2 stub errors: {counts}"

    print("SELF_TEST_PASS=1")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Audit external advisor responses against local ground truth.")
    parser.add_argument("--self-test", action="store_true", help="Run built-in deterministic test fixtures.")
    parser.add_argument("--scope", type=Path, help="Path to scope.json generated in Step 1.")
    parser.add_argument("--slug", help="Target slug used with --from-clipboard.")
    parser.add_argument("--response", type=Path, help="Path to saved advisor markdown response.")
    parser.add_argument("--from-clipboard", action="store_true", help="Read response via pbpaste.")
    parser.add_argument("--repo-root", type=Path, default=Path("."), help="Repository root path.")
    parser.add_argument(
        "--out",
        type=Path,
        default=Path(".agents/state/web-advisor-prompt/ingestion-audit.json"),
        help="Output path for ingestion audit JSON.",
    )
    parser.add_argument(
        "--verified-out",
        type=Path,
        default=Path(".agents/state/web-advisor-prompt/verified-findings.json"),
        help="Output path for verified files and citations allowlist.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.self_test:
        return run_self_test()

    repo_root = args.repo_root.resolve()
    scope_data: dict[str, object] = {}
    if args.scope:
        scope_data = json.loads(args.scope.read_text(encoding="utf-8"))

    slug = args.slug or str(scope_data.get("target_slug", ""))
    response_path = args.response

    if args.from_clipboard:
        if not slug:
            print("Error: --slug or --scope with target_slug required with --from-clipboard.", file=sys.stderr)
            return 2
        response_path = repo_root / "scratch" / "advisor_prompts" / f"{slug}.response.md"
        capture_clipboard_to_file(response_path)

    if response_path is None:
        if slug:
            response_path = repo_root / "scratch" / "advisor_prompts" / f"{slug}.response.md"
        else:
            print("Error: --response or --from-clipboard is required.", file=sys.stderr)
            return 2

    if not response_path.is_file():
        print(f"Error: response file not found ({response_path}).", file=sys.stderr)
        return 2

    audit_report, verified_manifest = audit_response(response_path, repo_root)

    out_path = args.out if args.out.is_absolute() else (repo_root / args.out)
    verified_path = args.verified_out if args.verified_out.is_absolute() else (repo_root / args.verified_out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    verified_path.parent.mkdir(parents=True, exist_ok=True)

    out_path.write_text(json.dumps(audit_report, indent=2) + "\n", encoding="utf-8")
    verified_path.write_text(json.dumps(verified_manifest, indent=2) + "\n", encoding="utf-8")

    print(f"VERIFIED={audit_report['verified_count']} UNVERIFIED={audit_report['unverified_count']}")
    return 1 if int(audit_report["unverified_count"]) > 0 else 0


if __name__ == "__main__":
    sys.exit(main())

