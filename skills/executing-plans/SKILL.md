---
name: executing-plans
description: Use when executing written implementation plans batch by batch inline in the current session or task by task via delegated subagents. Don't use for architectural design, plan authoring, or open-ended ideation.
---

# Executing implementation plans

Execute implementation plans written in `docs/superpowers/plans/` using either inline batch execution or delegated subagents. Maintain test-driven development discipline across every task, update markdown checkboxes directly inside the plan file, and run verification before completing the branch.

Announce the starting stance at session start:
`I am using the executing-plans skill to execute this plan.`

## Overview and mode selection

Implementation plans define structured tasks with explicit file paths, full code blocks, and automated test commands. Choose between two execution modes depending on task coupling, plan size, and session architecture:

| Dimension | Mode 1 (Inline Batch Execution) | Mode 2 (Subagent Delegation) |
| --- | --- | --- |
| Context isolation | Single session context | Fresh subagent per task |
| Best suited for | Tightly coupled tasks, small plans | Independent tasks, large plans |
| Review mechanism | User checkpoints between batches | Two-stage automated subagent review |
| Context consumption | Consumes primary session window | Preserves primary session window |
| Execution style | Direct sequential edits | Orchestrated delegation |

When the user specifies an execution mode, apply it directly. When the mode is not specified:
- Choose Mode 1 for plans with 1 to 3 tightly coupled tasks where context continuity is required.
- Choose Mode 2 for plans with 4 or more modular tasks where context preservation is required.
- Ask the user if task boundaries allow either approach and preference is ambiguous.

## Pre-execution verification

Complete these preparation steps before editing code under either mode:
1. Verify workspace isolation. Confirm work proceeds on a dedicated feature branch. Run `git rev-parse --abbrev-ref HEAD` and verify the branch is not `main` or `master`.
2. Inspect plan completeness. Confirm every task specifies exact file targets, full code blocks, and executable test commands. Ensure no placeholders like TODO or TBD remain.
3. Establish test baseline. Run the existing test suite once before making changes to confirm a clean starting state. If baseline tests fail, resolve them before touching plan code.
4. Synchronize git status. Ensure the working tree is clean:
```bash
git status --porcelain
```
Commit or stash any unrelated modifications before beginning execution.

## Mode 1. Inline batch execution

Execute tasks directly in the current session using structured batch checkpoints.

### Step 1. Define batch boundaries

Group plan tasks into logical batches before writing code:
- Set batch size to 1 to 3 related tasks.
- Keep tightly dependent changes in the same batch.
- Mark the current batch boundaries clearly for the user.

Completion criterion. Plan tasks partitioned into sequential batches of 1 to 3 related tasks with confirmed boundaries.

### Step 2. Test-driven task execution

Execute each task in the active batch following red, green, refactor cycles:
1. Run the failing test. Execute the test command specified in the plan task and confirm failure. Verify the failure matches expected missing functionality rather than broken imports or syntax.
2. Implement minimum code. Write the minimal code necessary to make the test pass. Avoid speculative flexibility or unrequested abstractions.
3. Run the passing test. Re-run the test command and verify all assertions pass cleanly.
4. Clean up refactors. Remove orphan imports, unused variables, and temporary debugging logs.
5. Update plan status. Change the task checkbox in the plan markdown file from `- [ ]` to `- [x]`.
6. Commit changes. Create a git commit referencing the completed task with a clear message:
```bash
git add <changed-files>
git commit -m "feat(scope): implement specific task functionality"
```

Repeat this sequence for every task within the batch.

Completion criterion. All tasks in the active batch pass their red-green test cycles, reflect `- [x]` in the plan file, and have dedicated git commits.

### Step 3. Batch review checkpoint

Pause at the end of each batch to inspect changes and report progress:
1. Run regression tests. Execute existing test suites to confirm no breaks occurred in adjacent code.
2. Inspect diff scope. Run diff stats against the starting commit of the batch:
```bash
git diff --stat <base-sha>..HEAD
```
3. Present batch report. Summarize completed tasks, passing test outputs, and git commit hashes to the user:
```markdown
Batch checkpoint report
- Completed tasks including Task 1 and Task 2
- Passing tests confirmed with zero failures
- Commit hashes recorded for each task
- Next batch preview covering Task 3 and Task 4
```
4. Request user confirmation. Await explicit user approval before proceeding to the next batch.

Completion criterion. Regression tests pass with zero failures and explicit user confirmation is received before advancing to the next batch.

## Mode 2. Subagent delegation

Execute tasks by orchestrating isolated subagents per task to preserve the primary context window and enforce independent dual-stage review gates.

### Step 1. Plan parsing and task queue

Initialize execution state from the plan file:
- Read the plan file in `docs/superpowers/plans/` and extract all tasks.
- Maintain full task specifications in memory, including target files, commands, and acceptance criteria.
- Keep the plan file synchronized as the single source of truth.

Completion criterion. All tasks parsed from the plan file into a structured task queue with exact paths, commands, and acceptance criteria.

### Step 2. Dispatch implementer subagent

Dispatch a fresh subagent for each task using the template at `prompts/implementer-prompt.md`:
- Provide complete task text, target files, and architectural context in the prompt. Never force the subagent to read the entire plan file directly.
- Ensure the prompt includes exact test commands and relevant interfaces so the subagent operates autonomously.
- The orchestrator stays in supervisory mode and never writes task code directly.
- The implementer follows test-driven development, executes tests, commits changes, and self-reviews.
- The implementer reports one of four lifecycle statuses:
  - DONE. Implementation complete and tested. Proceed directly to spec compliance review.
  - DONE_WITH_CONCERNS. Implementation complete but with doubts. Read concerns, resolve blockers, then proceed to review.
  - NEEDS_CONTEXT. Information is missing. Provide the necessary context and re-dispatch.
  - BLOCKED. Implementer cannot proceed. Assess whether to supply context, upgrade model strength, or escalate to the user.
- Never dispatch parallel implementers on shared files or overlapping branches. Consult `references/parallel-dispatch.md` for domain partitioning criteria and parallel prompt templates when dispatching subagents across disjoint domains.

Completion criterion. Implementer subagent completes task execution and reports a verified status with clean test output.

### Step 3. Two-stage review cycle

Every completed task must pass two independent reviews before acceptance:

1. Spec compliance review. Dispatch a reviewer subagent using `prompts/spec-reviewer-prompt.md`. The reviewer inspects actual git diffs line by line against requirements without trusting implementer claims. If missing features or scope creep are identified, instruct the implementer to fix them before proceeding.
2. Code quality review. After spec compliance passes, dispatch a reviewer using `prompts/code-quality-reviewer-prompt.md`. The reviewer evaluates single responsibility, interface clarity, test rigor, and maintainability. The implementer resolves all blocker and high-priority findings.

Repeat the review loop until both reviewers approve the changes. Never skip either review stage.

Completion criterion. Independent spec compliance and code quality reviews both pass with zero unresolved high-priority findings.

### Step 4. Mark task completed and advance

Once both reviews pass:
- Update the plan file to mark the task checkbox as completed (`- [x]`).
- Advance to the next task in the plan.
- After all tasks complete, dispatch a final code reviewer subagent across the entire implementation before branch handoff:
```bash
BASE_SHA=$(git merge-base origin/main HEAD)
git diff --stat ${BASE_SHA}..HEAD
```

Completion criterion. The completed task checkbox is marked `- [x]` in the plan file and diff statistics are verified before advancing.

## Model selection for subagents

Assign models strategically to conserve resources while maintaining quality:
- Lightweight models. Isolated helper functions, mechanical test updates, and straightforward edits.
- Standard models. Multi-file integrations, debugging failures, or cross-module refactors.
- Advanced models. Spec compliance audits, code quality reviews, and complex architectural seam modifications.

## Execution rules

### Stop conditions

Halt execution immediately and request user guidance when any of these conditions occur:
- A test failure persists after implementing the changes specified in the plan.
- The plan lacks required file paths, type definitions, or dependency instructions.
- A required package, tool, or build command fails to install or execute.
- Unexpected git conflicts, dirty workspace state, or external modifications arise.
- An implementer subagent remains blocked after escalation attempts.

Never invent speculative requirements or bypass failing tests without explicit user confirmation.

### State tracking

Track progress directly within the plan file:
- Use standard markdown checkboxes (`- [ ]` and `- [x]`).
- Synchronize plan file checkboxes with git commits after every completed task.
- Keep the plan file as the single source of truth for task progress.
- Protect against context compaction. For extensive plans exceeding 5 tasks, persist milestone reports to disk. When an individual task involves surveying massive datasets or broad codebases, delegate it to a subagent via `invoke_subagent` to keep the primary execution context window lean.

## Integration

Coordinate with related workflow skills:
- `writing-plans` creates the structured implementation plan in `docs/superpowers/plans/` that this skill executes.
- `testing-patterns` provides red, green, refactor mechanics and test charter patterns for individual tasks.
- `code-review` provides templates and evaluation rubrics for code reviewers.
- `verification-before-completion` conducts final verification of test outputs and git state.

## Handoff to completion

After all tasks in the plan are completed and verified:
1. Verify that every checkbox in the plan file is marked `- [x]`.
2. Run the complete automated test suite to ensure system integrity.
3. Announce transition to `verification-before-completion` to conduct final test verification and prepare the branch for pull request creation.
