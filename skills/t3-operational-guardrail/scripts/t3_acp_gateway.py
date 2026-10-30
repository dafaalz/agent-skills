#!/usr/bin/env python3
"""
T3 ACP Call Path Gateway (Fail-Closed, Out-of-Tree)
Location: ~/Library/Application Support/t3/bin/t3_acp_gateway.py
Handles:
- MCP tools/call
- ACP fs/read_text_file and fs/write_text_file
- ACP terminal/create
- Native tool/execute
Tracks hash-chained ledgers with out-of-band pinned_last_hash.
Verifies runtime attestation of control binaries against trusted root.
"""
import sys
import os
import json
import time
import hashlib
import subprocess
from pathlib import Path

T3_ROOT = Path.home() / "Library/Application Support/t3"
DISPATCH_BIN = T3_ROOT / "bin/t3_dispatch.py"
LEDGER_DIR = T3_ROOT / "ledgers"
LEDGER_DIR.mkdir(parents=True, exist_ok=True)
PINNED_HASH_FILE = LEDGER_DIR / ".pinned_last_hash"

FALLBACK_TURN_CAP = 8

def verify_runtime_attestation():
    trusted_file = LEDGER_DIR / "trusted_root_hashes.json"
    if not trusted_file.exists():
        sys.stderr.write("[GATEWAY DENIED 80] Missing trusted root attestation ledger: FAIL-CLOSED.\n")
        return False
    try:
        with open(trusted_file, "r") as f:
            trusted_data = json.load(f)
        hashes = trusted_data.get("bin_hashes", {})
        if not hashes:
            sys.stderr.write("[GATEWAY DENIED 80] Empty trusted root attestation ledger: FAIL-CLOSED.\n")
            return False
        for fname, exp_hash in hashes.items():
            fpath = T3_ROOT / "bin" / fname
            if not fpath.exists():
                sys.stderr.write(f"[GATEWAY DENIED 80] Control binary missing: {fname}\n")
                return False
            cur_hash = hashlib.sha256(fpath.read_bytes()).hexdigest()
            if cur_hash != exp_hash:
                sys.stderr.write(f"[GATEWAY DENIED 80] Control binary runtime integrity violation: {fname}\n")
                return False
    except Exception as e:
        sys.stderr.write(f"[GATEWAY DENIED 80] Attestation check failure: {e}\n")
        return False
    return True

def get_last_line_hash(ledger_file: Path) -> str:
    if PINNED_HASH_FILE.exists():
        try:
            return PINNED_HASH_FILE.read_text().strip()
        except Exception:
            pass
    if not ledger_file.exists() or ledger_file.stat().st_size == 0:
        return "0" * 64
    try:
        with open(ledger_file, "r", encoding="utf-8") as f:
            lines = [l.strip() for l in f if l.strip()]
            if not lines:
                return "0" * 64
            last_line = lines[-1]
            return hashlib.sha256(last_line.encode("utf-8")).hexdigest()
    except Exception:
        return "0" * 64

def append_ledger(session_id: str, entry: dict):
    ledger_file = LEDGER_DIR / f"enforcement-{session_id}.jsonl"
    entry["ts"] = time.time()
    prev = get_last_line_hash(ledger_file)
    entry["prev_hash"] = prev
    line = json.dumps(entry, sort_keys=True)
    curr_hash = hashlib.sha256(line.encode("utf-8")).hexdigest()
    with open(ledger_file, "a", encoding="utf-8") as f:
        f.write(line + "\n")
    # Pin last hash out-of-band
    PINNED_HASH_FILE.write_text(curr_hash)

def inject_pinned(manifest_path: Path, ctx: list) -> str:
    if not manifest_path.exists():
        raise FileNotFoundError(f"Manifest missing: {manifest_path}")
    data = manifest_path.read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    pinned_block = f"[PINNED sha256={digest}]\n{data.decode('utf-8')}\n[/PINNED]"
    ctx.insert(0, pinned_block)
    return digest

def handle_tool_call(session_id: str, tool_name: str, args: dict, manifest_path: Path = None, expected_hash: str = None, turn_count: int = 1, is_fallback: bool = False) -> dict:
    if not verify_runtime_attestation():
        return {"status": "denied", "exit_code": 80, "error": "Control binary runtime attestation mismatch"}

    if is_fallback and turn_count > FALLBACK_TURN_CAP:
        sys.stderr.write(f"[GATEWAY DENIED 78] Fallback mode turn cap exceeded ({turn_count} > {FALLBACK_TURN_CAP}).\n")
        return {"status": "denied", "exit_code": 78, "error": "Fallback turn cap exceeded"}

    # Extract payload based on tool or ACP wire method
    if tool_name in {"run_command", "terminal/create"}:
        cmd = args.get("command", "")
        extra_args = args.get("args", [])
        if extra_args:
            payload = f"{cmd} {' '.join(extra_args)}"
        else:
            payload = cmd
    elif tool_name in {"edit_file", "create_file", "view_file", "fs/read_text_file", "fs/write_text_file"}:
        payload = args.get("path", "")
    elif tool_name in {"read_url_content", "search_web"}:
        payload = args.get("url", "") or args.get("query", "")
    else:
        payload = ""

    targets_str = ""
    if manifest_path and manifest_path.exists():
        try:
            with open(manifest_path, "r") as mf:
                mdata = json.load(mf)
                targets_str = ",".join(mdata.get("targets", []))
        except Exception:
            pass

    cmd = [
        sys.executable, str(DISPATCH_BIN),
        "--tool", tool_name,
        "--payload", payload,
        "--targets", targets_str,
        "--session", session_id
    ]
    if expected_hash:
        cmd.extend(["--hash", expected_hash])

    # Enforce scrubbed environment without external GIT config injection
    sub_env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    sub_env["GIT_CONFIG_NOSYSTEM"] = "1"
    sub_env["GIT_CONFIG_GLOBAL"] = "/dev/null"
    sub_env["GIT_ATTR_NOSYSTEM"] = "1"
    sub_env["GIT_EDITOR"] = "true"
    sub_env["GIT_PAGER"] = "cat"

    res = subprocess.run(cmd, capture_output=True, text=True, env=sub_env)

    log_entry = {
        "session_id": session_id,
        "tool": tool_name,
        "payload": payload,
        "returncode": res.returncode,
        "stdout": res.stdout.strip(),
        "stderr": res.stderr.strip()
    }
    append_ledger(session_id, log_entry)

    if res.returncode != 0:
        return {
            "status": "denied",
            "exit_code": res.returncode,
            "error": res.stderr.strip()
        }

    return {
        "status": "allowed",
        "exit_code": 0,
        "stdout": res.stdout.strip()
    }

def run_jsonrpc_loop():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
        except Exception:
            continue

        req_id = req.get("id")
        method = req.get("method")
        params = req.get("params", {})

        # Handle MCP tools/call
        if method == "tools/call":
            tool_name = params.get("name")
            tool_args = params.get("arguments", {})
            session_id = params.get("session_id", "default")
            manifest_p = T3_ROOT / f"sessions/{session_id}/task-manifest.json"
            res = handle_tool_call(session_id, tool_name, tool_args, manifest_path=manifest_p)

        # Handle ACP fs/write_text_file
        elif method == "fs/write_text_file":
            session_id = params.get("sessionId", "default")
            manifest_p = T3_ROOT / f"sessions/{session_id}/task-manifest.json"
            res = handle_tool_call(session_id, "fs/write_text_file", params, manifest_path=manifest_p)

        # Handle ACP fs/read_text_file
        elif method == "fs/read_text_file":
            session_id = params.get("sessionId", "default")
            manifest_p = T3_ROOT / f"sessions/{session_id}/task-manifest.json"
            res = handle_tool_call(session_id, "fs/read_text_file", params, manifest_path=manifest_p)

        # Handle ACP terminal/create
        elif method == "terminal/create":
            session_id = params.get("sessionId", "default")
            manifest_p = T3_ROOT / f"sessions/{session_id}/task-manifest.json"
            res = handle_tool_call(session_id, "terminal/create", params, manifest_path=manifest_p)

        # Handle native tool/execute
        elif method == "tool/execute":
            tool_name = params.get("name")
            tool_args = params.get("arguments", {})
            session_id = params.get("session_id", "default")
            manifest_p = T3_ROOT / f"sessions/{session_id}/task-manifest.json"
            res = handle_tool_call(session_id, tool_name, tool_args, manifest_path=manifest_p)

        else:
            continue

        if res["status"] == "denied":
            resp = {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {
                    "code": res["exit_code"],
                    "message": res["error"]
                }
            }
        else:
            resp = {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "content": res["stdout"]
                }
            }
        sys.stdout.write(json.dumps(resp) + "\n")
        sys.stdout.flush()

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--jsonrpc":
        run_jsonrpc_loop()
    elif len(sys.argv) >= 4:
        sess = sys.argv[1]
        tname = sys.argv[2]
        targs = json.loads(sys.argv[3])
        mpath = Path(sys.argv[4]) if len(sys.argv) > 4 else None
        ehash = sys.argv[5] if len(sys.argv) > 5 else None
        out = handle_tool_call(sess, tname, targs, mpath, ehash)
        print(json.dumps(out, indent=2))
        sys.exit(out["exit_code"])
    else:
        sys.exit(1)
