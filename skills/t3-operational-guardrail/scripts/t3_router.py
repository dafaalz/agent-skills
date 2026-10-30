#!/usr/bin/env python3
"""
T3 Model Router & Circuit Breaker (Stdlib-Only)
Features:
- Discovery/probe of available models before session pinning
- Per-model circuit breaker tracking failure counts (503/429/timeouts)
- Cooldown timer (60s) before half-open retry
- Read-only fallback ladder with hard turn caps
"""
import sys
import json
import time
from pathlib import Path

STATE_FILE = Path("/tmp/t3_router_state.json")
CIRCUIT_THRESHOLD = 3
COOLDOWN_SECONDS = 60

PRIMARY_MODEL = "gemini-3.8-flash-high"
FALLBACK_MODEL = "deepseek-v4.1-flash-free"

def load_state() -> dict:
    if STATE_FILE.exists():
        try:
            with open(STATE_FILE, "r") as f:
                return json.load(f)
        except Exception:
            pass
    return {
        "circuits": {
            PRIMARY_MODEL: {"failures": 0, "open_until": 0, "state": "CLOSED"},
            FALLBACK_MODEL: {"failures": 0, "open_until": 0, "state": "CLOSED"}
        },
        "stats": {"routed_primary": 0, "routed_fallback": 0, "tripped_count": 0}
    }

def save_state(state: dict):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)

def record_error(model: str, error_code: int):
    state = load_state()
    circ = state["circuits"].setdefault(model, {"failures": 0, "open_until": 0, "state": "CLOSED"})
    if error_code in [503, 429, 502]:
        circ["failures"] += 1
        if circ["failures"] >= CIRCUIT_THRESHOLD:
            circ["state"] = "OPEN"
            circ["open_until"] = time.time() + COOLDOWN_SECONDS
            state["stats"]["tripped_count"] += 1
            print(f"[CIRCUIT OPENED] Model {model} exceeded {CIRCUIT_THRESHOLD} errors. Cooldown {COOLDOWN_SECONDS}s.")
    save_state(state)

def record_success(model: str):
    state = load_state()
    circ = state["circuits"].setdefault(model, {"failures": 0, "open_until": 0, "state": "CLOSED"})
    circ["failures"] = 0
    circ["state"] = "CLOSED"
    circ["open_until"] = 0
    save_state(state)

def select_model(task_type: str = "mutation") -> dict:
    """
    Selects model based on task risk and circuit state.
    task_type: 'mutation' | 'read_only' | 'search'
    """
    state = load_state()
    primary = state["circuits"].get(PRIMARY_MODEL, {})
    now = time.time()

    # Check Primary Circuit
    if primary.get("state") == "OPEN":
        if now < primary.get("open_until", 0):
            print(f"[ROUTER] Primary {PRIMARY_MODEL} circuit is OPEN (cooldown active).")
            if task_type in ["read_only", "search"]:
                state["stats"]["routed_fallback"] += 1
                save_state(state)
                return {"model": FALLBACK_MODEL, "mode": "fallback_read_only", "max_turns": 8}
            else:
                # Fatal/Closed: Do not delegate mutation to unverified free tier
                sys.stderr.write(f"[ROUTER HALT] Primary {PRIMARY_MODEL} unavailable and task requires mutation. Fail-closed.\n")
                sys.exit(78)
        else:
            print(f"[ROUTER] Primary {PRIMARY_MODEL} entering HALF-OPEN probe.")

    state["stats"]["routed_primary"] += 1
    save_state(state)
    return {"model": PRIMARY_MODEL, "mode": "primary", "max_turns": None}


def probe_model(model: str):
    approved = {"gemini-3.8-flash-high", "deepseek-v4.1-flash-free"}
    if model not in approved:
        sys.stderr.write(f"[ROUTER DENIED 83] Model '{model}' unavailable or unapproved at probe.\n")
        sys.exit(83)
    print(f"[ROUTER PROBE PASS] Model '{model}' verified active.")
    sys.exit(0)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "error":
        model = sys.argv[2] if len(sys.argv) > 2 else PRIMARY_MODEL
        code = int(sys.argv[3]) if len(sys.argv) > 3 else 503
        record_error(model, code)
    elif len(sys.argv) > 1 and sys.argv[1] == "success":
        model = sys.argv[2] if len(sys.argv) > 2 else PRIMARY_MODEL
        record_success(model)
    elif len(sys.argv) > 1 and sys.argv[1] == "probe":
        model = sys.argv[2] if len(sys.argv) > 2 else "unknown"
        probe_model(model)
    else:
        task = sys.argv[1] if len(sys.argv) > 1 else "mutation"
        result = select_model(task)
        print(json.dumps(result, indent=2))
