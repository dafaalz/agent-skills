import os
import unittest

SKILLS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "skills"))

EXPECTED_SKILLS = {
    "brainstorming",
    "code-review",
    "codebase-design",
    "conventional-commit",
    "copy-web-design",
    "executing-plans",
    "frontend-design",
    "i18n",
    "laravel",
    "prototype",
    "react",
    "s13n",
    "security-audit",
    "summarize",
    "systematic-debugging",
    "technical-writing",
    "testing-patterns",
    "ui-motion",
    "ui-ux-review",
    "unslop",
    "upsert-codebase-docs",
    "verification-before-completion",
    "workspace-onboarding",
    "writing-for-agents",
    "writing-plans",
}

DEPRECATED_SKILLS = {
    "graphify",
    "output-skill",
    "dispatching-parallel-agents",
    "finishing-a-development-branch",
    "ping",
    "qa-engineer",
}

REQUIRED_REFERENCES = [
    ("conventional-commit", "references/resolving-conflicts.md"),
    ("executing-plans", "references/parallel-dispatch.md"),
    ("testing-patterns", "references/test-matrix-and-charters.md"),
    ("verification-before-completion", "references/lighthouse-ci.md"),
    ("react", "SKILL.md"),
    ("s13n", "references/divergence-taxonomy.md"),
    ("i18n", "references/intl-language.md"),
    ("summarize", "SKILL.md"),
    ("security-audit", "references/baas-and-fullstack-frameworks.md"),
]


class TestConsolidation(unittest.TestCase):
    def test_active_skills_exact_match(self):
        actual_skills = {
            d for d in os.listdir(SKILLS_DIR)
            if os.path.isdir(os.path.join(SKILLS_DIR, d)) and not d.startswith(".")
        }
        self.assertEqual(
            actual_skills,
            EXPECTED_SKILLS,
            f"Active skills mismatch. Found {len(actual_skills)}, expected {len(EXPECTED_SKILLS)}."
        )

    def test_deprecated_skills_removed(self):
        actual_skills = {
            d for d in os.listdir(SKILLS_DIR)
            if os.path.isdir(os.path.join(SKILLS_DIR, d)) and not d.startswith(".")
        }
        overlapping = actual_skills.intersection(DEPRECATED_SKILLS)
        self.assertEqual(
            overlapping,
            set(),
            f"Deprecated skills still present in skills directory: {overlapping}"
        )

    def test_required_references_exist(self):
        for skill_name, rel_path in REQUIRED_REFERENCES:
            target_path = os.path.join(SKILLS_DIR, skill_name, rel_path)
            self.assertTrue(
                os.path.exists(target_path),
                f"Missing required file: {skill_name}/{rel_path}"
            )

    def test_credentials_hygiene_covers_client_prefixes(self):
        target = os.path.join(SKILLS_DIR, "security-audit", "references", "credentials-hygiene.md")
        with open(target, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("NEXT_PUBLIC_", content)
        self.assertIn("EXPO_PUBLIC_", content)
        self.assertIn("VITE_", content)

    def test_protocols_covers_payment_and_raw_body(self):
        target = os.path.join(SKILLS_DIR, "security-audit", "references", "protocols-rpc-and-messaging.md")
        with open(target, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("express.raw", content)
        self.assertIn("Stripe Price IDs", content)


if __name__ == "__main__":
    unittest.main()
