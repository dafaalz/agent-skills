---
name: executing-plans
description: "Use when executing written implementation plans batch by batch inline in the current session or task by task via delegated subagents. Don't use for architectural design (use codebase-design), plan authoring (use writing-plans), open-ended ideation (use brainstorming), or multi-task plan verification and audit defense (use agent-planning)."
---

# Executing implementation plans

Execute implementation plans written in `docs/superpowers/plans/` using either inline batch execution or delegated subagents. Maintain test-driven development discipline across every task, update markdown checkboxes directly inside the plan file, and run verification before completing the branch.

Announce the starting stance at session start:
`I am using the executing-plans skill to execute this plan.`

<HARD-GATE>
Write-Target Boundary. Write only to paths declared in the active plan task `Files` block, the plan file itself for checkbox updates, and `.agents/state/` for receipts and blockers. Do not modify files outside that set. Do not run `git commit --amend`, `git reset --hard`, `git push --force`, or any destructive command without explicit user approval. Mode 1 and Mode 2 both inherit this gate.
</HARD-GATE>

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
1. Verify workspace isolation. Confirm work proceeds on a dedicated feature branch. Run `git rev-parse --abbrev-ref HEAD` and verify the branch is not `main` or `master`. Exception: repository maintenance, skill audits, or prompt updates under `skills/` or `.agents/` may be committed directly to `main` when operating in single-branch maintenance mode.
2. Inspect plan completeness. Confirm every task specifies exact file targets, interface contracts, and executable test commands. Ensure no placeholders like TODO or TBD remain.
3. Establish test baseline. Run the existing test suite once before making changes to confirm a clean starting state. If baseline tests fail, record the failing command and output in `.agents/state/baseline-failures.md`, stop, and ask the user whether to repair baseline or abort. Do not repair unrelated baseline failures without approval.
4. Synchronize git status. Ensure the working tree is clean:
```bash
git status --porcelain
```
Commit or stash any unrelated modifications before beginning execution.
5. Prioritize compiler and test diagnostics over plan snippets. When compiler errors, linter rules, or test failures contradict code examples in the plan markdown, resolve the issue using live toolchain feedback rather than forcing invalid plan code. The live toolchain takes precedence over markdown text.

Completion criterion. Git status confirms a clean working tree on a non-main feature branch (or documented maintenance mode on main) and baseline test suites pass with exit code 0.

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
- Read the plan file in `docs/superpowers/plans/` and extract all tasks.
- Maintain full task specifications in memory, including target files, commands, and acceptance criteria.
- Keep the plan file synchronized as the single source of truth.

Completion criterion. All tasks parsed from the plan file into a structured task queue with exact paths, commands, and acceptance criteria.

### Step 2. Dispatch implementer subagent with invariant envelope

Apply the zero-paraphrase protocol. Never paraphrase or summarize task instructions into the prompt string. Instead, pass immutable file pointers and task IDs inside a compiled invariant envelope:

```yaml
# SUBAGENT INVARIANT ENVELOPE (DO NOT MODIFY)
task_source_file: docs/superpowers/plans/<slug>-plan.md
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
1. Validate git diff boundaries. Run `git status --porcelain` and `git diff --name-only`. If any modified file falls outside the declared `write_allowlist`, stop the task. If the unauthorized change is uncommitted, run `git restore --source=HEAD --staged --worktree -- <file>`. If it is committed, record the commit SHA and stop. Do not rewrite history without explicit user approval.
2. Spec compliance review. Dispatch a reviewer subagent using `prompts/spec-reviewer-prompt.md`. The reviewer inspects actual git diffs line by line against requirements without trusting implementer claims.
3. Code quality review. After spec compliance passes, dispatch a reviewer using `prompts/code-quality-reviewer-prompt.md`. The reviewer evaluates single responsibility, interface clarity, and maintainability.

Run at most 3 review cycles per task. On cycle 3 failure, stop. Write `.agents/state/execution-blocker.json` with `task_id`, `failed_review`, `diff_sha`, and `reviewer_output`. Ask the user to resolve the blocker. Do not dispatch another reviewer for the same task.

Completion criterion. Git diff strictly matches write allowlist, review cycles remain at or under 3, and independent spec compliance and code quality reviews both pass.

### Step 4. Mark task completed and advance

Once all checks pass:
- Update the plan file to mark the task checkbox as completed (`- [x]`).
- Advance to the next task in the plan.
- After all tasks complete, verify global diff statistics:
```bash
BASE_REF=$(git rev-parse --abbrev-ref --symbolic-full-name '@{upstream}' 2>/dev/null || printf 'main')
BASE_SHA=$(git merge-base "$BASE_REF" HEAD)
git diff --stat "${BASE_SHA}..HEAD"
```

Completion criterion. The completed task checkbox is marked `- [x]` in the plan file and diff statistics are verified before advancing.

## Boundary isolation

Apply execution rules strictly to orchestration, review checkpoints, and git tracking. Keep application code syntax, database schemas, and terminal commands idiomatic, clean, and free of persona artifacts.

## Integration and completion handoff

Coordinate with related workflow skills:
- `writing-plans` creates the structured implementation plan in `docs/superpowers/plans/` that this skill executes.
- `testing-patterns`, `frontend-design`, `ui-motion`, `codebase-design`, and `security-audit` provide domain constraints injected during subagent dispatch.
- `code-review` provides templates and evaluation rubrics for code reviewers.
- `verification-before-completion` conducts final verification of test outputs and git state.

After all tasks in the plan are completed and verified:
1. Verify that every checkbox in the plan file is marked `- [x]`.
2. Run the complete automated test suite to ensure system integrity.
3. Emit execution receipt to `.agents/state/execution-receipt.json`.
4. Read the plan header `Source spec` field. If it names a path, verify the referenced file header declares `artifact_type: component-spec` before recording `component_spec_path_abs`. If the field is `none` or absent, skip component-spec purge entirely. Never infer the component spec path from the plan file name.
5. Derive the repo-relative plan path before recording recovery:
   * `plan_path_rel`: output of `git ls-files --full-name -- "$plan_path_abs"`
   * If `git ls-files` returns empty (file untracked), record `plan_recovery_command: "not-recoverable"` and `plan_tracked: false`.
   * Otherwise record `plan_recovery_command`: `git show <plan_last_commit_sha>:<plan_path_rel>`.
   * Record `plan_path_rel` alongside `plan_path_abs` in the receipt.
   * If a component spec is present, derive `component_spec_path_rel` and its recovery command using the same git check.
6. Present `plan_recovery_command` to the user with the confirmation gate. After explicit user confirmation, run `rm -f -- "$plan_path_abs"`. When a component spec is present, run `rm -f -- "$component_spec_path_abs"`. The `--` flag prevents paths beginning with a dash from being parsed as options. Record `plan_cleanup: "confirmed"` in the receipt. On refusal, record `plan_cleanup: "user-declined"`.
7. Transition to `verification-before-completion` for final test verification and PR preparation.

Completion criterion. All plan checkboxes reflect `[x]`, execution receipt emitted to `.agents/state/execution-receipt.json` with recovery provenance, plan cleanup decision recorded, and full test suites pass with zero failures.

## Quick audit checklist

Review this table before completing plan execution:

| Check | Passing condition |
|---|---|
| Hard gate | Write-target boundary active across Mode 1 and Mode 2 |
| Workspace isolation | Feature branch active and not `main` or `master` (except documented maintenance mode) |
| Zero-paraphrase dispatch | Tasks passed via immutable plan path and task ID inside invariant envelope |
| Diff boundary check | Mutated files strictly contained within declared `write_allowlist` |
| Minimal diff | Shortest working diff applied without extra dependencies |
| Review passes | Spec compliance and code quality reviews approved within 3 cycles |
| Plan synchronization | All plan checkboxes reflect `[x]` and commit hashes recorded |
