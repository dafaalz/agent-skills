# Agent Skills Collection

A curated collection of modular skills for AI coding agents, designed according to the open Agent Skills Specification (`agentskills.io`).

## Overview

Each skill encapsulates a proven engineering workflow, procedure, or design standard into an isolated folder containing a `SKILL.md` entrypoint. The skills run directly across modern coding assistants including Google Antigravity, Claude Code, and Cursor.

## Installation and Usage

### Option 1: Global setup via symbolic links

To make these skills globally available across your local agent sessions, link the `skills` directory to your target agent configuration path:

For Google Antigravity:
```bash
ln -sfn /path/to/agent-skills/skills/* ~/.gemini/config/skills/
```

For Claude Code:
```bash
ln -sfn /path/to/agent-skills/skills/* ~/.claude/skills/
```

For Generic Agents:
```bash
ln -sfn /path/to/agent-skills/skills/* ~/.agents/skills/
```

### Option 2: Project-level installation

Copy individual skill folders directly into your active project workspace:
```bash
mkdir -p .gemini/skills
cp -r /path/to/agent-skills/skills/<skill-name> .gemini/skills/
```

### Option 3: Direct agent prompt

Point your agent directly to a skill folder or file URL:
```text
Load and follow the workflow in skills/brainstorming/SKILL.md
```

## Skills Catalog

| Skill | Purpose and Trigger Context |
|---|---|
| `brainstorming` | Use when scoping new features, exploring architectural requirements, planning refactors, stress-testing design decisions, or designing greenfield components before writing implementation plans or code. |
| `build-awwwards-quality-sites` | Use when building, art-directing, or auditing motion-heavy marketing sites, interactive portfolios, GSAP or Three.js WebGL scenes, and smooth-scroll interfaces. |
| `dispatching-parallel-agents` | Use when facing two or more independent tasks that can run without shared state or sequential dependencies. |
| `executing-plans` | Execute written implementation plans batch by batch with review checkpoints in the current session. |
| `finishing-a-development-branch` | Use when implementation is complete, all automated tests pass, and the working branch or worktree is ready for integration, pull request creation, or cleanup. |
| `graphify` | Use for questions about a codebase, architecture, file relationships, or project content. Converts code, docs, and diagrams into a persistent knowledge graph. |
| `hallmark` | Anti-AI-slop design skill for greenfield pages, audits, redesigns, and design extraction from URLs or screenshots. |
| `interface-review` | Use when auditing UI implementation quality, CSS architecture, design token compliance, visual hierarchy, web accessibility standards, or frontend code diffs. |
| `output-skill` | Overrides default LLM truncation behavior. Enforces complete code generation, bans placeholder patterns, and handles token-limit splits cleanly. |
| `pick-ui-library` | Use when selecting frontend libraries, choosing UI primitives, picking animation tools, or finding curated component packages for a project. |
| `prototype` | Use when prototyping divergent visual or interaction variants for a UI component, or comparing interactive UI explorations. |
| `qa-engineer` | Use when testing features from a user perspective, executing exploratory test charters, auditing PR diffs, investigating test flakiness, or verifying release quality gates. |
| `receiving-code-review` | Use when receiving code review feedback, before implementing suggestions, requiring technical rigor and verification. |
| `redesign-skill` | Use when auditing or updating an existing website, web app, or frontend UI to replace generic AI patterns, fix typography and layout issues, or improve polish. |
| `requesting-code-review` | Use when completing tasks, implementing major features, or before merging to verify work meets requirements. |
| `security-audit` | Use when auditing codebases for security vulnerabilities, conducting threat modeling, reviewing auth boundaries, evaluating exploitability, or verifying security fixes. |
| `stitch-skill` | Use when generating or reviewing Google Stitch screen designs, crafting DESIGN.md specifications, or translating visual direction into semantic UI constraints. |
| `subagent-driven-development` | Use when executing implementation plans with independent tasks in the current session. |
| `systematic-debugging` | Debug any bug, test failure, unexpected behavior, or performance issue before proposing fixes. |
| `taste-skill` | Use when building frontend interfaces, styling layouts with Tailwind CSS, animating with Framer Motion, or fixing generic AI interface designs. |
| `tdd` | Test-first development using red, green, and vertical slices. |
| `technical-writing` | Use when writing or reviewing human-facing documentation, RFCs, README files, PR descriptions, or technical guides. |
| `testing-patterns` | Use when writing automated tests, creating test fixtures, configuring test mocks or testcontainers, implementing contract tests, or refactoring test suites. |
| `ui-motion` | Master skill for UI animations, micro-interactions, CSS transitions, Apple gesture physics, codebase motion audits, and 60fps performance optimization. |
| `unslop` | Use when drafting prose, reviewing text for AI patterns, editing documentation, rewriting generic AI output, or cutting LLM writing habits. |
| `using-git-worktrees` | Use when starting feature work that needs isolation from current workspace or before executing implementation plans. |
| `using-superpowers` | Use when starting any conversation. Establishes skill discovery and requires Skill tool invocation before any response. |
| `ux-review` | Use when auditing product user experience, task flows, cognitive load, form usability, error resilience, or mobile interaction ergonomics. |
| `verification-before-completion` | Use when about to claim work is complete, fixed, or passing, before committing or creating PRs. Requires evidence before assertions. |
| `writing-for-agents` | Use when drafting or editing agent instructions, AGENTS.md, CLAUDE.md, prompt runbooks, context pointers, or skill documentation. |
| `writing-plans` | Write phased implementation plans with test-first tasks from a spec or design before touching code. |
| `writing-skills` | Use when creating new skills, modifying existing skills, or verifying agent instruction compliance across workspaces. |

## Contributing

To contribute a new skill:
1. Create a new directory inside `skills/<skill-name>/` using kebab-case naming.
2. Add a `SKILL.md` file with valid YAML frontmatter containing `name` and `description`.
3. Keep supporting documentation inside `references/` and helper scripts inside `scripts/`.
4. Ensure all internal references use relative paths.
5. Push changes to open a pull request and verify that the GitHub Actions validation check passes.

## License

MIT
