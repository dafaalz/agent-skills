# Skill usage guide

Orchestrate the 36 specialized skills in this repository across the complete software delivery lifecycle.

## Overview

Each skill defines operational procedures, hard gates, and completion criteria for a specific engineering task. Combine skills intentionally to eliminate unverified assumptions, prevent context window compaction, and deliver verified production changes.

```
Session init -> Design & explore -> Implementation planning -> TDD execution -> Quality audit -> Finalization
```

---

## 1. Session initialization and workspace setup

Start every new conversation or unfamiliar workspace with initialization skills to lock runtime stacks, database engines, and governing rules.

| Skill | Directory | Primary purpose | Command invocation |
|---|---|---|---|
| `workspace-onboarding` | `skills/workspace-onboarding` | Detect runtime stack, database drivers, and governing rules | `$workspace-onboarding $unslop` |
| `unslop` | `skills/unslop` | Eliminate AI conversational filler and enforce direct developer tone | `$unslop` |
| `using-superpowers` | `skills/using-superpowers` | Automatically select and sequence skills for ambiguous tasks | `$using-superpowers` |
| `using-git-worktrees` | `skills/using-git-worktrees` | Create isolated git worktrees and safety-checked branches | `$using-git-worktrees` |

### Recommended workflow
1. Begin turn 1 with `$workspace-onboarding $unslop`.
2. Let the agent inspect project manifests (`composer.json`, `package.json`, `.env`) and print the single status verification bracket.
3. If beginning a multi-task feature, invoke `$using-git-worktrees` to establish a dedicated worktree before modifying repository files.

---

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
| `pick-ui-library` | `skills/pick-ui-library` | Evaluate and select curated UI primitives and packages | `$pick-ui-library` |
| `design-taste-frontend` | `skills/taste-skill` | Build modern Tailwind layouts with proper visual hierarchy | `$design-taste-frontend` |
| `ui-motion` | `skills/ui-motion` | Author spring physics animations and view transitions | `$ui-motion` |
| `build-awwwards-quality-sites` | `skills/build-awwwards-quality-sites` | Craft interactive 3D WebGL, Three.js, and GSAP experiences | `$build-awwwards-quality-sites` |
| `copy-web-design` | `skills/copy-web-design` | Extract design tokens, layout trees, and animations from URLs | `$copy-web-design` |
| `stitch-design-taste` | `skills/stitch-skill` | Define Google Stitch DESIGN.md tokens and semantic themes | `$stitch-design-taste` |
| `redesign-existing-projects` | `skills/redesign-skill` | Modernize dated interfaces without modifying core stacks | `$redesign-existing-projects` |
| `hallmark` | `skills/hallmark` | Audit UI quality and extract tokens for greenfield pages | `$hallmark` |
| `prototype` | `skills/prototype` | Build rapid interactive click-dummies to validate UX flow | `$prototype` |

### Recommended workflow
1. Invoke `$brainstorming` to explore contrasting approaches.
2. For modules handling over 500 items, verify data scaling against `skills/brainstorming/references/architecture-scalability.md` to guarantee server-side pagination.
3. Use `$codebase-design` to lock minimal interfaces and inspect database migration files on disk before creating models.

---

## 3. Planning and subagent orchestration

Deconstruct approved technical specifications into testable task batches.

| Skill | Directory | Primary purpose | Command invocation |
|---|---|---|---|
| `writing-plans` | `skills/writing-plans` | Convert design specifications into phased TDD plans | `$writing-plans` |
| `dispatching-parallel-agents` | `skills/dispatching-parallel-agents` | Run two or more independent, non-overlapping tasks concurrently | `$dispatching-parallel-agents` |
| `subagent-driven-development` | `skills/subagent-driven-development` | Execute plan tasks through independent subagents with fresh review gates | `$subagent-driven-development` |

### Recommended workflow
1. Generate the implementation plan using `$writing-plans`.
2. Confirm that each task contains exact file targets, complete code snippets, and automated test commands.
3. If tasks touch disjoint directories (such as database migrations and frontend components), invoke `$dispatching-parallel-agents` to run them concurrently.

---

## 4. Implementation and test-driven development

Write production code using strict vertical slices and test-first iterations.

| Skill | Directory | Primary purpose | Command invocation |
|---|---|---|---|
| `executing-plans` | `skills/executing-plans` | Execute plans batch by batch with diff checkpoints | `$executing-plans` |
| `tdd` | `skills/tdd` | Drive code development via Red, Green, and Refactor cycles | `$tdd` |
| `testing-patterns` | `skills/testing-patterns` | Author unit fixtures, contract tests, and database factories | `$testing-patterns` |
| `systematic-debugging` | `skills/systematic-debugging` | Identify root causes before proposing patches or bug fixes | `$systematic-debugging` |
| `full-output-enforcement` | `skills/output-skill` | Enforce full code generation and ban truncated placeholder comments | `$full-output-enforcement` |

### Recommended workflow
1. Execute the current task batch using `$executing-plans`.
2. Write the failing test first, run the test runner to observe expected failure, implement minimal code, and verify green status.
3. When investigating bugs, trigger `$systematic-debugging`. If the investigation involves massive logs or multi-database queries, delegate data collection to a subagent to defend against context compaction.

---

## 5. Review and quality assurance

Audit code and interface quality from multiple specialized engineering angles.

| Skill | Directory | Primary purpose | Command invocation |
|---|---|---|---|
| `interface-review` | `skills/interface-review` | Audit visual hierarchy, Tailwind classes, and accessibility | `$interface-review` |
| `ux-review` | `skills/ux-review` | Audit cognitive load, interaction ergonomics, and error states | `$ux-review` |
| `qa-engineer` | `skills/qa-engineer` | Execute exploratory testing charters and stress edge cases | `$qa-engineer` |
| `security-audit` | `skills/security-audit` | Evaluate authentication boundaries, CSRF, and injection attack vectors | `$security-audit` |
| `requesting-code-review` | `skills/requesting-code-review` | Prepare structured PR summaries and reviewer checklists | `$requesting-code-review` |
| `receiving-code-review` | `skills/receiving-code-review` | Process PR feedback with technical rigor and search-backed pushback | `$receiving-code-review` |

### Recommended workflow
1. For frontend changes, run `$interface-review` and `$ux-review` to confirm typography contrast and interaction feedback.
2. For backend endpoints, run `$security-audit` to inspect authorization policies and request validation.
3. When team feedback suggests merging unrelated concerns into a single file, invoke `$receiving-code-review` to validate counter-arguments with targeted web searches and maintain Single Responsibility boundaries.

---

## 6. Verification, finalization, and documentation

Conduct final safety checks, clean up temporary branches, and write human documentation.

| Skill | Directory | Primary purpose | Command invocation |
|---|---|---|---|
| `verification-before-completion` | `skills/verification-before-completion` | Hard-gate requiring test outputs, scoped linting, and git state checks | `$verification-before-completion` |
| `finishing-a-development-branch` | `skills/finishing-a-development-branch` | Merge feature branches, clean up worktrees, and finalize PRs | `$finishing-a-development-branch` |
| `technical-writing` | `skills/technical-writing` | Write clear human documentation, README files, and RFCs | `$technical-writing` |
| `writing-for-agents` | `skills/writing-for-agents` | Draft and update `AGENTS.md`, `CODEBASE.md`, and prompt runbooks | `$writing-for-agents` |
| `writing-skills` | `skills/writing-skills` | Author new skills or refactor existing skill workflows | `$writing-skills` |

### Recommended workflow
1. Run `$verification-before-completion` before making any completion claim.
2. The agent executes `git status --short` to confirm zero core documentation files were deleted, runs scoped linters (`pint`, `eslint`) on touched files, and validates fresh test output.
3. Invoke `$finishing-a-development-branch` to complete git operations.
4. Update repository documentation using `$technical-writing` for developers or `$writing-for-agents` for agent guidance files.

---

## Complete lifecycle example

Follow this end-to-end command progression when delivering a full feature:

```bash
# Step 1. Initialize session and discover environment
$workspace-onboarding $unslop kita mau bikin sistem export invoice ke PDF dan Excel

# Step 2. Explore architecture and database schema
$brainstorming $codebase-design gimana arsitektur worker queue dan skema tabel invoice export?

# Step 3. Write structured implementation plan
$writing-plans buat plan implementasi bertahap untuk worker dan controller export

# Step 4. Execute implementation with test-driven development
$executing-plans $tdd eksekusi batch 1 (job class dan unit test)

# Step 5. Polish frontend export modal
$design-taste-frontend $ui-motion buat modal pilihan format export dan progress bar

# Step 6. Verify security and QA edge cases
$security-audit $qa-engineer uji apakah user bisa mendownload invoice milik tenant lain

# Step 7. Final verification and branch completion
$verification-before-completion $finishing-a-development-branch verifikasi perubahan dan siapkan PR
```
