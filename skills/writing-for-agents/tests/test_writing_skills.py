import os
import re
import unittest

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILL_MD = os.path.join(SKILL_DIR, "SKILL.md")
REFERENCES_DIR = os.path.join(SKILL_DIR, "references")

BANNED_WORDS = [
    "additionally", "crucial", "delve", "enduring", "enhance", "fostering",
    "garner", "interplay", "intricate", "pivotal", "showcase",
    "tapestry", "testament", "underscore", "vibrant"
]

class TestWritingSkillsCompliance(unittest.TestCase):
    def setUp(self):
        self.assertTrue(os.path.exists(SKILL_MD), f"SKILL.md must exist at {SKILL_MD}")
        with open(SKILL_MD, "r", encoding="utf-8") as f:
            self.content = f.read()

    def test_frontmatter(self):
        match = re.match(r"^---\n(.*?)\n---\n", self.content, re.DOTALL)
        self.assertIsNotNone(match, "Frontmatter must be present")
        fm = match.group(1)
        self.assertIn("name: writing-skills", fm)
        self.assertTrue(re.search(r"description:\s+Use when", fm), "Description must start with 'Use when'")

    def test_no_em_or_en_dashes(self):
        self.assertNotIn("\u2014", self.content, "Em dashes (\u2014) are banned")
        self.assertNotIn("\u2013", self.content, "En dashes (\u2013) are banned")

    def test_no_decorative_emojis(self):
        self.assertNotIn("❌", self.content)
        self.assertNotIn("✅", self.content)

    def test_no_banned_ai_words(self):
        lower_content = self.content.lower()
        for word in BANNED_WORDS:
            pattern = rf"\b{word}\b"
            matches = re.findall(pattern, lower_content)
            self.assertEqual(len(matches), 0, f"Banned AI word found in SKILL.md: {word}")

    def test_conciseness_and_sprawl(self):
        lines = self.content.splitlines()
        self.assertLess(len(lines), 250, f"SKILL.md sprawls: {len(lines)} lines (must be < 250)")

    def test_binary_completion_criteria(self):
        self.assertIn("Completion criterion.", self.content)

    def test_references_unslop_compliance(self):
        self.assertTrue(os.path.isdir(REFERENCES_DIR), "references/ directory must exist")
        ref_files = [f for f in os.listdir(REFERENCES_DIR) if f.endswith(".md")]
        self.assertGreater(len(ref_files), 0, "At least one reference file must exist")

        for fname in ref_files:
            fpath = os.path.join(REFERENCES_DIR, fname)
            with open(fpath, "r", encoding="utf-8") as f:
                ref_content = f.read()
            self.assertNotIn("\u2014", ref_content, f"Em dash found in {fname}")
            self.assertNotIn("\u2013", ref_content, f"En dash found in {fname}")
            self.assertNotIn("❌", ref_content, f"Emoji found in {fname}")
            self.assertNotIn("✅", ref_content, f"Emoji found in {fname}")
            lower_ref = ref_content.lower()
            for word in BANNED_WORDS:
                pattern = rf"\b{word}\b"
                matches = re.findall(pattern, lower_ref)
                self.assertEqual(len(matches), 0, f"Banned AI word '{word}' found in {fname}")

    def test_legacy_files_removed(self):
        banned_legacy_files = [
            "persuasion-principles.md",
            "testing-skills-with-subagents.md",
            "render-graphs.js",
            "graphviz-conventions.dot"
        ]
        for legacy in banned_legacy_files:
            legacy_path = os.path.join(SKILL_DIR, legacy)
            self.assertFalse(os.path.exists(legacy_path), f"Legacy file must be removed: {legacy}")

if __name__ == "__main__":
    unittest.main()
