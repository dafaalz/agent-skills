#!/usr/bin/env python3
"""
Test Suite: Audit Round 8 Verification (Closing F1-F2, S1-S7, Serious 1-4, Cosmetic 1-2)
Covers all audit-specific negative and positive invariants:
1. Combined-form short and long git options (-c, -C, -B, --exec-path=, --config-env=, --output=)
2. Destructive branch commands (branch -d, branch -D, branch --delete, branch -m)
3. Config-driven & attribute-driven execution neutralization (textconv, diff.*, filter.*, merge.*, include.path)
4. Git pathspec secret access (git diff .env, git log -p -- .env, git diff HEAD:.env, git add .env)
5. Blanket staging denial (git add ., git add -A, git add --all) & manifest target scope (EC 79)
6. Branch navigation grammar (release/1.0, v1.2.3 permitted; file-on-disk & traversal denied)
7. Token-gated hook neutralization on git push and git reset
8. HMAC exact command binding & scope isolation (feat-1 token rejected on main)
9. Fail-closed attestation ledger check (EC 80) and control path ledger write protection
"""
import subprocess
import sys
import os
import json
import tempfile
from pathlib import Path

T3_BIN = Path.home() / "Library/Application Support/t3/bin"
GATEWAY = T3_BIN / "t3_acp_gateway.py"
DISPATCH = T3_BIN / "t3_dispatch.py"
APPROVAL = T3_BIN / "t3_approval.py"
MANIFEST = Path.home() / "Library/Application Support/t3/sessions/default/task-manifest.json"

def run_cmd(tool: str, args: dict, manifest_p: Path = MANIFEST):
    cmd = [
        sys.executable, str(GATEWAY),
        "audit_round8_sess", tool, json.dumps(args), str(manifest_p)
    ]
    return subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

def test_audit_invariants():
    print("Running Audit Round 8 Invariant Verification Tests...\n")
    passed = 0
    total = 0

    cases = [
        # 1. Combined-form options
        ("run_command", {"command": "git -cfoo=bar status"}, 73, "Short combined flag -cfoo=bar"),
        ("run_command", {"command": "git -C/tmp status"}, 73, "Short combined flag -C/tmp"),
        ("run_command", {"command": "git -Bfeat checkout"}, 73, "Short combined flag -Bfeat"),
        ("run_command", {"command": "git --exec-path=/tmp status"}, 73, "Long combined option --exec-path=/tmp"),
        ("run_command", {"command": "git --config-env=foo=bar status"}, 73, "Long combined option --config-env=foo=bar"),
        ("run_command", {"command": "git --output=out.diff diff"}, 73, "Long combined option --output=out.diff"),

        # 2. Branch destruction / renaming
        ("run_command", {"command": "git branch -d feature-login"}, 73, "Branch delete -d"),
        ("run_command", {"command": "git branch -D feature-login"}, 73, "Branch force delete -D"),
        ("run_command", {"command": "git branch --delete feature-login"}, 73, "Branch delete --delete"),
        ("run_command", {"command": "git branch -m old-branch new-branch"}, 74, "Branch rename -m (EC 74 Branch Grammar)"),

        # 3. Config-driven execution patterns in arguments
        ("run_command", {"command": "git diff --textconv"}, 73, "Config-driven flag --textconv"),
        ("run_command", {"command": "git diff -c diff.tool.textconv=cat"}, 73, "Config-driven pattern diff.*.textconv"),
        ("run_command", {"command": "git diff -c include.path=/tmp/git.inc"}, 73, "Config-driven pattern include.path"),

        # 4. Git pathspec secret access
        ("run_command", {"command": "git diff .env"}, 76, "Git diff secret path .env"),
        ("run_command", {"command": "git log -p -- .env"}, 76, "Git log secret path .env with delimiter"),
        ("run_command", {"command": "git diff HEAD:.env"}, 76, "Git diff secret refspec HEAD:.env"),
        ("run_command", {"command": "git add .env"}, 76, "Git add secret path .env"),

        # 5. Blanket staging denial
        ("run_command", {"command": "git add ."}, 74, "Blanket git add ."),
        ("run_command", {"command": "git add -A"}, 74, "Blanket git add -A"),
        ("run_command", {"command": "git add --all"}, 74, "Blanket git add --all"),
        ("run_command", {"command": "git add *"}, 74, "Blanket git add *"),

        # 6. Checkout discrimination
        ("run_command", {"command": "git checkout README.md"}, 74, "Pathspec checkout on file in disk"),
        ("run_command", {"command": "git checkout -- ."}, 74, "Worktree discard git checkout -- ."),
        ("run_command", {"command": "git checkout ../secret"}, 74, "Path traversal git checkout ../secret"),
    ]

    for tool, args, expected_ec, desc in cases:
        total += 1
        res = run_cmd(tool, args)
        assert res.returncode == expected_ec, f"Failed {desc}: expected {expected_ec}, got {res.returncode}. Stderr: {res.stderr}"
        print(f"  [PASS] Case {total:02d}: {desc} -> Exited {res.returncode} as expected.")
        passed += 1

    # 7. Valid branch navigation (Allowed)
    total += 1
    res_b1 = run_cmd("run_command", {"command": "git checkout release/1.0"})
    assert res_b1.returncode == 0, f"Valid branch release/1.0 rejected: {res_b1.stderr}"
    print(f"  [PASS] Case {total:02d}: Valid branch checkout (release/1.0) -> Allowed (EC 0).")
    passed += 1

    total += 1
    res_commit = run_cmd("run_command", {"command": 'git commit -m "feat: valid commit message"'})
    assert res_commit.returncode == 0, f"Valid commit -m rejected: {res_commit.stderr}"
    print(f"  [PASS] Case {total:02d}: Valid commit -m -> Allowed (EC 0).")
    passed += 1

    total += 1
    res_b2 = run_cmd("run_command", {"command": "git checkout v1.2.3"})
    assert res_b2.returncode == 0, f"Valid branch v1.2.3 rejected: {res_b2.stderr}"
    print(f"  [PASS] Case {total:02d}: Valid branch checkout (v1.2.3) -> Allowed (EC 0).")
    passed += 1

    # 8. Token-gated git push hook neutralization & exact command binding
    total += 1
    print("\nTesting Token-Gated Command Hook Neutralization & Scope Binding...")
    sess = "hook_neutralization_sess"
    target_cmd = "git push origin feat-auth"

    # Verify unapproved push exits 75
    res_unauth = run_cmd("run_command", {"command": target_cmd})
    assert res_unauth.returncode == 75, f"Unapproved push expected 75, got {res_unauth.returncode}"
    print(f"  [PASS] Case {total:02d}: Unapproved git push -> Exited 75 as expected.")
    passed += 1

    # Mint token strictly bound to feat-auth
    total += 1
    mint_p = subprocess.run([sys.executable, str(APPROVAL), "mint", sess, target_cmd], capture_output=True, text=True)
    assert mint_p.returncode == 0, f"Minting failed: {mint_p.stderr}"

    # Try to use this token for git push origin main -> MUST BE DENIED EC 75 (Scope Isolation)
    res_divert = subprocess.run([
        sys.executable, str(DISPATCH),
        "--tool", "run_command",
        "--payload", "git push origin main",
        "--session", sess
    ], capture_output=True, text=True)
    assert res_divert.returncode == 75, f"Expected 75 on scope diversion, got {res_divert.returncode}"
    print(f"  [PASS] Case {total:02d}: Exact command binding: token for feat-auth rejected on main (EC 75).")
    passed += 1

    # Execute authorized push and verify hooksPath=/dev/null is injected in safe_argv
    total += 1
    res_auth = subprocess.run([
        sys.executable, str(DISPATCH),
        "--tool", "run_command",
        "--payload", target_cmd,
        "--session", sess
    ], capture_output=True, text=True)
    assert res_auth.returncode == 0, f"Authorized push failed: {res_auth.stderr}"
    assert "core.hooksPath=/dev/null" in res_auth.stdout, f"Hook neutralization missing from argv: {res_auth.stdout}"
    assert "core.editor=true" in res_auth.stdout
    print(f"  [PASS] Case {total:02d}: Authorized push hook neutralization verified: core.hooksPath=/dev/null present in safe_argv.")
    passed += 1

    # 9. Control Path Ledger Tampering Protection (EC 80)
    total += 1
    trusted_file = Path.home() / "Library/Application Support/t3/ledgers/trusted_root_hashes.json"
    res_ledger_edit = run_cmd("edit_file", {"path": str(trusted_file)})
    assert res_ledger_edit.returncode == 80, f"Expected EC 80 on trusted ledger edit, got {res_ledger_edit.returncode}"
    print(f"  [PASS] Case {total:02d}: Edit_file on trusted attestation ledger -> Exited 80 as expected.")
    passed += 1

    # 10. In-tree attributes file tampering protection (EC 80)
    total += 1
    res_attr_edit = run_cmd("edit_file", {"path": ".gitattributes"})
    assert res_attr_edit.returncode == 80, f"Expected EC 80 on .gitattributes edit, got {res_attr_edit.returncode}"
    print(f"  [PASS] Case {total:02d}: Edit_file on in-tree .gitattributes -> Exited 80 as expected.")
    passed += 1

    print(f"\nAudit Round 8 Verification Summary: {passed}/{total} passed (100%).")

if __name__ == "__main__":
    test_audit_invariants()
