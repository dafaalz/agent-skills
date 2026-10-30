#!/usr/bin/env python3
"""
Test Suite: Audit Round 18 Scenarios
Verifies:
1. Trailing dot after backup extension (config/app.php.bak.) blocked as secret path (EC 76) [C-R17-1]
2. Trailing dot without extension (config/app.php.) blocked as secret path (EC 76) [C-R17-2]
3. Leading prefix tilde (~config/app.php) blocked as secret path (EC 76) [C-R17-3]
4. Basename prefix tilde (config/~app.php) blocked as secret path (EC 76) [C-R17-3]
5. Lockfile prefix marker (~$config/app.php) blocked as secret path (EC 76) [C-R17-4]
6. Trailing dot on double backup (.env.bak.old.) blocked as secret path (EC 76) [C-R17-1]
7. Multiple message options (-m "msg" --message="--output=/tmp/evil") allowed (EC 0) [C-R17-5]
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
        "--session", "audit_round18"
    ]
    if targets is not None:
        args.extend(["--targets", ",".join(targets)])
    return subprocess.run(args, cwd=cwd, capture_output=True, text=True)

def test_round18_scenarios():
    print("=== Running Audit Round 18 Scenarios ===\n")

    # 1. Trailing dot after backup extension (C-R17-1)
    res1 = run_dispatch("view_file", "config/app.php.bak.")
    print("Scenario 1 (view_file config/app.php.bak.):")
    print(f"  Returncode: {res1.returncode}")
    print(f"  Stderr: {res1.stderr.strip()}")
    assert res1.returncode == 76, f"Expected 76, got {res1.returncode}"
    assert "Access to secret path prohibited" in res1.stderr

    # 2. Trailing dot without extension (C-R17-2)
    res2 = run_dispatch("view_file", "config/app.php.")
    print("\nScenario 2 (view_file config/app.php.):")
    print(f"  Returncode: {res2.returncode}")
    print(f"  Stderr: {res2.stderr.strip()}")
    assert res2.returncode == 76, f"Expected 76, got {res2.returncode}"
    assert "Access to secret path prohibited" in res2.stderr

    # 3. Leading prefix tilde (C-R17-3)
    res3 = run_dispatch("view_file", "~config/app.php")
    print("\nScenario 3 (view_file ~config/app.php):")
    print(f"  Returncode: {res3.returncode}")
    print(f"  Stderr: {res3.stderr.strip()}")
    assert res3.returncode == 76, f"Expected 76, got {res3.returncode}"
    assert "Access to secret path prohibited" in res3.stderr

    # 4. Basename prefix tilde (C-R17-3)
    res4 = run_dispatch("view_file", "config/~app.php")
    print("\nScenario 4 (view_file config/~app.php):")
    print(f"  Returncode: {res4.returncode}")
    print(f"  Stderr: {res4.stderr.strip()}")
    assert res4.returncode == 76, f"Expected 76, got {res4.returncode}"
    assert "Access to secret path prohibited" in res4.stderr

    # 5. Lockfile prefix marker (C-R17-4)
    res5 = run_dispatch("view_file", "~$config/app.php")
    print("\nScenario 5 (view_file ~$config/app.php):")
    print(f"  Returncode: {res5.returncode}")
    print(f"  Stderr: {res5.stderr.strip()}")
    assert res5.returncode == 76, f"Expected 76, got {res5.returncode}"
    assert "Access to secret path prohibited" in res5.stderr

    # 6. Trailing dot on double backup via git log (C-R17-1)
    res6 = run_dispatch("run_command", "git log -p .env.bak.old.")
    print("\nScenario 6 (git log -p .env.bak.old.):")
    print(f"  Returncode: {res6.returncode}")
    print(f"  Stderr: {res6.stderr.strip()}")
    assert res6.returncode == 76, f"Expected 76, got {res6.returncode}"
    assert "Secret path access prohibited" in res6.stderr

    # 7. Multiple message options tracking (C-R17-5)
    res7 = run_dispatch("run_command", 'git commit -m "msg" --message="--output=/tmp/evil"')
    print("\nScenario 7 (git commit -m 'msg' --message='--output=/tmp/evil'):")
    print(f"  Returncode: {res7.returncode}")
    assert res7.returncode == 0, f"Expected 0, got {res7.returncode}. Stderr: {res7.stderr}"
    print("  Commit with both -m and --message allowed without false-positive EC 73 (EC 0).")

    print("\nALL ROUND 18 SCENARIOS PASSED PERFECTLY (100%).\n")

if __name__ == "__main__":
    test_round18_scenarios()
