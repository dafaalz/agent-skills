---
name: ux-review
description: Use when auditing product user experience, task flows, cognitive load, form usability, error resilience, or mobile interaction ergonomics.
---

# UX review

Audit user experience, interaction friction, cognitive load, and usability heuristics with empirical evidence.

## Overview

Audit interfaces and task journeys across six domains. These cover usability heuristics, cognitive psychology laws, information architecture, form ergonomics, system status transparency, and mobile touch mechanics. Focus on task completion barriers, working memory overload, and recovery failures. Consult reference documents in `references/` on demand.

## Workflow router

Identify user intent and route the evaluation sequence immediately:

1. **Task flows and journey audits.** When inspecting multi-step workflows like onboarding, checkout, registration, or wizards, read `references/task-flows-and-ia.md`. Inspect step branching, progress indicators, drop-off risks, and Lostness Metric.
2. **Component and form usability audits.** When inspecting inputs, dialogs, empty states, or destructive actions, read `references/forms-and-error-recovery.md`. Inspect label alignment, validation timing, autosave resilience, and undo patterns.
3. **Pull request and git diff UX audits.** When reviewing code diffs touching interfaces, read `references/heuristics-and-principles.md`. Scan for blocked back navigation, removed focus states, premature validation triggers, and missing loading states.

## Execution invariants

Enforce these execution invariants during review:

1. **Audit interaction friction over styling.** Focus on task completion time, cognitive load, error rates, and mental model mismatches. Disregard decorative aesthetics, custom fonts, and personal taste.
2. **Enforce exact cognitive thresholds.** Take empirical numbers from reference documentation. Enforce Nelson Cowan 4-chunk limits, Doherty 400ms feedback bounds, and Fitts's Law 48px touch targets without inventing arbitrary thresholds.
3. **Use undo for reversible actions.** Prescribe instant execution paired with a 5 to 10 second undo toast. Avoid modal confirmation dialogs because habituation renders repeated confirmation prompts ineffective against slips.
4. **Prevent unrecoverable data loss.** Flag any form or workflow that wipes user input on network drops, session expiries, or back navigation as an automatic blocker.

## The evaluation sequence

Follow these four steps in sequence:

### Step 1. Goal and persona resolution

Define the evaluation scope and baseline user intent before inspecting screens or code:

1. Identify the primary task goal that the user attempts to achieve on the target screen or workflow.
2. Define the assumed mental model, domain familiarity, and operating environment of the user.
3. Map the minimum theoretical steps required to complete the task.
4. Record excluded views, third-party redirects, and out-of-scope backend processes.

Completion criterion. A written record naming the target user goal, baseline mental model, and optimal step count.

### Step 2. Friction and cognitive load scan

Scan the interface for immediate cognitive and motor friction:

1. Count the number of choices presented simultaneously. Apply Hick-Hyman Law and flag choice overload if raw options exceed 5 to 7 without grouping.
2. Audit working memory demands against Nelson Cowan 4-chunk limits. Flag forms or menus that require holding more than 4 distinct items in memory.
3. Check spatial layout against Gestalt laws of proximity, similarity, continuity, and figure-ground contrast.
4. Measure touch targets and spacing against Fitts's Law standards.

Completion criterion. A documented list of cognitive bottlenecks, chunking violations, and motor target deficiencies.

### Step 3. Ordered domain evaluation

Audit target interfaces across each domain in sequence. Consult reference documents in `references/` on demand:

1. **Usability heuristics and principles.** Check NN/g 10 heuristics, Norman signifiers and constraints, Shneiderman golden rules, and ISO 9241-110 dialogue standards. Read `references/heuristics-and-principles.md`.
2. **Cognitive laws and psychology.** Check Fitts's Law, Hick-Hyman Law, Doherty Threshold, Peak-End Rule, and Zeigarnik Effect. Read `references/cognitive-laws.md`.
3. **Information architecture and task flows.** Check four IA systems, Krug scannability, progressive disclosure 80/20 rule, and Lostness Metric. Read `references/task-flows-and-ia.md`.
4. **Form usability and error recovery.** Check top-aligned labels, single-column paths, inline validation timing, Poka-Yoke constraints, and graceful undo. Read `references/forms-and-error-recovery.md`.
5. **System status and states.** Check six-state completeness across empty, partial, loading, error, success, and rollback states, skeleton screens versus spinners, and optimistic UI. Read `references/system-status-and-states.md`.
6. **Mobile touch ergonomics.** Check Steven Hoober thumb zones, Josh Clark natural reach, 48px touch target dimensions, and modal sheet detents. Read `references/mobile-touch-ergonomics.md`.

Completion criterion. Target interfaces evaluated across all six domains with zero skipped categories.

### Step 4. Metric-backed report consolidation

Consolidate findings into a structured report following the format in `references/report-format.md`:

1. Classify each finding into `Blocker`, `Warning`, or `Nit` severity tiers.
2. Present findings using the Before, After, and Why comparison format.
3. Attribute every finding to a specific cognitive law, heuristic, or empirical research citation.
4. Provide concrete, actionable code diffs or interface copy adjustments for every finding.
5. Project the impact on quantitative usability metrics including Task Completion Rate (TCR), Single Ease Question (SEQ), or Drop-off Rate.

Completion criterion. A formatted report containing categorized findings, Before-After-Why evidence tables, and projected usability impacts.

## Never ship UX checklist

Audit designs and implementations against this checklist. Every item represents an automatic rejection:

| Never | Instead |
| --- | --- |
| Placeholder attribute used as form field label | Persistent `<label>` element above the input field |
| Border and text turning red while the user is actively typing | Delay error validation until `onBlur`, then live revalidate on `onInput` |
| Disabled submit button with no explanation | Keep submit button enabled, show inline errors and jump to first invalid field on click |
| Multi-column form layouts with zig-zagging fields | Single-column linear vertical layout |
| Modal confirmation popup on reversible actions | Instant execution with 5 to 10 second undo toast notification |
| Destructive permanent deletion executed via single regular button | Deliberate friction requiring resource name confirmation or typed confirmation |
| Form fields wiped clean on server validation error or network timeout | Preserve all input state locally and flag only the invalid field |
| Silent operation with no feedback during 400ms to 1000ms latency | Subtle inline spinner or button loading state |
| Generic error message stating "An error occurred" | Specific error copy explaining what failed and concrete steps to recover |
| Entire screen replaced by a single spinner on initial page load | Skeleton screens matching destination layout structure |
| Primary mobile action placed in top corners (Ow Zone) | Sticky bottom button or bottom app bar in the Natural Thumb Zone |
| Rejection of telephone or card numbers because of spaces or hyphens | Permit flexible input formatting per Postel's Law and sanitize on submission |
| Password masked with dots without an unmask toggle | Show/Hide password toggle accessible via keyboard and screen reader |
| Wall of 10+ inputs presented in a single unstructured page | Multi-step flow chunked into 3 to 4 logical fields per step with visual progress |
| Empty state rendered as blank white space | Instructive empty state explaining zero data and primary action to populate |
| Dropdown containing 15+ unranked options without search | Searchable combobox or progressive selection hierarchy |

## Quick verification checklist

Run this check before finishing any UX audit:

| Check | Passing condition |
| --- | --- |
| Persona and intent | Target user goal and baseline mental model recorded |
| Cognitive limits | Choices pruned to 5 to 7 items, chunking conforms to Nelson Cowan 4-item limit |
| Domain coverage | All six reference domains audited with zero skipped domains |
| Error resilience | Form recovery, draft persistence, and undo mechanisms verified |
| Latency budgets | Feedback latency under 100ms, progress bars present for actions exceeding 10s |
| Report structure | Findings formatted with severity tier, Before-After-Why tables, and research citations |
