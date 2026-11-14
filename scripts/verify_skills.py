#!/usr/bin/env python3
"""Unified verification entrypoint delegating to skills/review-a-skill/scripts/lint_skill.py."""

from __future__ import annotations

from pathlib import Path
import subprocess
import sys


def main() -> int:
    repo_root = Path(__file__).resolve().parent.parent
    linter_path = repo_root / "skills" / "review-a-skill" / "scripts" / "lint_skill.py"
    if not linter_path.is_file():
        print(f"Error: Canonical linter missing at {linter_path}", file=sys.stderr)
        return 1

    cmd = [sys.executable, str(linter_path), *sys.argv[1:]]
    completed = subprocess.run(cmd, check=False)
    return completed.returncode


if __name__ == "__main__":
    sys.exit(main())
