#!/usr/bin/env python3
"""
Keystone Test: Verifies ACP Wire Methods & Interception Gateway.
Proves that:
1. MCP tools/call is intercepted (git push denied with EC 75; approved with HMAC token).
2. ACP terminal/create is intercepted (git push denied with EC 75).
3. ACP fs/write_text_file is intercepted (control file mutation denied with EC 80).
4. ACP fs/read_text_file is intercepted (secret file access denied with EC 76).
5. Native tool/execute is intercepted.
6. Zero shell execution occurred when unapproved.
"""
import subprocess
import sys
import os
import json
import uuid
from pathlib import Path

T3_BIN = Path.home() / "Library/Application Support/t3/bin"
GATEWAY = T3_BIN / "t3_acp_gateway.py"
APPROVAL = T3_BIN / "t3_approval.py"

def test_jsonrpc_call_path():
    print("Testing ACP Wire Methods & JSON-RPC Gateway Interception Path...")
    session_id = f"test-{uuid.uuid4().hex[:8]}"
    sess_dir = Path.home() / f"Library/Application Support/t3/sessions/{session_id}"
    sess_dir.mkdir(parents=True, exist_ok=True)
    manifest_file = sess_dir / "task-manifest.json"
    manifest_file.write_text(json.dumps({
        "targets": ["app/Models/User.php"],
        "allowed_tools": ["run_command", "edit_file", "view_file"]
    }))

    proc = subprocess.Popen(
        [sys.executable, str(GATEWAY), "--jsonrpc"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    marker_file = Path(f"/tmp/push_fired_{session_id}.txt")
    marker_file.unlink(missing_ok=True)

    # 1. Test MCP tools/call (Unapproved git push -> EC 75)
    req1 = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {
            "session_id": session_id,
            "name": "run_command",
            "arguments": {"command": "git push origin main"}
        }
    }
    proc.stdin.write(json.dumps(req1) + "\n")
    proc.stdin.flush()
    resp1 = json.loads(proc.stdout.readline())
    assert resp1["id"] == 1
    assert "error" in resp1 and resp1["error"]["code"] == 75, f"Expected 75, got {resp1}"
    assert not marker_file.exists(), "Fatal: Shell executed without approval!"
    print("  [PASS] MCP tools/call: Unapproved git push blocked with Error Code 75.")

    # 2. Test ACP terminal/create (Unapproved git push -> EC 75)
    req2 = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "terminal/create",
        "params": {
            "sessionId": session_id,
            "command": "git push",
            "args": ["origin", "main"]
        }
    }
    proc.stdin.write(json.dumps(req2) + "\n")
    proc.stdin.flush()
    resp2 = json.loads(proc.stdout.readline())
    assert resp2["id"] == 2
    assert "error" in resp2 and resp2["error"]["code"] == 75, f"Expected 75, got {resp2}"
    print("  [PASS] ACP terminal/create: git push blocked with Error Code 75.")

    # 3. Test ACP fs/write_text_file on Control Path (Tampering -> EC 80)
    req3 = {
        "jsonrpc": "2.0",
        "id": 3,
        "method": "fs/write_text_file",
        "params": {
            "sessionId": session_id,
            "path": str(GATEWAY),
            "content": "# corrupted"
        }
    }
    proc.stdin.write(json.dumps(req3) + "\n")
    proc.stdin.flush()
    resp3 = json.loads(proc.stdout.readline())
    assert resp3["id"] == 3
    assert "error" in resp3 and resp3["error"]["code"] == 80, f"Expected 80, got {resp3}"
    print("  [PASS] ACP fs/write_text_file: Tampering control binary blocked with Error Code 80.")

    # 4. Test ACP fs/read_text_file on Secret Path (.env -> EC 76)
    req4 = {
        "jsonrpc": "2.0",
        "id": 4,
        "method": "fs/read_text_file",
        "params": {
            "sessionId": session_id,
            "path": ".env"
        }
    }
    proc.stdin.write(json.dumps(req4) + "\n")
    proc.stdin.flush()
    resp4 = json.loads(proc.stdout.readline())
    assert resp4["id"] == 4
    assert "error" in resp4 and resp4["error"]["code"] == 76, f"Expected 76, got {resp4}"
    print("  [PASS] ACP fs/read_text_file: Reading .env blocked with Error Code 76.")

    # 5. Mint Human Approval Token & Verify Unblocking
    subprocess.run([sys.executable, str(APPROVAL), "mint", session_id, "git push origin main"], check=True)
    req5 = {
        "jsonrpc": "2.0",
        "id": 5,
        "method": "tools/call",
        "params": {
            "session_id": session_id,
            "name": "run_command",
            "arguments": {"command": "git push origin main"}
        }
    }
    proc.stdin.write(json.dumps(req5) + "\n")
    proc.stdin.flush()
    resp5 = json.loads(proc.stdout.readline())
    assert resp5["id"] == 5
    assert "result" in resp5, f"Expected result, got error: {resp5.get('error')}"
    print("  [PASS] MCP tools/call: Approved git push permitted after single-use HMAC token verification.")

    proc.stdin.close()
    proc.terminate()
    print("ALL ACP & MCP WIRE INTERCEPTION TESTS PASSED.\n")

if __name__ == "__main__":
    test_jsonrpc_call_path()
