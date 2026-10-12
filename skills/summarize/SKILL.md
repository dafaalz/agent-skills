---
name: summarize
description: Use when generating structured session execution summaries, documenting root causes, evidence tables, or transferring context between agent sessions. Don't use for human-facing documentation or pull request bodies.
---

# Summarize

Produce an accurate, structured record of session execution. Write for two consumers. The primary consumer is the user who verifies changes. The secondary consumer is a subsequent agent session that continues the work without rediscovery.

## Modes

Select a summarization mode before Step 1:
- Summary mode (default). Distill session activities, modifications, and findings into structured evidence tables.
- Handoff mode. Package system state, active variables, and next immediate steps for a subsequent agent or user.

## Integrity rule

Report exclusively what occurred during the current session:
- Inspect diffs directly; never claim a file changed without inspecting diffs.
- Observe clean terminal output directly; never state a test passed without observing clean terminal output.
- Record verified facts and actual results; never present plans or proposals as completed modifications.
- Record failures, discarded attempts, and dead ends so future sessions do not repeat them.
- Flag unverified paths explicitly instead of assuming success.

Inspect actual repository and working tree state before drafting:

```bash
git status --short
git diff --stat
git log --oneline -n 5
```

If the session produced no code modifications, state this directly.

## Workflow

Follow these four steps in sequence:

### Step 1. State reconnaissance and evidence extraction

Run status, diff, and log commands to inspect the exact working tree changes and recorded command runs from the session.

Completion criterion. An inventory of all modified, created, and deleted files cross-referenced with executed terminal commands.

### Step 2. Synthesize actions and root causes

Draft the overview, chronological actions table, and root-cause breakdowns citing concrete file paths and test outputs.

Completion criterion. Chronological actions and resolved issues drafted with zero unverified claims and zero omitted failures.

### Step 3. Tabulate verification and gaps

Construct the verification evidence table and document known gaps, unverified edge cases, and next steps plainly.

Completion criterion. Every automated verification command is tabulated with exact exit status and unverified areas are explicitly listed.

### Step 4. Context handoff assembly

When transferring work to another agent, append the structured handoff block that contains branch, entry point, verification commands, and open tasks.

Completion criterion. A complete session execution summary rendered to the user or persisted to disk.

## Execution summary structure

Render sections in sequence. Omit a section only when empty, stating the omission explicitly.

### 1. Overview

Two to three sentences stating session purpose, final status, and present state. The first sentence must answer whether the objective was met.

### 2. Actions taken

List chronological operations with concrete evidence in a table:

| # | Action | Target | Result |
|---|---|---|---|
| 1 | Read | `src/auth/session.ts` | Located token expiration logic |
| 2 | Edit | `src/auth/session.ts` | Added expiry guard before refresh call |
| 3 | Run | `npm test -- auth` | 14 passed, 0 failed |
| 4 | Run | `npx tsc --noEmit` | Clean run with 0 errors |

Group by category when the list grows. Categorize entries by files created, files edited, files removed, and commands executed. State what changed and why for each path.

### 3. Issues and root causes

Document every encounter with bugs or failures:

```markdown
#### Issue 1. [Concise symptom description]

**Symptom** Observed error text and stack traces.
**Root cause** Underlying system defect and mechanism.
**Evidence** File path, line number, or command output proving the root cause.
**Fix** Architectural modification addressing the root cause.
**Verification** Command executed to validate the fix.
```

Distinguish between three categories:
- User-reported defects.
- Discovered defects found during implementation.
- Pre-existing defects present before the session started.

### 4. Verification evidence table

Record verification commands with exact output:

| Check | Command | Result |
|---|---|---|
| Type check | `npx tsc --noEmit` | Passed. 0 errors |
| Test suite | `npm test` | Passed. 42 passed, 0 failed |
| Linter | `npm run lint` | Passed. Clean output |
| Build | `npm run build` | Passed. Output generated in `dist/` |

List every unverified check under Known gaps.

### 5. Known gaps and unverified items

State gaps without softening:
- Untested code paths due to missing fixtures or unavailable external APIs.
- Unverified deployment or integration behaviors.
- Open questions that require external decisions.

### 6. Actionable next steps

Numbered list of concrete next tasks:
1. Add regression test for boundary conditions at `src/auth/session.ts`.
2. Update callers that reference deprecated function signatures.
3. Fix pre-existing type warnings in legacy files.

### 7. Agent handoff block

To transfer context to another agent, append this structured block:

```markdown
## Context handoff

**State** Completed feature implementation, pending PR creation.
**Branch** `feat/session-refresh`
**Entry point** `src/auth/session.ts`
**Verification command** `npm test && npm run build`
**Open tasks** Caller migration documented in next steps.
**Caution** Do not revert schema migration timestamp constraint.
```

## Boundary isolation

Summarization operates strictly in an analytical and reporting capacity. Never edit application code, alter configuration files, or execute mutating commands while creating summaries.

## Anti-slop and precision guidelines

- State factual outcomes immediately in leading sentences.
- Prefer tables over narrative paragraphs for enumerable data.
- Cite exact file paths with line references (`src/auth/session.ts:42`).
- Quote exact error messages and exit codes verbatim.
- Drop conversational padding such as "successfully", "carefully", or "it is worth noting".
- Strip emojis and decorative styling.

## Quick audit checklist

Audit summaries against this table before finalizing:

| Anti-pattern | Correct practice |
|---|---|
| Claiming untested fixes work | Execute verification commands and record exact outputs |
| Omitting failed attempts | Record failures, discarded paths, and root causes plainly |
| Speculative completion claims | Record verified facts; never claim plans as modifications |
| Narrative status descriptions | Use structured tables with command, path, and result columns |
| Conversational padding | Present findings directly without filler or introductory fluff |
| Unanchored file references | Cite exact repository file paths and line numbers |
