---
name: agent-planning
description: "Use when authoring multi-task execution plans, defining acceptance criteria for tasks spanning multiple files or repos, verifying plan evidence before submission, or responding to audit feedback. Don't use for single-task drafting (use writing-plans), batch execution (use executing-plans), external model prompting (use web-advisor-prompt), UI styling (use frontend-design), or UX critique (use ui-ux-review)."
---

# Agent Planning & Empirical Verification

Governs the authoring, verification, and audit response discipline for complex multi-task execution plans. Enforces strict empirical verification standards, boundary assertions, rate-limit budgeting, and immutable sealed-state amendments.

## Reference quick routing

| Topic / Phase | Reference File | Cap |
|---|---|:---:|
| Authoring discipline & invariants | [plan-authoring-discipline.md](references/plan-authoring-discipline.md) | <= 200 |
| Pre-submission readiness checklist | [plan-readiness-checklist.md](references/plan-readiness-checklist.md) | <= 200 |
| Audit feedback & blocker response | [audit-response-discipline.md](references/audit-response-discipline.md) | <= 200 |
| Auditor & advisor verification discipline | [auditor-and-evaluator-discipline.md](references/auditor-and-evaluator-discipline.md) | <= 200 |

## Core Principles

1. **Empirical Primacy:** An assertion without a corresponding raw stdout capture is unverified speculation. Never predict what a command will do; run it and report what it did.
2. **Ground-Truth Boundaries:** Always inspect boundaries with `sed -n` or interactive slice checking before committing slicing scripts to plans.
3. **Sealed State Invariance:** A task that has been formally verified and sealed is immutable. Altering its artifacts requires an explicit amendment ceremony.
4. **Bidirectional Accountability:** Evaluator and auditor commands must be verified against target environments to ensure reproducible truth.
