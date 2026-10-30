import unittest
import subprocess
import sys
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
GUARDRAIL_TESTS_DIR = REPO_ROOT / "skills/t3-operational-guardrail/tests"

class TestGuardrailBehavioralGate(unittest.TestCase):
    """
    Official CI gate integration for the guardrail behavioral suite.
    """
    def test_all_guardrail_behavioral_suites(self):
        res = subprocess.run(
            [sys.executable, "-m", "unittest", "discover", "-s", str(GUARDRAIL_TESTS_DIR)],
            capture_output=True,
            text=True,
            cwd=REPO_ROOT
        )
        self.assertEqual(
            res.returncode, 0,
            f"Guardrail behavioral suites failed with exit code {res.returncode}:\nSTDOUT:\n{res.stdout}\nSTDERR:\n{res.stderr}"
        )
        output = res.stderr or res.stdout
        match = re.search(r"Ran (\d+) tests", output)
        self.assertIsNotNone(match, f"Unable to parse test count from output:\n{output}")
        discovered = int(match.group(1))
        expected_suites = len([p for p in GUARDRAIL_TESTS_DIR.glob("test_*.py") if p.name != "test_guardrail_runner.py"])
        self.assertEqual(discovered, expected_suites)
        self.assertGreaterEqual(discovered, 23)

if __name__ == "__main__":
    unittest.main()
