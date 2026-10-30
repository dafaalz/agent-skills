#!/usr/bin/env python3
"""
Integration Test Suite for:
1. Manifest hash mismatch abort (EC 82)
2. Compaction pinning wrapper injection (inject_pinned)
3. Semantic-unit worktree collision (EC 81)
4. Router circuit open fail-closed on mutation (EC 78)
"""
import subprocess
import sys
import os
import json
import hashlib
from pathlib import Path

T3_BIN = Path.home() / "Library/Application Support/t3/bin"
GATEWAY = T3_BIN / "t3_acp_gateway.py"
DISPATCH = T3_BIN / "t3_dispatch.py"
QUEUE = T3_BIN / "t3_worktree_queue.py"
ROUTER = T3_BIN / "t3_router.py"
MANIFEST = Path.home() / "Library/Application Support/t3/sessions/default/task-manifest.json"

def test_manifest_hash_check():
    print("Testing manifest hash-pinning check (EC 82)...")
    correct_hash = hashlib.sha256(MANIFEST.read_bytes()).hexdigest()
    tampered_hash = "0000000000000000000000000000000000000000000000000000000000000000"

    # Call gateway with tampered expected hash
    cmd = [
        sys.executable, str(GATEWAY),
        "test_session", "run_command", json.dumps({"command": "git status"}),
        str(MANIFEST), tampered_hash
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    assert res.returncode == 82, f"Expected EC 82 on manifest mismatch, got {res.returncode}"
    print("  [PASS] Tampered manifest hash aborted session with EC 82 as expected.")

def test_compaction_pinning():
    print("Testing wrapper compaction pinning injection...")
    sys.path.insert(0, str(T3_BIN))
    from t3_acp_gateway import inject_pinned

    ctx = ["assistant: Previous turn summary", "user: Proceed with task"]
    digest = inject_pinned(MANIFEST, ctx)
    assert ctx[0].startswith(f"[PINNED sha256={digest}]"), "Pinned manifest must be injected at index 0"
    assert "allowed_tools" in ctx[0], "Pinned content must contain manifest data"
    print("  [PASS] Compaction pinning injection validated at index 0.")

def test_semantic_unit_worktree_collision():
    print("Testing semantic-unit worktree queue collision (EC 81)...")
    # Session A registers user-index unit (Controller + Blade pair)
    subprocess.run([
        sys.executable, str(QUEUE), "register", "session_A",
        "user-index", "app/Http/Controllers/UserController.php,resources/views/user/index.blade.php"
    ], check=True)

    # Session B attempts to register a unit touching the same Blade partial -> MUST FAIL with EC 81
    res = subprocess.run([
        sys.executable, str(QUEUE), "register", "session_B",
        "user-edit", "resources/views/user/index.blade.php,resources/views/user/edit.blade.php"
    ], capture_output=True, text=True)
    assert res.returncode == 81, f"Expected EC 81 on semantic-unit collision, got {res.returncode}"

    # Cleanup
    subprocess.run([sys.executable, str(QUEUE), "release", "session_A"], check=True)
    print("  [PASS] Semantic-unit conflict blocked with EC 81 as expected.")

def test_router_mutation_fail_closed():
    print("Testing router mutation fail-closed when circuit is open (EC 78)...")
    # Reset
    subprocess.run([sys.executable, str(ROUTER), "success"], check=True)
    # Trip circuit with 3 failures
    for _ in range(3):
        subprocess.run([sys.executable, str(ROUTER), "error", "gemini-3.8-flash-high", "503"], check=True)

    # Request mutation -> Must fail with 78
    res = subprocess.run([sys.executable, str(ROUTER), "mutation"], capture_output=True, text=True)
    assert res.returncode == 78, f"Expected EC 78 on open circuit mutation, got {res.returncode}"
    print("  [PASS] Router fail-closed on mutation with EC 78 as expected.")

if __name__ == "__main__":
    test_manifest_hash_check()
    test_compaction_pinning()
    test_semantic_unit_worktree_collision()
    test_router_mutation_fail_closed()
    print("\nALL INTEGRATION & RESILIENCE TESTS PASSED.")
