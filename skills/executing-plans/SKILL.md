---
name: executing-plans
description: Use when executing written implementation plans batch by batch inline in the current session or task by task via delegated subagents. Don't use for architectural design, plan authoring, or open-ended ideation.
---

# Executing implementation plans

Execute implementation plans written in `docs/plans/` using either inline batch execution or delegated subagents. Maintain test-driven development discipline across every task, update markdown checkboxes directly inside the plan file, and run verification before completing the branch.

Announce the starting stance at session start:
`I am using the executing-plans skill to execute this plan.`

## Modes

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
2. Inspect plan completeness. Confirm every task specifies exact file targets, interface contracts, and executable test commands. Ensure no placeholders like TODO or TBD remain.
3. Establish test baseline. Run the existing test suite once before making changes to confirm a clean starting state. If baseline tests fail, resolve them before touching plan code.
4. Synchronize git status. Ensure the working tree is clean:
```bash
git status --porcelain
```
Commit or stash any unrelated modifications before beginning execution.
5. Prioritize compiler and test diagnostics over plan snippets. When compiler errors, linter rules, or test failures contradict code examples in the plan markdown, resolve the issue using live toolchain feedback rather than forcing invalid plan code. The live toolchain takes precedence over markdown text.

Completion criterion. Git status confirms a clean working tree on a non-main feature branch and baseline test suites pass with exit code 0.

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
2. Implement minimum code. Write the minimal code necessary to make the test pass. Apply the reuse hierarchy in order by choosing existing codebase helpers first, standard library features second, installed dependencies third, and minimal new code last.
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
3. Present batch report. Summarize completed tasks, passing test outputs, and git commit hashes to the user.
4. Request user confirmation. Await explicit user approval before proceeding to the next batch.

Completion criterion. Regression tests pass with zero failures and explicit user confirmation is received before advancing to the next batch.

## Mode 2. Subagent delegation

Execute tasks by orchestrating isolated subagents per task to preserve the primary context window and enforce zero-paraphrase boundaries.

### Step 1. Plan parsing and task queue

Initialize execution state from the plan file:
- Read the plan file in `docs/plans/` and extract all tasks.
- Maintain full task specifications in memory, including target files, commands, and acceptance criteria.
- Keep the plan file synchronized as the single source of truth.

Completion criterion. All tasks parsed from the plan file into a structured task queue with exact paths, commands, and acceptance criteria.

### Step 2. Dispatch implementer subagent with invariant envelope

Apply the zero-paraphrase protocol. Never paraphrase or summarize task instructions into the prompt string. Instead, pass immutable file pointers and task IDs inside a compiled invariant envelope:

```yaml
# SUBAGENT INVARIANT ENVELOPE (DO NOT MODIFY)
task_source_file: docs/plans/<slug>-plan.md
task_id: "Phase X, Task Y"
workspace_runtime:
  package_manager: "<pm>"
  test_runner: "<test-runner-cmd>"
required_skills_to_load: ["<path-to-skill-1>/SKILL.md"]
write_allowlist: ["<target-file-1>", "<target-file-2>"]
prohibited_actions:
  rule_1: "Do not modify files outside write_allowlist."
  rule_2: "Do not alter package.json or lockfiles unless specified."
  rule_3: "Do not skip the exact verification command."
```

- Read references for subagent configuration. Read `references/subagent-skill-loading.md` for mandatory skill mapping, and read `references/parallel-dispatch.md` for parallel execution rules.
- Require skill ingestion confirmation. Implementers must confirm reading the mandated skills in their opening turn before editing code.
- Require evidence-only return receipt. The implementer terminates by reporting task ID, mutated files, verification command, exit code, and raw output tail.

Completion criterion. Implementer subagent completes execution and returns an evidence-only receipt with zero unhandled errors.

### Step 3. Boundary validation and two-stage review cycle

Before accepting subagent claims, enforce a mechanical boundary check:
1. Validate git diff boundaries. Run `git status --porcelain` and `git diff --name-only`. If any modified file falls outside the declared `write_allowlist`, revert unauthorized files via `git checkout -- <file>` and reject the task.
2. Spec compliance review. Dispatch a reviewer subagent using `prompts/spec-reviewer-prompt.md`. The reviewer inspects actual git diffs line by line against requirements without trusting implementer claims.
3. Code quality review. After spec compliance passes, dispatch a reviewer using `prompts/code-quality-reviewer-prompt.md`. The reviewer evaluates single responsibility, interface clarity, and maintainability.

Repeat the review loop until both reviewers approve the changes.

Completion criterion. Git diff strictly matches write allowlist and independent spec compliance and code quality reviews both pass.

### Step 4. Mark task completed and advance

Once all checks pass:
- Update the plan file to mark the task checkbox as completed (`- [x]`).
- Advance to the next task in the plan.
- After all tasks complete, verify global diff statistics:
```bash
BASE_SHA=$(git merge-base origin/main HEAD)
git diff --stat ${BASE_SHA}..HEAD
```

Completion criterion. The completed task checkbox is marked `- [x]` in the plan file and diff statistics are verified before advancing.

## Boundary isolation

Apply execution rules strictly to orchestration, review checkpoints, and git tracking. Keep application code syntax, database schemas, and terminal commands idiomatic, clean, and free of persona artifacts.

## Integration and completion handoff

Coordinate with related workflow skills:
- `writing-plans` creates the structured implementation plan in `docs/plans/` that this skill executes.
- `testing-patterns`, `frontend-design`, `ui-motion`, `codebase-design`, and `security-audit` provide domain constraints injected during subagent dispatch.
- `code-review` provides templates and evaluation rubrics for code reviewers.
- `verification-before-completion` conducts final verification of test outputs and git state.

After all tasks in the plan are completed and verified:
1. Verify that every checkbox in the plan file is marked `- [x]`.
2. Run the complete automated test suite to ensure system integrity.
3. Emit execution receipt to `.agents/state/execution-receipt.json`.
4. Transition to `verification-before-completion` for final test verification and PR preparation.

Completion criterion. All plan checkboxes reflect `[x]`, execution receipt emitted to `.agents/state/execution-receipt.json`, and full test suites pass with zero failures.

## Quick audit checklist

Review this table before completing plan execution:

| Check | Passing condition |
|---|---|
| Workspace isolation | Feature branch active and not `main` or `master` |
| Zero-paraphrase dispatch | Tasks passed via immutable plan path and task ID inside invariant envelope |
| Diff boundary check | Mutated files strictly contained within declared `write_allowlist` |
| Minimal diff | Shortest working diff applied without extra dependencies |
| Review passes | Spec compliance and code quality reviews approved |
| Plan synchronization | All plan checkboxes reflect `[x]` and commit hashes recorded |
