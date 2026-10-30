---
name: agent-planning
description: "Use when authoring multi-task execution plans, defining acceptance criteria for tasks spanning multiple files or repos, verifying plan evidence before submission, or responding to audit feedback. Don't use for single-task drafting (use writing-plans), batch execution (use executing-plans), external model prompting (use web-advisor-prompt), UI styling (use frontend-design), or UX critique (use ui-ux-review)."
---

# Agent Planning & Empirical Verification

Governs the authoring, verification, and audit response discipline for complex multi-task execution plans. Enforces strict empirical verification standards, boundary assertions, rate-limit budgeting, and immutable sealed-state amendments.

<HARD-GATE>
Write-Target Boundary. Read-only outside the declared plan paths. Writes are permitted only to the declared plan file and under `.agents/state/` for plan-audit.md, plan-evidence/, and blockers. Do not edit application source, tests, schemas, or configuration during plan authoring or verification. Any state mutation outside `.agents/state/` requires an explicit user-approved amendment and a recorded rollback command.
</HARD-GATE>

## Modes

Select a mode before Step 1.
- Author mode (default). Draft a new multi-task plan. Run Steps 1 through 4.
- Verification mode. Audit an existing plan without changing task status. Run Step 1, Step 2, and Step 4. Step 3 is skipped because verification produces no new plan artifacts.
- Audit-response mode. Amend a sealed plan only through the amendment ceremony. Run Steps 1 through 4.

Precedence. `writing-plans` owns task content and plan structure. This skill owns the evidence seal and audit response.

## Reference quick routing

| Topic / Phase | Reference File | Cap |
|---|---|:---:|
| Authoring discipline & invariants | [plan-authoring-discipline.md](references/plan-authoring-discipline.md) | <= 200 |
| Pre-submission readiness checklist | [plan-readiness-checklist.md](references/plan-readiness-checklist.md) | <= 200 |
| Audit feedback & blocker response | [audit-response-discipline.md](references/audit-response-discipline.md) | <= 200 |
| Auditor & advisor verification discipline | [auditor-and-evaluator-discipline.md](references/auditor-and-evaluator-discipline.md) | <= 200 |

## Core Principles

1. **Empirical primacy.** An assertion without a corresponding raw stdout capture is unverified speculation. Never predict what a command will do. Run it and report what it did.
2. **Ground-truth boundaries.** Always inspect boundaries with `sed -n` or interactive slice checking before committing slicing scripts to plans.
3. **Sealed state invariance.** A task that has been formally verified and sealed is immutable. Altering its artifacts requires an explicit amendment ceremony.
4. **Bidirectional accountability.** Evaluator and auditor commands must be verified against target environments to ensure reproducible truth.

## Workflow

### Step 1. Intake and target map

Record the plan path, target files, acceptance criteria, and rollback command.

Completion criterion. `.agents/state/plan-audit.md` exists and lists every target path with an acceptance criterion and rollback command.

### Step 2. Author or verify

Run the mode selected above.

Completion criterion. Author mode leaves the declared plan file with numbered tasks, binary acceptance criteria, and exact verification commands. Verification mode leaves `.agents/state/plan-audit.md` with one defect per line and a rule ID.

### Step 3. Evidence seal

Capture raw stdout for every verification command.

Completion criterion. `.agents/state/plan-evidence/` contains one file per command and the plan references each evidence file path.

### Step 4. Submission gate

Present the plan path and evidence paths to the user.

Completion criterion. `.agents/state/plan-approval.json` exists with `approved: true` and the approved path. No task is sealed before that file exists.

## Anti-patterns

| ID | Title | Pattern description | Why it fails | Concrete fix |
|---|---|---|---|---|
| APA-1 | Disjunctive gate | Approves a plan or an audit report in one criterion | No single artifact proves readiness | Split the criterion by mode |
| APA-2 | Read-only gate, writing step | Forbids plan writes in the gate and requires them in Step 2 | The agent must violate the gate | Carve the plan file into the write set |
| APA-3 | Undefined mode traversal | Declares modes without naming the steps each runs | Verification mode executes authoring steps | State the step set per mode |
| APA-4 | Unsealed approval | Treats chat approval as the seal | No audit trail for the approval | Write `.agents/state/plan-approval.json` |

## Boundary isolation

Plan authoring and verification stay inside the declared plan file and `.agents/state/`. Do not edit application source, test suites, schemas, or configuration while a plan is open. Any change outside those paths needs a recorded amendment and a rollback command.

## Quick audit checklist

| Check | Passing condition |
|---|---|
| Hard gate | Read-only boundary observed outside plan paths and state artifacts |
| Mode selected | Explicit branch between author, verification, or audit response |
| Empirical evidence | Raw stdout captured for every verification assertion |
| Sealed state | No post-hoc mutations without explicit amendment ceremony |
