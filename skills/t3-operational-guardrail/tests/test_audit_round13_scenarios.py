#!/usr/bin/env python3
"""
Test Suite: Audit Round 13 Scenarios
Verifies:
1. git diff -m --output=<path> is blocked by global flags (EC 73) [F-1 Concrete Bypass A]
2. git diff -m --no-index is blocked by global flags (EC 73) [F-1 variant]
3. git log -p -m .env is blocked by secret path check (EC 76) [F-1 Concrete Bypass B]
4. git commit -m "msg" -- vendor/src/config.py with target ["src/config.py"] is blocked (EC 79) [S-1]
5. git commit -m "msg" vendor/src/config.py with target ["src/config.py"] is blocked (EC 79) [S-1]
6. git commit -m "msg" --pathspec-from-file=/tmp/paths is blocked (EC 74) [S-1]
7. is_path_in_targets fails closed on empty or None allowed_targets (EC 79) [S-2]
8. is_path_in_targets resolves targets against repo root when CWD is in a subdirectory (EC 79 / EC 0) [S-3]
9. git commit --allow-empty -m "msg" is allowed (EC 0) [Cosmetic-1]
10. git commit -m "-c legitimate message" is allowed (EC 0) [Cosmetic verification]
11. git commit -c core.pager=cat -m "msg" is blocked (EC 73) [Flag safety verification]
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
        "--session", "audit_round13"
    ]
    if targets is not None:
        args.extend(["--targets", ",".join(targets)])
    return subprocess.run(args, cwd=cwd, capture_output=True, text=True)

def test_round13_scenarios():
    print("=== Running Audit Round 13 Scenarios ===\n")

    # 1. git diff -m --output=<path> (F-1 Concrete Bypass A verification)
    # 1A: Target is a control artifact -> EC 80 (Tampering with control path)
    res_ctrl = run_dispatch(f'git diff -m --output="{T3_BIN}/t3_dispatch.py"')
    print("Scenario 1A (git diff -m --output=<control_binary>):")
    print(f"  Returncode: {res_ctrl.returncode}")
    print(f"  Stderr: {res_ctrl.stderr.strip()}")
    assert res_ctrl.returncode == 80, f"Expected 80, got {res_ctrl.returncode}"

    # 1B: Target is regular file -> EC 73 (Prohibited Git redirection / destructive flag)
    res_dest = run_dispatch('git diff -m --output=/tmp/diff.txt')
    print("Scenario 1B (git diff -m --output=/tmp/diff.txt):")
    print(f"  Returncode: {res_dest.returncode}")
    print(f"  Stderr: {res_dest.stderr.strip()}")
    assert res_dest.returncode == 73, f"Expected 73, got {res_dest.returncode}"

    # 2. git diff -m --no-index (F-1 variant verification)
    res = run_dispatch('git diff -m --no-index /etc/hosts /tmp/hosts')
    print("\nScenario 2 (git diff -m --no-index):")
    print(f"  Returncode: {res.returncode}")
    print(f"  Stderr: {res.stderr.strip()}")
    assert res.returncode == 73, f"Expected 73, got {res.returncode}"

    # 3. git log -p -m .env (F-1 Concrete Bypass B verification)
    res = run_dispatch('git log -p -m .env')
    print("\nScenario 3 (git log -p -m .env):")
    print(f"  Returncode: {res.returncode}")
    print(f"  Stderr: {res.stderr.strip()}")
    assert res.returncode == 76, f"Expected 76, got {res.returncode}"
    assert "Secret path access prohibited" in res.stderr

    # 4. git commit -m "msg" -- vendor/src/config.py with target ["src/config.py"] (S-1 verification)
    res = run_dispatch('git commit -m "msg" -- vendor/src/config.py', targets=["src/config.py"])
    print("\nScenario 4 (git commit -m 'msg' -- vendor/src/config.py):")
    print(f"  Returncode: {res.returncode}")
    print(f"  Stderr: {res.stderr.strip()}")
    assert res.returncode == 79, f"Expected 79, got {res.returncode}"
    assert "outside manifest target scope" in res.stderr

    # 5. git commit -m "msg" vendor/src/config.py with target ["src/config.py"] (S-1 verification)
    res = run_dispatch('git commit -m "msg" vendor/src/config.py', targets=["src/config.py"])
    print("\nScenario 5 (git commit -m 'msg' vendor/src/config.py):")
    print(f"  Returncode: {res.returncode}")
    print(f"  Stderr: {res.stderr.strip()}")
    assert res.returncode == 79, f"Expected 79, got {res.returncode}"
    assert "outside manifest target scope" in res.stderr

    # 6. git commit -m "msg" --pathspec-from-file=/tmp/paths (S-1 verification)
    res = run_dispatch('git commit -m "msg" --pathspec-from-file=/tmp/paths', targets=["src/config.py"])
    print("\nScenario 6 (git commit -m 'msg' --pathspec-from-file=/tmp/paths):")
    print(f"  Returncode: {res.returncode}")
    print(f"  Stderr: {res.stderr.strip()}")
    assert res.returncode == 74, f"Expected 74, got {res.returncode}"

    # 7. Fail-closed on empty or None allowed_targets (S-2 verification)
    with tempfile.TemporaryDirectory() as td:
        subprocess.run(["git", "init"], cwd=td, capture_output=True)
        (Path(td) / "safe.txt").write_text("content\n")
        # Direct call with no targets passed
        res = run_dispatch("git add safe.txt", cwd=td, targets=None)
        print("\nScenario 7A (git add safe.txt with targets=None):")
        print(f"  Returncode: {res.returncode}")
        print(f"  Stderr: {res.stderr.strip()}")
        assert res.returncode == 79, f"Expected 79, got {res.returncode}"

        # Direct file tool call with no targets passed
        res_file = subprocess.run([
            sys.executable, str(DISPATCH),
            "--tool", "edit_file",
            "--payload", str(Path(td) / "safe.txt"),
            "--session", "audit_round13"
        ], capture_output=True, text=True)
        print("Scenario 7B (edit_file safe.txt with targets=None):")
        print(f"  Returncode: {res_file.returncode}")
        print(f"  Stderr: {res_file.stderr.strip()}")
        assert res_file.returncode == 79, f"Expected 79, got {res_file.returncode}"

    # 8. Subdirectory CWD resolution against repo root (S-3 verification)
    with tempfile.TemporaryDirectory() as td:
        subprocess.run(["git", "init"], cwd=td, capture_output=True)
        repo_root = Path(td)
        (repo_root / "src").mkdir(parents=True, exist_ok=True)
        (repo_root / "src/config.py").write_text("# root config\n")
        vendor_dir = repo_root / "vendor"
        vendor_dir.mkdir(parents=True, exist_ok=True)
        (vendor_dir / "src").mkdir(parents=True, exist_ok=True)
        (vendor_dir / "src/config.py").write_text("# vendor config\n")

        # Staging relative to CWD in vendor (wrong target)
        res_wrong = run_dispatch("git add src/config.py", cwd=str(vendor_dir), targets=["src/config.py"])
        print("\nScenario 8A (git add from vendor/ of vendor/src/config.py):")
        print(f"  Returncode: {res_wrong.returncode}")
        print(f"  Stderr: {res_wrong.stderr.strip()}")
        assert res_wrong.returncode == 79, f"Expected 79, got {res_wrong.returncode}"

        # Staging pointing to repo root target from vendor/
        res_right = run_dispatch("git add ../src/config.py", cwd=str(vendor_dir), targets=["src/config.py"])
        print("Scenario 8B (git add from vendor/ of ../src/config.py):")
        print(f"  Returncode: {res_right.returncode}")
        assert res_right.returncode == 0, f"Expected 0, got {res_right.returncode}. Stderr: {res_right.stderr}"
        print("  Staging ../src/config.py matched repo-root target (EC 0).")

    # 9. git commit --allow-empty -m "msg" (Cosmetic-1 fix verification)
    res = run_dispatch('git commit --allow-empty -m "legitimate empty commit"')
    print("\nScenario 9 (git commit --allow-empty -m 'msg'):")
    print(f"  Returncode: {res.returncode}")
    assert res.returncode == 0, f"Expected 0, got {res.returncode}. Stderr: {res.stderr}"
    print("  Commit with --allow-empty allowed (EC 0).")

    # 10. git commit -m "-c legitimate message" (Cosmetic verification)
    res = run_dispatch('git commit -m "-c legitimate commit message"')
    print("\nScenario 10 (git commit -m '-c legitimate commit message'):")
    print(f"  Returncode: {res.returncode}")
    assert res.returncode == 0, f"Expected 0, got {res.returncode}. Stderr: {res.stderr}"
    print("  Commit with '-c ...' message allowed (EC 0).")

    # 11. git commit -c core.pager=cat -m "msg" (Ensuring -c flag is still blocked)
    res = run_dispatch('git commit -c core.pager=cat -m "msg"')
    print("\nScenario 11 (git commit -c core.pager=cat -m 'msg'):")
    print(f"  Returncode: {res.returncode}")
    print(f"  Stderr: {res.stderr.strip()}")
    assert res.returncode == 73, f"Expected 73, got {res.returncode}"

    print("\nALL ROUND 13 SCENARIOS PASSED PERFECTLY (100%).\n")

if __name__ == "__main__":
    test_round13_scenarios()
