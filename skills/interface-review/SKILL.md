---
name: interface-review
description: Use when auditing UI implementation quality, CSS architecture, design token compliance, visual hierarchy, web accessibility standards, or frontend code diffs.
---

# Interface review

Audit frontend interfaces, component implementations, and design system tokens with strict empirical standards.

## Overview

Audit user interfaces across six core domains. These cover web accessibility (W3C APG and WCAG 2.2), spatial systems and 8pt grids, typography mechanics and fluid scales, color contrast and token architectures, component mechanics, and interface copy. Audit either targeted pull request diffs or full screen surfaces. Maintain evidence over taste. Leave deliberate brand expressions intact and focus on concrete regressions, visual defects, and specification violations.

## Workflow router

Identify user intent and route execution immediately:

1. **Component implementation audits.** When inspecting frontend components like buttons, comboboxes, modals, or tabs, read `references/accessibility.md` and `references/component-mechanics.md`. Inspect ARIA state patterns, focus visibility, keyboard navigation, concentric radii geometry, and touch target bounds.
2. **Screen and layout surface audits.** When inspecting an entire view, page route, or dashboard, read `references/layout-and-space.md`, `references/typography.md`, and `references/color-and-contrast.md`. Inspect 8pt spatial scales, CSS Subgrid alignment, container query boundaries, fluid typography clamps, color token tiering, and Cumulative Layout Shift mitigation.
3. **Pull request and git diff reviews.** When reviewing git commits or pull requests, read `references/scope-and-diff.md`. Inspect modified files for visual regressions, broken keyboard flows, stripped focus rings, hardcoded hex values, and layout shifts.

## Execution invariants

Enforce these execution invariants during review:

1. **Enforce visible focus rings.** Never accept `outline: none` without a verified replacement. Require `:focus-visible` rings with at least a 3:1 contrast ratio and 2px thickness.
2. **Use discrete surface tokens for elevation.** Demand semantic surface tokens based on lightness steps instead of semi-transparent white overlays.
3. **Apply concentric border radii geometry.** Enforce the concentric corner formula on nested containers to eliminate pinched corners. Never permit identical inner and outer border radii on nested containers.
4. **Restrict animations to composited properties.** Limit micro-interactions to `transform` and `opacity`. Reject animations on layout-triggering properties like `width`, `height`, `margin`, `padding`, `top`, or `left`.
5. **Enforce CSS logical properties.** Require logical properties such as `margin-inline-start` and `padding-inline` on shared components. Reject hardcoded physical properties like `margin-left` or `padding-right`.

## The evaluation sequence

Follow these four steps in sequence:

### Step 1. Scope resolution and reconnaissance

Determine target boundaries and project constraints before inspecting code:

1. If reviewing a PR or commit, establish the blast radius and filter non-UI assets using `references/scope-and-diff.md`.
2. Inspect project configuration files (package manifests, Tailwind configs, style dictionaries) to identify the styling engine, design token setup, and icon library.
3. Check for existing design guidelines (`AGENTS.md`, `DESIGN.md`, Storybook rules).
4. Adapt all recommended code fixes to the project's native styling idioms.

Completion criterion. Target files, active styling engine, and project design guidelines recorded.

### Step 2. Semantic and structural scan

Scan the target surfaces for immediate mechanical defects:

1. Inspect HTML semantic structure and verify that interactive widgets use native tags (`<button>`, `<dialog>`) instead of generic elements with click handlers.
2. Verify that input fields possess persistent `<label>` tags linked via `for` and `id` attributes.
3. Check for the presence of skip links and landmark roles (`<main>`, `<nav>`, `<header>`).
4. Validate that layout containers declare explicit aspect ratios to prevent Cumulative Layout Shift.

Completion criterion. A documented list of semantic deficiencies, missing labels, and layout shift hazards.

### Step 3. Ordered domain evaluation

Audit target surfaces through each domain in sequence. Consult reference documents in `references/` on demand:

1. **Accessibility.** Verify WCAG 2.2 AA compliance, W3C WAI-ARIA APG patterns, roving tabindex, focus traps, and AccName 1.2 rules. Read `references/accessibility.md`.
2. **Layout and space.** Verify 8pt grid compliance, CSS Subgrid, Container Queries, optical spacing, and nesting ratios. Read `references/layout-and-space.md`.
3. **Typography.** Verify measure (45 to 75 characters per line), fluid clamp formulas, unitless line heights, tabular numbers, and font loading strategies. Read `references/typography.md`.
4. **Color and contrast.** Verify APCA and WCAG contrast thresholds, DTCG 3-tier token structures, OKLCH scales, dark mode halation mitigation, and Windows forced-colors compatibility. Read `references/color-and-contrast.md`.
5. **Component mechanics.** Verify concentric radii calculations, Popover API usage, CSS Anchor Positioning, `@starting-style` transitions, and relational `:has()` selectors. Read `references/component-mechanics.md`.
6. **Interface copy.** Verify action verb clarity, error message recovery guidance, and empty-state instructions. Read `references/copy-writing.md`.

Completion criterion. Target surfaces evaluated against all six domains with zero skipped categories.

### Step 4. Consolidation and reporting

Consolidate findings into a structured report following the format in `references/report-format.md`:

1. Classify each finding into `Blocker`, `Warning`, or `Nit` severity tiers.
2. Present findings using the Before, After, and Why comparison format.
3. Provide exact file paths, line numbers, and actionable code diffs for every finding.
4. Cap findings at a maximum of 12 items, prioritizing accessibility blockers and visual regressions over cosmetic nits.
5. Assign an `Approve` or `Changes Requested` final verdict.

Completion criterion. A formatted report containing categorized findings, exact line references, Before-After-Why evidence tables, and a final verdict.

## Five-dimension design critique scorecard

When evaluating visual polish and aesthetics beyond mechanical accessibility, apply these five dimensions:

1. **Philosophy alignment.** Verify whether every visual detail traces directly back to the declared design system or brand anchor, rather than drifting into generic AI defaults.
2. **Visual hierarchy.** Conduct a squint test. Verify that the primary focal point catches the eye first and that the display title to body text size ratio is at least 2.5 to 1.
3. **Craft quality.** Verify consistent spatial rhythm, border-radius harmony, and constraint discipline (limit palettes to at most 4 deliberate colors and at most 2 font families).
4. **Functionality and deletion test.** Apply the deletion test: if an element, decorative divider, or card badge is removed, does the interface become worse or clearer? If clearer, remove the element.
5. **Originality and cliché elimination.** Eliminate formulaic AI templates, unprompted purple gradients, left-border accent stripes, and arbitrary floating shapes.

## Never ship UI checklist

Audit implementations against this checklist. Every item represents an automatic rejection:

| Never | Instead |
| --- | --- |
| `outline: none` or `outline: 0` without a visible replacement | `:focus-visible` with a minimum 2px solid outline and 2px offset |
| Nested child container sharing identical `border-radius` with parent | Concentric radius formula `R_inner = max(0, R_outer - (padding + border))` |
| Pure black `#000000` applied to large dark mode canvas surfaces | Dark neutral tones (OKLCH lightness 0.16 to 0.20, such as `#121212`) |
| Stacking white opacity overlays for dark mode surface elevations | Discrete semantic container tokens with stepped lightness values |
| Hover styling triggered unconditionally on touchscreen devices | Wrap hover rules in `@media (hover: hover) and (pointer: fine)` |
| Static pixels for root font size (`html { font-size: 16px; }`) | Relative browser percentage `html { font-size: 100%; }` |
| Line height declared with fixed units (`line-height: 24px`) | Unitless proportional values (`line-height: 1.5;`) |
| Unbounded body paragraphs exceeding 80 characters per line | Restrict reading width using `max-inline-size: 65ch;` |
| Numbers in tables or counters rendered with proportional glyphs | Enforce uniform width via `font-variant-numeric: tabular-nums;` |
| Animating `width`, `height`, `top`, `left`, `margin`, or `padding` | Animate GPU-accelerated `transform` and `opacity` exclusively |
| Responsive components bound solely to global window media queries | Use CSS Container Queries (`@container`) for modular portability |
| JavaScript timer hacks (`setTimeout`) for modal entry animations | Modern CSS `@starting-style` and `transition-behavior: allow-discrete` |
| Hardcoded hex values used directly inside component templates | Reference 3-tier semantic design tokens (`var(--color-surface)`) |
| Images rendered without explicit dimensions or aspect ratios | Declare `width`, `height`, and `aspect-ratio: 16 / 9;` to prevent CLS |
| Borderless buttons that disappear in Windows High Contrast Mode | Supply `border: 1px solid transparent;` and support forced colors |
| Generic clickable `div` elements representing buttons or links | Semantic native `<button type="button">` or `<a href="...">` |

## Quick verification checklist

Run this check before completing any interface review:

| Check | Passing condition |
| --- | --- |
| Scope boundaries | Target surfaces, excluded files, and active styling engines confirmed |
| Focus integrity | Every interactive element displays a high-contrast focus ring |
| Spatial hierarchy | Spacing follows 8pt modular scale, nested radii are concentric |
| Contrast compliance | Text satisfies APCA and WCAG thresholds, non-text controls exceed 3:1 |
| Layout stability | Cumulative Layout Shift mitigated via aspect ratios and reserved spaces |
| Report structure | Max 12 findings formatted with Before-After-Why tables and concrete diffs |
