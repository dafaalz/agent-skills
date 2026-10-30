---
name: conventional-commit
description: "Use when creating atomic git commits adhering to the Conventional Commits specification, staging selective hunks, or writing commit messages. Don't use for merge commits (use pull-request) or branch cleanup (run `git branch -d` directly or use the repository's branch cleanup tooling)."
allowed-tools: Bash Read Grep Glob
---

# Conventional commit

Commit the working tree as atomic commits following the Conventional Commits 1.0.0 specification with concise imperative subjects.

## Invariants

1. Do not add a co-author trailer unless explicitly requested or mandated by repository policy. Never fabricate an identity.
2. Never use `git commit -a`. Stage files deliberately so unrelated edits cannot leak into history.
3. Never run `git add .` or `git add -A` blindly. Inspect the working tree diff first.
4. Never commit without reading the diff. The commit message must describe actual changes on disk.
5. Consult `references/commit-types.md` for standard commit types. Never invent custom types or fake scopes.
6. Create new commits for additional changes; never amend, rebase, or force-push commits created in previous sessions.
7. Consult `references/resolving-conflicts.md` to resolve merge or rebase conflicts before staging.

<HARD-GATE>
Write-Target Boundary. Manipulate git staging area and create commits only. Never modify working tree files, alter configuration files, run `git commit -a`, `git add -A`, `git add .` without inspecting diff first, or execute `git reset --hard`, `git rebase -i`, or `git push --force`. Refuse any commit whose staged diff contains a file path matching `(^|/)\.env(\.|$)|\.pem$|credentials\.json$|(^|/)dist/|(^|/)build/`.
</HARD-GATE>

## Modes

Select the commit mode before Step 1:
- Commit mode (default). Run Steps 1 through 6 in full. Write the target commit message to `.agents/state/conventional-commit/commit-msg.txt` before committing.
- Dry-run mode. Run Steps 1 through 4 only. Emit `.agents/state/conventional-commit/dry-run-plan.md` with one record per planned commit: `commit_index`, `type`, `scope`, `subject`, `body`, `footer`, `paths`. Skip Steps 5 and 6.

## Reversibility

A commit is a reversible state mutation via `git revert`. Every invocation that produces a commit must be reversible without history rewrite:
- To reverse a commit's content change, run `git revert <sha>` and use the resulting revert commit message (default: `Revert "<original subject>"`).
- To correct a commit message without changing history semantics, do not amend. Instead, create a follow-up commit of type `docs` with a body explaining the correction, or ask the user before amending.
- Commit creation, revert creation, and re-application of the fix must each round-trip cleanly without history corruption.

## Workflow

### Step 1. Inspect before staging

Run status and diff inspections to evaluate the tree:

```bash
git status --short --branch
git diff --stat
git diff --cached --stat
```

For large diffs, read changes file by file:

```bash
git diff -- <path>
git diff --cached -- <path>
```

Identify any credential files (`.env`, `*.pem`, `credentials.json`) or build output (`dist/`, `build/`). If secrets are present, unstage them immediately using `git restore --staged <path>` and alert the user.

Completion criterion. The diff and status are inspected, secrets and build artifacts are unstaged, and the change boundary is identified.

### Step 2. Decide commit count

Ensure one logical change per commit so each commit remains independently revertable.

Split the changes when:
- The working tree spans multiple commit types, such as `feat` alongside `fix`.
- Changes touch unrelated subsystems that belong in separate reviews.
- A mechanical formatting sweep is mixed with behavioral code. Always split these, because reviewers cannot spot logic changes inside wide formatting diffs.
- Dependency manifest updates are mixed with code consuming the dependency.
- Test additions for separate features are mixed together.

Do not split when changes form a single atomic unit, such as a bug fix accompanied by its regression test.

Completion criterion. A planned commit count where each planned commit contains exactly one logical, revertable change.

### Step 3. Stage one logical change

Stage specific files cleanly:

```bash
git add <path1> <path2>
```

When a single file contains mixed concerns, stage individual hunks interactively:

```bash
git add -p <path>
```

Use `s` to split hunks into the smallest possible units. Verify staged contents before writing the commit message:

```bash
git diff --cached --stat
git diff --cached
```

Completion criterion. Only the specific files or hunks for the target logical change appear in `git diff --cached`.

### Step 4. Choose format mode and compose message

Determine whether the project or user prefers oneline or multiline commits:

#### Format options

1. Oneline mode (Single-line). Syntax follows `<type>[optional scope]: <description>`. Use when the subject line alone conveys complete intent. Sample: `feat(ui): add custom-select blade component`.
2. Multiline mode. Syntax follows `<type>[optional scope][!]: <description>`, followed by optional body and optional footers (`BREAKING CHANGE:`, `Closes: #123`).

#### Message component rules

- Type. Pick one standard type documented in `references/commit-types.md` (`feat`, `fix`, `refactor`, `perf`, `test`, `build`, `ci`, `docs`, `style`, `chore`, `revert`).
- Scope. Add a scope only when changes are isolated to a single bounded module, package, or directory. Use lowercase kebab-case naming. Omit the scope for repository-wide changes.
- Breaking change marker. Add `!` immediately before the colon when upgrading requires consumers to modify their code. Always pair `!` with a `BREAKING CHANGE:` footer detailing the migration.
- Description. Use imperative present tense (`add` instead of `added`, `fix` instead of `fixes`). Start with lowercase, omit trailing periods, and keep the line under 72 characters.
- Body. Optional. Wrap at 72 characters. Explain motivation and constraints rather than restating the diff.
- Footers. Optional. Include issue references (`Closes: #123`) or migration guides (`BREAKING CHANGE: payload key renamed to data`).
- Co-author trailer. Optional. Include only when requested. Format: `Co-authored-by: Name <email@example.com>`.

In Commit mode, write the drafted message to `.agents/state/conventional-commit/commit-msg.txt`.
In Dry-run mode, write planned commit entries to `.agents/state/conventional-commit/dry-run-plan.md` and stop.

Completion criterion. In Commit mode, `.agents/state/conventional-commit/commit-msg.txt` exists on disk with a valid Conventional Commits message under 72 chars for the subject. In Dry-run mode, `.agents/state/conventional-commit/dry-run-plan.md` exists with all 7 fields populated per commit and git status untouched.

### Step 5. Commit

Commit using the drafted `.agents/state/conventional-commit/commit-msg.txt`:

```bash
git commit --file=.agents/state/conventional-commit/commit-msg.txt
```

Completion criterion. A newly minted git commit recorded in HEAD with the exact drafted message.

### Step 6. Repeat and verify

Loop back to Step 1 until the working tree is clean. Validate the resulting git history:

```bash
git status --short
git log --oneline -5
```

Verify subjects mechanically:

```bash
git log --format='%s' -5 | grep -vE '^[a-z]+(\([a-z0-9-]+\))?!?: .+$' && echo 'INVALID SUBJECTS' || echo 'all subjects valid'
```

If co-author trailers were not requested, ensure no accidental trailers were committed:

```bash
git log --format='%B' -5 | grep -iE 'co-authored-by|generated with' && echo 'UNWANTED TRAILER' || echo 'clean'
```

Completion criterion. Working tree status is completely clean and the subject verification command returns all subjects valid.

## Common mistakes

| ID | Title | Pattern description | Why it fails | Concrete fix |
|---|---|---|---|---|
| CC-1 | Blind staging | `git add .` or `git add -A` without inspecting status | Bundles unrelated edits, generated files, or secrets | Run `git status --short` and `git diff` first; stage specific paths or use `git add -p` |
| CC-2 | Vague subject | Subject like `fix: bug fix` | Changelog reader cannot determine the change | Describe the repaired behavior: `fix(cart): clear discounts on logout` |
| CC-3 | Scope on broad sweep | Applying a scope to a repository-wide change | Misrepresents blast radius and routes reviewers to wrong files | Omit scope on global changes |
| CC-4 | Breaking marker without footer | Adding `!` without `BREAKING CHANGE:` footer | Consumers see `!` but no migration guide | Always pair `!` with a `BREAKING CHANGE:` footer |
| CC-5 | Fabricated co-author | Inventing a co-author identity | Permanent false attribution in git log | Omit the trailer unless a real identity is provided |
| CC-6 | Mixed concerns | Merging formatting and logic in one commit | Reviewers cannot spot logic changes inside wide formatting diffs | Split into a `style:` or `refactor:` commit first |

## Boundary isolation

Commit operations manipulate git history and staging state only. Never modify source code, alter configuration files, or run destructive git reset or checkout commands during commit creation.

## Quick audit checklist

Run this check before completing any commit task:

| Check | Passing condition |
|---|---|
| Unstaged secrets | Zero credential files (`.env`, `*.pem`) or build artifacts in staged diff |
| Atomicity | Each commit contains exactly one logical, revertable change |
| Message syntax | Imperative subject, lowercase, under 72 chars, valid standard type |
| Breaking change | Every `!` paired with a `BREAKING CHANGE:` footer |
| Clean tree | Working tree status clean and subject verification command passes |
