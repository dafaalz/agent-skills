# Skill usage guide

Orchestrate the 31 specialized skills in this repository across the complete software delivery lifecycle.

## Overview

Each skill defines operational procedures, hard gates, and completion criteria for a specific engineering task. Combine skills to eliminate unverified assumptions, prevent context compaction, and deliver verified production changes.

```
Codebase docs -> Session init -> Technical design -> Implementation planning -> Test-driven execution -> Quality audit -> Finalization
```

## 1. Codebase documentation and session initialization

Start every new conversation or project by bootstrapping high-signal documentation, locking runtime stacks, and setting direct execution rules.

| Skill | Directory | Primary purpose | Command invocation |
|---|---|---|---|
| `upsert-codebase-docs` | `skills/upsert-codebase-docs` | Bootstrap or synchronize `AGENTS.md` and `CODEBASE.md` docs | `$upsert-codebase-docs` |
| `workspace-onboarding` | `skills/workspace-onboarding` | Detect runtime stack, database drivers, and governing rules | `$workspace-onboarding $unslop` |
| `unslop` | `skills/unslop` | Eliminate AI conversational filler and enforce direct developer tone | `$unslop` |
| `ping` | `skills/ping` | Probe shell round-trip latency, process overhead, and host facts | `$ping` |

### Recommended workflow
1. Run `$upsert-codebase-docs` to bootstrap or synchronize `AGENTS.md` and `CODEBASE.md`.
2. Once documentation exists on disk, launch feature discovery with `$unslop $brainstorming @AGENTS.md @CODEBASE.md` so the agent grounds design decisions in repository architecture.
3. Use `$workspace-onboarding $unslop` when entering unfamiliar repositories to verify active runtime stacks and manifests.
4. Execute `$ping` before starting heavy autonomous workflows to verify tool responsiveness and measure shell round-trip latency.

## 2. Technical design and architecture

Resolve domain contracts, evaluate data scaling, and prevent architectural debt before writing implementation code.

### Backend architecture and domain modeling
| Skill | Directory | Primary purpose | Command invocation |
|---|---|---|---|
| `brainstorming` | `skills/brainstorming` | Explore approaches, evaluate trade-offs, and conduct ADRs | `$brainstorming` |
| `codebase-design` | `skills/codebase-design` | Formulate deep module boundaries, interfaces, and seams | `$codebase-design` |
| `graphify` | `skills/graphify` | Build dependency knowledge graphs across complex systems | `$graphify` |
| `laravel` | `skills/laravel` | Structure Eloquent models, Livewire, Inertia, and jobs | `$laravel` |

### Frontend architecture, layout, and motion
| Skill | Directory | Primary purpose | Command invocation |
|---|---|---|---|
| `frontend-design` | `skills/frontend-design` | Build Tailwind layouts, tokens, DESIGN.md specs, and select UI libraries | `$frontend-design` |
| `react` | `skills/react` | Optimize React and Next.js applications using 70 Vercel performance rules | `$react` |
| `ui-motion` | `skills/ui-motion` | Author spring physics animations, gesture tracking, and route motion audits | `$ui-motion` |
| `copy-web-design` | `skills/copy-web-design` | Extract design tokens, layout trees, and animations from URLs | `$copy-web-design` |
| `i18n` | `skills/i18n` | Implement internationalization, locale negotiation, ICU messages, and RTL layouts | `$i18n` |
| `prototype` | `skills/prototype` | Build rapid interactive click-dummies to validate UX flow | `$prototype` |

### Recommended workflow
1. Invoke `$brainstorming` to explore contrasting approaches.
2. For modules handling over 500 items, verify data scaling against `skills/brainstorming/references/architecture-scalability.md` to guarantee server-side pagination.
3. Use `$codebase-design` to lock minimal interfaces and inspect database migration files on disk before creating models.
4. For interface layouts, visual token systems, and UI library selection, invoke `$frontend-design` to build accessible layouts and upgrade visual polish within the existing stack. For resilient network interaction, apply `skills/frontend-design/references/api-resilience.md`.
5. For React and Next.js applications, invoke `$react` to optimize Server Components, eliminate data waterfalls, and prevent unnecessary client re-renders.
6. For multi-language support, pluralization, or bidirectional layouts, invoke `$i18n` to audit and structure localized content.
7. For physics-based animations, micro-interactions, or codebase motion audits, invoke `$ui-motion` to engineer hardware-accelerated transitions or route structured audit plans.

## 3. Planning and execution orchestration

Deconstruct approved technical specifications into testable task batches and select execution modes.

| Skill | Directory | Primary purpose | Command invocation |
|---|---|---|---|
| `writing-plans` | `skills/writing-plans` | Convert design specifications into phased implementation plans | `$writing-plans` |
| `dispatching-parallel-agents` | `skills/dispatching-parallel-agents` | Run two or more independent, non-overlapping tasks concurrently | `$dispatching-parallel-agents` |
| `executing-plans` | `skills/executing-plans` | Execute plans via inline batches or delegated subagents with review gates | `$executing-plans` |

### Recommended workflow
1. Generate the implementation plan using `$writing-plans`.
2. Confirm that each task contains exact file targets, complete code snippets, and automated test commands.
3. Select an execution strategy in `$executing-plans`. Use Mode 1 (Inline Batch Execution) with diff checkpoints for tightly coupled tasks in the current session, or Mode 2 (Subagent Delegation) with two-stage automated review for independent tasks.
4. If tasks touch disjoint directories (such as database migrations and frontend components), invoke `$dispatching-parallel-agents` to run them concurrently.

## 4. Implementation and test-driven development

Write production code using strict vertical slices and test-first iterations.

| Skill | Directory | Primary purpose | Command invocation |
|---|---|---|---|
| `executing-plans` | `skills/executing-plans` | Execute plan tasks through inline batch loops or delegated subagents | `$executing-plans` |
| `testing-patterns` | `skills/testing-patterns` | Drive code development via red-green loops, fixtures, and contract tests | `$testing-patterns` |
| `systematic-debugging` | `skills/systematic-debugging` | Identify root causes before proposing patches or bug fixes | `$systematic-debugging` |
| `s13n` | `skills/s13n` | Standardize inconsistent patterns across files and install linter guards | `$s13n` |
| `conventional-commit` | `skills/conventional-commit` | Commit task batches as atomic commits with imperative subjects | `$conventional-commit` |
| `full-output-enforcement` | `skills/output-skill` | Enforce full code generation and ban truncated placeholder comments | `$full-output-enforcement` |

### Recommended workflow
1. Execute the plan using `$executing-plans`, choosing inline batch execution for coupled changes or subagent task delegation for isolated tasks.
2. Apply `$testing-patterns` to write the failing test first, run the test runner to observe expected failure, implement minimal code, and verify green status.
3. When investigating bugs, trigger `$systematic-debugging`. If the investigation involves massive logs or multi-database queries, delegate data collection to a subagent to defend against context compaction.
4. Commit verified task batches atomically using `$conventional-commit` with selective staging.
5. When spotting diverging implementation styles or inconsistent error handling across files, trigger `$s13n` to standardize patterns and install linter enforcement.

## 5. Review and quality assurance

Audit code and interface quality from multiple specialized engineering angles.

| Skill | Directory | Primary purpose | Command invocation |
|---|---|---|---|
| `ui-ux-review` | `skills/ui-ux-review` | Audit visual hierarchy, accessibility, ergonomics, and cognitive load | `$ui-ux-review` |
| `code-review` | `skills/code-review` | Request structured reviews, evaluate feedback, and verify fixes | `$code-review` |
| `qa-engineer` | `skills/qa-engineer` | Execute exploratory testing charters and stress edge cases | `$qa-engineer` |
| `security-audit` | `skills/security-audit` | Evaluate authentication boundaries, CSRF, and injection attack vectors | `$security-audit` |

### Recommended workflow
1. For frontend changes, run `$ui-ux-review` to confirm typography contrast, accessibility compliance, and interaction ergonomics.
2. For backend endpoints, run `$security-audit` to inspect authorization policies and request validation.
3. When requesting reviews or receiving feedback, invoke `$code-review` to validate counter-arguments with targeted web searches, protect architectural boundaries, and verify fixes before merging.

## 6. Verification, finalization, and documentation

Conduct final safety checks, clean up temporary branches, and write human documentation.

| Skill | Directory | Primary purpose | Command invocation |
|---|---|---|---|
| `verification-before-completion` | `skills/verification-before-completion` | Hard-gate requiring test outputs, scoped linting, and git state checks | `$verification-before-completion` |
| `finishing-a-development-branch` | `skills/finishing-a-development-branch` | Merge feature branches, verify clean git state, and finalize PRs | `$finishing-a-development-branch` |
| `summarize` | `skills/summarize` | Generate structured session execution summaries, evidence tables, and handoffs | `$summarize` |
| `technical-writing` | `skills/technical-writing` | Write clear human documentation, README files, and RFCs | `$technical-writing` |
| `writing-for-agents` | `skills/writing-for-agents` | Draft and update `AGENTS.md`, `CODEBASE.md`, prompt runbooks, and skill specifications | `$writing-for-agents` |

### Recommended workflow
1. Run `$verification-before-completion` before making any completion claim.
2. The agent executes `git status --short` to confirm zero core documentation files were deleted, runs scoped linters (`pint`, `eslint`) on touched files, and validates fresh test output.
3. Invoke `$finishing-a-development-branch` to complete git operations.
4. Run `$summarize` at the end of a session to record actions, root causes, test verification, and next steps for agent or teammate handoff.
5. Update repository documentation using `$technical-writing` for human developers or `$writing-for-agents` for agent guidance files and skill specifications.

## Complete lifecycle example

Follow this end-to-end command progression when delivering a full feature:

```bash
# Step 1. Bootstrap or audit codebase documentation
$upsert-codebase-docs bootstrap atau audit dokumentasi AGENTS.md dan CODEBASE.md

# Step 2. Explore architecture and brainstorm feature grounded in docs
$unslop $brainstorming @AGENTS.md @CODEBASE.md kita mau bikin sistem export invoice ke PDF dan Excel

# Step 3. Write structured implementation plan
$writing-plans buat plan implementasi bertahap untuk worker dan controller export

# Step 4. Execute implementation with test-driven development
$executing-plans $testing-patterns eksekusi batch 1 (job class dan unit test)

# Step 5. Polish frontend export modal
$frontend-design $ui-motion buat modal pilihan format export dan progress bar

# Step 6. Verify security and QA edge cases
$security-audit $qa-engineer uji apakah user bisa mendownload invoice milik tenant lain

# Step 7. Final verification and branch completion
$verification-before-completion $finishing-a-development-branch verifikasi perubahan dan siapkan PR
```
