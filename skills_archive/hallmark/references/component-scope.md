# Component-scope flow

When the brief is a component rather than a full page, follow this specialized runbook.

## Component-scope signals

Check scope before entering the full design flow:
- The brief names a single UI element: button, input, card, modal, dropdown, tooltip, select, checkbox, switch, tab strip, chip, badge, banner, snackbar, popover, slider, date picker, or avatar.
- The brief is short (under 30 words) and refers to one element.
- The target file is a single component (such as `./Button.tsx`, `./components/Input.css`, `app/components/Card.vue`).
- The user explicitly requests a single element ("just the button", "only this card").

If two signals fire, route to component scope.

## What component scope retains

- **Step 0. Pre-flight scan.** Read existing tokens, fonts, framework, and microinteraction stance. A button in a project using Geist and Tailwind must adopt those tokens rather than inventing new ones.
- **Step 1. Genre detection.** Editorial, modern minimal, atmospheric, or playful. The component inherits the genre of its surroundings.
- **Step 2.6. Theme route.** If `tokens.css` or `design.md` exists, the component uses those tokens.
- **Font discipline.** Use the standard project font pairing.
- **State discipline.** Every interactive component must support all eight states: default, hover, focus-visible, active, disabled, loading, error, and success. Consult `references/interaction-and-states.md`.
- **Slop test.** Run visual, microinteraction, contrast, and accessibility gates.

## What component scope skips

- Step 2. Macrostructure selection (components do not have page macrostructures).
- Navigation and footer archetypes.
- Hero polish patterns.
- Step 4. Hero enrichment.
- Step 5. Multi-section preview (replaced by the eight-state demo wrapper).
- Project memory logging (components do not rotate catalog themes).

## What component scope emits

Emit two files side by side:

1. **The component artifact.** A single self-contained file matching project conventions:
   - React, Vue, or Svelte: `Button.tsx`, `Button.vue`, or `Button.svelte`.
   - Vanilla web: `button.css` plus `button.html`.
   - Tailwind: a component file with class chains and a companion `tokens.css` if missing.
   - The component consumes tokens by name (`var(--color-accent)`) without inlining arbitrary OKLCH values.

2. **Eight-state demo wrapper.** `<ComponentName>.preview.html` or `<ComponentName>.preview.tsx`. A standalone preview rendering all eight states stacked vertically:

```text
┌──── Button: 8 states ──────────────────────────┐
│                                                │
│ default       [ Click me                  ]    │
│ hover         [ Click me                  ]    │
│ focus         [ Click me                  ]    │
│ active        [ Click me                  ]    │
│ disabled      [ Click me                  ]    │
│ loading       [ Working...                ]    │
│ error         [ Try again                 ]    │
│ success       [ Saved                     ]    │
│                                                │
└────────────────────────────────────────────────┘
```

## Stamp format for component output

Stamp component artifacts using this format:

```css
/* Hallmark: component: <type>, genre: <genre>, theme: <theme>
 * states: default, hover, focus, active, disabled, loading, error, success
 * contrast: pass
 */
```
