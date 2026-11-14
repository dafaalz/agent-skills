---
name: council-review
description: "Use when orchestrating an adversarial review council of independent specialized reviewer threads to stress-test designs, interactions, and accessibility. Don't use for single-thread code reviews (use code-review), single-perspective UI heuristic checks (use ui-ux-review), or greenfield design ideation (use brainstorming)."
---

# Council review

Orchestrate an adversarial council of three independent reviewer threads to stress-test a running web application.

The council assigns three specialized seats:
1. Visual and design system audit (contrast, layout resilience, token hierarchy, theme modes).
2. Interaction and motion physics audit (spring curves, touch targets, state latency, layout shifts).
3. Accessibility and WCAG audit (keyboard navigation, focus traps, semantic ARIA trees).

All three reviewer threads run with the exact provider and model of the calling conversation. Reviewers inspect running interfaces independently and score using an uncapped reductive scale starting from 10.00 without a floor at zero. Passing requires all three seats to score strictly above 9.00.

<HARD-GATE>
Write-Target Boundary. In Audit mode, do not write files outside `.agents/state/council-review/`. In Remediation mode, modify only files needed to resolve verified defects reported by council auditors. Do not edit package manifests or database schemas unless an auditor finding explicitly identifies them.
</HARD-GATE>

## Modes

Declare the execution mode before Step 1:
- Audit mode (default). Discover caller environment, spawn three independent reviewer threads, collect findings, and compile the verdict report without altering application source files.
- Remediation mode. Apply fixes for reported flaws, run verification test commands, and dispatch re-evaluation requests until all three reviewer seats score above 9.00.

## Workflow

Follow the four steps in sequence.

### Step 1. Discover caller environment and target

Query `orchestrator_capabilities` from `t3-code` following `references/orchestration-protocol.md`.

Extract these values:
1. `inheritedProviderInstanceId`
2. `inheritedModel`
3. `inheritedOptions`

Identify the active preview URL and source directories under inspection. Write the discovery state to disk.

Completion criterion. `.agents/state/council-review/discovery.json` exists on disk with `inheritedProviderInstanceId`, `inheritedModel`, and `target_url`.

### Step 2. Dispatch three independent reviewer threads

Read prompts from `references/council-prompts.md`.

Format three audit prompts with the active URL and source paths:
1. Seat 1 for visual polish and design system consistency.
2. Seat 2 for interaction ergonomics and motion physics.
3. Seat 3 for WCAG 2.1 and 2.2 AA accessibility compliance.

Spawn all three threads in one call to `create_threads` following `references/orchestration-protocol.md`. Set `target` on each thread to the discovered provider instance ID and model. Reviewers must never read sibling threads.

Completion criterion. `.agents/state/council-review/council-session.json` exists on disk containing exactly three active reviewer thread IDs.

### Step 3. Collect audits and synthesize verdict

Poll reviewer threads using `t3_thread_read` until each seat completes its evaluation.

Validate that every reviewer followed the reductive scoring formula in `references/scoring-rubric.md`:
1. Starting score is strictly 10.00.
2. Deductions map to Fatal Flaw, Structural Flaw, Serious Flaw, or Cosmetic Flaw.
3. Every deduction includes file path, line number, and visual or DOM evidence.

Compile the findings and compute the compound minimum score.

Completion criterion. `.agents/state/council-review/council-verdict.md` exists on disk recording scores and itemized deductions for all three seats.

### Step 4. Remediate defects and re-evaluate

Check if the council score clears the passing invariant:

$$\min(\text{Score}_{\text{Visual}}, \text{Score}_{\text{Motion}}, \text{Score}_{\text{A11y}}) > 9.00$$

When all three seats exceed 9.00, record completion. When any seat scores 9.00 or lower, enter the remediation loop:
1. Apply targeted code changes addressing reported file paths.
2. Run test suites and verify local preview builds.
3. Send the re-evaluation prompt from `references/council-prompts.md` to failing threads via `t3_thread_send`.
4. Read updated scores with `t3_thread_read`.

Repeat until all three seats score strictly above 9.00.

Completion criterion. `.agents/state/council-review/audit-signoff.json` exists on disk with all three seat scores strictly greater than 9.00.

## Boundary isolation

Execute council reviews with strict read-only thread separation. Write state exclusively to `.agents/state/council-review/`. Reviewer threads must never inspect sibling thread transcripts or mutate application repository files. All remediation occurs through independent patch proposals verified against the council sign-off threshold.

## Anti-patterns

| ID | Title | Pattern description | Why it fails | Concrete fix |
|---|---|---|---|---|
| CR-1 | Provider drift | Hardcodes default provider instead of querying orchestrator | Reviewer threads execute on mismatched or unsupported models | Read inherited provider and model from orchestrator capabilities |
| CR-2 | Cross-thread contamination | Instructs reviewers to inspect sibling thread findings | Independent adversarial judgment is replaced by herd bias | Enforce strict isolation with forbidden cross-thread reading directive |
| CR-3 | Inflationary scoring | Starts score from 0 and adds points for good features | Critical flaws are masked by unrelated aesthetic praise | Enforce strict reductive scoring starting at 10.0 with mathematical deductions |
| CR-4 | Premature exit | Terminates audit loop when average score passes | Unresolved fatal flaws in a single seat reach production | Require minimum score across all three seats strictly above 9.0 |

## Quick audit checklist

Run this check before completing a council review:

| Check | Passing condition |
|---|---|
| Environment discovery | Discovered caller provider and model recorded in discovery JSON |
| Thread isolation | Three separate threads created with zero shared state |
| Scoring mechanics | Reductive calculation strictly from 10.00 with itemized flaws |
| Passing threshold | All three seats score strictly greater than 9.00 |
| Verification artifact | Final sign-off JSON written with scores and thread links |
