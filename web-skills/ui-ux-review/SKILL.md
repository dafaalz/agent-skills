---
name: ui-ux-review
description: Use when auditing user interfaces, frontend component code, user journeys, accessibility standards (WCAG 2.2 AA), CSS layout architecture, or interaction friction. Don't use for backend logic review, database schema auditing, or build pipeline debugging.
---

# UI and UX Review for Claude Web

Audit user interfaces, frontend code, and user journeys with empirical rigor and cognitive ergonomics on Claude Web.

<initiative_and_scope>
When asked to review an interface, screenshot, or frontend code, complete the entire audit rigorously across visual mechanics, cognitive heuristics, and accessibility. Stop and report when done. Do not add unrequested feature implementations or unrelated redesigns. If you spot secondary suggestions, list them as non-blocking Nits.
</initiative_and_scope>

<claude_web_environment>
Operate within the Claude Web interface.
- Accept screenshots, UI images, Figma specs, or frontend code snippets pasted into chat or uploaded as files.
- Deliver the structured UI/UX Audit Report as a standalone Markdown Claude Artifact (`text/markdown`).
- In the chat body, provide only a high-level executive summary, key blockers, and the final verdict (`Approve` or `Changes Requested`).
</claude_web_environment>

## Execution invariants

Enforce these foundational invariants across all audits:
1. **Enforce visible focus rings.** Never accept `outline: none` without a verified replacement. Require `:focus-visible` rings with at least a 3:1 contrast ratio, 2px solid thickness, and 2px offset.
2. **Apply concentric border radii geometry.** Enforce the concentric corner formula on nested containers `R_inner = max(0, R_outer - (padding + border))`.
3. **Use discrete surface tokens for elevation.** Demand semantic surface tokens based on lightness steps instead of semi-transparent white overlays.
4. **Audit interaction friction over styling.** Focus on task completion time, cognitive load, error rates, and mental model mismatches before fine-tuning aesthetics.
5. **Use undo for reversible actions.** Prescribe instant execution paired with a 5 to 10 second undo toast. Avoid modal confirmation dialogs for routine actions.
6. **Prevent unrecoverable data loss.** Flag any form or workflow that wipes user input on network drops, validation errors, or back navigation as an automatic blocker.
7. **Enforce CSS logical properties.** Require logical properties (`margin-inline-start`, `padding-inline`) over hardcoded physical properties.

## Workflow

### Step 1. Scope and stack reconnaissance

Identify the target surface and environment from user input:
- Target type: component control, layout surface, multi-step flow, or code diff.
- Styling engine and UI library (Tailwind CSS, CSS Modules, Radix UI, Shadcn, MUI).
- Primary user goals, baseline mental models, and optimal step count.

Completion criterion. Target surface and environment parameters classified with user goals documented.

### Step 2. UI mechanics audit

Evaluate the implementation against technical and structural standards:
1. **Accessibility (WCAG 2.2 AA).** Check semantic HTML, accessible names, keyboard navigation, modal focus traps, and `:focus-visible` rings. Consult `references/accessibility.md`.
2. **Target size.** Confirm all interactive elements meet WCAG 2.2 AA minimum 24x24px bounding box (recommended 44x44px).
3. **Spatial geometry.** Verify spacing adheres to an 8pt/4pt modular scale and concentric border radii. Consult `references/layout-and-space.md`.
4. **Typography and readability.** Verify line measure between 45 and 75 characters (`max-inline-size: 65ch`), unitless line heights, and tabular figures for numbers. Consult `references/typography.md`.
5. **Color and contrast.** Verify APCA / WCAG text contrast (minimum 4.5:1 for body, 3:1 for controls). On dynamic video or animated canvas surfaces, sweep 5 milestones (0%, 25%, 50%, 75%, 100%) and verify worst-case frame contrast. Consult `references/color-and-contrast.md`.
6. **Layout stability.** Check container queries (`@container`), aspect ratios to prevent CLS, and CSS logical properties. Consult `references/component-mechanics.md`.

Completion criterion. UI mechanics findings cataloged with exact file references and CSS properties.

### Step 3. UX cognitive and journey audit

Inspect the experience through cognitive psychology heuristics:
1. **Cognitive load (Cowan 4-chunk limit).** Confirm views do not force users to hold more than four discrete working memory items simultaneously.
2. **Mental models and feedback (Doherty 400ms threshold).** Verify that user actions receive immediate feedback within 400ms. Provide progress indicators for operations exceeding 1000ms.
3. **Dead-scroll and pacing.** Detect dead-scroll zones where scrolling exceeds 300px or 50vh without perceptible visual updates or where sticky scenes stall. Consult `references/task-flows-and-ia.md`.
4. **Fitts's Law and motor ergonomics.** Check touch target hit areas, spacing between destructive triggers, and thumb-zone accessibility.
5. **Error prevention and recovery.** Verify inline real-time validation, non-destructive defaults, and undo toasts over habituation-inducing modals. Consult `references/forms-and-error-recovery.md`.

Completion criterion. Cognitive friction points and flow drop-offs documented with clear psychological heuristics.

### Step 4. Structured audit report delivery

Compile findings into a standalone Markdown Claude Artifact formatted as follows:

```markdown
# UI/UX Audit Report: [Target View/Component]

## Executive Summary
[High-level evaluation, user impact, and overall quality rating]

## Findings Matrix

| ID | Category | Severity (Blocker / Major / Minor / Nit) | Heuristic / Standard | Description and Impact | Recommendation |
|---|---|---|---|---|---|
| F-01 | A11y / UI / UX | Blocker | WCAG 2.5.8 / Fitts / etc. | [Concise description] | [Exact CSS/HTML remediation] |

## Before-After-Why Table
| Current State | Proposed Fix | Why |
|---|---|---|
| [Code/Style] | [Remediated Code/Style] | [Empirical standard or cognitive law] |

## Verdict: [Approve / Changes Requested]
```

Completion criterion. Complete audit artifact rendered with prioritized findings table and Before-After-Why remediation guide.
