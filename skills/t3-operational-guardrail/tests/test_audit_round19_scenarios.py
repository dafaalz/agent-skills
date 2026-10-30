#!/usr/bin/env python3
"""
Test Suite: Audit Round 19 Scenarios
Verifies:
1. Home directory secret file (view_file ~/.env) blocked as secret path (EC 76) [C-R18-4]
2. Home directory git config (view_file ~/.config/git/config) blocked as secret path (EC 76) [C-R18-4]
3. git log -p on home directory secret (git log -p ~/.env) blocked as secret path (EC 76) [C-R18-4]
4. Module-level hoisted normalize_backup_path (view_file config/app.php.bak.) blocked (EC 76) [C-R18-1]
5. Module-level hoisted normalize_backup_path (view_file ~config/app.php) blocked (EC 76) [C-R18-1]
6. Safe-direction handling of ~user segments (view_file ~user/config/app.php) blocked (EC 76) [C-R18-2]
7. Lockfile prefix with module-level normalizer (view_file ~$config/app.php) blocked (EC 76) [C-R18-1]
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
        "--session", "audit_round19"
    ]
    if targets is not None:
        args.extend(["--targets", ",".join(targets)])
    return subprocess.run(args, cwd=cwd, capture_output=True, text=True)

def test_round19_scenarios():
    print("=== Running Audit Round 19 Scenarios ===\n")

    # 1. view_file ~/.env (C-R18-4)
    res1 = run_dispatch("view_file", "~/.env")
    print("Scenario 1 (view_file ~/.env):")
    print(f"  Returncode: {res1.returncode}")
    print(f"  Stderr: {res1.stderr.strip()}")
    assert res1.returncode == 76, f"Expected 76, got {res1.returncode}"
    assert "Access to secret path prohibited" in res1.stderr

    # 2. view_file ~/.config/git/config (C-R18-4)
    res2 = run_dispatch("view_file", "~/.config/git/config")
    print("\nScenario 2 (view_file ~/.config/git/config):")
    print(f"  Returncode: {res2.returncode}")
    print(f"  Stderr: {res2.stderr.strip()}")
    assert res2.returncode == 76, f"Expected 76, got {res2.returncode}"
    assert "Access to secret path prohibited" in res2.stderr

    # 3. git log -p ~/.env (C-R18-4)
    res3 = run_dispatch("run_command", "git log -p ~/.env")
    print("\nScenario 3 (git log -p ~/.env):")
    print(f"  Returncode: {res3.returncode}")
    print(f"  Stderr: {res3.stderr.strip()}")
    assert res3.returncode == 76, f"Expected 76, got {res3.returncode}"
    assert "Secret path access prohibited" in res3.stderr

    # 4. Hoisted normalize_backup_path trailing dot (C-R18-1)
    res4 = run_dispatch("view_file", "config/app.php.bak.")
    print("\nScenario 4 (view_file config/app.php.bak.):")
    print(f"  Returncode: {res4.returncode}")
    print(f"  Stderr: {res4.stderr.strip()}")
    assert res4.returncode == 76, f"Expected 76, got {res4.returncode}"
    assert "Access to secret path prohibited" in res4.stderr

    # 5. Hoisted normalize_backup_path prefix tilde (C-R18-1)
    res5 = run_dispatch("view_file", "~config/app.php")
    print("\nScenario 5 (view_file ~config/app.php):")
    print(f"  Returncode: {res5.returncode}")
    print(f"  Stderr: {res5.stderr.strip()}")
    assert res5.returncode == 76, f"Expected 76, got {res5.returncode}"
    assert "Access to secret path prohibited" in res5.stderr

    # 6. ~user segment stripping safe-direction (C-R18-2)
    res6 = run_dispatch("view_file", "~user/config/app.php")
    print("\nScenario 6 (view_file ~user/config/app.php):")
    print(f"  Returncode: {res6.returncode}")
    print(f"  Stderr: {res6.stderr.strip()}")
    assert res6.returncode == 76, f"Expected 76, got {res6.returncode}"
    assert "Access to secret path prohibited" in res6.stderr

    # 7. Lockfile prefix marker with hoisted normalizer (C-R18-1)
    res7 = run_dispatch("view_file", "~$config/app.php")
    print("\nScenario 7 (view_file ~$config/app.php):")
    print(f"  Returncode: {res7.returncode}")
    print(f"  Stderr: {res7.stderr.strip()}")
    assert res7.returncode == 76, f"Expected 76, got {res7.returncode}"
    assert "Access to secret path prohibited" in res7.stderr

    print("\nALL ROUND 19 SCENARIOS PASSED PERFECTLY (100%).\n")

if __name__ == "__main__":
    test_round19_scenarios()
