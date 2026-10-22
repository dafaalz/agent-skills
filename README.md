# Agent skills collection

A collection of 35 modular skills for AI coding agents. Each skill follows the open Agent Skills Specification (`agentskills.io`).

## Overview

Each skill packages an engineering procedure or design standard into an isolated directory that contains a `SKILL.md` entrypoint. The skills run directly across coding assistants such as Google Antigravity, Claude Code, and Cursor.

## Installation and usage

### Option 1. Global setup with symbolic links

To make these skills available across local sessions, link the `skills` directory to your agent configuration path.

For Google Antigravity:
```bash
ln -sfn /path/to/agent-skills/skills/* ~/.gemini/config/skills/
```

For Claude Code:
```bash
ln -sfn /path/to/agent-skills/skills/* ~/.claude/skills/
```

For generic agents:
```bash
ln -sfn /path/to/agent-skills/skills/* ~/.agents/skills/
```

### Option 2. Project-level installation

To install a skill in your active project, copy the skill directory into your project workspace:
```bash
mkdir -p .gemini/skills
cp -r /path/to/agent-skills/skills/<skill-name> .gemini/skills/
```

### Option 3. Direct agent prompt

To run a skill directly, provide the skill path to your agent:
```text
Load and follow the workflow in skills/brainstorming/SKILL.md
```

## Skills catalog

The repository provides 35 verified skills:

| Skill | Purpose and trigger context |
|---|---|
| `agent-planning` | Author multi-task execution plans, enforce empirical verification evidence, audit readiness checklists, and respond to audit reviews with bidirectional discipline. |
| `brainstorming` | Scope new features, explore architectural requirements, plan refactors, or design greenfield components before you write code. |
| `code-review` | Request reviews for code changes, evaluate review feedback, push back against incorrect suggestions, or verify review fixes. |
| `codebase-design` | Design module interfaces, evaluate abstraction depth, identify code seams, or turn shallow wrappers into deep modules. |
| `conventional-commit` | Create atomic git commits that adhere to Conventional Commits, stage selective hunks, or write commit messages. |
| `copy-web-design` | Reverse-engineer, deconstruct, benchmark, or replicate web designs, tokens, layout structures, and animations. |
| `executing-plans` | Execute written implementation plans batch by batch inline or task by task via delegated subagents. |
| `frontend-design` | Build frontend interfaces, style layouts with Tailwind CSS, establish visual tokens, and create DESIGN.md files. |
| `i18n` | Implement internationalization, localization, locale negotiation, date and number formats, ICU messages, and RTL layouts. |
| `laravel` | Build, modify, review, test, or debug Laravel applications, Eloquent queries, Artisan commands, and queue jobs. |
| `prototype` | Prototype divergent visual or interaction variants for a UI component, or compare interactive UI explorations. |
| `pull-request` | Draft structured pull request descriptions with visual summaries, before-and-after verification evidence, and merge-danger risk assessments. |
| `react` | Audit, profile, and optimize React and Next.js performance, waterfalls, bundle size, Server Components, and re-renders. |
| `recursive-research` | Research a topic to expert depth, tier sources by reliability, and map state of the art before a spec or plan. |
| `reflect-to-skill` | Reflect on conversation sessions, analyze failure modes, and graft preventive rules into agent skills to prevent recurrence. |
| `review-a-skill` | Review, audit, benchmark, or compare agent skills against AgentSkills specifications and structural guidelines. |
| `s13n` | Standardize inconsistent code patterns across a repository, resolve architectural divergence, or install linter guards. |
| `schema-migration` | Author, review, test, and execute zero-downtime database schema migrations, column renames, and batched backfills. |
| `security-audit` | Audit codebases for security vulnerabilities, conduct threat modeling, review auth boundaries, and evaluate exploitability. |
| `skill-testing` | Empirically benchmark and refine agent skills through parallel subagents and human evaluation. |
| `summarize` | Generate structured session execution summaries, root cause documentation, evidence tables, and session handoffs. |
| `systematic-debugging` | Debug bugs, test failures, unexpected behaviors, and performance regressions before you propose fixes. |
| `technical-writing` | Write or review human-facing documentation, RFCs, README files, PR descriptions, and technical guides. |
| `testing-patterns` | Write automated tests, create test fixtures, configure test mocks and containers, and implement contract tests. |
| `ui-motion` | Add interface animations, gestures, spring physics, and audit motion performance across application routes. |
| `ui-ux-review` | Audit user interfaces, user experience, web accessibility standards, CSS layouts, and design token compliance. |
| `unslop` | Review text for AI patterns, edit documentation, rewrite generic AI text, and cut LLM writing habits. |
| `upsert-codebase-docs` | Create and update AGENTS.md and CODEBASE.md documentation files, or audit documentation drift against git changes. |
| `verification-before-completion` | Validate work through fresh command execution, scoped lint checks, and test outputs before you claim completion. |
| `vibe-wise` | Design system architectures, model relational data, plan API boundaries, and learn while you build features. |
| `web-advisor-prompt` | Package repository context and architectural trade-offs into an adversarial prompt for an external frontier reasoning model. |
| `wizard` | Generate self-contained interactive terminal scripts that guide humans through manual setup, credential provisioning, or production cutovers. |
| `workspace-onboarding` | Initialize work on a project, discover the active technology stack, and establish execution constraints. |
| `writing-for-agents` | Draft and edit agent instructions, AGENTS.md, prompt runbooks, context pointers, design specs, and skill files. |
| `writing-plans` | Create phased implementation plans with test-first tasks from a design specification before you write code. |

## Verification

The repository contains an automated verification script and an AST linter to validate every skill:

```bash
# Run the structural contract verification harness
python3 scripts/verify_skills.py --all

# Run the AST and linguistic linter
python3 skills/review-a-skill/scripts/lint_skill.py --all
```

## Contributing

Follow these steps to contribute a new skill:
1. Create a directory inside `skills/<skill-name>/` with kebab-case naming.
2. Add a `SKILL.md` file with YAML frontmatter that contains `name` and `description`.
3. Put reference documentation inside `references/` and executable helper scripts inside `scripts/`.
4. Make sure that internal reference links point directly to local files.
5. Run `python3 scripts/verify_skills.py --all` to make sure all verification checks pass.
6. Push changes to open a pull request.

## License

MIT
