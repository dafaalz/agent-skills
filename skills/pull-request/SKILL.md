---
name: pull-request
description: Use when drafting, reviewing, or structuring pull request descriptions with visual summaries, before-and-after verification evidence, and merge-danger risk assessments. Don't use for atomic git commit messages (use conventional-commit), branch cleanup, or direct git push.
allowed-tools: Bash Read Grep Glob
---

# Pull request

Structure pull request bodies that convey intent immediately to reviewers, provide before-and-after verification evidence, and classify operational merge risk.

## Boundary isolation

Pull request authoring reads git diffs, commit histories, and test results. Never alter application code, run destructive git resets, or amend previous session commits while drafting pull request descriptions.

## Principles and constraints

1. Smallest visual summary. Open the pull request with the smallest visual artifact that makes the change clear: an ASCII diagram, a schema diff table, or terminal before-and-after logs.
2. Concrete verification evidence. Include exact test commands, exit codes, and output snippets. Never assert that changes work without recorded tool verification.
3. Merge-danger call. Classify every pull request as a two-way door (reversible without state corruption) or a one-way door (destructive migrations, auth alterations, external webhook updates) with an explicit blast radius estimate.
4. Unslop compliance. Zero em dashes, zero en dashes, and zero hyphens acting as dashes. Use colons only before lists, tables, or code blocks.
5. Line budget. Keep the main pull request template concise and under 150 lines.

## Modes

Select a mode before Step 1:
- Draft mode (default). Inspect current branch changes against the base branch and compose the complete pull request description.
- Audit mode. Review an existing pull request body against the risk rubric and verification checklist without publishing.

## Workflow

Follow these five steps in sequence.

### Step 1. Diff inspection and commit log audit

Inspect the branch divergence against the target upstream branch before drafting:

```bash
git log origin/main..HEAD --oneline
git diff origin/main...HEAD --stat
```

1. Identify modified subsystems, new dependencies, schema migrations, and configuration updates.
2. Verify that all commits follow the Conventional Commits specification.
3. Confirm that zero secret files (`.env`, `credentials.json`) exist in the diff.

Completion criterion. Inventory of modified files, commit log, and target base branch confirmed.

### Step 2. Visual summary formulation

Construct the smallest visual representation that explains the core change:

- For architectural or routing changes, render an ASCII data flow diagram.
- For database migrations or model shifts, render a before-and-after schema table.
- For frontend UI changes, link the verified screenshot or DOM inspection table.
- For CLI or performance changes, render a before-and-after command output block.

Completion criterion. One compact visual representation drafted that communicates the primary delta without requiring full diff reading.

### Step 3. Merge-danger and blast radius assessment

Evaluate operational risk before assembling the final description:

1. Classify the decision type:
   * Two-way door. The change can be reverted cleanly with `git revert` with zero persistent state corruption or data loss.
   * One-way door. The change involves destructive migrations, external API contracts, token invalidations, or live data backfills that require a choreographed rollback plan.
2. Determine blast radius:
   * Low. Confined to internal utilities, isolated components, or behind disabled feature flags.
   * Medium. Touches primary controllers, shared services, or active cache layers.
   * High. Alters authentication, authorization boundaries, billing, or core relational schemas.
3. Document the rollback plan: state the exact command or procedure required if the deployment must be aborted.

Completion criterion. Merge-danger classification, blast radius, and rollback plan documented.

### Step 4. Verification evidence compilation

Gather and format deterministic verification results:

1. Execute test suites and linters covering the affected paths:
   ```bash
   npm test
   # or
   pytest
   ```
2. Capture exact test counts, pass rates, and execution time.
3. Document manual verification steps if the change involves interactive UI or external services.

Completion criterion. Test execution output captured showing exit code 0 across affected suites.

### Step 5. Body assembly and registration

Assemble the pull request description using the standard template below:

1. Combine the visual summary, summary bullet points, merge-danger call, verification evidence, and tracking links.
2. If the user requests publishing via GitHub CLI, output the command:
   ```bash
   gh pr create --title "type(scope): description" --body-file pr-body.md
   ```
3. If running in a collaborative harness supporting pull request tracking, link the pull request URL immediately.

Completion criterion. Pull request markdown document delivered passing all checklist checks.

## Pull request template

Use this standard layout for pull request descriptions:

````markdown
## Summary

[One to two sentences stating the objective and mechanism]

### Visual summary

```text
[ASCII diagram, schema delta, or before-and-after flow]
```

## Changes

- [Component]: [Exact change applied]
- [Test]: [Regression test added]

## Merge danger and operational risk

- **Decision type:** [Two-way door | One-way door]
- **Blast radius:** [Low | Medium | High]
- **Rollback strategy:** [git revert <hash> | specific rollback steps]

## Verification evidence

```text
[Command run and test runner output confirming exit code 0]
```

## Related issues

Closes #[Issue Number]
````

## Quick audit checklist

| Check | Passing condition |
|---|---|
| Visual summary | Includes an ASCII flow, schema table, or terminal delta |
| Merge danger | Classified as two-way or one-way door with explicit blast radius |
| Rollback plan | States exact command or procedure to reverse the change |
| Verification | Cites fresh command output and test suite results with exit code 0 |
| Conventional title | PR title matches `<type>(<scope>): <description>` format |
| Clean diff | Zero secrets, temporary probes, or orphan files present |
