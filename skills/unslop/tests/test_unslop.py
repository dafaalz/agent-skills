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

class TestUnslopCompliance(unittest.TestCase):
    def setUp(self):
        self.assertTrue(os.path.exists(SKILL_MD), f"SKILL.md must exist at {SKILL_MD}")
        with open(SKILL_MD, "r", encoding="utf-8") as f:
            self.content = f.read()

    def test_frontmatter(self):
        match = re.match(r"^---\n(.*?)\n---\n", self.content, re.DOTALL)
        self.assertIsNotNone(match, "Frontmatter must be present")
        fm = match.group(1)
        self.assertIn("name: unslop", fm)
        self.assertTrue(re.search(r"description:\s+Use when", fm), "Description must start with 'Use when'")
        desc_match = re.search(r"description:\s+(.*)", fm)
        self.assertIsNotNone(desc_match)
        self.assertLess(len(desc_match.group(1)), 500, "Description must be under 500 characters")

    def test_no_em_or_en_dashes(self):
        self.assertNotIn("\u2014", self.content, "Em dashes (\u2014) are banned in SKILL.md")
        self.assertNotIn("\u2013", self.content, "En dashes (\u2013) are banned in SKILL.md")

    def test_no_decorative_emojis(self):
        emojis = ["❌", "✅", "🚀", "💡", "⚠️", "📌"]
        for emoji in emojis:
            self.assertNotIn(emoji, self.content, f"Emoji {emoji} found in SKILL.md")

    def test_conciseness_and_sprawl(self):
        lines = self.content.splitlines()
        self.assertLess(len(lines), 250, f"SKILL.md sprawls: {len(lines)} lines (must be < 250)")

    def test_binary_completion_criteria(self):
        steps = re.findall(r"### Step \d+\..*?(?=### Step|\n## |\Z)", self.content, re.DOTALL)
        self.assertGreater(len(steps), 0, "Steps must be present")
        for step in steps:
            self.assertIn("Completion criterion.", step, "Every step must have a binary completion criterion")

    def test_references_directory_and_compliance(self):
        self.assertTrue(os.path.isdir(REFERENCES_DIR), "references/ directory must exist")
        indonesian_ref = os.path.join(REFERENCES_DIR, "indonesian-patterns.md")
        self.assertTrue(os.path.exists(indonesian_ref), "indonesian-patterns.md must exist")

        with open(indonesian_ref, "r", encoding="utf-8") as f:
            ref_content = f.read()

        self.assertNotIn("\u2014", ref_content, "Em dash found in indonesian-patterns.md")
        self.assertNotIn("\u2013", ref_content, "En dash found in indonesian-patterns.md")

        emojis = ["❌", "✅", "🚀", "💡", "⚠️", "📌"]
        for emoji in emojis:
            self.assertNotIn(emoji, ref_content, f"Emoji {emoji} found in indonesian-patterns.md")

    def test_sentence_case_headings(self):
        allowed_proper_nouns = {
            "ai", "api", "jwt", "skill.md", "step", "indonesia", "unslop", "chatgpt", "gemini"
        }
        files_to_check = [SKILL_MD]
        if os.path.isdir(REFERENCES_DIR):
            for fname in os.listdir(REFERENCES_DIR):
                if fname.endswith(".md"):
                    files_to_check.append(os.path.join(REFERENCES_DIR, fname))

        for fpath in files_to_check:
            with open(fpath, "r", encoding="utf-8") as f:
                for line_idx, line in enumerate(f, 1):
                    if line.startswith("#"):
                        heading_text = line.lstrip("#").strip()
                        # Ignore leading numbering like "1. ", "Step 1. ", "Contoh 1. "
                        cleaned = re.sub(r"^(Step\s+\d+\.|Contoh\s+\d+\.|\d+\.)\s*", "", heading_text, flags=re.IGNORECASE)
                        words = [w.strip("(),.:'\"") for w in cleaned.split() if w.strip("(),.:'\"")]
                        if len(words) > 1:
                            for word in words[1:]:
                                if word.isupper() and len(word) > 1:
                                    continue
                                if word.lower() in allowed_proper_nouns:
                                    continue
                                if "/" in word:
                                    subwords = word.split("/")
                                    if all(sw.islower() or sw.lower() in allowed_proper_nouns for sw in subwords):
                                        continue
                                self.assertFalse(
                                    word[0].isupper(),
                                    f"Heading in {os.path.basename(fpath)}:{line_idx} violates sentence case: '{heading_text}' (word '{word}')"
                                )

    def test_no_pseudo_labels(self):
        banned_pseudo_labels = ["Draf AI:", "Hasil Unslop:", "Note:", "Catatan:", "Summary:", "Ringkasan:", "Keterangan:"]
        files_to_check = [SKILL_MD]
        if os.path.isdir(REFERENCES_DIR):
            for fname in os.listdir(REFERENCES_DIR):
                if fname.endswith(".md"):
                    files_to_check.append(os.path.join(REFERENCES_DIR, fname))

        for fpath in files_to_check:
            with open(fpath, "r", encoding="utf-8") as f:
                for line_idx, line in enumerate(f, 1):
                    for label in banned_pseudo_labels:
                        self.assertNotIn(
                            label, line,
                            f"Pseudo-label '{label}' found in {os.path.basename(fpath)}:{line_idx}"
                        )

    def test_no_banned_puffery_in_reference_instructional_prose(self):
        indonesian_ref = os.path.join(REFERENCES_DIR, "indonesian-patterns.md")
        with open(indonesian_ref, "r", encoding="utf-8") as f:
            lines = f.readlines()

        for idx, line in enumerate(lines[:34], 1):
            self.assertNotIn("panduan komprehensif", line.lower(), f"Banned puffery found at line {idx}")

    def test_indonesian_pattern_categories(self):
        indonesian_ref = os.path.join(REFERENCES_DIR, "indonesian-patterns.md")
        with open(indonesian_ref, "r", encoding="utf-8") as f:
            content = f.read()

        expected_categories = [
            "1. Frasa pembuka dan penutup basa-basi",
            "2. Konjungsi transisi robotik dan interferensi asing (calque)",
            "3. Kata sifat dan pengisi abstrak (puffery)",
            "4. Pleonasme dan perangkai mubazir",
            "5. Pola formulaik simetris dan triadik",
            "6. Nominalisasi berlebih dan verba pelemah",
        ]
        for category in expected_categories:
            self.assertIn(category, content, f"Missing Indonesian pattern category: {category}")

    def test_indonesian_repaired_examples_cleanliness(self):
        indonesian_ref = os.path.join(REFERENCES_DIR, "indonesian-patterns.md")
        with open(indonesian_ref, "r", encoding="utf-8") as f:
            content = f.read()

        repaired_blocks = re.findall(r"#### Naskah hasil perbaikan\n\n(.*?)(?=\n###|\n## |\Z)", content, re.DOTALL)
        self.assertGreater(len(repaired_blocks), 0, "Repaired examples must exist")

        banned_in_repaired = [
            "di mana", "yang mana", "memainkan peran penting", "dalam lanskap",
            "sebuah bukti nyata", "menyelami lebih dalam", "tidak hanya",
            "bukan sekadar", "perlu diingat", "tentu saja", "semoga membantu",
            "secara keseluruhan", "mulus tanpa hambatan", "guna untuk"
        ]
        for block in repaired_blocks:
            lower_block = block.lower()
            for pattern in banned_in_repaired:
                self.assertNotIn(
                    pattern, lower_block,
                    f"Banned pattern '{pattern}' found in repaired example block:\n{block}"
                )

if __name__ == "__main__":
    unittest.main()
