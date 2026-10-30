---
name: prototype
description: "Use when running live interactive prototyping sessions, generating design variants, rapid mockups, or establishing browser sandbox loops. Don't use for production components (use frontend-design), UX audits (use ui-ux-review), CSS animations (use ui-motion), React profiling (use react), or multi-task execution plans (use agent-planning)."
---

# Prototyping variants

Explore divergent visual and interaction directions for a single UI component behind an interactive picker harness.

This skill builds distinct, production-ready variants for a single UI component and renders them in an isolated picker harness. The user evaluates variants in context and selects a direction to integrate.

<HARD-GATE>
Write-Target Boundary. In Exploration branch, write only under `.agents/scratch/prototypes/<variant-id>/` and the isolated preview route path declared in `.agents/state/prototype/harness-path.txt`. Never modify production component files, routing tables, or global build configuration. In Promotion branch, migrate only the winning variant into production after user confirmation recorded in `.agents/scratch/prototypes/<variant-id>/PROTOTYPE_LOCK.md`.
</HARD-GATE>

## Modes

Select an execution branch based on user invocation:
- Exploration branch (default). Run Steps 1 through 5 to research, build, and verify candidate variants.
- Promotion branch (`keep <variant>`). Skip directly to Step 6 to integrate the chosen component and clean up scratch files.

## Core rules

- Build all variants and the picker harness in an isolated route or standalone HTML file instead of editing production components during exploration.
- Differentiate variants by layout, density, motion, or interaction pattern rather than presenting variants that vary only by color tint or placeholder text.
- Supply realistic domain copy, interactive states, and transitions for every variant instead of relying on placeholder text or dead buttons.
- Keep interaction transitions under 300ms, animate transform and opacity exclusively, use ease-out curves on entrances, and respect reduced-motion preferences.
- Render the picker component exactly as defined in [PICKER.md](PICKER.md) instead of restyling it with project tokens or theme colors.
- Emit a viewable v0 draft containing layout skeletons, design tokens, and explicit module placeholders (such as `[image]` or `[icon]`) to confirm direction with the user before investing in complex interaction choreography or micro-motion.
- Delete the prototype harness and unselected variants once the user confirms a winning direction.

## Reference quick routing

| Workflow domain | Reference module | Scope |
|---|---|---|
| Live session loop | [references/live-session-loop.md](references/live-session-loop.md) | Live browser prototyping session control |
| Variant generation | [references/variant-generation.md](references/variant-generation.md) | Generative design permutations & A/B variants |
| Live generate workflow | [references/live-generate-workflow.md](references/live-generate-workflow.md) | Generation pipelines & artifact output |
| Live setup guide | [references/live-setup-guide.md](references/live-setup-guide.md) | First-time configuration & server prerequisites |

## Workflow

Follow these six steps in sequence:

### Step 1. Scope and brief definition

If `.agents/scratch/prototypes/<variant-id>/spike-brief.md` exists, read it as the authoritative brief. Extract `target_component`, `target_surface`, and `primary_job` from the file. Skip the remaining Step 1 isolation instructions unless the brief is missing or malformed.

If the file does not exist, isolate the target UI component from the user request as described below.
- If the request targets a complex screen or multi-component flow, select the component that carries the highest interaction risk or design ambiguity.
- State the brief in one declarative sentence defining the component, its target surface, and its primary job.

Completion criterion. `.agents/scratch/prototypes/<variant-id>/brief.md` exists on disk with a single `# Brief` heading and one sentence under it. If `spike-brief.md` was read, the brief content matches the values in that file.

### Step 2. Technical and visual recon

Inspect the active codebase to identify design constraints and styling tokens.

- Stack. Identify the UI framework, styling library, and animation libraries in use.
- Tokens. Extract active values for spacing, border radii, type scale, and core palette.
- Context. Inspect the container dimensions, background surfaces, and sibling components where the target piece mounts.
- Standalone fallback. If no existing codebase exists, default to semantic HTML, standard system fonts, neutral slate tones, and one accent color.

Completion criterion. `.agents/scratch/prototypes/<variant-id>/inventory.json` exists on disk recording target stack, design tokens, and surrounding DOM constraints.

### Step 3. Direction and axis selection

Define three distinct directions before writing code. Expand to five only when the design space warrants deeper exploration.

- Assign each direction a descriptive name such as Quiet, Editorial, Playful, or Dense.
- Pair each direction with an explicit axis of variation, such as density, spatial hierarchy, interaction cadence, or feedback mechanism.
- Verify that no two variants occupy the same point on a chosen axis.

Completion criterion. `.agents/scratch/prototypes/<variant-id>/directions.json` exists on disk specifying 3 to 5 named directions with mutually exclusive variation axes.

### Step 4. Harness construction

Assemble the isolated preview environment and embed the standard picker.

- Dev server environment. Create a dedicated route or preview page at `/prototypes/<component-slug>` containing variant components and the harness.
- Static environment. Generate a single self-contained HTML file containing inline styles and scripts for direct browser execution.
- Picker integration. Copy markup, styles, and event wiring verbatim from [PICKER.md](PICKER.md).
- Display standards. Render one variant at a time at full size with surrounding layout context instead of using thumbnail grids, and switch variants instantly without transitional animations.

Completion criterion. The operational harness renders variants one at a time and switches instantly via keyboard and mouse controls.

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

1. When the user selects a winner, write `.agents/scratch/prototypes/<variant-id>/PROTOTYPE_LOCK.md` containing:
   - `variant_id`
   - `selected_direction` (the direction name from Step 3)
   - `selection_timestamp` (ISO 8601)
   - `harness_path` (from `.agents/state/prototype/harness-path.txt`)
   - `files_to_promote`
2. Copy the lock file to `.agents/state/prototype/locks/<variant-id>.md` for durable record.
3. Migrate the winning component into production paths following codebase file structure and token conventions.
4. Delete the prototype route, variant files, and harness unless the user explicitly requests retention. Do not delete `PROTOTYPE_LOCK.md` or its archived copy.

Completion criterion. `.agents/scratch/prototypes/<variant-id>/PROTOTYPE_LOCK.md` exists on disk with all five fields. `.agents/state/prototype/locks/<variant-id>.md` exists with matching content. `ls /prototypes/` (or the framework equivalent path from `harness-path.txt`) returns zero prototype files unless the user requested retention.

## Boundary isolation

Keep prototype code strictly confined to scratch preview paths (`/prototypes/` or temporary HTML files):
- Keep prototype edits confined to scratch preview paths; never modify production component files, routing tables, or global build configurations during exploration.
- Strip prototype harnesses and scratch dependencies before merging; do not commit prototype harnesses or scratch dependencies to production bundles.

## Invocation variants

| Invocation | Behavior |
|---|---|
| `<description>` | Full workflow covering scope, recon, 3 variants, picker, and waiting for choice |
| `<description> x5` | Full workflow with 5 variants |
| `riff <variant>` | New round keeping the harness and diverging around the chosen variant |
| `keep <variant>` | Promote that variant into the codebase and delete the prototype surface |
| `keep <variant>, leave the picker` | Promote that variant while retaining the prototype surface |

## Quick audit checklist

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
