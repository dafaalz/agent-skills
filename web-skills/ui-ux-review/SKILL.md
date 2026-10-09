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

## Workflow

### Step 1. Scope and stack reconnaissance

Identify the target surface and environment from user input:
- Target type: component control, layout surface, multi-step flow, or code diff.
- Styling engine & UI library (e.g., Tailwind CSS, CSS Modules, Radix UI, Shadcn, MUI).
- Primary user goals, baseline mental models, and optimal step count.

### Step 2. UI mechanics audit

Evaluate the implementation against technical and structural standards:
1. **Accessibility (WCAG 2.2 AA).** Check semantic HTML, accessible names, keyboard navigation, focus trap in modals, and visible focus rings (`:focus-visible` with at least 3:1 contrast, 2px solid, 2px offset). Consult `references/accessibility.md`.
2. **Spatial geometry.** Verify spacing adheres to an 8pt/4pt modular scale. Enforce concentric border radius formula: `R_inner = max(0, R_outer - (padding + border))`. Consult `references/layout-and-space.md`.
3. **Typography & Readability.** Verify line measure between 45 and 75 characters (`max-inline-size: 65ch`), unitless line heights, and tabular figures for numbers. Consult `references/typography.md`.
4. **Color & Contrast.** Verify APCA / WCAG text contrast (minimum 4.5:1 for body text, 3:1 for controls). Ensure surface elevations use stepped lightness tokens instead of stacking white opacity overlays. Consult `references/color-and-contrast.md`.
5. **Layout stability & Modern CSS.** Check container queries (`@container`), explicit aspect ratios to prevent CLS, and CSS logical properties. Consult `references/component-mechanics.md`.

### Step 3. UX cognitive and journey audit

Evaluate the workflow against cognitive psychology laws and human ergonomics:
1. **Hick-Hyman Law.** Check if choices are pruned to 5 to 7 items or organized with progressive disclosure. Consult `references/cognitive-laws.md`.
2. **Nelson Cowan 4-chunk limit.** Verify working memory does not require holding more than 4 items across steps or screens.
3. **Fitts's Law touch targets.** Ensure touch targets measure at least 48x48px with 8px separation on mobile viewports. Consult `references/mobile-touch-ergonomics.md`.
4. **Form validation timing.** Validate on `onBlur`, live revalidate on `onInput` only after initial blur. Keep submit buttons enabled and jump to the first invalid field. Consult `references/forms-and-error-recovery.md`.
5. **Reversible actions & System status.** Prefer instant execution paired with a 5 to 10 second undo toast notification over modal confirmation popups for reversible actions. Show skeleton loaders instead of blank spinners. Consult `references/system-status-and-states.md`.

### Step 4. Report generation as Claude Artifact

Consolidate findings into a standalone Markdown Claude Artifact formatted per `references/report-format.md`:
1. Executive summary with usability metric impact (Task Completion Rate, Lostness, Drop-off).
2. Findings table categorized into `Blocker`, `Warning`, or `Nit` (maximum 12 items total).
3. Comparative **Before, After, and Why** tables with concrete, copy-pasteable code diffs or microcopy:

| Before | After | Why |
|---|---|---|
| `outline: none;` | `:focus-visible { outline: 2px solid var(--primary); outline-offset: 2px; }` | Eliminates keyboard trap; satisfies WCAG 2.4.7 |
| Identical inner/outer `rounded-xl` | `R_inner = max(0, 12px - 8px) = 4px` | Eliminates corner pinching; maintains concentric geometry |
| Modal confirmation for archive | Instant archive with 8s Undo toast | Prevents confirmation dialog habituation slips |

4. Clear final verdict: **Approve** or **Changes Requested**.

## Never ship checklist

Audit implementations against this checklist. Every violation is an automatic Blocker:

| Never | Instead |
|---|---|
| `outline: none` without replacement | `:focus-visible` with 2px solid outline and 2px offset |
| Nested container sharing identical `border-radius` | Concentric radius `R_inner = max(0, R_outer - (padding + border))` |
| Pure black `#000000` dark mode background | Dark neutral tones (OKLCH lightness 0.16 to 0.20, e.g., `#121212`) |
| Animating layout properties (`width`, `height`, `margin`) | Animate GPU-composited `transform` and `opacity` exclusively |
| Placeholder attribute used as form field label | Persistent `<label>` element above the input field |
| Red error triggers while user is actively typing | Validate on `onBlur`, then live revalidate on `onInput` |
| Disabled submit button with no explanation | Keep submit button enabled, show inline errors, shift focus |
| Modal confirmation popup on reversible actions | Instant execution with 5 to 10 second undo toast |
| Wall of 10+ inputs presented in a single page | Multi-step flow chunked into 3 to 4 logical fields per step |
| Dropdown containing 15+ options without search | Searchable combobox or progressive hierarchy |
| Generic error copy "An error occurred" | State what failed and provide concrete recovery action |

## Quick verification checklist

| Check | Passing condition |
|---|---|
| Artifact delivery | Complete report rendered as a Claude Artifact |
| Severity grading | Every finding tagged as Blocker, Warning, or Nit |
| Max findings | Capped at 12 prioritized items to prevent cognitive fatigue |
| Actionable diffs | Before-After-Why tables provide exact code or copy replacements |
| Final verdict | Explicit Approve or Changes Requested rating |
