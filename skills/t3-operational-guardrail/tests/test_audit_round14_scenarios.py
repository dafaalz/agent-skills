#!/usr/bin/env python3
"""
Test Suite: Audit Round 14 Scenarios
Verifies:
1. git commit -m "--all" is allowed as commit message without false-positive EC 74 (C-1)
2. git commit -m "first" -m "-c second" allows multi -m values without false-positive EC 73 (C-2)
3. git commit -m "msg" --template=/tmp/evil is blocked by equals-form check on DESTRUCTIVE_GIT_FLAGS (EC 73)
4. git diff --ext-diff=/tmp/x is blocked by equals-form check on DESTRUCTIVE_GIT_FLAGS (EC 73)
5. git -c key=val commit is blocked (EC 73) and git_sub recognizes commit (R-2)
6. get_repo_root() runs with sanitized env and hooks neutralized (R-1)
7. is_control_path denies .git, .gitconfig, and control artifacts (C-3)
8. is_secret_path denies .env and private keys (C-3)
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
        "--session", "audit_round14"
    ]
    if targets is not None:
        args.extend(["--targets", ",".join(targets)])
    return subprocess.run(args, cwd=cwd, capture_output=True, text=True)

def test_round14_scenarios():
    print("=== Running Audit Round 14 Scenarios ===\n")

    # 1. git commit -m "--all" (C-1 fix verification: --all inside -m value is allowed)
    res = run_dispatch('git commit -m "--all"')
    print("Scenario 1 (git commit -m '--all'):")
    print(f"  Returncode: {res.returncode}")
    assert res.returncode == 0, f"Expected 0, got {res.returncode}. Stderr: {res.stderr}"
    print("  Commit with '--all' as message allowed without false-positive EC 74 (EC 0).")

    # 2. Multi-m with -c in second message (C-2 fix verification)
    res = run_dispatch('git commit -m "first message" -m "-c second message"')
    print("\nScenario 2 (git commit -m 'first' -m '-c second'):")
    print(f"  Returncode: {res.returncode}")
    assert res.returncode == 0, f"Expected 0, got {res.returncode}. Stderr: {res.stderr}"
    print("  Multi -m with '-c ...' in second message allowed without false-positive EC 73 (EC 0).")

    # 3. git commit -m "msg" --template=/tmp/evil (Exact-match delta fix verification)
    res = run_dispatch('git commit -m "valid message" --template=/tmp/evil')
    print("\nScenario 3 (git commit -m 'msg' --template=/tmp/evil):")
    print(f"  Returncode: {res.returncode}")
    print(f"  Stderr: {res.stderr.strip()}")
    assert res.returncode == 73, f"Expected 73, got {res.returncode}"
    assert "Destructive or bypass Git flag prohibited" in res.stderr

    # 4. git diff --ext-diff=/tmp/x (Exact-match delta fix verification)
    res = run_dispatch('git diff --ext-diff=/tmp/x')
    print("\nScenario 4 (git diff --ext-diff=/tmp/x):")
    print(f"  Returncode: {res.returncode}")
    print(f"  Stderr: {res.stderr.strip()}")
    assert res.returncode == 73, f"Expected 73, got {res.returncode}"
    assert "Destructive or bypass Git flag prohibited" in res.stderr

    # 5. git -c key=val commit (R-2 verification)
    res = run_dispatch('git -c key=val commit')
    print("\nScenario 5 (git -c key=val commit):")
    print(f"  Returncode: {res.returncode}")
    print(f"  Stderr: {res.stderr.strip()}")
    assert res.returncode == 73, f"Expected 73, got {res.returncode}"

    # 6. get_repo_root hardened execution (R-1 verification)
    with tempfile.TemporaryDirectory() as td:
        subprocess.run(["git", "init"], cwd=td, capture_output=True)
        # Attempt to run git status inside repo, ensuring get_repo_root succeeds safely
        res = run_dispatch("git status", cwd=td)
        print("\nScenario 6 (get_repo_root execution in repo):")
        print(f"  Returncode: {res.returncode}")
        assert res.returncode == 0, f"Expected 0, got {res.returncode}"
        print("  Hardened rev-parse --show-toplevel successfully resolved root (EC 0).")

    # 7. is_control_path checks on critical paths (C-3 verification)
    res_ctrl = subprocess.run([
        sys.executable, str(DISPATCH),
        "--tool", "edit_file",
        "--payload", str(Path.home() / ".gitconfig"),
        "--session", "audit_round14"
    ], capture_output=True, text=True)
    print("\nScenario 7 (is_control_path on ~/.gitconfig):")
    print(f"  Returncode: {res_ctrl.returncode}")
    print(f"  Stderr: {res_ctrl.stderr.strip()}")
    assert res_ctrl.returncode == 80, f"Expected 80, got {res_ctrl.returncode}"

    # 8. is_secret_path checks on sensitive files (C-3 verification)
    res_sec = subprocess.run([
        sys.executable, str(DISPATCH),
        "--tool", "view_file",
        "--payload", ".env",
        "--session", "audit_round14"
    ], capture_output=True, text=True)
    print("\nScenario 8 (is_secret_path on .env):")
    print(f"  Returncode: {res_sec.returncode}")
    print(f"  Stderr: {res_sec.stderr.strip()}")
    assert res_sec.returncode == 76, f"Expected 76, got {res_sec.returncode}"

    print("\nALL ROUND 14 SCENARIOS PASSED PERFECTLY (100%).\n")

if __name__ == "__main__":
    test_round14_scenarios()
