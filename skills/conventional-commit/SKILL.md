---
name: conventional-commit
description: Use when creating atomic git commits adhering to the Conventional Commits specification, staging selective hunks, or writing commit messages. Don't use for merge commits or branch cleanup.
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
6. Never amend, rebase, or force-push commits created in previous sessions.
7. Consult `references/resolving-conflicts.md` to resolve merge or rebase conflicts before staging.

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

Determine whether the project or user prefers **oneline** or **multiline** commits:

#### Format Options

1. **Oneline Mode (Single-line)**:
   - Format: `<type>[optional scope]: <description>`
   - Use when the subject line alone conveys complete intent, or when the user / repository standard requires compact commit history.
   - Do NOT include empty lines, bodies, descriptions, or footers.
   - Example: `feat(ui): add custom-select blade component`

2. **Multiline Mode**:
   - Format:

     ```text
     <type>[optional scope][!]: <description>

     [optional body]

     [optional footer(s)]
     ```

   - Use when detailing complex reason, migration guides, breaking changes (`BREAKING CHANGE:`), or tracking issue references (`Closes: #123`).

#### Rules for message components

Rules for message components:

- Type. Pick one standard type documented in `references/commit-types.md` (`feat`, `fix`, `refactor`, `perf`, `test`, `build`, `ci`, `docs`, `style`, `chore`, `revert`).
- Scope. Add a scope only when changes are isolated to a single bounded module, package, or directory. Use lowercase kebab-case naming, such as `fix(auth):` or `feat(api):`. Omit the scope for repository-wide changes.
- Breaking change marker. Add `!` immediately before the colon when upgrading requires consumers to modify their code. Always pair `!` with a `BREAKING CHANGE:` footer detailing the migration.
- Description. Use imperative present tense (`add` instead of `added`, `fix` instead of `fixes`). Start with lowercase, omit trailing periods, and keep the line under 72 characters.
- Body. Optional. Wrap at 72 characters. Explain the motivation and constraints rather than restating the diff.
- Footers. Optional. Include issue references (`Closes: #123`) or migration guides (`BREAKING CHANGE: payload key renamed to data`).

Optional co-author trailer:

- Include a co-author trailer only when the user requests it or repository guidelines require attribution.
- Resolve identity strictly from real sources, including explicit user prompt, git configuration (`git config --get coauthor.name`), or existing repository history. If no real identity exists, omit the trailer.
- Place the trailer at the bottom of the footers block separated by a blank line:

```text
Co-authored-by: Name <email@example.com>
```

Completion criterion. A commit message matching Conventional Commits syntax with a lowercase imperative subject under 72 characters.

### Step 5. Commit

#### For Oneline Commits (Single-line):

```bash
git commit -m "feat(ui): add custom-select blade component"
```

#### For Multiline Commits:

Commit using a heredoc so multi-line messages and blank lines are preserved:

```bash
git commit -F - <<'EOF'
fix(auth): reject expired refresh tokens on rotation

Validate expiry timestamp before generating a replacement token pair.
Returns 401 instead of propagating stale sessions.

Closes: #341
EOF
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

| Mistake                              | Consequence                                      | Correct approach                                                        |
| ------------------------------------ | ------------------------------------------------ | ----------------------------------------------------------------------- |
| Running `git add .` indiscriminately | Bundles unrelated edits and generated files      | Stage specific paths or use `git add -p`                                |
| Vague subject like `fix: bug fix`    | Changelog provides zero actionable context       | Describe what was repaired, like `fix(cart): clear discounts on logout` |
| Scope used on broad sweep            | Misrepresents change blast radius                | Omit scope on global changes                                            |
| Adding `!` without breaking footer   | Leaves consumers without migration details       | Always provide a `BREAKING CHANGE:` footer                              |
| Fabricating co-author identity       | Injects false attribution into permanent git log | Omit trailer when no identity is provided                               |
| Merging formatting and logic         | Hides logic changes during code review           | Split into a `style:` or `refactor:` commit first                       |
