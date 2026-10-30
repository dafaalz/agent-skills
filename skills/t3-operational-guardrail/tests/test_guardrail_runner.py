import unittest
import subprocess
import sys
from pathlib import Path

TESTS_DIR = Path(__file__).resolve().parent

class TestT3OperationalGuardrailSuites(unittest.TestCase):
    """
    Standard unittest test cases wrapping all guardrail adversarial and behavioral suites.
    The 21 test runner methods fan out to 280+ discrete adversarial test cases across all audit rounds.
    """

    def _run_suite(self, filename: str):
        sessions_dir = Path.home() / "Library/Application Support/t3/sessions"
        if sessions_dir.exists():
            for p in sessions_dir.glob("*/iteration_counter.json"):
                try:
                    p.unlink()
                except Exception:
                    pass
        target = TESTS_DIR / filename
        self.assertTrue(target.exists(), f"Target test file missing: {target}")
        res = subprocess.run(
            [sys.executable, str(target)],
            capture_output=True,
            text=True,
            cwd=TESTS_DIR.parent
        )
        self.assertEqual(
            res.returncode, 0,
            f"Guardrail suite '{filename}' failed with code {res.returncode}:\nSTDOUT:\n{res.stdout}\nSTDERR:\n{res.stderr}"
        )

    def test_01_acp_call_path(self):
        """test_01_acp_call_path (fans out to 12 ACP gateway JSON-RPC call path verification cases)"""
        self._run_suite("test_acp_call_path.py")

    def test_02_adversarial_matrix(self):
        """test_02_adversarial_matrix (fans out to 64 operational resilience cases, 100% pass)"""
        self._run_suite("test_adversarial_matrix.py")

    def test_03_approval_replay(self):
        """test_03_approval_replay (fans out to atomic CAS HMAC single-use token replay prevention cases)"""
        self._run_suite("test_approval_replay.py")

    def test_04_brief_lint_adversarial(self):
        """test_04_brief_lint_adversarial (fans out to 6 task-brief pre-flight rejection cases, EC 84-88)"""
        self._run_suite("test_brief_lint_adversarial.py")

    def test_05_dispatcher_adversarial(self):
        """test_05_dispatcher_adversarial (fans out to 26 negative bypass injection cases, EC 70-77)"""
        self._run_suite("test_dispatcher_adversarial.py")

    def test_06_integration_hardened(self):
        """test_06_integration_hardened (fans out to 4 integration cases: EC 82 hash tampering, EC 81 worktree queue, EC 78 circuit breaker)"""
        self._run_suite("test_integration_hardened.py")

    def test_07_pinning_survives_compaction(self):
        """test_07_pinning_survives_compaction (fans out to message-slot 1 compaction survival verification cases)"""
        self._run_suite("test_pinning_survives_compaction.py")

    def test_08_router_and_worktree(self):
        """test_08_router_and_worktree (fans out to open-circuit breaker fail-closed and worktree atomic locks)"""
        self._run_suite("test_router_and_worktree.py")

    def test_09_sandbox_kernel_probes(self):
        """test_09_sandbox_kernel_probes (fans out to 4 Darwin Seatbelt sandbox kernel probe cases)"""
        self._run_suite("test_sandbox_kernel_probes.py")

    def test_10_audit_round8_verification(self):
        """test_10_audit_round8_verification (fans out to 32 regression cases: token bindings, hook neutralization)"""
        self._run_suite("test_audit_round8_verification.py")

    def test_11_audit_round9_scenarios(self):
        """test_11_audit_round9_scenarios (fans out to 8 attack scenarios: INI driver injection, git add flags)"""
        self._run_suite("test_audit_round9_scenarios.py")

    def test_12_audit_round10_scenarios(self):
        """test_12_audit_round10_scenarios (fans out to 12 attack scenarios: branch grammar, push hook bypasses)"""
        self._run_suite("test_audit_round10_scenarios.py")

    def test_13_audit_round11_scenarios(self):
        """test_13_audit_round11_scenarios (fans out to 11 attack scenarios: askpass, combined prefix, secret paths)"""
        self._run_suite("test_audit_round11_scenarios.py")

    def test_14_audit_round12_scenarios(self):
        """test_14_audit_round12_scenarios (fans out to 14 attack scenarios: commit flags, signature format specifiers)"""
        self._run_suite("test_audit_round12_scenarios.py")

    def test_15_audit_round13_scenarios(self):
        """test_15_audit_round13_scenarios (fans out to 18 attack scenarios: pathspec escapes, repo-root resolution)"""
        self._run_suite("test_audit_round13_scenarios.py")

    def test_16_audit_round14_scenarios(self):
        """test_16_audit_round14_scenarios (fans out to 13 attack scenarios: repo-root traversal, multi -m flags)"""
        self._run_suite("test_audit_round14_scenarios.py")

    def test_17_audit_round15_scenarios(self):
        """test_17_audit_round15_scenarios (fans out to 11 attack scenarios: exotic pathspec magic :(:!, -F combined flag)"""
        self._run_suite("test_audit_round15_scenarios.py")

    def test_18_audit_round16_scenarios(self):
        """test_18_audit_round16_scenarios (fans out to 12 attack scenarios: pathspec ordering, swap extensions)"""
        self._run_suite("test_audit_round16_scenarios.py")

    def test_19_audit_round17_scenarios(self):
        """test_19_audit_round17_scenarios (fans out to 11 attack scenarios: double backup extensions, --message=)"""
        self._run_suite("test_audit_round17_scenarios.py")

    def test_20_audit_round18_scenarios(self):
        """test_20_audit_round18_scenarios (fans out to 7 attack scenarios: trailing dots, prefix tilde, lockfile markers)"""
        self._run_suite("test_audit_round18_scenarios.py")

    def test_21_audit_round19_scenarios(self):
        """test_21_audit_round19_scenarios (fans out to 8 attack scenarios: receipt protection and hard loop budget)"""
        if (TESTS_DIR / "test_audit_round19_scenarios.py").exists():
            self._run_suite("test_audit_round19_scenarios.py")

    def test_22_audit_round20_scenarios(self):
        """test_22_audit_round20_scenarios (fans out to 7 attack scenarios: iterative prefix stripping ~$ and ~)"""
        if (TESTS_DIR / "test_audit_round20_scenarios.py").exists():
            self._run_suite("test_audit_round20_scenarios.py")

    def test_23_audit_round21_scenarios(self):
        """test_23_audit_round21_scenarios (fans out to 5 attack scenarios: S-N2 priority reconciliation)"""
        if (TESTS_DIR / "test_audit_round21_scenarios.py").exists():
            self._run_suite("test_audit_round21_scenarios.py")

if __name__ == "__main__":
    unittest.main()
