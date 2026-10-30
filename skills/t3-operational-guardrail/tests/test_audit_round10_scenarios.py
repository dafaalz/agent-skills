#!/usr/bin/env python3
"""
Test Suite: Audit Round 10 Scenarios
Verifies:
1. git commit -m works and is allowed (EC 0)
2. INI-format [pager] in .git/config is blocked (EC 73)
3. git --paginate flag is blocked (EC 73)
4. INI-format [gpg] and git log --show-signature are blocked (EC 73)
5. INI-format [url] insteadOf rewriting is blocked (EC 73)
6. INI-format [credential] helper is blocked (EC 73)
7. Secret path access to config/database.php is blocked (EC 76)
8. Branch rename git branch -m is blocked by branch grammar (EC 74)
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
        "--session", "audit_round10"
    ]
    return subprocess.run(args, cwd=cwd, capture_output=True, text=True)

def test_round10_scenarios():
    print("=== Running Audit Round 10 Attack & Functional Scenarios ===\n")

    # 1. Functional commit -m (S-1 fix verification)
    res = run_dispatch('git commit -m "feat: standard conventional commit"')
    print(f"Scenario 1 (Valid git commit -m):")
    print(f"  Returncode: {res.returncode}")
    print(f"  Stdout: {res.stdout.strip()}")
    assert res.returncode == 0, f"Expected 0, got {res.returncode}. Stderr: {res.stderr}"

    # 2. INI-format [pager] in .git/config (F-1 fix verification)
    with tempfile.TemporaryDirectory() as td:
        subprocess.run(["git", "init"], cwd=td, capture_output=True)
        cfg = Path(td) / ".git/config"
        with open(cfg, "a") as f:
            f.write('\n[pager]\n\tstatus = /tmp/evil\n')
        res = run_dispatch("git status", cwd=td)
        print(f"\nScenario 2 (INI [pager] in .git/config):")
        print(f"  Returncode: {res.returncode}")
        print(f"  Stderr: {res.stderr.strip()}")
        assert res.returncode == 73, f"Expected 73, got {res.returncode}"
        assert "[pager]" in res.stderr

    # 3. --paginate flag blocked (F-1 / Serious-3 fix verification)
    res = run_dispatch("git --paginate status")
    print(f"\nScenario 3 (git --paginate flag):")
    print(f"  Returncode: {res.returncode}")
    print(f"  Stderr: {res.stderr.strip()}")
    assert res.returncode == 73, f"Expected 73, got {res.returncode}"
    assert "--paginate" in res.stderr

    # 4. INI-format [gpg] and git log --show-signature (S-3 fix verification)
    with tempfile.TemporaryDirectory() as td:
        subprocess.run(["git", "init"], cwd=td, capture_output=True)
        cfg = Path(td) / ".git/config"
        with open(cfg, "a") as f:
            f.write('\n[gpg]\n\tprogram = /tmp/evil\n')
        res = run_dispatch("git status", cwd=td)
        print(f"\nScenario 4A (INI [gpg] in .git/config):")
        print(f"  Returncode: {res.returncode}")
        print(f"  Stderr: {res.stderr.strip()}")
        assert res.returncode == 73, f"Expected 73, got {res.returncode}"
        assert "[gpg]" in res.stderr

    res = run_dispatch("git log --show-signature")
    print(f"\nScenario 4B (git log --show-signature flag):")
    print(f"  Returncode: {res.returncode}")
    print(f"  Stderr: {res.stderr.strip()}")
    assert res.returncode == 73, f"Expected 73, got {res.returncode}"
    assert "--show-signature" in res.stderr

    # 5. INI-format [url] insteadOf rewriting (S-4 fix verification)
    with tempfile.TemporaryDirectory() as td:
        subprocess.run(["git", "init"], cwd=td, capture_output=True)
        cfg = Path(td) / ".git/config"
        with open(cfg, "a") as f:
            f.write('\n[url "https://attacker.com/"]\n\tinsteadOf = https://github.com/\n')
        res = run_dispatch("git status", cwd=td)
        print(f"\nScenario 5 (INI [url] insteadOf rewriting):")
        print(f"  Returncode: {res.returncode}")
        print(f"  Stderr: {res.stderr.strip()}")
        assert res.returncode == 73, f"Expected 73, got {res.returncode}"
        assert "[url" in res.stderr

    # 6. INI-format [credential] helper (S-5 fix verification)
    with tempfile.TemporaryDirectory() as td:
        subprocess.run(["git", "init"], cwd=td, capture_output=True)
        cfg = Path(td) / ".git/config"
        with open(cfg, "a") as f:
            f.write('\n[credential]\n\thelper = /tmp/evil\n')
        res = run_dispatch("git status", cwd=td)
        print(f"\nScenario 6 (INI [credential] helper):")
        print(f"  Returncode: {res.returncode}")
        print(f"  Stderr: {res.stderr.strip()}")
        assert res.returncode == 73, f"Expected 73, got {res.returncode}"
        assert "[credential]" in res.stderr

    # 7. Framework-specific secret path config/database.php (Serious-2 fix verification)
    res = run_dispatch("git diff config/database.php")
    print(f"\nScenario 7 (git diff on config/database.php):")
    print(f"  Returncode: {res.returncode}")
    print(f"  Stderr: {res.stderr.strip()}")
    assert res.returncode == 76, f"Expected 76, got {res.returncode}"
    assert "Secret path access prohibited" in res.stderr

    # 8. Branch rename git branch -m blocked by branch grammar (S-1 branch isolation)
    res = run_dispatch("git branch -m old-feat new-feat")
    print(f"\nScenario 8 (git branch -m branch rename):")
    print(f"  Returncode: {res.returncode}")
    print(f"  Stderr: {res.stderr.strip()}")
    assert res.returncode == 74, f"Expected 74, got {res.returncode}"
    assert "Branch mutation flag prohibited" in res.stderr

    print("\nALL ROUND 10 SCENARIOS PASSED PERFECTLY (100%).\n")

if __name__ == "__main__":
    test_round10_scenarios()
