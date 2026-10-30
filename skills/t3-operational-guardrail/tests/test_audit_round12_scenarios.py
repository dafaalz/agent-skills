#!/usr/bin/env python3
"""
Test Suite: Audit Round 12 Scenarios
Verifies:
1. git commit -a -m "msg" is blocked (EC 74)
2. git commit --all -m "msg" is blocked (EC 74)
3. git commit --include -m "msg" is blocked (EC 74)
4. git commit -m "-c legitimate commit message" is allowed (EC 0, resolving cosmetic flaw)
5. git add vendor/src/config.py with target ["src/config.py"] is blocked (EC 79, component-wise comparison)
6. git add src/config.py with target ["src/config.py"] is allowed (EC 0)
7. git log --format="%h %G?" signature inspection is blocked (EC 73)
8. git log --pretty=format:"%G?" signature inspection is blocked (EC 73)
9. git log --format "%h %G?" signature inspection is blocked (EC 73)
10. git log -n 5 safe log is allowed (EC 0)
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
        "--session", "audit_round12"
    ]
    if targets:
        args.extend(["--targets", ",".join(targets)])
    return subprocess.run(args, cwd=cwd, capture_output=True, text=True)

def test_round12_scenarios():
    print("=== Running Audit Round 12 Scenarios ===\n")

    # 1. git commit -a -m "msg" (S-1 fix verification)
    res = run_dispatch('git commit -a -m "unmanifest staging attempt"')
    print("Scenario 1 (git commit -a -m 'msg'):")
    print(f"  Returncode: {res.returncode}")
    print(f"  Stderr: {res.stderr.strip()}")
    assert res.returncode == 74, f"Expected 74, got {res.returncode}"
    assert "Blanket staging" in res.stderr

    # 2. git commit --all -m "msg" (S-1 fix verification)
    res = run_dispatch('git commit --all -m "unmanifest staging attempt"')
    print("\nScenario 2 (git commit --all -m 'msg'):")
    print(f"  Returncode: {res.returncode}")
    print(f"  Stderr: {res.stderr.strip()}")
    assert res.returncode == 74, f"Expected 74, got {res.returncode}"
    assert "Blanket staging" in res.stderr

    # 3. git commit --include -m "msg" (S-1 fix verification)
    res = run_dispatch('git commit --include -m "unmanifest staging attempt"')
    print("\nScenario 3 (git commit --include -m 'msg'):")
    print(f"  Returncode: {res.returncode}")
    print(f"  Stderr: {res.stderr.strip()}")
    assert res.returncode in (73, 74), f"Expected 73 or 74, got {res.returncode}"

    # 4. Commit message starting with -c (Cosmetic fix verification)
    res = run_dispatch('git commit -m "-c legitimate commit message"')
    print("\nScenario 4 (git commit -m '-c legitimate commit message'):")
    print(f"  Returncode: {res.returncode}")
    assert res.returncode == 0, f"Expected 0, got {res.returncode}. Stderr: {res.stderr}"
    print("  Commit with '-c ...' message allowed (EC 0).")

    # 5. git add vendor/src/config.py with target ["src/config.py"] (S-2 suffix bypass fix verification)
    with tempfile.TemporaryDirectory() as td:
        subprocess.run(["git", "init"], cwd=td, capture_output=True)
        vendor_dir = Path(td) / "vendor/src"
        vendor_dir.mkdir(parents=True, exist_ok=True)
        (vendor_dir / "config.py").write_text("# vendor config\n")
        res = run_dispatch("git add vendor/src/config.py", cwd=td, targets=["src/config.py"])
        print("\nScenario 5 (git add vendor/src/config.py with manifest ['src/config.py']):")
        print(f"  Returncode: {res.returncode}")
        print(f"  Stderr: {res.stderr.strip()}")
        assert res.returncode == 79, f"Expected 79, got {res.returncode}"
        assert "outside manifest target scope" in res.stderr

    # 6. git add src/config.py with target ["src/config.py"] (Component-wise valid match)
    with tempfile.TemporaryDirectory() as td:
        subprocess.run(["git", "init"], cwd=td, capture_output=True)
        src_dir = Path(td) / "src"
        src_dir.mkdir(parents=True, exist_ok=True)
        (src_dir / "config.py").write_text("# valid src config\n")
        res = run_dispatch("git add src/config.py", cwd=td, targets=["src/config.py"])
        print("\nScenario 6 (git add src/config.py with manifest ['src/config.py']):")
        print(f"  Returncode: {res.returncode}")
        assert res.returncode == 0, f"Expected 0, got {res.returncode}. Stderr: {res.stderr}"
        print("  Staging manifest target allowed (EC 0).")

    # 7. git log --format="%h %G?" (Serious-1 fix verification)
    res = run_dispatch('git log --format="%h %G?"')
    print("\nScenario 7 (git log --format='%h %G?'):")
    print(f"  Returncode: {res.returncode}")
    print(f"  Stderr: {res.stderr.strip()}")
    assert res.returncode == 73, f"Expected 73, got {res.returncode}"
    assert "Signature inspection" in res.stderr

    # 8. git log --pretty=format:"%G?" (Serious-1 fix verification)
    res = run_dispatch('git log --pretty=format:"%G?"')
    print("\nScenario 8 (git log --pretty=format:'%G?'):")
    print(f"  Returncode: {res.returncode}")
    print(f"  Stderr: {res.stderr.strip()}")
    assert res.returncode == 73, f"Expected 73, got {res.returncode}"
    assert "Signature inspection" in res.stderr

    # 9. git log --format "%h %G?" (Two-token format inspection)
    res = run_dispatch('git log --format "%h %G?"')
    print("\nScenario 9 (git log --format '%h %G?'):")
    print(f"  Returncode: {res.returncode}")
    print(f"  Stderr: {res.stderr.strip()}")
    assert res.returncode == 73, f"Expected 73, got {res.returncode}"
    assert "Signature inspection" in res.stderr

    # 10. git log -n 5 (Safe log execution)
    res = run_dispatch("git log -n 5")
    print("\nScenario 10 (git log -n 5 safe invocation):")
    print(f"  Returncode: {res.returncode}")
    assert res.returncode == 0, f"Expected 0, got {res.returncode}. Stderr: {res.stderr}"
    print("  Standard git log allowed (EC 0).")

    print("\nALL ROUND 12 SCENARIOS PASSED PERFECTLY (100%).\n")

if __name__ == "__main__":
    test_round12_scenarios()
