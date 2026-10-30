#!/usr/bin/env python3
"""
Test Suite: Audit Round 11 Scenarios
Verifies:
1. Combined short flag with attached key: -ccredential.https://x.helper=/tmp/evil is blocked (EC 73)
2. INI-format [core] askPass = /tmp/evil is blocked by hygiene (EC 73)
3. core.askPass=true is present in enforcing_configs
4. Commit message containing secret names (git commit -m "fix .env loader") is allowed (EC 0)
5. Commit message containing config/app.php (git commit -m "update config/app.php") is allowed (EC 0)
6. git log --format="%G?" signature inspection is blocked (EC 73)
7. git log --pretty="%G?" signature inspection is blocked (EC 73)
8. view_file on ~/.gitconfig is blocked as secret path (EC 76)
9. edit_file on ~/.gitconfig is blocked as control path (EC 80)
"""
import subprocess
import sys
import os
import tempfile
from pathlib import Path

T3_BIN = Path.home() / "Library/Application Support/t3/bin"
DISPATCH = T3_BIN / "t3_dispatch.py"

def run_dispatch(cmd_str: str, cwd: str = None):
    if cwd is None:
        cwd = os.getcwd()
    args = [
        sys.executable, str(DISPATCH),
        "--tool", "run_command",
        "--payload", cmd_str,
        "--session", "audit_round11"
    ]
    return subprocess.run(args, cwd=cwd, capture_output=True, text=True)

def test_round11_scenarios():
    print("=== Running Audit Round 11 Scenarios ===\n")

    # 1. Combined short flag -ccredential.https://x.helper=/tmp/evil (F-1 fix verification)
    res = run_dispatch("git -ccredential.https://x.helper=/tmp/evil status")
    print(f"Scenario 1 (Combined short flag -c<key>=<val>):")
    print(f"  Returncode: {res.returncode}")
    print(f"  Stderr: {res.stderr.strip()}")
    assert res.returncode == 73, f"Expected 73, got {res.returncode}"
    assert "Prohibited single-token short Git flag" in res.stderr

    # 2. INI-format [core] askPass = /tmp/evil in .git/config (S-1 fix verification)
    with tempfile.TemporaryDirectory() as td:
        subprocess.run(["git", "init"], cwd=td, capture_output=True)
        cfg = Path(td) / ".git/config"
        with open(cfg, "a") as f:
            f.write('\n[core]\n\taskPass = /tmp/evil\n')
        res = run_dispatch("git status", cwd=td)
        print(f"\nScenario 2 (INI [core] askPass = /tmp/evil in .git/config):")
        print(f"  Returncode: {res.returncode}")
        print(f"  Stderr: {res.stderr.strip()}")
        assert res.returncode == 73, f"Expected 73, got {res.returncode}"
        assert "askpass" in res.stderr

    # 3. core.askPass=true injected in enforcing_configs
    res = run_dispatch('git status')
    print(f"\nScenario 3 (core.askPass=true injection verification):")
    print(f"  Returncode: {res.returncode}")
    assert res.returncode == 0
    assert "core.askPass=true" in res.stdout
    print("  core.askPass=true verified present in argv.")

    # 4. Commit message with .env (Serious-2 fix verification)
    res = run_dispatch('git commit -m "fix .env loader"')
    print(f"\nScenario 4 (git commit -m 'fix .env loader'):")
    print(f"  Returncode: {res.returncode}")
    assert res.returncode == 0, f"Expected 0, got {res.returncode}. Stderr: {res.stderr}"
    print("  Commit with '.env' in message allowed (EC 0).")

    # 5. Commit message with config/app.php
    res = run_dispatch('git commit -m "update config/app.php logic"')
    print(f"\nScenario 5 (git commit -m 'update config/app.php logic'):")
    print(f"  Returncode: {res.returncode}")
    assert res.returncode == 0, f"Expected 0, got {res.returncode}. Stderr: {res.stderr}"
    print("  Commit with 'config/app.php' in message allowed (EC 0).")

    # 6. git log --format="%G?" signature inspection (Serious-3 fix verification)
    res = run_dispatch('git log --format="%G?"')
    print(f"\nScenario 6 (git log --format='%G?'):")
    print(f"  Returncode: {res.returncode}")
    print(f"  Stderr: {res.stderr.strip()}")
    assert res.returncode == 73, f"Expected 73, got {res.returncode}"
    assert "Signature inspection" in res.stderr

    # 7. git log --pretty="%G?"
    res = run_dispatch('git log --pretty="%G?"')
    print(f"\nScenario 7 (git log --pretty='%G?'):")
    print(f"  Returncode: {res.returncode}")
    print(f"  Stderr: {res.stderr.strip()}")
    assert res.returncode == 73, f"Expected 73, got {res.returncode}"
    assert "Signature inspection" in res.stderr

    # 8. view_file on ~/.gitconfig is blocked as secret path (EC 76)
    res = subprocess.run([
        sys.executable, str(DISPATCH),
        "--tool", "view_file",
        "--payload", str(Path.home() / ".gitconfig"),
        "--session", "audit_round11"
    ], capture_output=True, text=True)
    print(f"\nScenario 8 (view_file on ~/.gitconfig):")
    print(f"  Returncode: {res.returncode}")
    print(f"  Stderr: {res.stderr.strip()}")
    assert res.returncode == 76, f"Expected 76, got {res.returncode}"

    # 9. edit_file on ~/.gitconfig is blocked as control path (EC 80)
    res = subprocess.run([
        sys.executable, str(DISPATCH),
        "--tool", "edit_file",
        "--payload", str(Path.home() / ".gitconfig"),
        "--session", "audit_round11"
    ], capture_output=True, text=True)
    print(f"\nScenario 9 (edit_file on ~/.gitconfig):")
    print(f"  Returncode: {res.returncode}")
    print(f"  Stderr: {res.stderr.strip()}")
    assert res.returncode == 80, f"Expected 80, got {res.returncode}"

    print("\nALL ROUND 11 SCENARIOS PASSED PERFECTLY (100%).\n")

if __name__ == "__main__":
    test_round11_scenarios()
