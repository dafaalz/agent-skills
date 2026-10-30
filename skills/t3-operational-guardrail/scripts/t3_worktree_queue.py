#!/usr/bin/env python3
"""
T3 Subagent Semantic-Unit Worktree Isolation & Merge Queue (Stdlib-Only)
Location: ~/Library/Application Support/t3/bin/t3_worktree_queue.py
Features:
- Enforces semantic-unit locking (e.g. controller + Blade pair)
- Prevents cross-subagent collisions on interdependent files
- Exit Code 81: Worktree Queue Conflict (Human Approval Required)
"""
import sys
import os
import json
from pathlib import Path

QUEUE_DIR = Path.home() / "Library/Application Support/t3/worktrees"
QUEUE_DIR.mkdir(parents=True, exist_ok=True)
LOCK_FILE = QUEUE_DIR / "locked_units.json"
EC_WORKTREE_CONFLICT = 81

def load_locks() -> dict:
    if LOCK_FILE.exists():
        try:
            with open(LOCK_FILE, "r") as f:
                return json.load(f)
        except Exception:
            pass
    return {}

def save_locks(locks: dict):
    with open(LOCK_FILE, "w") as f:
        json.dump(locks, f, indent=2)

def register_semantic_unit(session_id: str, unit_name: str, paths: list):
    locks = load_locks()
    for existing_unit, data in locks.items():
        if data["owner"] != session_id:
            # Check for path overlap
            overlap = set(paths).intersection(set(data["paths"]))
            if overlap:
                sys.stderr.write(f"[QUEUE CONFLICT 81] Semantic unit '{unit_name}' conflicts on paths {list(overlap)} with owner {data['owner']}.\n")
                sys.stderr.write("Human approval or serialized queuing required.\n")
                sys.exit(EC_WORKTREE_CONFLICT)

    locks[unit_name] = {"owner": session_id, "paths": paths}
    save_locks(locks)
    print(f"[WORKTREE LOCKED] Session '{session_id}' acquired semantic unit '{unit_name}' ({len(paths)} paths).")

def release_units(session_id: str):
    locks = load_locks()
    remaining = {k: v for k, v in locks.items() if v.get("owner") != session_id}
    save_locks(remaining)
    print(f"[WORKTREE RELEASED] Session '{session_id}' released all semantic unit locks.")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: t3_worktree_queue.py <register|release> <session_id> [unit_name] [paths_comma_separated]")
        sys.exit(1)

    action = sys.argv[1]
    sess = sys.argv[2]

    if action == "register":
        uname = sys.argv[3] if len(sys.argv) > 3 else "default_unit"
        upaths = sys.argv[4].split(",") if len(sys.argv) > 4 else []
        register_semantic_unit(sess, uname, upaths)
    elif action == "release":
        release_units(sess)
    else:
        sys.exit(1)
