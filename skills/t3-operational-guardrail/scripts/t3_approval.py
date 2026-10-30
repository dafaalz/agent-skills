#!/usr/bin/env python3
"""
T3 HMAC Human Approval Token Minter & Verifier (Keychain-Exclusive, Atomic CAS Replay Protected, Exact-Command Bound)
Location: ~/Library/Application Support/t3/bin/t3_approval.py

Enforces cryptographically signed approval tokens with 5-minute TTL.
Uses macOS Keychain (service: t3-approval-key) as the EXCLUSIVE secret store.
Atomic Compare-and-Swap (CAS) consumption prevents concurrent replay races.
Tokens are strictly bound to the SHA-256 digest of the exact normalized command line.
"""
import sys
import os
import time
import hmac
import hashlib
import json
import shlex
import subprocess
from pathlib import Path

TOKEN_DIR = Path.home() / "Library/Application Support/t3/tokens"
TOKEN_DIR.mkdir(parents=True, exist_ok=True)
TTL_SECONDS = 300
KEYCHAIN_SERVICE = "t3-approval-key"

def compute_cmd_digest(action: str) -> str:
    try:
        tokens = shlex.split(action.strip())
        norm_cmd = " ".join(tokens)
    except Exception:
        norm_cmd = action.strip()
    return hashlib.sha256(norm_cmd.encode("utf-8")).hexdigest()

def get_secret_key() -> bytes:
    user = os.environ.get("USER", "groundfox")
    # 1. Read key from macOS Keychain
    try:
        res = subprocess.run(
            ["security", "find-generic-password", "-a", user, "-s", KEYCHAIN_SERVICE, "-w"],
            capture_output=True, text=True
        )
        if res.returncode == 0 and res.stdout.strip():
            return res.stdout.strip().encode("utf-8")
    except Exception as e:
        sys.stderr.write(f"[KEYCHAIN ERROR] Failed reading Keychain item: {e}\n")

    # 2. If missing, provision into macOS Keychain
    new_key = os.urandom(32).hex()
    try:
        subprocess.run(
            ["security", "add-generic-password", "-a", user, "-s", KEYCHAIN_SERVICE, "-w", new_key, "-U"],
            capture_output=True, check=True
        )
        return new_key.encode("utf-8")
    except Exception as e:
        sys.stderr.write(f"[KEYCHAIN FATAL] Cannot provision or access macOS Keychain: {e}\n")
        sys.exit(75)

def mint_token(session_id: str, action: str) -> str:
    key = get_secret_key()
    ts = int(time.time())
    nonce = os.urandom(16).hex()
    cmd_digest = compute_cmd_digest(action)
    payload = f"{session_id}:{cmd_digest}:{ts}:{nonce}".encode("utf-8")
    sig = hmac.new(key, payload, hashlib.sha256).hexdigest()
    token_data = {
        "session_id": session_id,
        "action": action,
        "cmd_digest": cmd_digest,
        "timestamp": ts,
        "nonce": nonce,
        "signature": sig
    }
    token_file = TOKEN_DIR / f"approval-{session_id}-{cmd_digest[:16]}.json"
    with open(token_file, "w", encoding="utf-8") as f:
        json.dump(token_data, f)
    print(f"[TOKEN MINTED] Action '{action}' (hash={cmd_digest[:12]}) approved for session '{session_id}'. Nonce={nonce[:8]}... TTL={TTL_SECONDS}s.")
    return str(token_file)

def verify_token(session_id: str, action: str) -> bool:
    cmd_digest = compute_cmd_digest(action)
    token_file = TOKEN_DIR / f"approval-{session_id}-{cmd_digest[:16]}.json"
    consuming_file = TOKEN_DIR / f"consuming-{session_id}-{cmd_digest[:16]}-{os.getpid()}-{time.time_ns()}.json"

    # Atomic Compare-and-Swap (CAS): atomic rename prevents replay races
    try:
        os.replace(token_file, consuming_file)
    except (FileNotFoundError, OSError):
        sys.stderr.write(f"[APPROVAL DENIED 75] No active or already consumed approval token for exact action: '{action}' (hash={cmd_digest[:12]})\n")
        return False

    try:
        with open(consuming_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        key = get_secret_key()
        ts = data.get("timestamp", 0)
        nonce = data.get("nonce", "")
        token_digest = data.get("cmd_digest", "")
        now = int(time.time())

        # Verify command binding
        if token_digest != cmd_digest:
            sys.stderr.write(f"[APPROVAL DENIED 75] Token command binding mismatch: expected {cmd_digest[:12]}, got {token_digest[:12]}\n")
            return False

        if now - ts > TTL_SECONDS:
            sys.stderr.write(f"[APPROVAL DENIED 75] Token expired ({now - ts}s > {TTL_SECONDS}s).\n")
            return False

        expected_payload = f"{session_id}:{cmd_digest}:{ts}:{nonce}".encode("utf-8")
        expected_sig = hmac.new(key, expected_payload, hashlib.sha256).hexdigest()
        if not hmac.compare_digest(expected_sig, data.get("signature", "")):
            sys.stderr.write("[APPROVAL DENIED 75] Forged token signature detected.\n")
            return False

        return True
    finally:
        consuming_file.unlink(missing_ok=True)

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: t3_approval.py <mint|verify> <session_id> <action>")
        sys.exit(1)
    mode = sys.argv[1]
    sess = sys.argv[2]
    act = " ".join(sys.argv[3:])
    if mode == "mint":
        mint_token(sess, act)
        sys.exit(0)
    elif mode == "verify":
        if verify_token(sess, act):
            print(f"[APPROVAL VERIFIED] Token valid for exact command: {act}")
            sys.exit(0)
        else:
            sys.exit(75)
    else:
        sys.exit(1)
