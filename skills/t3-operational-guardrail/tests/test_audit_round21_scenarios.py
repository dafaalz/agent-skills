#!/usr/bin/env python3
"""
Test Suite: Audit Round 21 Scenarios
Verifies S-N2 priority order reconciliation:
1. Mutation tools strictly prioritize control path tamper checks (edit_file ~/.gitconfig -> EC 80) [S-N2]
2. Read tools enforce secret path protection (view_file ~/.gitconfig -> EC 76) [S-N2]
3. Mutation on XDG git config strictly blocks with EC 80 (edit_file ~/.config/git/config -> EC 80) [S-N2]
4. Read on XDG git config blocks with EC 76 (view_file ~/.config/git/config -> EC 76) [S-N2]
5. Clean literal repeated lockfile check (view_file ~$~$config/app.php -> EC 76) [C-R20-1]
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
        "--session", "audit_round21"
    ]
    if targets is not None:
        args.extend(["--targets", ",".join(targets)])
    return subprocess.run(args, cwd=cwd, capture_output=True, text=True)

def test_round21_scenarios():
    print("=== Running Audit Round 21 Scenarios ===\n")

    # 1. edit_file ~/.gitconfig (S-N2: Mutation tools prioritize EC 80)
    res1 = run_dispatch("edit_file", "~/.gitconfig")
    print("Scenario 1 (edit_file ~/.gitconfig):")
    print(f"  Returncode: {res1.returncode}")
    print(f"  Stderr: {res1.stderr.strip()}")
    assert res1.returncode == 80, f"Expected 80, got {res1.returncode}"
    assert "Tampering with control artifact prohibited" in res1.stderr

    # 2. view_file ~/.gitconfig (S-N2: Read tools prioritize EC 76)
    res2 = run_dispatch("view_file", "~/.gitconfig")
    print("\nScenario 2 (view_file ~/.gitconfig):")
    print(f"  Returncode: {res2.returncode}")
    print(f"  Stderr: {res2.stderr.strip()}")
    assert res2.returncode == 76, f"Expected 76, got {res2.returncode}"
    assert "Access to secret path prohibited" in res2.stderr

    # 3. edit_file ~/.config/git/config (S-N2: Mutation tools prioritize EC 80)
    res3 = run_dispatch("edit_file", "~/.config/git/config")
    print("\nScenario 3 (edit_file ~/.config/git/config):")
    print(f"  Returncode: {res3.returncode}")
    print(f"  Stderr: {res3.stderr.strip()}")
    assert res3.returncode == 80, f"Expected 80, got {res3.returncode}"
    assert "Tampering with control artifact prohibited" in res3.stderr

    # 4. view_file ~/.config/git/config (S-N2: Read tools prioritize EC 76)
    res4 = run_dispatch("view_file", "~/.config/git/config")
    print("\nScenario 4 (view_file ~/.config/git/config):")
    print(f"  Returncode: {res4.returncode}")
    print(f"  Stderr: {res4.stderr.strip()}")
    assert res4.returncode == 76, f"Expected 76, got {res4.returncode}"
    assert "Access to secret path prohibited" in res4.stderr

    # 5. view_file ~$~$config/app.php (C-R20-1 clean literal verification)
    res5 = run_dispatch("view_file", "~$~$config/app.php")
    print("\nScenario 5 (view_file ~$~$config/app.php):")
    print(f"  Returncode: {res5.returncode}")
    print(f"  Stderr: {res5.stderr.strip()}")
    assert res5.returncode == 76, f"Expected 76, got {res5.returncode}"
    assert "Access to secret path prohibited" in res5.stderr

    print("\nALL ROUND 21 SCENARIOS PASSED PERFECTLY (100%).\n")

if __name__ == "__main__":
    test_round21_scenarios()
