# Git merge and rebase conflict resolution

A structured five-step protocol for resolving git merge and rebase conflicts cleanly without losing changes or introducing regressions.

## 1. Inspect intent and branch context

Never resolve conflict markers blindly. Inspect the history and intent of both branches first:

1. Identify the upstream branch and the current branch commit messages:
   ```bash
   git log --oneline -n 5 HEAD
   git log --oneline -n 5 MERGE_HEAD # for merge
   # or inspect REBASE_HEAD / ORIG_HEAD during rebase
   ```
2. Review the pull request description, issue tickets, or commit messages to understand the architectural intent behind both changes.

## 2. Inventory conflicting files

List all unresolved conflict paths in the working tree:

```bash
git status -s | grep -E "^(UU|AA|UD|DU)"
```

Focus on one file at a time. Do not attempt mass edits across multiple conflicting files in a single pass.

## 3. Resolve conflicts per hunk

Open each conflicting file and examine the conflict boundaries:

1. Locate conflict delimiters (`<<<<<<<`, `=======`, `>>>>>>>`).
2. Classify the conflict nature:
   - Orthogonal edits. Both branches modified adjacent lines for independent reasons. Keep both modifications in logical sequence.
   - Competing edits. Both branches modified the exact same expression or function. Choose the version that aligns with the approved specification.
   - Deletion conflicts. One branch edited a function while another branch deleted or renamed it. Trace the new call sites before discarding changes.
3. Clean all delimiter lines completely before saving. Never commit partial conflict markers into the codebase.

## 4. Run automated verification before staging

Do not mark conflicts as resolved before validating correctness:

1. Run the test suite on the affected files:
   ```bash
   pytest path/to/test.py
   # or npm test -- path/to/test.ts
   ```
2. Run the linter and type checker across the modified paths.
3. Once all checks pass, stage the resolved file:
   ```bash
   git add <resolved-file>
   ```

## 5. Conclude merge or rebase

Finalize the git operation cleanly:

- For merge conflicts, run `git commit` to write the standard merge commit.
- For rebase conflicts, run `git rebase --continue` to advance to the next patch.
- Prohibited action. Never execute `git merge --abort` or `git rebase --abort` when encountering hard conflicts without explicit user confirmation.
