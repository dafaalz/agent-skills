#!/usr/bin/env python3
"""
Test Suite: Audit Round 16 Scenarios
Verifies:
1. git log -p ':!vendor' is blocked as prohibited pathspec magic (EC 74) [S-N1 Residual]
2. git log -p ':^config/app.php' is blocked as secret path (EC 76) [S-N1 Residual]
3. git log ':^src/app.py' is blocked as prohibited pathspec magic (EC 74) [S-N1 Residual]
4. git log -p ':/config/app.php' is blocked as secret path (EC 76) [S-N1 Residual]
5. git log ':/src/app.py' is blocked as prohibited pathspec magic (EC 74) [S-N1 Residual]
6. git commit --message="-c legitimate message" tracks commit_msg_indices (EC 0) [Cosmetic-Consistency]
7. view_file config/app.php.bak is blocked as secret path (EC 76) [Cosmetic-Backup Variant]
8. view_file .env.swp is blocked as secret path (EC 76) [Cosmetic-Backup Variant]
9. git log -p config/app.php.orig is blocked as secret path (EC 76) [Cosmetic-Backup Variant]
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
        "--session", "audit_round16"
    ]
    if targets is not None:
        args.extend(["--targets", ",".join(targets)])
    return subprocess.run(args, cwd=cwd, capture_output=True, text=True)

def test_round16_scenarios():
    print("=== Running Audit Round 16 Scenarios ===\n")

    # 1. git log -p ':!vendor' (S-N1 Residual: :! pathspec magic check)
    res1 = run_dispatch("run_command", "git log -p ':!vendor'")
    print("Scenario 1 (git log -p ':!vendor'):")
    print(f"  Returncode: {res1.returncode}")
    print(f"  Stderr: {res1.stderr.strip()}")
    assert res1.returncode == 74, f"Expected 74, got {res1.returncode}"
    assert "Git pathspec magic prefix prohibited" in res1.stderr

    # 2. git log -p ':^config/app.php' (S-N1 Residual: secret path with :^ prefix)
    res2 = run_dispatch("run_command", "git log -p ':^config/app.php'")
    print("\nScenario 2 (git log -p ':^config/app.php'):")
    print(f"  Returncode: {res2.returncode}")
    print(f"  Stderr: {res2.stderr.strip()}")
    assert res2.returncode == 76, f"Expected 76, got {res2.returncode}"
    assert "Secret path access prohibited" in res2.stderr

    # 3. git log ':^src/app.py' (S-N1 Residual: non-secret :^ pathspec magic rejection)
    res3 = run_dispatch("run_command", "git log ':^src/app.py'")
    print("\nScenario 3 (git log ':^src/app.py'):")
    print(f"  Returncode: {res3.returncode}")
    print(f"  Stderr: {res3.stderr.strip()}")
    assert res3.returncode == 74, f"Expected 74, got {res3.returncode}"
    assert "Git pathspec magic prefix prohibited" in res3.stderr

    # 4. git log -p ':/config/app.php' (S-N1 Residual: secret path with :/ prefix)
    res4 = run_dispatch("run_command", "git log -p ':/config/app.php'")
    print("\nScenario 4 (git log -p ':/config/app.php'):")
    print(f"  Returncode: {res4.returncode}")
    print(f"  Stderr: {res4.stderr.strip()}")
    assert res4.returncode == 76, f"Expected 76, got {res4.returncode}"
    assert "Secret path access prohibited" in res4.stderr

    # 5. git log ':/src/app.py' (S-N1 Residual: non-secret :/ pathspec magic rejection)
    res5 = run_dispatch("run_command", "git log ':/src/app.py'")
    print("\nScenario 5 (git log ':/src/app.py'):")
    print(f"  Returncode: {res5.returncode}")
    print(f"  Stderr: {res5.stderr.strip()}")
    assert res5.returncode == 74, f"Expected 74, got {res5.returncode}"
    assert "Git pathspec magic prefix prohibited" in res5.stderr

    # 6. git commit --message="-c legitimate message" (commit_msg_indices tracking)
    res6 = run_dispatch("run_command", 'git commit --message="-c legitimate message"')
    print("\nScenario 6 (git commit --message='-c legitimate message'):")
    print(f"  Returncode: {res6.returncode}")
    assert res6.returncode == 0, f"Expected 0, got {res6.returncode}. Stderr: {res6.stderr}"
    print("  Commit with --message='-c ...' allowed without false-positive EC 73 (EC 0).")

    # 7. view_file config/app.php.bak (Backup variant secret protection)
    res7 = run_dispatch("view_file", "config/app.php.bak")
    print("\nScenario 7 (view_file config/app.php.bak):")
    print(f"  Returncode: {res7.returncode}")
    print(f"  Stderr: {res7.stderr.strip()}")
    assert res7.returncode == 76, f"Expected 76, got {res7.returncode}"
    assert "Access to secret path prohibited" in res7.stderr

    # 8. view_file .env.swp (Swap file variant secret protection)
    res8 = run_dispatch("view_file", ".env.swp")
    print("\nScenario 8 (view_file .env.swp):")
    print(f"  Returncode: {res8.returncode}")
    print(f"  Stderr: {res8.stderr.strip()}")
    assert res8.returncode == 76, f"Expected 76, got {res8.returncode}"
    assert "Access to secret path prohibited" in res8.stderr

    # 9. git log -p config/app.php.orig (Backup diff secret protection)
    res9 = run_dispatch("run_command", "git log -p config/app.php.orig")
    print("\nScenario 9 (git log -p config/app.php.orig):")
    print(f"  Returncode: {res9.returncode}")
    print(f"  Stderr: {res9.stderr.strip()}")
    assert res9.returncode == 76, f"Expected 76, got {res9.returncode}"
    assert "Secret path access prohibited" in res9.stderr

    print("\nALL ROUND 16 SCENARIOS PASSED PERFECTLY (100%).\n")

if __name__ == "__main__":
    test_round16_scenarios()
