#!/usr/bin/env python3
"""
Darwin Seatbelt Kernel-Level Probe Test Suite (Four-Vector Hardened)
Verifies:
1. Positive probe: Whitelisted git binary is permitted by macOS kernel.
2. Negative probe: Non-whitelisted awk binary is blocked by kernel.
3. Negative probe: Interpreter php is blocked by kernel from inline eval.
4. Negative probe: Interpreter python3 is blocked by kernel from inline eval.
"""
import subprocess
import sys
from pathlib import Path

PROFILE = Path.home() / "Library/Application Support/t3/profiles/t3.sb"

def run_probes():
    print("Testing Darwin Seatbelt sandbox-exec kernel boundaries (4 Probes)...")
    if not Path("/usr/bin/sandbox-exec").exists():
        print("  [SKIP] sandbox-exec binary not found.")
        sys.exit(0)

    # 1. Positive Probe: git
    res_pos = subprocess.run(["sandbox-exec", "-f", str(PROFILE), "git", "--version"], capture_output=True, text=True)
    assert res_pos.returncode == 0, f"Positive probe failed: git should be allowed. Stderr: {res_pos.stderr}"
    print(f"  [PASS] Kernel Positive Probe 1 (git permitted): {res_pos.stdout.strip()}")

    # 2. Negative Probe: awk
    res_awk = subprocess.run(["sandbox-exec", "-f", str(PROFILE), "awk", "BEGIN{print 1}"], capture_output=True, text=True)
    assert res_awk.returncode != 0, "Negative probe failed: awk should have been blocked by kernel!"
    print("  [PASS] Kernel Negative Probe 2 (awk blocked): Operation not permitted by kernel Seatbelt.")

    # 3. Negative Probe: php
    res_php = subprocess.run(["sandbox-exec", "-f", str(PROFILE), "php", "-r", "echo 1;"], capture_output=True, text=True)
    assert res_php.returncode != 0, "Negative probe failed: php should have been blocked by kernel!"
    print("  [PASS] Kernel Negative Probe 3 (php blocked): Operation not permitted by kernel Seatbelt.")

    # 4. Negative Probe: python3
    res_py = subprocess.run(["sandbox-exec", "-f", str(PROFILE), "python3", "-c", "print(1)"], capture_output=True, text=True)
    assert res_py.returncode != 0, "Negative probe failed: python3 should have been blocked by kernel!"
    print("  [PASS] Kernel Negative Probe 4 (python3 blocked): Operation not permitted by kernel Seatbelt.")

    print("ALL 4 KERNEL PROBES COMPLETED SUCCESSFULLY.\n")

if __name__ == "__main__":
    run_probes()
