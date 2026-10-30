#!/usr/bin/env python3
"""
Adversarial Negative Suite for t3-brief-lint.py
De-collided Codes:
1. Agent-supplied session_id (EC 84)
2. Symlink target rejection (EC 88)
3. Directory traversal .. (EC 85)
4. Missing design anchor (EC 86)
5. Unauthorized tools (EC 87)
6. Valid task brief minting isolated session manifest (EC 0)
"""
import subprocess
import sys
import os
import json
from pathlib import Path

LINTER = Path.home() / "Library/Application Support/t3/bin/t3-brief-lint.py"

def run_case(brief_data: dict, expected_code: int, desc: str):
    tmp_file = Path(f"/tmp/test_brief_{expected_code}.json")
    tmp_file.write_text(json.dumps(brief_data))
    res = subprocess.run([sys.executable, str(LINTER), str(tmp_file)], capture_output=True, text=True)
    tmp_file.unlink(missing_ok=True)
    assert res.returncode == expected_code, f"[{desc}] Expected code {expected_code}, got {res.returncode}. Stderr: {res.stderr}"
    print(f"  [PASS] {desc} -> Exited {res.returncode} as expected.")

def run_suite():
    print("Running Adversarial Tests against t3-brief-lint.py...")

    # 1. Agent-supplied session ID (EC 84)
    run_case({
        "session_id": "malicious_injected_session",
        "mode": "implement",
        "targets": ["app/Models/User.php"],
        "allowed_tools": ["view_file"]
    }, 84, "Agent-supplied session ID injection")

    # 2. Symlink target (EC 80)
    symlink_path = Path("symlink_target_test.php")
    symlink_path.unlink(missing_ok=True)
    real_target = Path("real_target_test.php")
    real_target.write_text("<?php // real")
    symlink_path.symlink_to(real_target)

    run_case({
        "mode": "implement",
        "targets": ["symlink_target_test.php"],
        "allowed_tools": ["view_file"]
    }, 88, "Symlink target rejection")

    symlink_path.unlink(missing_ok=True)
    real_target.unlink(missing_ok=True)

    # 3. Directory traversal (EC 85)
    run_case({
        "mode": "implement",
        "targets": ["../../etc/passwd"],
        "allowed_tools": ["view_file"]
    }, 85, "Directory traversal path")

    # 4. Missing design anchor (EC 86)
    run_case({
        "mode": "implement",
        "targets": ["app/Models/User.php"],
        "design_anchor": "nonexistent/DESIGN.md",
        "allowed_tools": ["view_file"]
    }, 86, "Missing design anchor")

    # 5. Unauthorized tools (EC 87)
    run_case({
        "mode": "implement",
        "targets": ["app/Models/User.php"],
        "allowed_tools": ["view_file", "malicious_unregistered_tool"]
    }, 87, "Unauthorized tool allowlist request")

    # 6. Valid brief (EC 0)
    run_case({
        "mode": "implement",
        "targets": ["scripts/t3_dispatch.py"],
        "allowed_tools": ["view_file", "edit_file", "run_command"]
    }, 0, "Valid task brief mints manifest")

    print("ALL LINTER ADVERSARIAL TESTS PASSED.\n")

if __name__ == "__main__":
    run_suite()
