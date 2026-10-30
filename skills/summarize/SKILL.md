---
name: summarize
description: Use when generating structured session execution summaries, documenting root causes, evidence tables, or transferring context between agent sessions. Don't use for human-facing documentation (use technical-writing) or pull request bodies (use pull-request).
---

# Summarize

Produce an accurate, structured record of session execution. Write for two consumers: the user who verifies changes and a subsequent agent session that continues the work without rediscovery.

<HARD-GATE>
Write-Target Boundary. Summarization operates strictly in a read-only and reporting capacity. Write only to `.agents/state/summarize/` or user-facing execution reports. Never edit application code, alter configuration files, or execute mutating commands while creating summaries.
</HARD-GATE>

## Modes

Declare the active operating mode before executing any steps:
- Summary mode (default): Distill session activities, modifications, and findings into structured evidence tables. Run Steps 1 through 3 sequentially and emit `.agents/state/summarize/session-summary.md`.
- Incident and handoff mode: Package system state, active variables, and failure timelines for incident audits or agent handoffs. Run Steps 1 through 4 sequentially and emit `.agents/state/summarize/incident.json` alongside the summary document.

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

Completion criterion. `.agents/state/summarize/state-inventory.json` exists on disk with `modified_files`, `created_files`, `deleted_files`, and `executed_commands`.

### Step 2. Synthesize actions and root causes

Draft overview, chronological actions table, and root-cause breakdowns citing concrete file paths and test outputs.

Completion criterion. Chronological actions and resolved issues drafted with zero unverified claims and zero omitted failures.

### Step 3. Tabulate verification and gaps

Construct the verification evidence table and document known gaps, unverified edge cases, and next steps plainly.

Completion criterion. `.agents/state/summarize/session-summary.md` exists on disk containing the verification evidence table with exact exit codes and unverified items explicitly cataloged.

### Step 4. Context handoff assembly

When operating in Incident and handoff mode, package system state, branch pointers, entry points, and root-cause details into machine-readable handoff artifacts.

Completion criterion. `.agents/state/summarize/incident.json` exists on disk recording `incident_trigger`, `root_cause`, `preventive_rule`, and `handoff_block`.

## Execution summary structure

Render sections in sequence. Omit a section only when empty, stating the omission explicitly:

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

### 3. Issues and root causes
Document every encounter with bugs or failures:
- Symptom: Observed error text and stack traces.
- Root cause: Underlying system defect and mechanism.
- Evidence: File path, line number, or command output proving the root cause.
- Fix: Architectural modification addressing the root cause.
- Verification: Command executed to validate the fix.

### 4. Verification evidence table
Record verification commands with exact output:

| Check | Command | Result |
|---|---|---|
| Type check | `npx tsc --noEmit` | Passed. 0 errors |
| Test suite | `npm test` | Passed. 42 passed, 0 failed |
| Linter | `npm run lint` | Passed. Clean output |
| Build | `npm run build` | Passed. Output generated in `dist/` |

### 5. Known gaps and unverified items
State gaps without softening: untested code paths, unverified deployment steps, or open questions requiring decisions.

### 6. Actionable next steps
Numbered list of concrete next tasks.

### 7. Agent handoff block
Append this structured block for subsequent agents:

```markdown
## Context handoff
**State** Completed feature implementation, pending PR creation.
**Branch** `feat/session-refresh`
**Entry point** `src/auth/session.ts`
**Verification command** `npm test && npm run build`
**Open tasks** Caller migration documented in next steps.
**Caution** Do not revert schema migration timestamp constraint.
```

## Anti-patterns

| ID | Title | Pattern description | Why it fails | Concrete fix |
|---|---|---|---|---|
| SUM-1 | Ungrounded claims | Asserts tests passed without running the verification command | Subsequent agents inherit broken state | Execute command and record raw exit code |
| SUM-2 | Narrative walls | Packs actions and diffs into continuous narrative paragraphs | Handoff details get lost in conversational text | Tabulate actions and verification in tables |
| SUM-3 | Emotional spin | Phrases outcomes as "We made amazing progress on the bug" | Masks unresolved risks and blocker items | Use objective metrics and explicit gap lists |
| SUM-4 | Unanchored paths | References modified files without line numbers or paths | Readers cannot inspect or verify changes | Format all modified paths as markdown links |
| SUM-5 | Concealed failure | Omits failed attempts or intermediate errors from report | Future agents repeat the identical failing path | Document failed attempts and underlying causes |
| SUM-6 | Hollow handoff | Transfers context without exact verification commands | Incoming agent wastes turns rediscovering state | Include exact entry point and verification commands |

## Boundary isolation

Summarization operates strictly in an analytical and reporting capacity. Never edit application code, alter configuration files, or execute mutating commands while creating summaries.

## Quick audit checklist

Audit summaries against this table before finalizing:

| Check | Passing condition |
|---|---|
| Verification evidence | Execute verification commands and record exact outputs |
| Failure disclosure | Record failures, discarded paths, and root causes plainly |
| Completion claims | Record verified facts only, never present plans as modifications |
| Status structure | Use structured tables with command, path, and result columns |
| Directness | Present findings directly without filler or introductory fluff |
| Anti-patterns | Anti-pattern table adheres to 5-column schema with stable IDs |
| File anchoring | Cite exact repository file paths and line numbers |
