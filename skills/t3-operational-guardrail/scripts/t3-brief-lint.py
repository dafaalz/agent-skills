#!/usr/bin/env python3
"""
T3 Pre-Flight Brief Linter (Fail-Closed, Out-of-Tree)
Location: ~/Library/Application Support/t3/bin/t3-brief-lint.py
De-collided Exit Codes:
  80: Symlink target rejection
  84: Agent-supplied session_id rejection
  85: Directory traversal or absolute path rejection
  86: Missing design anchor rejection
  87: Unauthorized tool allowlist request
"""
import sys
import json
import os
import uuid
from pathlib import Path

VALID_MODES = {"audit", "implement", "commit"}
VALID_TOOLS = {
    "view_file", "create_file", "edit_file", "run_command",
    "search_web", "read_url_content", "delegate_task"
}

EC_SYMLINK = 88
EC_AGENT_SUPPLIED_SESSION = 84
EC_LINT_TRAVERSAL = 85
EC_LINT_MISSING_ANCHOR = 86
EC_LINT_UNAUTHORIZED_TOOL = 87

def lint_brief(brief_path: str, session_id: str = None) -> int:
    path = Path(brief_path)
    if not path.exists():
        sys.stderr.write(f"[FATAL 85] Brief file not found: {brief_path}\n")
        return EC_LINT_TRAVERSAL

    try:
        with open(path, "r", encoding="utf-8") as f:
            brief = json.load(f)
    except Exception as e:
        sys.stderr.write(f"[FATAL 85] Malformed JSON in brief: {e}\n")
        return EC_LINT_TRAVERSAL

    # 1. Deny Agent-Supplied Session ID (EC 84)
    if "session_id" in brief:
        sys.stderr.write("[LINT DENIED 84] Agent-supplied session_id prohibited. Session ID must be minted by orchestrator.\n")
        return EC_AGENT_SUPPLIED_SESSION

    # 2. Mode Validation
    mode = brief.get("mode")
    if mode not in VALID_MODES:
        sys.stderr.write(f"[LINT DENIED 85] Invalid mode: '{mode}'. Must be one of {VALID_MODES}\n")
        return EC_LINT_TRAVERSAL

    # 3. Target Paths Validation
    targets = brief.get("targets", [])
    if not targets or not isinstance(targets, list):
        sys.stderr.write("[LINT DENIED 85] Target paths must be a non-empty list.\n")
        return EC_LINT_TRAVERSAL

    for t in targets:
        p = Path(t)
        # Traversal check (EC 85)
        if ".." in t or t.startswith("/"):
            sys.stderr.write(f"[LINT DENIED 85] Traversal or absolute path prohibited: {t}\n")
            return EC_LINT_TRAVERSAL
        # Symlink check (EC 80)
        if p.is_symlink():
            sys.stderr.write(f"[LINT DENIED 88] Symlink target rejected: {t}\n")
            return EC_SYMLINK
        if mode == "audit" and not p.exists():
            sys.stderr.write(f"[LINT DENIED 85] Target path does not exist for audit mode: {t}\n")
            return EC_LINT_TRAVERSAL

    # 4. Design Anchor Check (EC 86)
    anchor = brief.get("design_anchor")
    if anchor:
        ap = Path(anchor)
        if not ap.exists() or ap.is_symlink():
            sys.stderr.write(f"[LINT DENIED 86] Design anchor missing or symlink: {anchor}\n")
            return EC_LINT_MISSING_ANCHOR

    # 5. Tool Allowlist Check (EC 87)
    tools = brief.get("allowed_tools", [])
    if not tools or not isinstance(tools, list):
        sys.stderr.write("[LINT DENIED 87] allowed_tools must be a non-empty list.\n")
        return EC_LINT_UNAUTHORIZED_TOOL
    unknown_tools = set(tools) - VALID_TOOLS
    if unknown_tools:
        sys.stderr.write(f"[LINT DENIED 87] Unauthorized tools requested: {unknown_tools}\n")
        return EC_LINT_UNAUTHORIZED_TOOL

    # 6. Mint Session Manifest
    minted_session = session_id or str(uuid.uuid4())
    sess_dir = Path.home() / f"Library/Application Support/t3/sessions/{minted_session}"
    sess_dir.mkdir(parents=True, exist_ok=True)
    manifest_file = sess_dir / "task-manifest.json"

    manifest_data = {
        "session_id": minted_session,
        "mode": mode,
        "targets": targets,
        "allowed_tools": tools,
        "design_anchor": anchor,
        "test_policy": brief.get("test_policy", "contract"),
        "commit_allowed": False
    }

    with open(manifest_file, "w", encoding="utf-8") as mf:
        json.dump(manifest_data, mf, indent=2)

    print(f"[LINT PASSED] Session '{minted_session}' manifest minted at {manifest_file}")
    return 0

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: t3-brief-lint.py <task_brief.json> [session_id]")
        sys.exit(1)
    sess_arg = sys.argv[2] if len(sys.argv) > 2 else None
    sys.exit(lint_brief(sys.argv[1], sess_arg))
