#!/usr/bin/env python3
import subprocess
import sys
from pathlib import Path

T3_BIN = Path.home() / "Library/Application Support/t3/bin"
ROUTER = T3_BIN / "t3_router.py"
WORKTREE = T3_BIN / "t3_worktree_queue.py"

def test_router():
    print("Testing t3_router.py circuit breaker...")
    # 1. Reset state
    subprocess.run([sys.executable, str(ROUTER), "success"], check=True)
    
    # 2. Query normal routing
    res = subprocess.run([sys.executable, str(ROUTER), "mutation"], capture_output=True, text=True, check=True)
    assert "gemini-3.8-flash-high" in res.stdout, "Default route must be primary"

    # 3. Simulate 3 consecutive 503 errors to trip circuit
    for _ in range(3):
        subprocess.run([sys.executable, str(ROUTER), "error", "gemini-3.8-flash-high", "503"], check=True)

    # 4. Check fallback for read-only
    res = subprocess.run([sys.executable, str(ROUTER), "read_only"], capture_output=True, text=True, check=True)
    assert "deepseek-v4.1-flash-free" in res.stdout, "Read-only must fallback to deepseek when circuit open"

    # 5. Check fail-closed for mutation when primary open
    res = subprocess.run([sys.executable, str(ROUTER), "mutation"], capture_output=True, text=True)
    assert res.returncode == 78, f"Expected 78 fail-closed on mutation during open circuit, got {res.returncode}"
    print("  [PASS] Router Circuit Breaker tripped and failed closed as expected.")

def test_worktree_queue():
    print("Testing t3_worktree_queue.py lock and conflict policy...")
    # 1. Register session A with path X
    subprocess.run([sys.executable, str(WORKTREE), "register", "session_A", "user_model", "app/Models/User.php"], check=True)

    # 2. Session B attempts to lock overlapping path X -> Must exit 81 (Semantic-unit Conflict)
    res = subprocess.run([sys.executable, str(WORKTREE), "register", "session_B", "user_auth", "app/Models/User.php"], capture_output=True, text=True)
    assert res.returncode == 81, f"Expected 81 queue conflict on overlapping targets, got {res.returncode}"

    # 3. Release session A
    subprocess.run([sys.executable, str(WORKTREE), "release", "session_A"], check=True)
    print("  [PASS] Worktree Queue locks and collision prevention verified.")

if __name__ == "__main__":
    test_router()
    test_worktree_queue()
    print("ALL ROUTER & WORKTREE TESTS PASSED.")
