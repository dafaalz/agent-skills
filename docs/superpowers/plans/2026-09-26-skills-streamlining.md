# Skills Streamlining Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use subagent-driven-development (recommended) or executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Streamline custom skills from 31 to 25 by absorbing overlapping workflows, removing dead tools, and updating test validation.

**Architecture:** Adopt test-driven consolidation by updating `tests/test_consolidation.py` to assert the final 25 skills and four modular references, creating target references in recipient skills, archiving dead tools and tooling directories, and syncing user documentation.

**Tech Stack:** Python 3, unittest, Markdown, JSON, Git, Bash.

---

### Task 1: Update Test Suite to Assert 25 Skills (TDD Failing Test)

**Files:**
- Modify: `tests/test_consolidation.py`

- [x] **Step 1: Update test_consolidation.py with final 25 skills and new references**

```python
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


if __name__ == "__main__":
    unittest.main()
```

- [x] **Step 2: Run test suite to verify failure**

Run: `python3 -m unittest discover -s tests/`
Expected: FAIL with `Active skills mismatch` or `Deprecated skills still present`.

---

### Task 2: Create Target References and Update Recipient Skills

**Files:**
- Create: `skills/conventional-commit/references/resolving-conflicts.md`
- Create: `skills/executing-plans/references/parallel-dispatch.md`
- Create: `skills/testing-patterns/references/test-matrix-and-charters.md`
- Create: `skills/verification-before-completion/references/lighthouse-ci.md`
- Modify: `skills/conventional-commit/SKILL.md`
- Modify: `skills/executing-plans/SKILL.md`
- Modify: `skills/testing-patterns/SKILL.md`
- Modify: `skills/verification-before-completion/SKILL.md`

- [x] **Step 1: Write resolving-conflicts.md in conventional-commit**

Copy and sanitize conflict resolution procedures into `skills/conventional-commit/references/resolving-conflicts.md`.

- [x] **Step 2: Write parallel-dispatch.md in executing-plans**

Structure task partitioning, prompt templates, and isolated subagent boundaries in `skills/executing-plans/references/parallel-dispatch.md`.

- [x] **Step 3: Write test-matrix-and-charters.md in testing-patterns**

Structure equivalence partitioning, boundary value analysis, and exploratory testing charters in `skills/testing-patterns/references/test-matrix-and-charters.md`.

- [x] **Step 4: Write lighthouse-ci.md in verification-before-completion**

Move and adapt automated audit assertions into `skills/verification-before-completion/references/lighthouse-ci.md`.

- [x] **Step 5: Update recipient SKILL.md files to point to new references**

Update descriptions or workflows in `conventional-commit/SKILL.md`, `executing-plans/SKILL.md`, `testing-patterns/SKILL.md`, and `verification-before-completion/SKILL.md`.

---

### Task 3: Move Deprecated Skills to Archive and Clean MCP Tooling

**Files:**
- Move: `skills/graphify` to `skills_archive/graphify`
- Move: `skills/output-skill` to `skills_archive/output-skill`
- Move: `skills/finishing-a-development-branch` to `skills_archive/finishing-a-development-branch`
- Move: `skills/ping` to `skills_archive/ping`
- Move: `skills/dispatching-parallel-agents` to `skills_archive/dispatching-parallel-agents`
- Move: `skills/qa-engineer` to `skills_archive/qa-engineer`
- Delete: `/Users/groundfox/.gemini/antigravity/mcp/graphify`
- Modify: `/Users/groundfox/.gemini/config/config.json`

- [x] **Step 1: Move six skills to skills_archive**

Run relocation commands for the six target folders.

- [x] **Step 2: Remove Graphify MCP server directory**

Remove `/Users/groundfox/.gemini/antigravity/mcp/graphify`.

- [x] **Step 3: Remove command(graphify) permission from config.json**

Remove line containing `"command(graphify)",` in `/Users/groundfox/.gemini/config/config.json` while keeping JSON syntax valid.

---

### Task 4: Verify Test Suite Passes

**Files:**
- Verify: `tests/test_consolidation.py`

- [x] **Step 1: Execute test suite**

Run: `python3 -m unittest discover -s tests/`
Expected: PASS with 3 tests OK in under 0.05s.

---

### Task 5: Synchronize Documentation

**Files:**
- Modify: `README.md`
- Modify: `USAGE.md`

- [x] **Step 1: Update README.md catalog to list exactly 25 skills**

Remove archived skills from the markdown table.

- [x] **Step 2: Update USAGE.md catalog and workflows**

Remove deleted skill rows and document absorbed workflows under `executing-plans`, `conventional-commit`, and `testing-patterns`.

---

### Task 6: Commit Changes

- [x] **Step 1: Verify git status is clean and structured**

Run: `git status --short`

- [x] **Step 2: Commit atomic changes using single-line messages**

Create oneline commits adhering to conventional commits specification without commit bodies.
