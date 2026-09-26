---
name: qa-engineer
description: Use when testing features from a user perspective, executing exploratory test charters, auditing PR diffs, investigating test flakiness, or verifying release quality gates.
---

# QA engineer

Verify application quality through structured test matrices, exploratory charters, failure injection, and automated pipeline gates across web, API, and database layers.

Read the reference guides before initiating targeted sweeps:
* `references/exploratory-charters.md` for session charters, boundary value analysis, equivalence partitions, state transitions, and error guessing.
* `references/bug-report-template.md` for defect reproduction templates, technical evidence capture, severity triage, and release sign-off verdicts.
* `references/quality-gate-checklist.md` for pipeline latency limits, flaky test quarantine protocols, differential mutation thresholds, performance budgets, and security scans.
* `references/lighthouse-ci.md` for automated Core Web Vitals performance gating, median-of-N collection, and CI assertions.

## Workflow

Execute the six verification steps in sequence. Complete the binary verification criterion of each step before advancing to the next.

### Step 1. Scope and acceptance mapping

Deconstruct specifications, pull request diffs, and user stories into unambiguous assertions:

1. Map every business requirement to verifiable user actions and expected system states.
2. Review implementation code diffs to uncover unstated assumptions, implicit defaults, altered shared models, and newly exposed endpoints.
3. Identify external integration points such as payment gateways, webhooks, and asynchronous message queues.
4. Establish scope boundaries separating Tier 1 core user flows from lower priority edge validations.

Completion criterion. All acceptance criteria and code modifications map directly to test scenarios with explicit input conditions and expected system states.

### Step 2. Test matrix generation

Synthesize test matrices using formal black box test design techniques before touching runtime environments:

1. Apply boundary value analysis to every numeric range, string length, array capacity, and timestamp. Probe two-value and three-value boundaries at the edges.
2. Construct equivalence partitioning tables. Group inputs into valid and invalid partitions, selecting representative samples for each class.
3. Model dynamic entity lifecycles as finite state machines. Create state transition matrices covering all valid transitions and asserting that invalid transitions fail.
4. Apply error guessing heuristics targeting concurrency, nullability, character encoding anomalies, zero values, and network faults.

Completion criterion. A test matrix document exists covering boundary conditions, equivalence partitions, state transitions, and error guessing vectors.

### Step 3. Interactive runtime execution

Execute test cases systematically across user interfaces, application programming interfaces, and backing data stores:

1. Interact with user interfaces through automated or manual browser sessions. Prioritize accessibility locators and verify visual element stability.
2. Submit API requests covering complete parameter variations. Verify response status codes, payload structures, header constraints, and schema contracts.
3. Inspect persistent database state directly. Confirm that mutations update target rows, maintain foreign key integrity, trigger expected audit records, and preserve tenant data isolation.
4. Capture raw technical evidence during every test step, including network request logs, server logs, and browser console output.

Completion criterion. Every scenario in the test matrix has executed against live runtime environments with verified UI, API, and database persistence states.

### Step 4. Edge case and failure injection

Stress the system against hostile conditions, timing anomalies, and infrastructure disruptions:

1. Probe concurrency boundaries with rapid duplicate submissions on transactional endpoints to verify idempotency keys and database unique constraints.
2. Inject network interrupts, client disconnects, and packet delays mid-flight during transactions. Confirm that the application recovers cleanly, releases database locks, and maintains state consistency.
3. Fuzz endpoints with extreme payloads, oversized strings, multipart file edge cases, and SQL or script injection characters.
4. Simulate downstream dependency outages. Verify circuit breaker tripping, graceful degradation, and user-facing error banners.

Completion criterion. Target features execute under concurrency stress, network interruption, and hostile payload injection with verified state consistency and zero silent failures.

### Step 5. Defect reproduction and reporting

Document all discovered anomalies using standardized defect reproduction templates:

1. Formulate defect titles using the bracketed component prefix format `[Component] Description`.
2. Assign severity tiers following deterministic definitions from Blocker to Trivial using the lookup table below.
3. Document exact prerequisites, user roles, feature flag states, and test account environments.
4. Provide step-by-step reproduction instructions starting from a clean session.
5. Contrast expected behavior against actual behavior. Attach complete technical evidence including curl commands, HTTP payloads, browser console stack traces, and backend server logs.
6. Formulate a technical root cause hypothesis pointing to specific code paths or architectural flaws.

Completion criterion. Every discovered defect has a filed report containing reproduction steps, raw technical payloads, severity triage, and root cause diagnosis.

### Step 6. Quality gate audit and release sign-off

Subject the release candidate to automated pipeline quality gates and record a definitive release verdict:

1. Audit test flakiness. Quarantine any test exhibiting flip rates above 1% and enforce a seven-day remediation SLA.
2. Validate differential mutation test scores exceeding 80% on newly introduced pull request code.
3. Confirm performance budgets. Validate that API p99 latency stays within acceptable thresholds and frontend Core Web Vitals pass Lighthouse CI targets.
4. Verify automated security scans including secret detection, dependency vulnerabilities, and dynamic vulnerability assessments.
5. Record a formal Go, No-Go, or Conditional Go release verdict documented in the release record.

Completion criterion. Quality gates have executed, flaky tests are quarantined, performance and security budgets are met, and an unambiguous release sign-off verdict is recorded.

## Quick reference matrices

### Severity triage lookup

| Tier | Name | Impact | SLA and gate condition |
|---|---|---|---|
| Sev-1 | Blocker | Core business halted, data loss, critical security compromise | Immediate hotfix, blocks all releases |
| Sev-2 | Critical | Primary workflow broken with no workaround | Blocks release candidate without executive waiver |
| Sev-3 | Major | Non-critical workflow failure, or critical failure with intuitive workaround | Fix in current sprint |
| Sev-4 | Minor | Cosmetic defect, UI misalignment, non-blocking copy error | Backlog priority |
| Sev-5 | Trivial | Typographical error in internal comments, minor padding variance | Lowest priority |

### Boundary value heuristics

| Boundary type | Test vectors | Focus |
|---|---|---|
| Numeric range | `min - 1`, `min`, `min + 1`, `nominal`, `max - 1`, `max`, `max + 1` | Off-by-one errors, underflow, overflow |
| String length | `0` (empty), `1`, `max - 1`, `max`, `max + 1` | Truncation, buffer sizing, null termination |
| Collection or array | `0` elements, `1` element, `nominal`, `max capacity`, `max + 1` | Index out of bounds, memory allocation |
| Temporal or dates | Epoch zero, leap days, DST changeover, timezone boundaries, year 2038 | Clock skew, timezone parsing, rollover |

## Quick audit checklist

Run this check before completing any testing sweep:

| Check | Passing condition |
|---|---|
| Acceptance coverage | All PR diffs and user stories map to explicit test scenarios |
| Boundary probing | Boundary value analysis and equivalence partitions recorded in test matrix |
| Runtime evidence | Raw curl commands, HTTP payloads, and database queries attached to findings |
| Failure injection | Concurrency, network interruption, and fuzz payloads executed |
| Defect formatting | Standardized bracketed titles, reproduction steps, and root cause hypothesis filed |
| Quality gates | Flakiness flip rate under 1%, mutation score over 80%, and release verdict documented |
