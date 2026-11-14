# Agent Instructions (Agent Skills Repository)

## Project context
Agent skills repository containing 37 modular capabilities adhering to the AgentSkills specification.
Target environment: macOS Darwin, zsh 5.9, Python 3.14+, BSD userland. Timezone: Asia/Jakarta.

## Documentation map
- `CODEBASE.md`, deep technical reference on architecture, directory layout, and validation contracts.
- `GLOSSARY.md`, canonical definitions for skill concepts, rubric dimensions, and linter rules.
- `skills/review-a-skill/SKILL.md`, audit rubric, anti-pattern rules, and evaluation workflow.

## Commands cheatsheet
```bash
python3 skills/review-a-skill/scripts/lint_skill.py --self-test   # Run linter fixture self-tests
python3 skills/review-a-skill/scripts/lint_skill.py --all          # Lint all skills in repository
python3 skills/review-a-skill/scripts/lint_skill.py <skill-name>   # Lint a specific skill
python3 scripts/verify_skills.py --all                             # Run verification shim
python3 skills/unslop/tests/test_unslop.py                         # Run unslop unit tests
```

## Critical rules (READ FIRST)
1. Maintain main `SKILL.md` length strictly at most 250 lines (`<= 250`); move extensive documentation into `references/`.
2. Format frontmatter descriptions with positive triggers (`Use when`), negative exclusions (`Don't use for`), and keep length at most 500 characters.
3. Keep anti-pattern tables strictly to the 5-column schema (`ID | Title | Pattern description | Why it fails | Concrete fix`) across all rows.
4. Separate validator script edits from `SKILL.md` edits into decoupled commits to honor the Validator Independence Rule.
5. Pair every negative prohibition with an explicit positive alternative action.
6. Verify all changes through live terminal commands before declaring work complete.

## Non-default conventions
- Operational skills declare explicit `## Modes` before Step 1.
- Every skill includes `<HARD-GATE>` boundaries and `## Boundary isolation` sections.
- Completion criteria terminate on checkable binary artifacts, exit codes, or commit hashes.
- Prose adheres strictly to unslop guidelines (zero em dashes, zero en dashes, no mid-sentence colons, and direct verbs).

## Git workflow and definition of done
- Active working branch is `main`.
- Format commits following Conventional Commits 1.0.0 (`feat`, `fix`, `refactor`, `test`, `docs`, `chore`).
- Stage files selectively with `git add <file>`; never use `git commit -a` or `git add .`.
- Definition of Done:
  1. `python3 skills/review-a-skill/scripts/lint_skill.py --self-test` exits 0.
  2. `python3 skills/review-a-skill/scripts/lint_skill.py --all` passes all targets with 0 errors.
  3. `git diff` contains zero unintended file modifications or staged credentials.
