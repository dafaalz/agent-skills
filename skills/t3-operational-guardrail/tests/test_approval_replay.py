#!/usr/bin/env python3
"""
Test atomic Compare-and-Swap (CAS) replay protection and nonce isolation for t3_approval.py.
"""
import subprocess
import sys
import concurrent.futures
from pathlib import Path

APPROVAL_BIN = Path.home() / "Library/Application Support/t3/bin/t3_approval.py"

def test_approval_cas_replay():
    print("Testing HMAC Token Atomic CAS Replay Protection...")
    session_id = "replay_test_sess"
    action = "git push"

    # Mint token
    mint_res = subprocess.run([sys.executable, str(APPROVAL_BIN), "mint", session_id, action], capture_output=True, text=True)
    assert mint_res.returncode == 0, f"Minting failed: {mint_res.stderr}"
    print("  [PASS] Single-use HMAC token minted successfully.")

    # Concurrently try to verify and consume the token 10 times
    def attempt_verify(worker_id):
        res = subprocess.run([sys.executable, str(APPROVAL_BIN), "verify", session_id, action], capture_output=True, text=True)
        return worker_id, res.returncode

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(attempt_verify, range(10)))

    successes = [r for r in results if r[1] == 0]
    denials = [r for r in results if r[1] == 75]

    print(f"  [RESULT] Concurrent verify results: {len(successes)} succeeded, {len(denials)} denied (EC 75).")
    assert len(successes) == 1, f"Expected exactly 1 CAS success, got {len(successes)}"
    assert len(denials) == 9, f"Expected 9 replay denials, got {len(denials)}"
    print("  [PASS] Atomic CAS verified: Exactly 1 consumer succeeded, all concurrent replays rejected.")

if __name__ == "__main__":
    test_approval_cas_replay()
