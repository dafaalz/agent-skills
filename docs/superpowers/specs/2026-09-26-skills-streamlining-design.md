# Architecture Decision Record. Skills Streamlining and Pruning

## Status

Accepted

## Context

The repository currently maintains 31 active skills in `skills/`. While recent consolidation added modular references and distinct capabilities like React best practices and standardization, several skills introduce operational friction, bloat, or redundant definitions:

1. Unused runtime dependencies. The `graphify` skill requires external Python scripts, emits a `graphify-out/` workspace folder, and registers an idle background MCP server that is not utilized during daily development.
2. Passive rule as a skill. The `output-skill` (`full-output-enforcement`) contains only negative behavioral constraints against placeholders like `// TODO`. It does not provide an interactive workflow, so it belongs in global instructions rather than the skill registry.
3. Overlapping agent execution. The `dispatching-parallel-agents` skill duplicates built-in Antigravity subagent mechanics and overlaps with `executing-plans`.
4. Overly rigid git procedures. The `finishing-a-development-branch` skill wraps standard git commands in a verbose checklist, while its conflict resolution guidance is better placed in git commit workflows.
5. Single-purpose diagnostic. The `ping` skill measures shell latency and clock skew, which is a one-off diagnostic rather than an ongoing development workflow.
6. Corporate manual testing versus automation. The `qa-engineer` skill uses manual testing matrices that overlap with automated testing in `testing-patterns` and gate verification in `verification-before-completion`.

The user confirmed the following architectural boundaries:
- Absorb `dispatching-parallel-agents` into `executing-plans` under subagent-driven development.
- Keep `writing-for-agents` standalone to protect Single Responsibility Principle.
- Keep UI cluster skills (`frontend-design`, `ui-motion`, `ui-ux-review`, `copy-web-design`, `prototype`) separate.
- Absorb `qa-engineer` into `testing-patterns` and `verification-before-completion`.
- Retain `laravel` in global skills for low-friction PHP development across MAMP environments.
- Remove `graphify`, `output-skill`, `finishing-a-development-branch`, and `ping`.

## Decision

Execute a coordinated refactor across five areas:

### 1. Remove dead weight skills and tooling

- Move `skills/graphify` to `skills_archive/graphify` or delete it directly.
- Remove the MCP server directory at `/Users/groundfox/.gemini/antigravity/mcp/graphify`.
- Remove the `"command(graphify)"` entry from `/Users/groundfox/.gemini/config/config.json`.
- Move `skills/output-skill` to `skills_archive/output-skill`.
- Move `skills/ping` to `skills_archive/ping`.
- Preserve `skills/finishing-a-development-branch/references/resolving-conflicts.md` by transferring it to `skills/conventional-commit/references/resolving-conflicts.md`, then move `skills/finishing-a-development-branch` to `skills_archive/finishing-a-development-branch`.

### 2. Absorb dispatching parallel agents into executing plans

- Create `skills/executing-plans/references/parallel-dispatch.md` containing task partitioning logic, independent domain rules, and subagent prompt templates.
- Update `skills/executing-plans/SKILL.md` to reference `references/parallel-dispatch.md` during subagent-driven execution.
- Move `skills/dispatching-parallel-agents` to `skills_archive/dispatching-parallel-agents`.

### 3. Absorb QA engineer into testing patterns and verification

- Create `skills/testing-patterns/references/test-matrix-and-charters.md` capturing equivalence partitioning, boundary value analysis, and exploratory testing charters.
- Transfer Lighthouse CI verification guidance from `skills/qa-engineer/references/lighthouse-ci.md` into `skills/verification-before-completion/references/lighthouse-ci.md`.
- Update `skills/testing-patterns/SKILL.md` and `skills/verification-before-completion/SKILL.md` to reference the new files.
- Move `skills/qa-engineer` to `skills_archive/qa-engineer`.

### 4. Maintain boundary isolations

- Retain `skills/writing-for-agents` without merging into `upsert-codebase-docs`.
- Retain all individual UI skills intact: `frontend-design`, `ui-motion`, `ui-ux-review`, `copy-web-design`, and `prototype`.
- Retain `skills/laravel` in `skills/`.

### 5. Synchronize catalog, documentation, and tests

- Update `tests/test_consolidation.py` to assert the final 25 active skills and new reference paths.
- Update `README.md` and `USAGE.md` to reflect the 25 skills in the active catalog and document the absorbed reference locations.

## Alternatives considered

- Moving `laravel` to project-level `.agents/skills/laravel/`. Rejected because the user frequently develops Laravel applications across multiple directories, making the 40-token global registry cost preferable to repeated workspace setup.
- Merging `writing-for-agents` into `upsert-codebase-docs`. Rejected because `upsert-codebase-docs` handles repository documentation drift, while `writing-for-agents` provides instructions for authoring skills and prompts.
- Merging UI cluster into a single mega-skill. Rejected because separating visual styling, animation physics, and accessibility audit preserves clear cognitive boundaries for the agent.

## Consequences

- Total active skills decrease from 31 to 25.
- System prompt registry overhead decreases by approximately 20 percent.
- Core capabilities in subagent dispatching, conflict resolution, test design, and web quality audits are preserved in deep module references rather than lost.
- MCP server resource consumption is reduced by removing the idle Graphify server.

## Verification plan

- Run `python3 -m unittest discover -s tests/` to confirm all 25 active skills comply with the AgentSkills format and all required reference files exist.
- Inspect `git status` to verify clean relocations without orphan files.
- Inspect `~/.gemini/config/config.json` to verify valid JSON formatting after removing the Graphify permission grant.
