"""Automated consolidation test suite for skills.

Verifies skill existence, reference preservation, frontmatter compliance,
line budgets (under 250 lines), and punctuation invariants (zero em/en dashes).
Compatible with pytest, python3 -m unittest, and direct execution via python3.
"""

import os
import sys
import unittest

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILLS_DIR = os.path.join(REPO_ROOT, "skills")

TARGET_SKILLS = [
    "frontend-design",
    "ui-ux-review",
    "code-review",
    "executing-plans",
    "testing-patterns",
    "writing-for-agents",
    "ui-motion",
    "systematic-debugging",
    "security-audit",
    "codebase-design",
    "brainstorming",
    "finishing-a-development-branch",
    "qa-engineer",
    "react",
    "conventional-commit",
    "s13n",
    "i18n",
    "summarize",
    "ping",
]

REQUIRED_REFERENCES = {
    "frontend-design": [
        "references/design-template.md",
        "references/recommended-libraries.md",
        "references/creative-motion-webgl.md",
        "references/ui-patterns.md",
        "references/anti-patterns.md",
        "references/custom-theme.md",
        "references/responsive.md",
        "references/slop-test.md",
        "references/structure.md",
        "references/api-resilience.md",
    ],
    "ui-ux-review": [
        "references/accessibility.md",
        "references/layout-and-space.md",
        "references/typography.md",
        "references/color-and-contrast.md",
        "references/component-mechanics.md",
        "references/copy-writing.md",
        "references/cognitive-laws.md",
        "references/heuristics-and-principles.md",
        "references/task-flows-and-ia.md",
        "references/forms-and-error-recovery.md",
        "references/system-status-and-states.md",
        "references/mobile-touch-ergonomics.md",
    ],
    "code-review": [
        "references/code-reviewer-prompt.md",
        "references/architectural-lenses.md",
        "references/comment-hygiene.md",
    ],
    "executing-plans": [
        "prompts/implementer-prompt.md",
        "prompts/spec-reviewer-prompt.md",
        "prompts/code-quality-reviewer-prompt.md",
    ],
    "testing-patterns": [
        "references/tdd-anti-patterns.md",
        "references/frontend-patterns.md",
        "references/backend-patterns.md",
        "references/e2e-patterns.md",
        "references/test-data-builders.md",
        "references/pre-commit-hooks.md",
    ],
    "writing-for-agents": [
        "references/testing-skills.md",
    ],
    "ui-motion": [
        "references/audit-and-plans.md",
        "references/physics-and-gestures.md",
        "references/recipes.md",
    ],
    "systematic-debugging": [
        "references/reproduction-and-loops.md",
    ],
    "security-audit": [
        "references/credentials-hygiene.md",
    ],
    "codebase-design": [
        "references/codebase-health-and-hotspots.md",
    ],
    "brainstorming": [
        "references/domain-modeling.md",
    ],
    "finishing-a-development-branch": [
        "references/resolving-conflicts.md",
    ],
    "qa-engineer": [
        "references/lighthouse-ci.md",
    ],
    "conventional-commit": [
        "references/commit-types.md",
    ],
    "s13n": [
        "references/divergence-taxonomy.md",
    ],
    "i18n": [
        "references/intl-language.md",
        "references/intl-date-and-time-format.md",
        "references/intl-number-and-currency.md",
        "references/intl-bidi.md",
        "references/intl-pluralization.md",
        "references/intl-collation-and-sorting.md",
        "references/intl-text-processing.md",
        "references/intl-content-and-assets.md",
        "references/intl-testing-and-qa.md",
    ],
}


class TestConsolidation(unittest.TestCase):
    """Main verification suite for target skills consolidation."""

    def test_target_skills_exist(self):
        """Assert all target skills exist."""
        missing = [
            skill
            for skill in TARGET_SKILLS
            if not os.path.exists(os.path.join(SKILLS_DIR, skill, "SKILL.md"))
        ]
        self.assertEqual(
            missing,
            [],
            f"Missing target skills: {missing}",
        )

    def test_references_preserved(self):
        """Assert required references and prompts exist."""
        missing = []
        for skill, refs in REQUIRED_REFERENCES.items():
            for ref in refs:
                ref_path = os.path.join(SKILLS_DIR, skill, ref)
                if not os.path.exists(ref_path):
                    missing.append(f"{skill}/{ref}")
        self.assertEqual(
            missing,
            [],
            f"Missing required references: {missing}",
        )

    def test_frontmatter_and_budget(self):
        """Assert frontmatter format, line budget under 250, and zero dashes."""
        for skill in TARGET_SKILLS:
            skill_path = os.path.join(SKILLS_DIR, skill, "SKILL.md")
            if not os.path.exists(skill_path):
                continue
            with open(skill_path, "r", encoding="utf-8") as f:
                content = f.read()
                lines = content.splitlines()

            self.assertLessEqual(
                len(lines),
                250,
                f"{skill}/SKILL.md exceeds 250 lines ({len(lines)})",
            )
            self.assertTrue(
                content.startswith("---\n"),
                f"{skill}/SKILL.md missing frontmatter start",
            )
            self.assertIn(
                f"name: {skill}",
                content,
                f"{skill}/SKILL.md missing matching name",
            )
            desc_ok = (
                "description: Use when" in content
                or "description: >\n  Use when" in content
                or "description: |" in content
            )
            self.assertTrue(
                desc_ok,
                f"{skill}/SKILL.md description must start with 'Use when'",
            )
            self.assertNotIn("—", content, f"{skill}/SKILL.md contains em dash")
            self.assertNotIn("–", content, f"{skill}/SKILL.md contains en dash")


def _verify_single_skill(test_case, skill):
    skill_path = os.path.join(SKILLS_DIR, skill, "SKILL.md")
    test_case.assertTrue(
        os.path.exists(skill_path),
        f"Missing skill file: {skill_path}",
    )
    for ref in REQUIRED_REFERENCES.get(skill, []):
        ref_path = os.path.join(SKILLS_DIR, skill, ref)
        test_case.assertTrue(
            os.path.exists(ref_path),
            f"Reference missing in {skill}: {ref_path}",
        )
    with open(skill_path, "r", encoding="utf-8") as f:
        content = f.read()
        lines = content.splitlines()

    test_case.assertLessEqual(
        len(lines),
        250,
        f"{skill}/SKILL.md exceeds 250 lines ({len(lines)})",
    )
    test_case.assertTrue(
        content.startswith("---\n"),
        f"{skill}/SKILL.md missing frontmatter start",
    )
    test_case.assertIn(
        f"name: {skill}",
        content,
        f"{skill}/SKILL.md missing matching name",
    )
    desc_ok = (
        "description: Use when" in content
        or "description: >\n  Use when" in content
        or "description: |" in content
    )
    test_case.assertTrue(
        desc_ok,
        f"{skill}/SKILL.md description must start with 'Use when'",
    )
    test_case.assertNotIn("—", content, f"{skill}/SKILL.md contains em dash")
    test_case.assertNotIn("–", content, f"{skill}/SKILL.md contains en dash")


if "-k" in sys.argv:
    class TestIndividualSkills(unittest.TestCase):
        """Per-skill targeted test cases for filtering via -k flag."""

    for skill in TARGET_SKILLS:
        def _make_test(s):
            return lambda self: _verify_single_skill(self, s)

        setattr(TestIndividualSkills, f"test_skill_{skill}", _make_test(skill))
        setattr(
            TestIndividualSkills,
            "test_skill_" + skill.replace("-", "_"),
            _make_test(skill),
        )


if __name__ == "__main__":
    has_k = "-k" in sys.argv
    has_explicit_test = any(
        arg.startswith("Test") or arg.startswith("test_")
        for arg in sys.argv[1:]
    )
    if not has_k and not has_explicit_test:
        unittest.main(defaultTest="TestConsolidation")
    else:
        unittest.main()
