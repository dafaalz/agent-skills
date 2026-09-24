---
name: executing-plans
description: Use when executing written implementation plans batch by batch with review checkpoints in the current session.
---

# Executing implementation plans

Execute an existing implementation plan in the current session. Follow test-driven development for every task, update task checkboxes directly in the plan file, and pause at review checkpoints to confirm progress before proceeding.

Announce the following message at session start:
`I am using the executing-plans skill to execute this plan.`

## Workflow

Follow these four steps in sequence:

### Step 1. Plan audit and workspace setup

Read and inspect the implementation plan before making code changes:
- Verify workspace isolation. Confirm that work proceeds on a dedicated branch or worktree created by `using-git-worktrees`. Never modify `main` or `master` directly.
- Inspect plan structure. Verify that every task specifies exact file targets, full code blocks, and test commands.
- Surface ambiguities early. If the plan contains missing requirements, broken logic, or placeholders like TODO or TBD, stop and ask the user for clarification before editing code.
- Mark the first batch. Identify the logical task boundary for the first execution batch, typically 1 to 3 related tasks.

**Completion criterion.** The active git branch is verified as isolated, all plan tasks are confirmed complete with zero placeholders, and the first batch boundary is determined.

### Step 2. Batch task execution

Execute tasks in the current batch sequentially using test-driven development:
- Run the failing test. Execute the test command specified in the plan task and confirm failure.
- Implement the code. Apply the exact code changes specified in the plan.
- Run the passing test. Execute the test command and verify all assertions pass.
- Update the plan file. Edit the plan markdown file to mark the task checkbox as completed (`- [x]`).
- Commit the changes. Run `git commit` with a concise descriptive message naming the completed task.

Repeat this cycle for each task in the current batch.

**Completion criterion.** All tasks in the active batch have passing test runs, committed git changes, and checked boxes (`- [x]`) in the plan file.

### Step 3. Review checkpoint and diff inspection

Pause at the end of each task batch to inspect changes and report status:
- Run test suite sanity checks. Confirm no regression occurred in existing test suites.
- Inspect the git diff. Review modified files using `git diff --stat` and verify changes match the plan scope.
- Report batch completion. Present a concise summary to the user listing completed tasks, passing test outputs, and git commit hashes.
- Prompt for continuation. Ask the user for confirmation before beginning the next batch.

**Completion criterion.** The git diff is verified clean against the plan scope, test suites pass, and the user explicitly approves proceeding to the next batch.

### Step 4. Branch completion handoff

After all tasks in the plan are completed and verified:
- Verify total plan completion. Check that every checkbox in the plan file is marked `- [x]`.
- Invoke the completion skill. Announce transition to `finishing-a-development-branch` to run final test verification, present merge options, and handle branch cleanup.

**Completion criterion.** All plan checkboxes are marked `- [x]` and `finishing-a-development-branch` is invoked.

## Execution rules

### Stop conditions

Stop execution immediately and ask the user for direction when any of these conditions occur:
- A test failure persists after implementing the changes specified in the plan.
- The plan lacks required file paths, type definitions, or dependency instructions.
- A required command or package fails to install or execute.
- An unexpected merge conflict or uncommitted external modification is detected.

Never invent solutions or guess missing requirements without user confirmation.

### State tracking

Track execution state inside the plan file:
- Use standard markdown checkboxes (`- [ ]` and `- [x]`).
- Keep plan files synchronized with git commits after every completed task.
- Do not maintain duplicate task trackers in memory or scratch files.
- Protect against context compaction: For extensive plans exceeding 5 tasks or operations generating large terminal logs, persist batch milestone reports to disk. When an individual task involves surveying massive datasets or broad codebases, delegate it to a subagent via `invoke_subagent` to keep the primary execution context window lean.

## Integration

Coordinate with related workflow skills:
- `using-git-worktrees` sets up isolated workspaces before starting execution.
- `writing-plans` creates the structured implementation plan this skill executes.
- `finishing-a-development-branch` finishes branch integration after all tasks pass.
- `subagent-driven-development` serves as the alternative execution skill when delegating tasks to fresh subagents.
