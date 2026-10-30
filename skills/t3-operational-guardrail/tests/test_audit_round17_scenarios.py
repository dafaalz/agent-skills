#!/usr/bin/env python3
"""
Test Suite: Audit Round 17 Scenarios
Verifies:
1. Double-extension backup files (e.g. config/app.php.bak.swp) blocked as secret paths (EC 76) [C-R16-1]
2. Iterative backup stripping on .env (e.g. .env.bak.old) blocked as secret paths (EC 76) [C-R16-1]
3. git log -p on double-extension backup (config/app.php.bak.orig) blocked as secret paths (EC 76) [C-R16-1]
4. git log -p ':!config/app.php' blocked fail-closed as secret path (EC 76) [C-R16-2 / SKILL Point 7]
5. git commit --message="--output=/tmp/evil" tracks commit_msg_indices properly (EC 0) [C-R16-3]
6. git commit --message="-c legitimate message" defensive invariant check (EC 0) [C-R16-3]
"""
import subprocess
import sys
import os
from pathlib import Path

T3_BIN = Path.home() / "Library/Application Support/t3/bin"
DISPATCH = T3_BIN / "t3_dispatch.py"

def run_dispatch(tool: str, payload: str, cwd: str = None, targets: list = None):
    if cwd is None:
        cwd = os.getcwd()
    args = [
        sys.executable, str(DISPATCH),
        "--tool", tool,
        "--payload", payload,
        "--session", "audit_round17"
    ]
    if targets is not None:
        args.extend(["--targets", ",".join(targets)])
    return subprocess.run(args, cwd=cwd, capture_output=True, text=True)

def test_round17_scenarios():
    print("=== Running Audit Round 17 Scenarios ===\n")

    # 1. Double extension backup file config/app.php.bak.swp (C-R16-1 verification)
    res1 = run_dispatch("view_file", "config/app.php.bak.swp")
    print("Scenario 1 (view_file config/app.php.bak.swp):")
    print(f"  Returncode: {res1.returncode}")
    print(f"  Stderr: {res1.stderr.strip()}")
    assert res1.returncode == 76, f"Expected 76, got {res1.returncode}"
    assert "Access to secret path prohibited" in res1.stderr

    # 2. Iterative backup stripping on .env (C-R16-1 verification)
    res2 = run_dispatch("view_file", ".env.bak.old")
    print("\nScenario 2 (view_file .env.bak.old):")
    print(f"  Returncode: {res2.returncode}")
    print(f"  Stderr: {res2.stderr.strip()}")
    assert res2.returncode == 76, f"Expected 76, got {res2.returncode}"
    assert "Access to secret path prohibited" in res2.stderr

    # 3. git log -p on double-extension backup (C-R16-1 verification)
    res3 = run_dispatch("run_command", "git log -p config/app.php.bak.orig")
    print("\nScenario 3 (git log -p config/app.php.bak.orig):")
    print(f"  Returncode: {res3.returncode}")
    print(f"  Stderr: {res3.stderr.strip()}")
    assert res3.returncode == 76, f"Expected 76, got {res3.returncode}"
    assert "Secret path access prohibited" in res3.stderr

    # 4. Exclusion pathspec over-blocking on secret path (C-R16-2 verification)
    res4 = run_dispatch("run_command", "git log -p ':!config/app.php'")
    print("\nScenario 4 (git log -p ':!config/app.php'):")
    print(f"  Returncode: {res4.returncode}")
    print(f"  Stderr: {res4.stderr.strip()}")
    assert res4.returncode == 76, f"Expected 76, got {res4.returncode}"
    assert "Secret path access prohibited" in res4.stderr

    # 5. git commit --message="--output=/tmp/evil" (C-R16-3 verification)
    res5 = run_dispatch("run_command", 'git commit --message="--output=/tmp/evil"')
    print("\nScenario 5 (git commit --message='--output=/tmp/evil'):")
    print(f"  Returncode: {res5.returncode}")
    assert res5.returncode == 0, f"Expected 0, got {res5.returncode}. Stderr: {res5.stderr}"
    print("  Commit with --message='--output=...' allowed without false-positive EC 73 (EC 0).")

    # 6. git commit --message="-c legitimate message" (C-R16-3 defensive invariant)
    res6 = run_dispatch("run_command", 'git commit --message="-c legitimate message"')
    print("\nScenario 6 (git commit --message='-c legitimate message'):")
    print(f"  Returncode: {res6.returncode}")
    assert res6.returncode == 0, f"Expected 0, got {res6.returncode}. Stderr: {res6.stderr}"
    print("  Commit with --message='-c ...' allowed without false-positive EC 73 (EC 0).")

    print("\nALL ROUND 17 SCENARIOS PASSED PERFECTLY (100%).\n")

if __name__ == "__main__":
    test_round17_scenarios()
