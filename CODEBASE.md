# Agent Skills Codebase Reference

Deep factual reference for AI agents and developers. **Last verified: 2026-11-14.**
If you modify skills, validators, or schemas documented here, update this file in the same change.
Consult [`AGENTS.md`](./AGENTS.md) for working instructions and operational boundaries.

> If this file is older than 4 weeks, verify skills and linter rules against `skills/` and `skills/review-a-skill/scripts/lint_skill.py` before trusting it.

<!-- BEGIN AUTO GENERATED: STACK_MATRIX -->
| Layer | Technology | Details |
|---|---|---|
| Specification | AgentSkills Standard | Markdown SKILL.md files, strict 250-line budget |
| Language | Python 3.14+, Bash | BSD userland, zsh 5.9 compatibility |
| Linter Engine | lint_skill.py | AST and markdown token parser, R9 and R13 enforcement |
| Commit Policy | Conventional Commits 1.0.0 | Atomic commits, Validator Independence Rule |
<!-- END AUTO GENERATED: STACK_MATRIX -->

## Architecture data flow

Lifecycle of a skill invocation and verification pass:

```text
User Request / Task Instruction
  → Frontmatter Routing (Match "Use when", avoid "Don't use for")
  → Skill Entrypoint (skills/<name>/SKILL.md)
      → <HARD-GATE> verification (Enforce write boundaries before mutation)
      → Mode Declaration (Select deterministic mode branch)
      → Sequential Steps (Steps 1 to N, reading references/ as needed)
      → Step Termination (Binary completion criteria verification)
  → Automated Quality Gates
      → lint_skill.py --self-test (Verify fixture integrity)
      → lint_skill.py --all (Contract, boundary, and punctuation audit)
      → git commit (Pre-commit hook enforces validator independence)
  → Verified State Artifact / Git Commit
```

## Annotated directory layout

```text
skills/
├── agent-planning/                # Multi-task execution planning and plan auditing
├── brainstorming/                 # Greenfield design and architectural exploration
├── code-review/                   # Dual-axis review and adversarial critique
├── conventional-commit/           # Atomic git commit generation and formatting
├── review-a-skill/                # Quality audit engine and dimensional rubric
│   └── scripts/                   # Canonical linter (lint_skill.py) and fixtures
├── unslop/                        # AI pattern stripper and register policy
├── web-advisor-prompt/            # Frontier model packaging and ingestion audit
└── ...                            # 37 total modular domain skills
scripts/
├── verify_skills.py               # Delegator shim forwarding to lint_skill.py
└── audit-docs.mjs                 # Documentation integrity scanner
docs/                              # Architecture decision records and benchmark reports
.agents/
└── state/                         # Transient execution state per skill workflow
```

<!-- BEGIN AUTO GENERATED: DATABASE_SCHEMA -->
## Specification source of truth and introspection

Schema source of truth:
- Canonical Skill schema: `skills/review-a-skill/SKILL.md` (Dimensional evaluation rubric)
- Canonical Linter: `skills/review-a-skill/scripts/lint_skill.py`
- Pre-commit Hook: `skills/review-a-skill/scripts/pre-commit-check.sh`
- Anti-Slop Rules: `anti-slop-rules.yaml` and `skills/unslop/SKILL.md`

Introspection commands:
- Lint all skills: `python3 skills/review-a-skill/scripts/lint_skill.py --all`
- Output JSON metrics: `python3 skills/review-a-skill/scripts/lint_skill.py --all --json`
- Inspect line counts: `wc -l skills/*/SKILL.md`
<!-- END AUTO GENERATED: DATABASE_SCHEMA -->

<!-- BEGIN AUTO GENERATED: ROUTING_MATRIX -->
## Routing entrypoints and dispatch index

Skill entrypoints:
- Skill catalog: `skills/*/SKILL.md`
- Active distribution list: `scripts/verify_skills.py` (37 registered skills)

Discovery commands:
- List all active skills: `ls -d skills/*/`
- Check skill frontmatter: `head -n 5 skills/*/SKILL.md`
<!-- END AUTO GENERATED: ROUTING_MATRIX -->
