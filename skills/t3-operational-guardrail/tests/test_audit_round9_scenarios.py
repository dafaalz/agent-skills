#!/usr/bin/env python3
"""
Test Suite: Audit Round 9 Scenarios (Closing F-1, F-2, F-3, S-1, S-2, S-4, S-5, S-7)
Verifies:
1. INI-format [filter "evil"] in .git/config is blocked (EC 73)
2. INI-format [diff "evil"] in .git/config is blocked (EC 73)
3. INI-format [include] path = ... in .git/config is blocked (EC 73)
4. Subdirectory .gitattributes (src/.gitattributes) with filter= is blocked (EC 73)
5. Blanket & interactive git add flags (-u, -p, -i) are blocked (EC 74)
6. Worktree .git pointer file inheriting [filter "evil"] is blocked (EC 73)
7. Edit_file on ~/.gitconfig is blocked as control path (EC 80)
8. Fail-closed hygiene check on unreadable .git/config (EC 73)
"""
import subprocess
import sys
import os
import shutil
import tempfile
from pathlib import Path

T3_BIN = Path.home() / "Library/Application Support/t3/bin"
DISPATCH = T3_BIN / "t3_dispatch.py"

def run_dispatch(cmd_str: str, cwd: str, targets: str = ""):
    args = [
        sys.executable, str(DISPATCH),
        "--tool", "run_command",
        "--payload", cmd_str,
        "--targets", targets,
        "--session", "audit_round9"
    ]
    return subprocess.run(args, cwd=cwd, capture_output=True, text=True)

def test_round9_scenarios():
    print("=== Running Audit Round 9 Attack Scenarios ===\n")

    # 1. INI-format [filter "evil"] in .git/config
    with tempfile.TemporaryDirectory() as td:
        subprocess.run(["git", "init"], cwd=td, capture_output=True)
        cfg = Path(td) / ".git/config"
        with open(cfg, "a") as f:
            f.write('\n[filter "evil"]\n\tclean = /tmp/evil\n')
        res = run_dispatch("git add safe.txt", cwd=td)
        print(f"Scenario 1 (INI [filter \"evil\"] in .git/config):")
        print(f"  Returncode: {res.returncode}")
        print(f"  Stderr: {res.stderr.strip()}")
        assert res.returncode == 73, f"Expected 73, got {res.returncode}"
        assert "[filter \"evil\"]" in res.stderr

    # 2. INI-format [diff "evil"] in .git/config
    with tempfile.TemporaryDirectory() as td:
        subprocess.run(["git", "init"], cwd=td, capture_output=True)
        cfg = Path(td) / ".git/config"
        with open(cfg, "a") as f:
            f.write('\n[diff "evil"]\n\tcommand = /tmp/evil\n')
        res = run_dispatch("git diff", cwd=td)
        print(f"\nScenario 2 (INI [diff \"evil\"] in .git/config):")
        print(f"  Returncode: {res.returncode}")
        print(f"  Stderr: {res.stderr.strip()}")
        assert res.returncode == 73, f"Expected 73, got {res.returncode}"
        assert "[diff \"evil\"]" in res.stderr

    # 3. INI-format [include] path = ... in .git/config
    with tempfile.TemporaryDirectory() as td:
        subprocess.run(["git", "init"], cwd=td, capture_output=True)
        cfg = Path(td) / ".git/config"
        with open(cfg, "a") as f:
            f.write('\n[include]\n\tpath = /tmp/evil.inc\n')
        res = run_dispatch("git status", cwd=td)
        print(f"\nScenario 3 (INI [include] in .git/config):")
        print(f"  Returncode: {res.returncode}")
        print(f"  Stderr: {res.stderr.strip()}")
        assert res.returncode == 73, f"Expected 73, got {res.returncode}"
        assert "[include]" in res.stderr

    # 4. Subdirectory .gitattributes (src/.gitattributes)
    with tempfile.TemporaryDirectory() as td:
        subprocess.run(["git", "init"], cwd=td, capture_output=True)
        src_dir = Path(td) / "src"
        src_dir.mkdir()
        sub_attr = src_dir / ".gitattributes"
        sub_attr.write_text("*.py filter=evil\n")
        res = run_dispatch("git add src/foo.py", cwd=td)
        print(f"\nScenario 4 (Subdirectory src/.gitattributes):")
        print(f"  Returncode: {res.returncode}")
        print(f"  Stderr: {res.stderr.strip()}")
        assert res.returncode == 73, f"Expected 73, got {res.returncode}"
        assert "filter=" in res.stderr

    # 5. git add -u, -p, -i bypass attempts
    print("\nScenario 5 (git add -u / -p / -i bypass attempts):")
    for flg in ["-u", "-p", "-i", "--update", "--patch", "--interactive"]:
        res = run_dispatch(f"git add {flg}", cwd=os.getcwd())
        assert res.returncode == 74, f"Expected 74 for git add {flg}, got {res.returncode}"
        print(f"  git add {flg} -> Exited 74 (Denied as expected)")

    # 6. Worktree .git pointer file inheriting [filter "evil"]
    with tempfile.TemporaryDirectory() as td:
        main_repo = Path(td) / "main"
        main_repo.mkdir()
        subprocess.run(["git", "init"], cwd=str(main_repo), capture_output=True)
        cfg = main_repo / ".git/config"
        with open(cfg, "a") as f:
            f.write('\n[filter "evil"]\n\tclean = /tmp/evil\n')
        
        # Setup simulated worktree with .git pointer file
        wt_dir = Path(td) / "wt"
        wt_dir.mkdir()
        git_ptr = wt_dir / ".git"
        git_ptr.write_text(f"gitdir: {main_repo / '.git/worktrees/wt'}\n")
        (main_repo / ".git/worktrees/wt").mkdir(parents=True)
        (main_repo / ".git/worktrees/wt/commondir").write_text("../..\n")

        res = run_dispatch("git status", cwd=str(wt_dir))
        print(f"\nScenario 6 (Worktree .git pointer inheriting [filter \"evil\"]):")
        print(f"  Returncode: {res.returncode}")
        print(f"  Stderr: {res.stderr.strip()}")
        assert res.returncode == 73, f"Expected 73, got {res.returncode}"

    # 7. Edit_file on ~/.gitconfig
    print(f"\nScenario 7 (Edit_file on ~/.gitconfig):")
    user_gitconfig = Path.home() / ".gitconfig"
    res = subprocess.run([
        sys.executable, str(DISPATCH),
        "--tool", "edit_file",
        "--payload", str(user_gitconfig),
        "--session", "audit_round9"
    ], capture_output=True, text=True)
    print(f"  Returncode: {res.returncode}")
    print(f"  Stderr: {res.stderr.strip()}")
    assert res.returncode == 80, f"Expected 80, got {res.returncode}"

    # 8. Fail-closed hygiene on unreadable .git/config
    with tempfile.TemporaryDirectory() as td:
        subprocess.run(["git", "init"], cwd=td, capture_output=True)
        cfg = Path(td) / ".git/config"
        cfg.chmod(0o000)
        res = run_dispatch("git status", cwd=td)
        cfg.chmod(0o644)  # restore for cleanup
        print(f"\nScenario 8 (Fail-closed on unreadable .git/config chmod 000):")
        print(f"  Returncode: {res.returncode}")
        print(f"  Stderr: {res.stderr.strip()}")
        assert res.returncode == 73, f"Expected 73, got {res.returncode}"
        assert "Failed reading git config" in res.stderr

    print("\nALL SCENARIOS PASSED PERFECTLY (100%).\n")

if __name__ == "__main__":
    test_round9_scenarios()
