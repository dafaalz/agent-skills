---
name: prototype
description: Use when prototyping divergent visual or interaction variants for a UI component, or comparing interactive UI explorations.
disable-model-invocation: true
---

# Prototyping variants

Explore divergent visual and interaction directions for a single UI component behind an interactive picker harness.

This skill builds distinct, production-ready variants for a single UI component and renders them in an isolated picker harness. The user evaluates variants in context and selects a direction to integrate.

## Core rules

- **Isolate prototype code.** Never edit production components during exploration. Build all variants and the picker harness in an isolated route or standalone HTML file.
- **Diverge on explicit axes.** Differentiate variants by layout, density, motion, or interaction pattern. Do not present variants that differ only by color tint or placeholder text.
- **Build functional interactions.** Every variant must handle state, transitions, and realistic domain copy. Placeholder text and dead buttons are prohibited.
- **Follow motion standards.** Keep interaction transitions under 300ms. Animate transform and opacity exclusively. Use ease-out curves on entrances, and respect reduced-motion user preferences.
- **Preserve picker chrome.** Render the picker component exactly as defined in [PICKER.md](PICKER.md). Do not restyle the picker with project tokens or theme colors.
- **Deliver early v0 drafts.** Avoid the big reveal trap. Emit a viewable v0 draft containing layout skeletons, design tokens, and explicit module placeholders (such as `[image]` or `[icon]`) to confirm direction with the user before investing in complex interaction choreography or fine-tuned micro-motion.
- **Clean up on promotion.** Delete the prototype harness and unselected variants once the user confirms a winning direction.

## Workflow

Follow these six steps in sequence:

### Step 1. Scope and brief definition

Isolate a single high-impact UI component from the user request.

- If the request targets a complex screen or multi-component flow, select the single component that carries the highest interaction risk or design ambiguity.
- State the brief in one declarative sentence defining the component, its target surface, and its primary job.

Completion criterion. A written one-sentence brief defining a single target component and its operational context.

### Step 2. Technical and visual recon

Inspect the active codebase to identify design constraints and styling tokens.

- Stack. Identify the UI framework, styling library, and animation libraries in use.
- Tokens. Extract active values for spacing, border radii, type scale, and core palette.
- Context. Inspect the container dimensions, background surfaces, and sibling components where the target piece mounts.
- Standalone fallback. If no existing codebase exists, default to semantic HTML, standard system fonts, neutral slate tones, and one accent color.

Completion criterion. An inventory recording the target stack, design tokens, and surrounding DOM constraints.

### Step 3. Direction and axis selection

Define three distinct directions before writing code. Expand to five only when the design space warrants deeper exploration.

- Assign each direction a descriptive name such as Quiet, Editorial, Playful, or Dense.
- Pair each direction with an explicit axis of variation, such as density, spatial hierarchy, interaction cadence, or feedback mechanism.
- Verify that no two variants occupy the same point on a chosen axis.

Completion criterion. A list of 3 to 5 named variants with mutually exclusive variation axes.

### Step 4. Harness construction

Assemble the isolated preview environment and embed the standard picker.

- Dev server environment. Create a dedicated route or preview page at `/prototypes/<component-slug>` containing variant components and the harness.
- Static environment. Generate a single self-contained HTML file containing inline styles and scripts for direct browser execution.
- Picker integration. Copy markup, styles, and event wiring verbatim from [PICKER.md](PICKER.md).
- Display standards. Render one variant at a time at full size with surrounding layout context. Do not use thumbnail grids. Switch variants instantly without transitional animations.

Completion criterion. An operational harness rendering variants one at a time and switching instantly via keyboard and mouse controls.

### Step 5. Verification and review handoff

Validate variant functionality before presenting options to the user.

- Flip through every variant in the harness to verify state transitions and event responses.
- Inspect the browser console to confirm zero runtime errors or unhandled exceptions.
- Present the comparison table summarizing trade-offs:

| # | Variant | Axis | Best suited for | Trade-off |
|---|---|---|---|---|
| 1 | Quiet | Minimal motion, borders over shadows | High-frequency daily tools | Lowest visual impact |
| 2 | Editorial | High contrast typography, generous whitespace | Onboarding or milestone moments | Consumes vertical space |

- Report the active harness URL or local file path along with keyboard shortcut instructions.

Completion criterion. The harness executes cleanly without console warnings, and the comparison table articulates distinct trade-offs for each variant.

### Step 6. Variant promotion and cleanup

Integrate the chosen variant and remove temporary exploration artifacts.

- When the user selects a winner, migrate the winning component into production paths following codebase file structure and token conventions.
- Delete the prototype route, variant files, and harness unless the user explicitly requests retention.
- If the user requests further exploration, retain the harness and repeat Step 3 focusing on sub-variants of the favored direction.

Completion criterion. The chosen component is integrated into the destination codebase and all prototype scratch files are removed.

## Invocation variants

| Invocation | Behavior |
|---|---|
| `<description>` | Full workflow covering scope, recon, 3 variants, picker, and waiting for choice |
| `<description> x5` | Full workflow with 5 variants |
| `riff <variant>` | New round keeping the harness and diverging around the chosen variant |
| `keep <variant>` | Promote that variant into the codebase and delete the prototype surface |
| `keep <variant>, leave the picker` | Promote that variant while retaining the prototype surface |

## Quick reference checklist

Run this check before completing any prototyping pass:

| Check | Passing condition |
|---|---|
| Frontmatter | Description starts with "Use when" and lists operational triggers under 500 characters |
| Isolation | Zero prototype imports or scratch dependencies exist inside production files |
| Functional parity | Every variant executes real interactions without placeholder buttons or lorem ipsum text |
| Motion limits | All UI transitions run under 300ms using transform and opacity properties |
| Picker fidelity | Picker markup, styles, and keyboard handlers match [PICKER.md](PICKER.md) verbatim |
| Completion criteria | Every workflow step defines a checkable binary completion criterion |
| Style compliance | Zero em dashes, zero decorative emojis, and sentence case headings throughout |
