#!/usr/bin/env python3
"""
Test Suite: Audit Round 20 Scenarios
Verifies:
1. Repeated lockfile prefix (view_file ~$~$config/app.php) blocked as secret path (EC 76) [C-R19-1]
2. Repeated tilde prefix (view_file ~~config/app.php) blocked as secret path (EC 76) [C-R19-1]
3. Mixed repeated prefix (view_file ~$~config/app.php) blocked as secret path (EC 76) [C-R19-1]
4. Direct repo secret (view_file config/app.php) blocked as secret path (EC 76) [C-R19-4]
5. User git config secret (view_file ~/.gitconfig) blocked as secret path (EC 76) [C-R19-4]
6. User XDG git config secret (view_file ~/.config/git/config) blocked as secret path (EC 76) [C-R19-4]
7. Database secret diff (git log -p config/database.php) blocked as secret path (EC 76) [C-R19-4]
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
        "--session", "audit_round20"
    ]
    if targets is not None:
        args.extend(["--targets", ",".join(targets)])
    return subprocess.run(args, cwd=cwd, capture_output=True, text=True)

def test_round20_scenarios():
    print("=== Running Audit Round 20 Scenarios ===\n")

    # 1. view_file ~$~$config/app.php (C-R19-1)
    res1 = run_dispatch("view_file", "~$~$config/app.php")
    print("Scenario 1 (view_file ~$~$config/app.php):")
    print(f"  Returncode: {res1.returncode}")
    print(f"  Stderr: {res1.stderr.strip()}")
    assert res1.returncode == 76, f"Expected 76, got {res1.returncode}"
    assert "Access to secret path prohibited" in res1.stderr

    # 2. view_file ~~config/app.php (C-R19-1)
    res2 = run_dispatch("view_file", "~~config/app.php")
    print("\nScenario 2 (view_file ~~config/app.php):")
    print(f"  Returncode: {res2.returncode}")
    print(f"  Stderr: {res2.stderr.strip()}")
    assert res2.returncode == 76, f"Expected 76, got {res2.returncode}"
    assert "Access to secret path prohibited" in res2.stderr

    # 3. view_file ~$~config/app.php (C-R19-1)
    res3 = run_dispatch("view_file", "~$~config/app.php")
    print("\nScenario 3 (view_file ~$~config/app.php):")
    print(f"  Returncode: {res3.returncode}")
    print(f"  Stderr: {res3.stderr.strip()}")
    assert res3.returncode == 76, f"Expected 76, got {res3.returncode}"
    assert "Access to secret path prohibited" in res3.stderr

    # 4. view_file config/app.php (C-R19-4 baseline)
    res4 = run_dispatch("view_file", "config/app.php")
    print("\nScenario 4 (view_file config/app.php):")
    print(f"  Returncode: {res4.returncode}")
    print(f"  Stderr: {res4.stderr.strip()}")
    assert res4.returncode == 76, f"Expected 76, got {res4.returncode}"
    assert "Access to secret path prohibited" in res4.stderr

    # 5. view_file ~/.gitconfig (C-R19-4)
    res5 = run_dispatch("view_file", "~/.gitconfig")
    print("\nScenario 5 (view_file ~/.gitconfig):")
    print(f"  Returncode: {res5.returncode}")
    print(f"  Stderr: {res5.stderr.strip()}")
    assert res5.returncode == 76, f"Expected 76, got {res5.returncode}"
    assert "Access to secret path prohibited" in res5.stderr

    # 6. view_file ~/.config/git/config (C-R19-4)
    res6 = run_dispatch("view_file", "~/.config/git/config")
    print("\nScenario 6 (view_file ~/.config/git/config):")
    print(f"  Returncode: {res6.returncode}")
    print(f"  Stderr: {res6.stderr.strip()}")
    assert res6.returncode == 76, f"Expected 76, got {res6.returncode}"
    assert "Access to secret path prohibited" in res6.stderr

    # 7. git log -p config/database.php (C-R19-4)
    res7 = run_dispatch("run_command", "git log -p config/database.php")
    print("\nScenario 7 (git log -p config/database.php):")
    print(f"  Returncode: {res7.returncode}")
    print(f"  Stderr: {res7.stderr.strip()}")
    assert res7.returncode == 76, f"Expected 76, got {res7.returncode}"
    assert "Secret path access prohibited" in res7.stderr

    print("\nALL ROUND 20 SCENARIOS PASSED PERFECTLY (100%).\n")

if __name__ == "__main__":
    test_round20_scenarios()
