#!/usr/bin/env python3
"""
Adversarial Evasion Vector Test Suite (test_evasion.py)
Empirically tests that evasive attempts, argument bypasses, hand-crafted receipts,
untracked file tampering, and dummy executions FAIL closed under run_receipt.py and lint_skill.py.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


def run_cmd(cmd: list[str], cwd: Path) -> tuple[int, str, str]:
    proc = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    return proc.returncode, proc.stdout, proc.stderr


def main() -> int:
    repo_root = Path(__file__).resolve().parents[3]
    run_receipt = repo_root / "skills" / "verification-before-completion" / "scripts" / "run_receipt.py"
    lint_skill = repo_root / "skills" / "review-a-skill" / "scripts" / "lint_skill.py"
    fixtures_dir = repo_root / "skills" / "review-a-skill" / "scripts" / "fixtures" / "lint"

    tests_run = 0
    tests_passed = 0

    print("=" * 70)
    print("RUNNING ADVERSARIAL EVASION TEST SUITE")
    print("=" * 70)

    # 1. python3 -O -c 'pass' bypass attempt
    tests_run += 1
    code, out, err = run_cmd([sys.executable, str(run_receipt), "--command", "python3 -O -c pass"], repo_root)
    if code != 0 and "forbidden" in (out + err).lower():
        print("[PASS] Evasion 1: python3 -O -c 'pass' rejected")
        tests_passed += 1
    else:
        print(f"[FAIL] Evasion 1: python3 -O -c 'pass' was NOT rejected (exit {code})")

    # 2. --evil-flag bypass attempt
    tests_run += 1
    code, out, err = run_cmd([sys.executable, str(run_receipt), "--command", f"python3 {lint_skill} --evil-flag"], repo_root)
    if code != 0 and "forbidden or unknown argument" in (out + err).lower():
        print("[PASS] Evasion 2: --evil-flag rejected")
        tests_passed += 1
    else:
        print(f"[FAIL] Evasion 2: --evil-flag was NOT rejected (exit {code})")

    # 3. Metacharacter injection attempt
    tests_run += 1
    code, out, err = run_cmd([sys.executable, str(run_receipt), "--command", f"python3 {lint_skill} ; true"], repo_root)
    if code != 0 and "metacharacter" in (out + err).lower():
        print("[PASS] Evasion 3: Shell metacharacter ';' rejected")
        tests_passed += 1
    else:
        print(f"[FAIL] Evasion 3: Shell metacharacter was NOT rejected (exit {code})")

    # 4. Dummy command rejection
    tests_run += 1
    code, out, err = run_cmd([sys.executable, str(run_receipt), "--command", "true"], repo_root)
    if code != 0 and ("dummy command" in (out + err).lower() or "not in the trusted allowlist" in (out + err).lower()):
        print("[PASS] Evasion 4: Dummy command 'true' rejected by allowlist / dummy check")
        tests_passed += 1
    else:
        print(f"[FAIL] Evasion 4: Dummy command was NOT rejected (exit {code})")

    # 5. Untracked evil.txt created after receipt -> live worktree check in --verify
    tests_run += 1
    evil_file = repo_root / "evil.txt"
    try:
        evil_file.write_text("untracked evil content\n")
        code, out, err = run_cmd([sys.executable, str(run_receipt), "--verify"], repo_root)
        if code != 0 and "live worktree is dirty" in (out + err).lower():
            print("[PASS] Evasion 5: Untracked evil.txt detected by live worktree verify")
            tests_passed += 1
        else:
            print(f"[FAIL] Evasion 5: Untracked evil.txt was NOT caught by --verify (exit {code})")
    finally:
        if evil_file.exists():
            evil_file.unlink()

    # 6. Tampered line_counts in temporary receipt
    tests_run += 1
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        receipt_path = tmp_path / "verification-receipt.json"
        hash_path = tmp_path / "receipt-hash.txt"
        lc_path = repo_root / ".agents" / "state" / "verification-before-completion" / "line-counts.txt"

        src_receipt = json.loads((repo_root / ".agents" / "state" / "verification-before-completion" / "verification-receipt.json").read_text())
        tampered_receipt = dict(src_receipt)
        tampered_receipt["line_counts"] = dict(tampered_receipt.get("line_counts", {}))
        tampered_receipt["line_counts"]["agent-planning"] = 999

        tb = (json.dumps(tampered_receipt, indent=2) + "\n").encode("utf-8")
        receipt_path.write_bytes(tb)
        thash = hashlib.sha256(tb).hexdigest()
        hash_path.write_text(f"{thash}  {receipt_path.as_posix()}\n")

        code, out, err = run_cmd([
            sys.executable, str(run_receipt), "--verify",
            "--out", str(receipt_path),
            "--hash-out", str(hash_path),
            "--stdout-out", str(repo_root / ".agents" / "state" / "verification-before-completion" / "last-stdout.log"),
            "--line-counts-file", str(lc_path),
        ], repo_root)
        if code != 0 and ("exceeds line budget" in (out + err).lower() or "line count divergence" in (out + err).lower()):
            print("[PASS] Evasion 6: Tampered line_counts detected and rejected")
            tests_passed += 1
        else:
            print(f"[FAIL] Evasion 6: Tampered line_counts NOT rejected (exit {code})")

    # 7. Schema invalid timestamp format
    tests_run += 1
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        receipt_path = tmp_path / "verification-receipt.json"
        hash_path = tmp_path / "receipt-hash.txt"
        src_receipt = json.loads((repo_root / ".agents" / "state" / "verification-before-completion" / "verification-receipt.json").read_text())
        tampered_receipt = dict(src_receipt)
        tampered_receipt["start_time_iso8601"] = "invalid-date-format"

        tb = (json.dumps(tampered_receipt, indent=2) + "\n").encode("utf-8")
        receipt_path.write_bytes(tb)
        thash = hashlib.sha256(tb).hexdigest()
        hash_path.write_text(f"{thash}  {receipt_path.as_posix()}\n")

        code, out, err = run_cmd([
            sys.executable, str(run_receipt), "--verify",
            "--out", str(receipt_path),
            "--hash-out", str(hash_path),
            "--stdout-out", str(repo_root / ".agents" / "state" / "verification-before-completion" / "last-stdout.log"),
        ], repo_root)
        if code != 0 and "not valid iso-8601" in (out + err).lower():
            print("[PASS] Evasion 7: Invalid timestamp schema rejected")
            tests_passed += 1
        else:
            print(f"[FAIL] Evasion 7: Invalid timestamp NOT rejected (exit {code})")

    # 8. Wrong filename in receipt-hash.txt
    tests_run += 1
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        receipt_path = tmp_path / "verification-receipt.json"
        hash_path = tmp_path / "receipt-hash.txt"
        src_receipt_bytes = (repo_root / ".agents" / "state" / "verification-before-completion" / "verification-receipt.json").read_bytes()
        receipt_path.write_bytes(src_receipt_bytes)
        thash = hashlib.sha256(src_receipt_bytes).hexdigest()
        hash_path.write_text(f"{thash}  fake-wrong-receipt.json\n")

        code, out, err = run_cmd([
            sys.executable, str(run_receipt), "--verify",
            "--out", str(receipt_path),
            "--hash-out", str(hash_path),
            "--stdout-out", str(repo_root / ".agents" / "state" / "verification-before-completion" / "last-stdout.log"),
        ], repo_root)
        if code != 0 and "invalid target filename" in (out + err).lower():
            print("[PASS] Evasion 8: Wrong target filename in receipt-hash.txt rejected")
            tests_passed += 1
        else:
            print(f"[FAIL] Evasion 8: Wrong target filename was NOT rejected (exit {code})")

    # 9. R13 periodic padding fixture detection in lint_skill.py
    tests_run += 1
    code, out, err = run_cmd([sys.executable, str(lint_skill), str(fixtures_dir / "r13-periodic-padding-negative.md")], repo_root)
    if code != 0 and "periodic repetition padding" in (out + err).lower():
        print("[PASS] Evasion 9: R13 periodic padding ('abcabc') detected and rejected")
        tests_passed += 1
    else:
        print(f"[FAIL] Evasion 9: R13 periodic padding was NOT detected (exit {code})")

    # 10. R13 sequential padding fixture detection in lint_skill.py
    tests_run += 1
    code, out, err = run_cmd([sys.executable, str(lint_skill), str(fixtures_dir / "r13-sequential-padding-negative.md")], repo_root)
    if code != 0 and "sequential character padding" in (out + err).lower():
        print("[PASS] Evasion 10: R13 sequential padding ('abcdef') detected and rejected")
        tests_passed += 1
    else:
        print(f"[FAIL] Evasion 10: R13 sequential padding was NOT detected (exit {code})")

    # 11. R13 dummy phrase fixture detection in lint_skill.py
    tests_run += 1
    code, out, err = run_cmd([sys.executable, str(lint_skill), str(fixtures_dir / "r13-dummy-phrase-negative.md")], repo_root)
    if code != 0 and "dummy filler phrase" in (out + err).lower():
        print("[PASS] Evasion 11: R13 dummy phrase ('hello world') detected and rejected")
        tests_passed += 1
    else:
        print(f"[FAIL] Evasion 11: R13 dummy phrase was NOT detected (exit {code})")

    # 12. R9 backticked fuzzy identifier fixture detection in lint_skill.py
    tests_run += 1
    code, out, err = run_cmd([sys.executable, str(lint_skill), str(fixtures_dir / "r9-backtick-identifier-fuzzy-negative.md")], repo_root)
    if code != 0 and ("fuzzy word in code identifier" in (out + err).lower() or "fuzzy phrase matching" in (out + err).lower()):
        print("[PASS] Evasion 12: R9 backticked fuzzy identifier ('`ensure`') detected and rejected")
        tests_passed += 1
    else:
        print(f"[FAIL] Evasion 12: R9 backticked fuzzy identifier was NOT detected (exit {code})")

    print("=" * 70)
    print(f"ADVERSARIAL EVASION TEST RESULTS: {tests_passed}/{tests_run} passed")
    print("=" * 70)

    if tests_passed == tests_run:
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
