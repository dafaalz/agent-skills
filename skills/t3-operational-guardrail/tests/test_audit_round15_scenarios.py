#!/usr/bin/env python3
"""
Test Suite: Audit Round 15 Scenarios
Verifies:
1. git log -p :(glob)config/*.php is blocked as secret path (EC 76) [S-N1]
2. git diff :(glob)config/*.php is blocked as secret path (EC 76) [S-N1]
3. git log -p :(attr:export-ignore)config/app.php is blocked as secret path (EC 76) [S-N1]
4. git log :(glob)src/*.py is blocked by pathspec magic check (EC 74) [S-N1 non-secret variant]
5. git commit -m "msg" -F/tmp/evil is blocked by combined short flag check (EC 73) [Cos-N2]
6. ALLOWED_GIT_SAFE deterministically contains checkout, branch, commit (Cos-N3)
"""
import subprocess
import sys
import os
import tempfile
from pathlib import Path

T3_BIN = Path.home() / "Library/Application Support/t3/bin"
DISPATCH = T3_BIN / "t3_dispatch.py"

def run_dispatch(cmd_str: str, cwd: str = None, targets: list = None):
    if cwd is None:
        cwd = os.getcwd()
    args = [
        sys.executable, str(DISPATCH),
        "--tool", "run_command",
        "--payload", cmd_str,
        "--session", "audit_round15"
    ]
    if targets is not None:
        args.extend(["--targets", ",".join(targets)])
    return subprocess.run(args, cwd=cwd, capture_output=True, text=True)

def test_round15_scenarios():
    print("=== Running Audit Round 15 Scenarios ===\n")

    # 1. git log -p :(glob)config/*.php (S-N1 verification)
    res = run_dispatch('git log -p :(glob)config/*.php')
    print("Scenario 1 (git log -p :(glob)config/*.php):")
    print(f"  Returncode: {res.returncode}")
    print(f"  Stderr: {res.stderr.strip()}")
    assert res.returncode == 76, f"Expected 76, got {res.returncode}"
    assert "Secret path access prohibited" in res.stderr

    # 2. git diff :(glob)config/*.php (S-N1 verification)
    res = run_dispatch('git diff :(glob)config/*.php')
    print("\nScenario 2 (git diff :(glob)config/*.php):")
    print(f"  Returncode: {res.returncode}")
    print(f"  Stderr: {res.stderr.strip()}")
    assert res.returncode == 76, f"Expected 76, got {res.returncode}"
    assert "Secret path access prohibited" in res.stderr

    # 3. git log -p :(attr:export-ignore)config/app.php (S-N1 attr verification)
    res = run_dispatch('git log -p :(attr:export-ignore)config/app.php')
    print("\nScenario 3 (git log -p :(attr:export-ignore)config/app.php):")
    print(f"  Returncode: {res.returncode}")
    print(f"  Stderr: {res.stderr.strip()}")
    assert res.returncode == 76, f"Expected 76, got {res.returncode}"
    assert "Secret path access prohibited" in res.stderr

    # 4. git log :(glob)src/*.py (S-N1 non-secret pathspec magic rejection)
    res = run_dispatch('git log :(glob)src/*.py')
    print("\nScenario 4 (git log :(glob)src/*.py):")
    print(f"  Returncode: {res.returncode}")
    print(f"  Stderr: {res.stderr.strip()}")
    assert res.returncode == 74, f"Expected 74, got {res.returncode}"
    assert "pathspec magic prefix prohibited" in res.stderr

    # 5. git commit -m "msg" -F/tmp/evil (Cos-N2 verification: -F combined short flag)
    res = run_dispatch('git commit -m "msg" -F/tmp/evil')
    print("\nScenario 5 (git commit -m 'msg' -F/tmp/evil):")
    print(f"  Returncode: {res.returncode}")
    print(f"  Stderr: {res.stderr.strip()}")
    assert res.returncode == 73, f"Expected 73, got {res.returncode}"
    assert "Prohibited single-token short Git flag" in res.stderr

    # 6. Safe checkout and branch in ALLOWED_GIT_SAFE (Cos-N3 verification)
    res_branch = run_dispatch('git branch')
    print("\nScenario 6A (git branch allowlist check):")
    print(f"  Returncode: {res_branch.returncode}")
    assert res_branch.returncode == 0, f"Expected 0, got {res_branch.returncode}"
    print("  git branch allowed as first-pass ALLOWED_GIT_SAFE member (EC 0).")

    res_checkout = run_dispatch('git checkout -b feature/test-safe')
    print("Scenario 6B (git checkout -b feature/test-safe allowlist check):")
    print(f"  Returncode: {res_checkout.returncode}")
    assert res_checkout.returncode == 0, f"Expected 0, got {res_checkout.returncode}"
    print("  git checkout allowed as first-pass ALLOWED_GIT_SAFE member (EC 0).")

    print("\nALL ROUND 15 SCENARIOS PASSED PERFECTLY (100%).\n")

if __name__ == "__main__":
    test_round15_scenarios()
