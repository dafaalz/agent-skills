# Skill usage guide

Run the 31 skills in this repository across the software delivery lifecycle.

## Overview

Each skill defines procedures, gates, and completion criteria for an engineering task. Combine skills to resolve assumptions, prevent context compaction, and deliver verified production changes.

```text
Codebase docs -> Session init -> Technical design -> Implementation planning -> Test-driven execution -> Quality audit -> Finalization -> Meta reflection
```

## 1. Codebase documentation and session initialization

Start every new conversation or project by writing codebase documentation, locking runtime stacks, and setting direct execution rules.

| Skill | Directory | Primary purpose | Command invocation |
|---|---|---|---|
| `upsert-codebase-docs` | `skills/upsert-codebase-docs` | Create or update `AGENTS.md` and `CODEBASE.md` documentation | `$upsert-codebase-docs` |
| `workspace-onboarding` | `skills/workspace-onboarding` | Detect the runtime stack, database drivers, and governing rules | `$workspace-onboarding $unslop` |
| `unslop` | `skills/unslop` | Remove conversational filler and enforce direct developer tone | `$unslop` |

### Recommended workflow
1. Run `$upsert-codebase-docs` to create or update `AGENTS.md` and `CODEBASE.md`.
2. When documentation exists on disk, run `$unslop $brainstorming @AGENTS.md @CODEBASE.md` to ground design decisions in repository architecture.
3. When you enter unfamiliar repositories, run `$workspace-onboarding $unslop` to examine active runtime stacks and manifests.

## 2. Technical design, database, and architecture

Resolve domain contracts, evaluate data scaling, prevent architectural debt, and consult frontier models before you write code.

### Backend architecture, database, and system design
| Skill | Directory | Primary purpose | Command invocation |
|---|---|---|---|
| `brainstorming` | `skills/brainstorming` | Explore approaches, evaluate trade-offs, and conduct ADR checks | `$brainstorming` |
| `codebase-design` | `skills/codebase-design` | Formulate deep module boundaries, interfaces, and seams | `$codebase-design` |
| `laravel` | `skills/laravel` | Structure Eloquent models, Livewire components, Inertia adapters, and queue jobs | `$laravel` |
| `schema-migration` | `skills/schema-migration` | Author zero-downtime database migrations with four-gate safety checks | `$schema-migration` |
| `vibe-wise` | `skills/vibe-wise` | Design system architectures and model relational data collaboratively | `$vibe-wise` |

### Frontier web AI consultation
| Skill | Directory | Primary purpose | Command invocation |
|---|---|---|---|
| `web-advisor-prompt` | `skills/web-advisor-prompt` | Package zero-context adversarial prompts for external reasoning models | `$web-advisor-prompt` |

### Frontend architecture, layout, and motion
| Skill | Directory | Primary purpose | Command invocation |
|---|---|---|---|
| `frontend-design` | `skills/frontend-design` | Build Tailwind layouts, tokens, DESIGN.md specs, and select UI libraries | `$frontend-design` |
| `react` | `skills/react` | Optimize React and Next.js applications with performance rules | `$react` |
| `ui-motion` | `skills/ui-motion` | Build spring physics animations, gesture tracking, and route motion audits | `$ui-motion` |
| `copy-web-design` | `skills/copy-web-design` | Extract design tokens, layout trees, and animations from URLs | `$copy-web-design` |
| `i18n` | `skills/i18n` | Implement internationalization, locale negotiation, and RTL layouts | `$i18n` |
| `prototype` | `skills/prototype` | Build rapid interactive click-dummies to validate UX flow | `$prototype` |

### Recommended workflow
1. Run `$brainstorming` to explore contrasting approaches.
2. For modules that handle more than 500 items, verify data scaling against `skills/brainstorming/references/architecture-scalability.md` to require server-side pagination.
3. For database evolution, run `$schema-migration` to enforce expand-contract phases, batched backfills, and lock timeouts.
4. When you face complex architectural dilemmas, run `$web-advisor-prompt` to package an adversarial prompt for an external frontier reasoning model like Gemini 4 Argon.
5. Run `$codebase-design` to lock minimal interfaces and inspect database migration files on disk before you create models.
6. For interface layouts, visual token systems, and UI library selection, run `$frontend-design` to build accessible layouts within the existing stack.
7. For React and Next.js applications, run `$react` to optimize Server Components, eliminate data waterfalls, and prevent unnecessary client re-renders.
8. For multi-language support, pluralization, or bidirectional layouts, run `$i18n` to audit and structure localized content.
9. For physics-based animations, micro-interactions, or codebase motion audits, run `$ui-motion` to build hardware-accelerated transitions.

## 3. Planning and execution orchestration

Deconstruct approved technical specifications into testable task batches and select execution modes.

| Skill | Directory | Primary purpose | Command invocation |
|---|---|---|---|
| `writing-plans` | `skills/writing-plans` | Convert design specifications into phased implementation plans | `$writing-plans` |
| `executing-plans` | `skills/executing-plans` | Execute plans via inline batches or delegated subagents with review gates | `$executing-plans` |

### Recommended workflow
1. Run `$writing-plans` to generate the implementation plan.
2. Make sure that each task contains exact file targets, complete code snippets, and automated test commands.
3. Select an execution strategy in `$executing-plans`. Use Mode 1 for inline batch execution with diff checkpoints on coupled tasks. Use Mode 2 for subagent delegation with automated reviews on independent tasks.
4. If tasks touch disjoint directories, apply parallel dispatch from `skills/executing-plans/references/parallel-dispatch.md` to run subagents without shared state collisions.

## 4. Implementation and test-driven development

Write production code using strict vertical slices and test-first iterations.

| Skill | Directory | Primary purpose | Command invocation |
|---|---|---|---|
| `executing-plans` | `skills/executing-plans` | Execute plan tasks through inline batch loops or delegated subagents | `$executing-plans` |
| `testing-patterns` | `skills/testing-patterns` | Drive code development with red-green loops, fixtures, and contract tests | `$testing-patterns` |
| `systematic-debugging` | `skills/systematic-debugging` | Identify root causes before you propose patches or bug fixes | `$systematic-debugging` |
| `s13n` | `skills/s13n` | Standardize inconsistent patterns across files and install linter guards | `$s13n` |
| `conventional-commit` | `skills/conventional-commit` | Commit task batches as atomic commits with imperative subjects | `$conventional-commit` |

### Recommended workflow
1. Run `$executing-plans` to execute the plan tasks. Choose inline batch execution for coupled changes or subagent task delegation for isolated tasks.
2. Run `$testing-patterns` to write the failing test first, run the test runner to observe expected failure, write minimal code, and verify green status.
3. When you investigate bugs, run `$systematic-debugging`. If the investigation involves large logs or multi-database queries, delegate data collection to a subagent to prevent context compaction.
4. Commit verified task batches atomically with `$conventional-commit` using selective staging.
5. When you find diverging code styles across files, run `$s13n` to standardize patterns and install linter enforcement.

## 5. Review and quality assurance

Audit code and interface quality from multiple specialized engineering angles.

| Skill | Directory | Primary purpose | Command invocation |
|---|---|---|---|
| `ui-ux-review` | `skills/ui-ux-review` | Audit visual hierarchy, accessibility, ergonomics, and cognitive load | `$ui-ux-review` |
| `code-review` | `skills/code-review` | Request structured reviews, evaluate feedback, and verify fixes | `$code-review` |
| `security-audit` | `skills/security-audit` | Evaluate authentication boundaries, CSRF protection, and injection attack vectors | `$security-audit` |

### Recommended workflow
1. For frontend changes, run `$ui-ux-review` to confirm typography contrast, accessibility compliance, and interaction ergonomics.
2. For backend endpoints, run `$security-audit` to inspect authorization policies and request validation.
3. When you request reviews or receive feedback, run `$code-review` to protect architectural boundaries and verify fixes before you merge code.

## 6. Verification, finalization, and documentation

Conduct final safety checks, clean up temporary branches, and write documentation.

| Skill | Directory | Primary purpose | Command invocation |
|---|---|---|---|
| `verification-before-completion` | `skills/verification-before-completion` | Hard gate that requires fresh test outputs, scoped linting, and git state checks | `$verification-before-completion` |
| `summarize` | `skills/summarize` | Generate structured session execution summaries and evidence tables | `$summarize` |
| `technical-writing` | `skills/technical-writing` | Write clear human documentation, README files, and RFCs | `$technical-writing` |
| `writing-for-agents` | `skills/writing-for-agents` | Draft and update `AGENTS.md`, `CODEBASE.md`, prompt runbooks, and skill specifications | `$writing-for-agents` |

### Recommended workflow
1. Run `$verification-before-completion` before you make any completion claim.
2. Run `git status --short` to make sure that no core documentation files were deleted. Run scoped linters on touched files and validate fresh test output.
3. Commit clean changes with `$conventional-commit` and finalize pull requests.
4. Run `$summarize` at the end of a session to record actions, root causes, test verification, and next steps for handoffs.
5. Update repository documentation with `$technical-writing` for human developers or `$writing-for-agents` for agent guidance files and skill specifications.

## 7. Meta-skill engineering and reflection

Audit, test, and harden the skills catalog using empirical evidence and failure reflections.

| Skill | Directory | Primary purpose | Command invocation |
|---|---|---|---|
| `review-a-skill` | `skills/review-a-skill` | Audit skill structures against specifications and run the AST linter | `$review-a-skill` |
| `skill-testing` | `skills/skill-testing` | Benchmark skills against golden scenarios with parallel subagents | `$skill-testing` |
| `reflect-to-skill` | `skills/reflect-to-skill` | Distill session failures, regressions, and user corrections into preventive rules | `$reflect-to-skill` |

### Recommended workflow
1. Run `$review-a-skill` to audit a skill against the AgentSkills specification and run `python3 skills/review-a-skill/scripts/lint_skill.py`.
2. Run `$skill-testing` to conduct A/B benchmarks across multiple scenarios when you refine complex prompt workflows.
3. When an agent encounters unexpected friction or user corrections, run `$reflect-to-skill` to extract root causes and graft permanent preventive rules into target skills.

## Complete lifecycle example

Follow this end-to-end command progression when you deliver a full feature:

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
$security-audit $testing-patterns uji apakah user bisa mendownload invoice milik tenant lain

# Step 7. Final verification and branch completion
$verification-before-completion verifikasi perubahan dan siapkan PR
```
