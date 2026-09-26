# Agent skills collection

A collection of modular skills for AI coding agents, designed according to the open Agent Skills Specification (`agentskills.io`).

## Overview

Each skill encapsulates an engineering workflow, procedure, or design standard into an isolated folder containing a `SKILL.md` entrypoint. The skills run directly across modern coding assistants including Google Antigravity, Claude Code, and Cursor.

## Installation and usage

### Option 1. Global setup via symbolic links

To make these skills globally available across your local agent sessions, link the `skills` directory to your target agent configuration path.

For Google Antigravity.
```bash
ln -sfn /path/to/agent-skills/skills/* ~/.gemini/config/skills/
```

For Claude Code.
```bash
ln -sfn /path/to/agent-skills/skills/* ~/.claude/skills/
```

For Generic Agents.
```bash
ln -sfn /path/to/agent-skills/skills/* ~/.agents/skills/
```

### Option 2. Project-level installation

Copy individual skill folders directly into your active project workspace.
```bash
mkdir -p .gemini/skills
cp -r /path/to/agent-skills/skills/<skill-name> .gemini/skills/
```

### Option 3. Direct agent prompt

Point your agent directly to a skill folder or file path.
```text
Load and follow the workflow in skills/brainstorming/SKILL.md
```

## Skills catalog

| Skill | Purpose and trigger context |
|---|---|
| `brainstorming` | Use when scoping new features, exploring architectural requirements, planning refactors, stress-testing design decisions, or designing greenfield components before writing implementation plans or code. |
| `code-review` | Use when requesting review for code changes, evaluating review feedback, pushing back against incorrect suggestions, or verifying review fixes. |
| `codebase-design` | Use when designing module interfaces, evaluating abstraction depth, identifying code seams, or turning shallow pass-through wrappers into deep modules. |
| `conventional-commit` | Use when creating atomic git commits adhering to the Conventional Commits specification, staging selective hunks, resolving merge conflicts, or writing commit messages. |
| `copy-web-design` | Use when reverse-engineering, deconstructing, benchmarking, or replicating web designs, design tokens, layout structures, animations, or components from URLs or screenshots. |
| `executing-plans` | Use when executing written implementation plans batch by batch inline in the current session, or task by task via parallel subagents and delegated review gates. |
| `frontend-design` | Use when building frontend interfaces, styling layouts with Tailwind CSS, establishing visual tokens, generating DESIGN.md, or selecting UI libraries. |
| `i18n` | Use when implementing internationalization, localization, locale negotiation, date/number formatting, ICU messages, or RTL/BiDi layouts. |
| `laravel` | Use when building, modifying, reviewing, testing, or debugging Laravel applications, Eloquent queries, Artisan commands, Blade or Livewire components, Inertia adapters, Form Requests, migrations, or queue jobs. |
| `prototype` | Use when prototyping divergent visual or interaction variants for a UI component, or comparing interactive UI explorations. |
| `react` | Use when designing, building, testing, or optimizing React and Next.js applications, Server Components, client state, or data fetching. |
| `s13n` | Use when standardizing inconsistent code patterns across a repository, resolving architectural divergence, or installing linter guards. |
| `security-audit` | Use when auditing codebases for security vulnerabilities, conducting threat modeling, reviewing auth boundaries, evaluating exploitability, or verifying security fixes. |
| `summarize` | Use when generating structured session execution summaries, documenting root causes, evidence tables, or transferring context between agent sessions. |
| `systematic-debugging` | Use when debugging any bug, test failure, unexpected behavior, or performance issue before proposing fixes. |
| `technical-writing` | Use when writing or reviewing human-facing documentation, RFCs, README files, PR descriptions, or technical guides. |
| `testing-patterns` | Use when writing automated tests, creating test fixtures, designing test matrices and exploratory charters, configuring test mocks, or refactoring test suites. |
| `ui-motion` | Use when authoring UI animations, micro-interactions, spring physics, or auditing codebase motion performance. |
| `ui-ux-review` | Use when auditing user interfaces and user experience, web accessibility standards, CSS layout architecture, cognitive friction, or design token compliance. |
| `unslop` | Use when drafting prose, reviewing text for AI patterns, editing documentation, rewriting generic AI output, or cutting LLM writing habits. |
| `upsert-codebase-docs` | Use when creating or updating AGENTS.md and CODEBASE.md documentation files for a project, auditing documentation drift against git changes, or bootstrapping agent instructions for new repositories. |
| `verification-before-completion` | Use when about to claim work is complete, fixed, or passing, before committing or creating PRs, requiring fresh verification command output or automated Lighthouse audits before making assertions. |
| `workspace-onboarding` | Use when starting a new conversation, initializing work on a project, or onboarding to an unfamiliar workspace to discover the active stack, load rules, and establish execution constraints. |
| `writing-for-agents` | Use when drafting or editing agent instructions, AGENTS.md, CLAUDE.md, prompt runbooks, context pointers, or skill documentation. |
| `writing-plans` | Use when creating phased implementation plans with test-first tasks from a design specification before writing code. |

## Contributing

To contribute a new skill.
1. Create a new directory inside `skills/<skill-name>/` using kebab-case naming.
2. Add a `SKILL.md` file with valid YAML frontmatter containing `name` and `description`.
3. Keep supporting documentation inside `references/` and helper scripts inside `scripts/`.
4. Ensure all internal references use relative paths.
5. Push changes to open a pull request and verify that the GitHub Actions validation check passes.

## License

MIT
