---
name: ui-ux-review
description: "Use when auditing user interfaces, conducting UX heuristic critiques, evaluating WCAG accessibility compliance, checking copy clarity, or diagnosing layout defects. Don't use for visual layouts (use frontend-design), CSS animations (use ui-motion), live browser prototyping (use prototype), React rendering profiling (use react), or multi-task execution plans (use agent-planning)."
---

# UI and UX review

Audit user interfaces and user experiences with empirical rigor.

<HARD-GATE>
Write-Target Boundary. In Audit mode, do not modify any file outside `.agents/state/ui-ux-review/`. In Remediation mode, modify only CSS, HTML markup, and microcopy approved by the user. Never modify backend business logic, API routes, database schemas, or non-UI assets. Emit findings and patches to `.agents/state/ui-ux-review/` before applying.
</HARD-GATE>

## Modes

Select an execution mode before Step 1:
- Audit mode (default). Inspect UI components against WCAG standards, layout architecture, and cognitive load heuristics, and produce an evaluation findings table without modifying styles.
- Remediation mode. Apply surgical CSS/HTML patches to address approved UI/UX findings.

## Boundary isolation

UI/UX review evaluates interface usability and presentation only. Never alter backend business logic, API route parameters, or database schemas while remediating UI issues.

## Overview

Audit frontend implementations and user journeys across visual mechanics and cognitive ergonomics. Evaluate code and interfaces against objective browser standards, accessibility specifications, and cognitive psychology research. Disregard subjective taste or generic AI design tropes. Focus on measurable defects, interaction friction, working memory overload, and recovery failures. Consult reference documents in `references/` on demand.

## Workflow router

Identify user intent and route execution immediately:

1. **Component implementation audits.** When inspecting frontend controls like buttons, comboboxes, dialogs, or inputs, read `references/accessibility.md` and `references/component-mechanics.md`. Inspect ARIA state patterns, focus visibility, keyboard navigation, concentric radii geometry, and touch target bounds.
2. **Screen and layout surface audits.** When inspecting an entire view, page route, or dashboard, read `references/layout-and-space.md`, `references/typography.md`, and `references/color-and-contrast.md`. Inspect 8pt spatial scales, CSS Subgrid alignment, container query boundaries, fluid typography clamps, color token tiering, and Cumulative Layout Shift mitigation.
3. **Task flows and journey audits.** When inspecting multi-step workflows like onboarding, checkout, registration, or wizards, read `references/task-flows-and-ia.md`. Inspect step branching, progress indicators, drop-off risks, and the Lostness Metric.
4. **Pull request and git diff reviews.** When reviewing git commits or pull requests, read `references/scope-and-diff.md`. Inspect modified files for visual regressions, broken keyboard flows, stripped focus rings, hardcoded hex values, and premature validation triggers.

## Reference quick routing

| Domain | Reference module | Scope |
|---|---|---|
| UX scoring | [references/ux-scoring-rubric.md](references/ux-scoring-rubric.md) | Quantitative 100-point UX audit rubric |
| Persona testing | [references/persona-testing.md](references/persona-testing.md) | User persona simulation & journey walks |
| Critique workflow | [references/ux-critique-workflow.md](references/ux-critique-workflow.md) | Systematic design critique methodology |
| Heuristic scoring | [references/heuristic-scoring-guide.md](references/heuristic-scoring-guide.md) | Nielsen-Norman heuristic evaluation framework |
| Extended heuristics | [references/heuristics-extended-notes.md](references/heuristics-extended-notes.md) | Deep heuristic edge cases & notes |
| Copy clarity | [references/copy-clarity-and-component-review.md](references/copy-clarity-and-component-review.md) | Microcopy, labels, error messages, & button text |
| Technical UI audit | [references/technical-ui-audit.md](references/technical-ui-audit.md) | DOM nesting, responsive behavior, & CSS sanity |
| Onboarding heuristics | [references/onboarding-heuristics.md](references/onboarding-heuristics.md) | First-run UX, progressive onboarding, & cognitive load |
| Responsive inspection | [references/responsive-inspection.md](references/responsive-inspection.md) | Multi-device layout inspection & viewport stress-tests |

## Execution invariants

Enforce these foundational invariants across all audits:

1. **INV-1. Visible focus rings.** Never accept `outline: none` or `outline: 0` without a verified replacement. Require `:focus-visible` rings with at least a 3:1 contrast ratio, 2px solid thickness, and 2px offset.
2. **INV-2. Concentric border radii.** Enforce the concentric corner formula on nested containers `R_inner = max(0, R_outer-(padding + border))` to eliminate pinched corners. Never permit identical inner and outer radii on nested containers.
3. **INV-3. Discrete surface tokens.** Demand semantic surface tokens based on lightness steps instead of semi-transparent white overlays.
4. **INV-4. Interaction friction over styling.** Focus on task completion time, cognitive load, error rates, and mental model mismatches before fine-tuning aesthetics.
5. **INV-5. Cognitive thresholds.** Apply Nelson Cowan 4-chunk limits, Doherty 400ms feedback bounds, and Fitts's Law 48px touch targets without inventing arbitrary thresholds.
6. **INV-6. Undo for reversible actions.** Prescribe instant execution paired with a 5 to 10 second undo toast. Avoid modal confirmation dialogs because habituation renders repeated confirmation prompts ineffective against slips.
7. **INV-7. Unrecoverable data loss.** Flag any form or workflow that wipes user input on network drops, session expiries, or back navigation as an automatic blocker.
8. **INV-8. CSS logical properties.** Require logical properties such as `margin-inline-start` and `padding-inline` on shared components. Reject hardcoded physical properties like `margin-left` or `padding-right`.

## Section 1. UI mechanics and technical compliance

Enforce technical standards, layout stability, and accessibility invariants:

1. **WCAG 2.2 AA accessibility.** Verify W3C WAI-ARIA APG patterns, semantic HTML elements, roving tabindex, focus traps, and AccName 1.2 rules. Require native elements over generic containers. Read `references/accessibility.md`.
2. **8pt spatial grid and layout scales.** Enforce spacing on an 8pt or 4pt modular scale. Align columns using CSS Subgrid. Declare explicit dimensions and aspect ratios to prevent Cumulative Layout Shift. Read `references/layout-and-space.md`.
3. **APCA and contrast compliance.** Verify APCA and WCAG contrast thresholds across text and interactive controls. Check dynamic frame contrast across video and animated surfaces using localized scrims. Implement DTCG 3-tier token structures, OKLCH scales, dark mode halation mitigation, and Windows High Contrast Mode border fallbacks. Read `references/color-and-contrast.md`.
4. **Container queries and modular stability.** Use CSS Container Queries (`@container`) for modular components instead of binding solely to viewport media queries. Declare container contexts for responsive cards.
5. **Component mechanics.** Verify Popover API usage, CSS Anchor Positioning, `@starting-style` transitions, and relational `:has()` selectors. Read `references/component-mechanics.md`.
6. **Typography mechanics.** Verify reading measure between 45 and 75 characters per line, fluid clamp formulas, unitless line heights, and tabular numbers for structured tables. Read `references/typography.md`.
7. **Animation physics checks.** Restrict micro-interactions to GPU-composited properties `transform` and `opacity`. Reject animations on layout-triggering properties like width, height, margin, or padding. For spring physics, gesture tracking, choreographies, and frame-rate audits, activate the `ui-motion` skill.

## Section 2. UX cognitive heuristics and journey ergonomics

Enforce human-centered psychology laws, task efficiency, and error resilience:

1. **Hick-Hyman Law.** Reaction time increases logarithmically with the number and complexity of choices. Prune choices to 5 to 7 options per view, or group them logically with progressive disclosure. Read `references/cognitive-laws.md`.
2. **Nelson Cowan 4-chunk limit.** Working memory holds at most 4 distinct chunks simultaneously. Group content into at most 4 items across screen transitions, multi-step wizards, or dense navigation menus; never force users to retain more than 4 items simultaneously.
3. **Fitts's Law touch targets.** Target acquisition time depends on distance and target size. Require interactive elements to measure at least 48x48px on touchscreen interfaces with at least 8px separation between targets. Read `references/mobile-touch-ergonomics.md`.
4. **Form validation timing and error recovery.** Delay field error display until `onBlur`, then live revalidate on `onInput` after initial blur. Keep submit buttons enabled, display clear inline error messages, and shift focus to the first invalid input on submission. Read `references/forms-and-error-recovery.md`.
5. **Mobile thumb zones.** Place primary mobile actions and navigation triggers inside the Natural Thumb Zone along the screen bottom. Keep the Ow Zone at the top edges free of primary interactive triggers. Read `references/mobile-touch-ergonomics.md`.
6. **System status transparency.** Provide clear feedback within 100ms for user actions, display subtle progress indicators for operations taking 400ms to 1000ms, and render skeleton loaders instead of blank spinners. Read `references/system-status-and-states.md`.
7. **Task flows and information architecture.** Minimize steps to completion, eliminate dead-scroll zones (>300px travel without visual mutation), enforce Krug scannability, apply progressive disclosure 80/20 rules, and minimize the Lostness Metric. Read `references/task-flows-and-ia.md`.
8. **Usability heuristics and principles.** Check NN/g 10 heuristics, Norman signifiers and constraints, Shneiderman golden rules, and ISO 9241-110 dialogue standards. Read `references/heuristics-and-principles.md`.
9. **Interface copy and lexical consistency.** Enforce outcome verbs on triggers ("Save changes" instead of "Submit"). Maintain lexical cohesion across actions and status toasts ("Publish" triggers "Published"). Name interface concepts using user mental models rather than backend architectures ("Manage notifications" instead of "Webhook configuration"). Never write apologetic error copy; describe what failed and state concrete recovery steps. Omit decorative section counters (01, 02) when content is not an ordered sequence. Read `references/copy-writing.md`.

## Ordered evaluation sequence

Execute the review through four structured steps:

### Step 1. Scope resolution and reconnaissance

Establish review boundaries, blast radius, and user intent before inspecting code:

1. Resolve review boundaries and filter non-UI assets using `references/scope-and-diff.md`.
2. Expand blast radius by inspecting direct parent layouts (1 hop) and shared token consumers (2 hops).
3. Inspect project configuration files including package manifests, Tailwind configs, and token dictionaries to identify active styling engines and icon systems.
4. Check for existing design guidelines (`AGENTS.md`, `DESIGN.md`, Storybook rules).
5. Identify primary user goals, baseline mental models, and optimal step counts.
6. Record excluded files, third-party redirects, and out-of-scope backend processes.
7. Write or load `.agents/state/ui-ux-review/operate-brief.md` for operate and read routes before inspecting code. Do not write to `references/`.

Completion criterion. Target surfaces, active styling engines, guidelines, user goals, and operate brief confirmed and recorded in a scope checklist.

### Step 2. UI mechanics audit

Audit target surfaces against technical and structural standards:

1. Accessibility. Check WCAG 2.2 AA compliance, semantic markup, keyboard navigation, and AccName rules using `references/accessibility.md`.
2. Layout and space. Check 8pt grid scales, concentric radii, subgrid alignment, and container queries using `references/layout-and-space.md`.
3. Typography. Check measure (45 to 75 characters), fluid clamp formulas, unitless line heights, and tabular numbers using `references/typography.md`.
4. Color and contrast. Check APCA contrast ratios, 3-tier tokens, OKLCH scales, and forced colors using `references/color-and-contrast.md`.
5. Component mechanics. Check Popover API, CSS Anchor Positioning, and `@starting-style` transitions using `references/component-mechanics.md`.
6. Motion mechanics. Check composited properties and delegate spring physics to `ui-motion`.

Completion criterion. Target surfaces evaluated against all technical mechanics and recorded in an itemized evaluation table with zero skipped categories.

### Step 3. UX cognitive and interaction audit

Audit user journeys against cognitive and behavioral standards:

1. Usability heuristics. Verify NN/g 10 heuristics, Norman signifiers, and ISO 9241-110 dialogue principles using `references/heuristics-and-principles.md`.
2. Cognitive laws. Check Hick-Hyman choice pruning, Nelson Cowan 4-chunk limits, Doherty 400ms threshold, and Peak-End rule using `references/cognitive-laws.md`.
3. Task flows and information architecture. Check progressive disclosure, step counts, and Lostness Metric using `references/task-flows-and-ia.md`.
4. Forms and error recovery. Check single-column layouts, inline validation timing, persistent draft storage, and undo toasts using `references/forms-and-error-recovery.md`.
5. System status and states. Check six-state completeness, skeleton loaders, and optimistic updates using `references/system-status-and-states.md`.
6. Mobile touch ergonomics. Check 48px touch targets, bottom thumb zones, and swipe gestures using `references/mobile-touch-ergonomics.md`.

Completion criterion. Target workflows evaluated across cognitive laws, task flows, forms, and touch ergonomics and recorded in an itemized findings table with zero skipped domains.

### Step 4. Consolidation and reporting

Consolidate findings into a structured report using `references/report-format.md`:

1. Classify every finding into `Blocker`, `Warning`, or `Nit` severity tiers.
2. Present findings using Before, After, and Why comparative tables.
3. Provide exact file paths, line numbers, and concrete code diffs or microcopy fixes in project idiom.
4. Attribute each defect to specific standards, WCAG success criteria, cognitive laws, or usability heuristics.
5. Project impact on usability metrics including Task Completion Rate (TCR), Lostness, and Drop-off rate.
6. Cap findings at a maximum of 12 items to prevent cognitive fatigue and prioritize blockers.
7. Assign an `Approve` or `Changes Requested` final verdict.
8. Run finish review in fresh context with request, answers, artifact path, screenshots, direction contract, and hook findings as inputs. Inherit no transcript.

Completion criterion. The report is written to `.agents/state/ui-ux-review/report.md` with headings `## Verdict`, `## Findings`, `## Scope`, and `## Evidence`. The `## Verdict` section contains exactly one line matching `verdict: (Approve|Changes Requested)`. Screenshots are stored under `.agents/state/ui-ux-review/screenshots/`.

## Five-dimension design critique scorecard

When evaluating visual polish and aesthetics beyond mechanical accessibility, apply these five dimensions:

1. **Philosophy alignment.** Verify whether every visual detail traces directly back to declared design tokens rather than generic AI defaults.
2. **Visual hierarchy.** Conduct a squint test. Verify that the primary focal point catches the eye first and that the display title to body text ratio exceeds 2.5 to 1.
3. **Craft quality.** Enforce spatial rhythm, border-radius harmony, and constraint discipline by limiting palettes to at most 4 deliberate colors and at most 2 font families.
4. **Functionality and deletion test.** Apply the deletion test. If a decorative element or card badge is removed and the interface becomes clearer, delete the element.
5. **Originality and cliché elimination.** Eliminate formulaic AI templates, unprompted purple gradients, left-border accent stripes, and arbitrary floating shapes.

## Quick audit checklist

Audit implementations against this checklist. Every item represents an automatic rejection:

| ID | Title | Pattern description | Why it fails | Concrete fix |
|---|---|---|---|---|
| AA-1 | Focus ring removal | `outline: none` or `outline: 0` without a visible replacement | Keyboard users lose navigation position; fails WCAG 2.4.7 | `:focus-visible` with minimum 2px solid outline and 2px offset |
| AA-2 | Concentric radius violation | Nested child container sharing identical `border-radius` with parent | Corners pinch visually and hierarchy reads flat | Concentric radius formula `R_inner = max(0, R_outer-(padding + border))` |
| AA-3 | Pure black canvas | Pure black `#000000` applied to large dark mode canvas surfaces | OLED smearing and harsh contrast eye fatigue | Dark neutral tones with OKLCH lightness 0.16 to 0.20 such as `#121212` |
| AA-4 | White opacity layering | Stacking white opacity overlays for dark mode surface elevations | Creates muddy contrast and indeterminate lightness steps | Discrete semantic container tokens with stepped lightness values |
| AA-5 | Unconditional hover styling | Hover styling triggered unconditionally on touchscreen devices | Causes sticky hover states on mobile touch tap | Wrap hover rules in `@media (hover: hover) and (pointer: fine)` |
| AA-6 | Fixed unit line-height | Line height declared with fixed units such as `line-height: 24px` | Causes text collision when users scale font sizes | Unitless proportional values such as `line-height: 1.5;` |
| AA-7 | Unbounded line length | Unbounded body paragraphs exceeding 80 characters per line | Degrades reading tracking and increases cognitive strain | Restrict reading width using `max-inline-size: 65ch;` |
| AA-8 | Proportional numbers in data | Numbers in tables or counters rendered with proportional glyphs | Columns jitter and alignment drifts across updates | Enforce uniform width via `font-variant-numeric: tabular-nums;` |
| AA-9 | Layout property animation | Animating layout properties like width, height, margin, or top | Triggers main-thread layout recalculations and dropped frames | Animate GPU-accelerated `transform` and `opacity` exclusively |
| AA-10 | Window-bound media queries | Responsive components bound solely to global window media queries | Breaks component portability across different column widths | Use CSS Container Queries (`@container`) for modular portability |
| AA-11 | Missing image dimensions | Images rendered without explicit dimensions or aspect ratios | Triggers Cumulative Layout Shift when asset loads | Declare explicit dimensions and `aspect-ratio` to prevent CLS |
| AA-12 | Clickable div elements | Generic clickable `div` elements representing buttons or links | Inaccessible to screen readers and keyboard navigation | Semantic native `<button type="button">` or `<a href="...">` |
| AA-13 | Placeholder as label | Placeholder attribute used as form field label | Disappears upon user input and fails cognitive recall | Persistent `<label>` element above the input field |
| AA-14 | Premature validation errors | Border and text turning red while the user is actively typing | Punishes the user before they finish data entry | Delay error validation until `onBlur`, then live revalidate on `onInput` |
| AA-15 | Disabled submit button | Disabled submit button with no explanation | Users cannot discover what input requirements are missing | Keep submit button enabled, show inline errors and jump to first invalid field |
| AA-16 | Zig-zagging form fields | Multi-column form layouts with zig-zagging fields | Increases eye travel and form completion abandonment | Single-column linear vertical layout |
| AA-17 | Modal popup on reversible action | Modal confirmation popup on reversible actions | Interrupts flow; repeated prompts cause habituated clicks | Instant execution with 5 to 10 second undo toast notification |
| AA-18 | Single-click destructive deletion | Destructive permanent deletion executed via single regular button | Invites catastrophic accidental data loss from misclicks | Deliberate friction requiring resource name confirmation or typed prompt |
| AA-19 | Form wipe on network error | Form fields wiped clean on server validation error or network timeout | Destroys user effort and forces complete re-entry | Preserve all input state locally and flag only the invalid field |
| AA-20 | Unfeedbacked operation latency | Silent operation with no feedback during 400ms to 1000ms latency | Leaves user uncertain whether click registered | Subtle inline spinner or button loading state |
| AA-21 | Apologetic error copy | Generic or apologetic error copy like "Sorry, an error occurred" | Provides zero actionable path forward | Specific statement of what failed followed by concrete recovery steps |
| AA-22 | Generic CTA verbs | Generic passive CTA label like "Submit" or "Click here" | Ambiguous outcome verb creates decision hesitation | Specific outcome verb matching intent like "Save changes" or "Create project" |
| AA-23 | Lexical state drift | Lexical drift between trigger button and status notification | Breaks mental model continuity across task execution | Exact lexical pairing across flow ("Publish" button triggers "Published" toast) |
| AA-24 | System jargon in UI copy | System architecture terminology exposed in user copy | Exposes implementation mechanics instead of user goals | User mental model terms ("Manage notifications" instead of "Webhook settings") |
| AA-25 | Full screen spinner replacement | Entire screen replaced by a single spinner on initial page load | Creates jarring visual pop-in when content arrives | Skeleton screens matching destination layout structure |
| AA-26 | Mobile action in Ow Zone | Primary mobile action placed in top corners (Ow Zone) | Forces uncomfortable one-handed reach gymnastics | Sticky bottom button or bottom bar in Natural Thumb Zone |
| AA-27 | Punitive input formatting | Rejection of telephone or card numbers because of spaces or hyphens | Fails Postel principle by punishing human input habits | Permit flexible input formatting per Postel law and sanitize on submission |
| AA-28 | Wall of unchunked inputs | Wall of 10+ inputs presented in a single unstructured page | Overwhelms cognitive working memory capacity | Multi-step flow chunked into 3 to 4 logical fields per step with progress |
| AA-29 | Blank white empty state | Empty state rendered as blank white space | Leaves user stranded without onboarding guidance | Instructive empty state explaining zero data and primary action to populate |
| AA-30 | Unranked flat dropdown | Dropdown containing 15+ unranked options without search | Forces tedious linear scrolling through long menus | Searchable combobox or progressive selection hierarchy |
| AA-31 | Dead scroll zones | Dead scroll zones where scrolling changes nothing on screen | Misleads user into believing page has frozen | Continuous feedback or eliminate redundant pinning |
| AA-32 | Dynamic canvas text contrast | Text rendered over dynamic video or canvas without multi-frame contrast check | Becomes illegible when background video brightness shifts | Localized scrim or contrast-adaptive text fill passing WCAG AA across all frames |
| AA-33 | False sequence numbering | Numbered markers (01 / 02 / 03) applied to non-sequential content | Falsely implies rigid chronological order where none exists | Omit numbers; use semantic headings or topic cards unless step order is strictly required |

## Quick verification checklist

Run this check before completing any review:

| Check | Passing condition |
| --- | --- |
| Scope boundaries | Target surfaces, user goals, and active styling engines confirmed |
| Focus integrity | Every interactive element displays a high-contrast focus ring |
| Spatial hierarchy | Spacing follows 8pt modular scale, nested radii are concentric |
| Contrast compliance | Text satisfies APCA and WCAG thresholds, non-text controls exceed 3:1 |
| Layout stability | Cumulative Layout Shift mitigated via aspect ratios and reserved space |
| Cognitive limits | Choices pruned to 5 to 7 items, chunking conforms to 4-item limit |
| Error resilience | Form recovery, draft persistence, and undo mechanisms verified |
| Touch ergonomics | Interactive elements meet 48px targets and reside in natural thumb zones |
| Scroll and timeline | Zero dead-scroll zones (>300px travel), verified dynamic frame contrast over video/motion |
| Copy integrity | Actions use outcome verbs, toasts match trigger vocabulary, errors give recovery steps without apologies |
| Report structure | Max 12 findings formatted with Before-After-Why tables and concrete diffs |
