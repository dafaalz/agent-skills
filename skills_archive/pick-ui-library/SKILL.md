---
name: pick-ui-library
description: Use when selecting frontend libraries, choosing UI primitives, picking animation tools, or finding curated component packages for a project.
---

# Pick UI library

Match frontend requirements to verified single-purpose libraries.

## Workflow

Follow these four steps in sequence:

### Step 1. Task classification

Extract the underlying UI problem from the user prompt instead of relying on the named library. For example, a request for a dropdown needs an unstyled primitive like base-ui, regardless of phrasing.

**Completion criterion.** An identified UI capability mapped to a single category in the curated tables.

### Step 2. Dependency check

Inspect `package.json` in the active project directory for existing dependencies before recommending a new package. If the project already contains a listed library, use it. If the project uses a working alternative such as react-window instead of Virtuoso, keep the existing dependency unless the user explicitly requests a replacement.

**Completion criterion.** Verified dependency status confirming whether the project already has the target tool or an established alternative.

### Step 3. Library recommendation

Recommend exactly one primary library from the curated tables and state its concrete mechanism in one sentence. Do not generate open-ended option lists when a direct match exists. Offer an alternative only when the table explicitly lists one, such as dialkit alongside Leva.

**Completion criterion.** A single library recommendation with its installation command and a one-sentence technical rationale.

### Step 4. Boundary fallback

When a requested task falls outside the curated tables, state that the requirement exceeds the curated list before suggesting an external alternative from general knowledge.

**Completion criterion.** An explicit out-of-scope statement followed by an uncurated recommendation.

## Curated libraries

Consult these tables to match frontend requirements to libraries:

### UI components and primitives

| Task | Library |
|---|---|
| Unstyled accessible UI components (dialogs, popovers, menus, selects) | [base-ui](https://base-ui.com) |
| Command menus (keyboard palettes) | [cmdk](https://cmdk.paco.me) |
| Toasts and notifications | [Sonner](https://sonner.emilkowal.ski) |
| One-time password and verification code inputs | [input-otp](https://input-otp.rodz.dev) |
| Control panels and debug GUIs | [Leva](https://github.com/pmndrs/leva), with [dialkit](https://joshpuckett.me/dialkit) as an alternative |

### Motion and visuals

| Task | Library |
|---|---|
| General animation (springs, layout animations, exit transitions) | [motion](https://motion.dev) |
| Number animation (counters, prices, metrics) | [NumberFlow](https://number-flow.barvian.me) |
| Animated text components | [torph](https://torph.lochie.me/) |
| Interactive 3D globes | [Cobe](https://cobe.vercel.app) |
| Dynamic OG image generation (HTML or CSS to SVG or PNG) | [Satori](https://github.com/vercel/satori) |
| Syntax highlighting | [shiki](https://shiki.style) |

Use motion for physics springs, layout shifts, exit animations, or gesture interactions. Use plain CSS transitions for simple hover states or basic opacity changes.

### Charts

| Task | Library |
|---|---|
| Streaming real-time charts | [Liveline](https://github.com/benjitaylor/liveline) |
| General dashboards (static or interactive charts) | [recharts](https://recharts.org) |

When data points stream live and the timeline scrolls continuously, select Liveline. For standard dashboards or analytical visualizations, select recharts.

### Interaction and performance

| Task | Library |
|---|---|
| Drag and drop | [dnd kit](https://dndkit.com) |
| Virtualization (large lists, tall tables) | [Virtuoso](https://virtuoso.dev) |

### State and styling

| Task | Library |
|---|---|
| Client state management | [zustand](https://zustand.docs.pmnd.rs) |
| Conditional class name strings | [clsx](https://github.com/lukeed/clsx) |
| Variant-driven styling for Tailwind CSS | [cva](https://cva.style) |
| Theme switching and dark mode without flash | [next-themes](https://github.com/pacocoursey/next-themes) |

Use clsx for ad hoc conditional class strings. Use cva when components require structured variant props such as size, tone, or visual state. The two tools compose together because cva accepts clsx expressions directly.

## Replacement patterns

Replace common ad hoc implementations with verified libraries:

- Replace custom toast implementations with Sonner.
- Replace manual div dropdowns or custom dialogs with base-ui for keyboard accessibility and focus trapping.
- Replace manual number re-rendering loops with NumberFlow for smooth digit transitions.
- Replace unvirtualized lists containing more than 1,000 items with Virtuoso.
- Replace deeply nested prop drilling or scattered React state with zustand.
- Replace multi-level template literal class ternaries with clsx or cva.
