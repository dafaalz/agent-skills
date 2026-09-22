---
name: finishing-a-development-branch
description: Use when implementation is complete, all automated tests pass, and the working branch or worktree is ready for integration, pull request creation, or cleanup.
---

# Finishing a development branch

Guide completion of development work by verifying tests, presenting branch options, executing the user's choice, and cleaning up worktrees.

When starting this workflow, state that you are using the finishing-a-development-branch skill to complete the work.

## Workflow

Follow these five steps in sequence:

### Step 1. Verify tests

Run the project test suite before presenting branch options. Execute the repository test runner command, such as `npm test`, `cargo test`, `pytest`, or `go test ./...`.

If tests fail, stop immediately:

```text
Tests failing (<N> failures). Must fix before completing:

[Show failures]

Cannot proceed with merge or pull request until tests pass.
```

Do not present integration options or proceed to step 2 while tests fail.

If tests pass, proceed to step 2.

Completion criterion. The test suite command exits with status code 0 and zero failing assertions.

### Step 2. Determine base branch

Identify the base branch using `git merge-base`:

```bash
git merge-base HEAD main 2>/dev/null || git merge-base HEAD master 2>/dev/null
```

If the base branch remains ambiguous, ask the user to confirm whether the branch split from `main`, `master`, or another target branch.

Completion criterion. The target base branch name is verified and recorded.

### Step 3. Present branch options

Present exactly four numbered options to the user:

```text
Implementation complete. What would you like to do?

1. Merge back to <base-branch> locally
2. Push and create a Pull Request
3. Keep the branch as-is (I'll handle it later)
4. Discard this work

Which option?
```

Do not add extra commentary or expand the option list. Keep the prompt text exact.

Completion criterion. The user receives the four numbered choices and pauses execution for the user selection.

### Step 4. Execute chosen branch option

#### Option 1. Merge locally

Check out the base branch, pull latest upstream commits, and merge the feature branch:

```bash
git checkout <base-branch>
git pull
git merge <feature-branch>
```

Run the project test suite against the merge result. If tests pass, delete the feature branch:

```bash
git branch -d <feature-branch>
```

Then proceed to step 5 to clean up the worktree.

#### Option 2. Push and create pull request

Push the feature branch to the remote repository and open a pull request:

```bash
git push -u origin <feature-branch>
gh pr create --title "<title>" --body "$(cat <<'EOF'
## Summary
<2-3 bullets of what changed>

## Test Plan
- [ ] <verification steps>
EOF
)"
```

Preserve the worktree so that reviewers or continuous integration feedback can be addressed locally.

#### Option 3. Keep branch unchanged

Inform the user that the branch remains active and the worktree at `<path>` is preserved:

```text
Keeping branch <name>. Worktree preserved at <path>.
```

Do not remove the worktree.

#### Option 4. Discard branch

Prompt for explicit confirmation before destroying any commits:

```text
This will permanently delete:
- Branch <name>
- All commits: <commit-list>
- Worktree at <path>

Type 'discard' to confirm.
```

Wait for the user to type `discard`. If confirmed, switch branches and force delete the feature branch:

```bash
git checkout <base-branch>
git branch -D <feature-branch>
```

Then proceed to step 5 to clean up the worktree.

Completion criterion. The chosen option commands complete without error, and git repository state matches the selected outcome.

### Step 5. Clean up worktree

For option 1 (merge locally) and option 4 (discard), remove the isolated worktree after completing branch operations.

Check if the current directory is an active worktree:

```bash
git worktree list | grep $(git branch --show-current)
```

If an isolated worktree path matches, remove it:

```bash
git worktree remove <worktree-path>
```

For option 2 (push and create pull request) and option 3 (keep branch unchanged), preserve the worktree.

Completion criterion. The worktree is removed for options 1 and 4, or confirmed preserved for options 2 and 3.

## Quick reference

| Option | Merge locally | Push to remote | Retain worktree | Delete branch |
|---|---|---|---|---|
| 1. Merge locally | Yes | No | No | Yes |
| 2. Create pull request | No | Yes | Yes | No |
| 3. Keep as-is | No | No | Yes | No |
| 4. Discard | No | No | No | Yes (force) |

## Common mistakes

| Mistake | Consequence | Correct action |
|---|---|---|
| Skipping test verification | Merges broken code or opens a failing pull request | Run the test suite before presenting options. |
| Asking open-ended questions | Introduces ambiguity and delays completion | Present the exact four numbered options. |
| Removing worktrees prematurely | Destroys local environments needed for pull request review | Remove worktrees only for options 1 and 4. |
| Deleting work without confirmation | Causes permanent loss of unmerged commits | Require explicit typed confirmation before running destructive commands. |

## Invariants

- Never proceed with failing tests. Stop immediately and display the test runner output.
- Never merge code into the base branch without running the test suite on the merged result.
- Never delete branches or worktrees destructively without receiving typed user confirmation.
- Never force-push branches to remote repositories unless the user explicitly requests a force push.
- Always verify all automated tests pass before presenting integration options.
- Always present exactly the four specified numbered choices.
- Always preserve worktrees when creating pull requests or keeping branches unchanged.

## Related skills

### Upstream callers
- `subagent-driven-development`, step 7, after completing all tasks.
- `executing-plans`, step 5, after completing all task batches.

### Companion skills
- `using-git-worktrees`, which provisions the isolated worktrees cleaned up by this skill.
