---
name: ui-motion
description: Use when designing, building, or auditing interface animations, micro-interactions, CSS transitions, spring physics, gestures, or motion performance. Don't use for static CSS styling, color schemes, or general layout bug fixing.
---

# UI Motion Engineering for Claude Web

Design, build, audit, and optimize hardware-accelerated user interface motion on Claude Web.

<initiative_and_scope>
When asked to build or refine motion, evaluate interaction frequency first. If the motion passes the frequency gate, write complete, copy-pasteable animation code. Stop and report when done. Do not add unrequested decorative animations or complex physics to elements that should remain static.
</initiative_and_scope>

<claude_web_environment>
Operate within the Claude Web interface.
- Output complete motion code (CSS keyframes, Tailwind config, Framer Motion/Motion components, or interactive HTML/React prototypes) as standalone Claude Artifacts (`application/vnd.ant.code` or `text/html`).
- In the chat body, report the frequency gate result, sanctioned purpose, curve tokens, and duration budgets.
</claude_web_environment>

## Workflow

### Step 1. Frequency gate

Evaluate interaction frequency before writing motion code:

| Frequency | Decision |
|---|---|
| 100+ times per day (keyboard shortcuts, command palette, core navigation) | Disqualify motion immediately. Use an instant 0ms state toggle. |
| Tens of times per day (hover effects, list navigation, frequent toggles) | Limit to subtle transitions under 160ms or disqualify. |
| Occasional (modals, drawers, toasts, settings dialogs) | Eligible for standard transitions (150ms to 250ms). |
| Rare or first-time (onboarding, empty states, task completion) | Permitted for expressive feedback transitions (up to 400ms). |

Keyboard-initiated actions disqualify animation automatically. If disqualified, output the instant 0ms state toggle and state why.

Completion criterion. Interaction frequency classified and confirmed eligible for motion, or disqualified in favor of an instant 0ms state toggle.

### Step 2. Sanctioned purpose selection

Declare exactly one purpose before writing code:
- **Feedback.** Confirm that the interface registered user interaction.
- **Spatial consistency.** Show element origin and departure points.
- **State indication.** Make a state transition legible.
- **Preventing a jarring change.** Bridge content that would otherwise jump instantaneously.
- **Delight.** Permitted only for rare or first-time interactions.

If no purpose applies, do not write animation code. Data tables, financial graphs, and reading content must remain stationary.

Completion criterion. Exactly one sanctioned purpose declared before writing animation code.

### Step 3. Tool selection

Select the cheapest capable tool:
1. Hover, press, color, class toggle: **CSS transition**
2. Entry animation on mount without JS state: **CSS `@starting-style`**
3. Predetermined motion running off main thread: **CSS animation**
4. Programmatic control with CSS performance: **WAAPI (`element.animate()`)**
5. Springs, layout animations, exit animations, gestures: **Motion (`motion.dev`)**

Never mix CSS transition utility classes with JavaScript animation libraries on the same node.

Completion criterion. Cheapest capable tool selected with compositor CSS transitions prioritized over JS libraries.

### Step 4. Hardware acceleration and property scoping

- **Animate `transform` and `opacity` exclusively; never animate `width`, `height`, `margin`, `padding`, `top`, or `left`.** Transforms and opacity execute on the compositor thread without reflow.
- **Start entry transitions from `scale(0.95)` with zero opacity; never use `scale(0)`.**
- **Set `transform-origin` at trigger.** Anchor popovers, dropdowns, and tooltips to trigger coordinates via `var(--transform-origin)`. Modals stay centered.
- **Force layout reflow before unhiding off-screen transforms.** Trigger `void element.offsetHeight` between removing `hidden` and releasing offset classes.
- **Orchestrate modal and dialog exit transitions.** Never unmount or apply `hidden` synchronously. Retain dismiss classes, wait for transition completion, and restore focus to trigger.

Completion criterion. Styles animate `transform` and `opacity` exclusively with trigger-anchored origins and orchestrated exit transitions.

### Step 5. Easing curves and duration calibration

Standard browser easings lack punch. Use these tokens:
```css
--ease-out: cubic-bezier(0.23, 1, 0.32, 1); /* UI entries */
--ease-in-out: cubic-bezier(0.77, 0, 0.175, 1); /* on-screen movement */
--ease-drawer: cubic-bezier(0.32, 0.72, 0, 1); /* drawer curve */
--ease-quintic: cubic-bezier(0.22, 1, 0.36, 1); /* weighted hero entries */
--ease-expo: cubic-bezier(0.16, 1, 0.3, 1); /* kinetic text reveals */
```

Never use `ease-in` on interactive UI. It delays response and feels sluggish.

Duration budget reference:
- Button press feedback: 100ms to 160ms
- Tooltips and popovers: 125ms to 200ms
- Dropdowns and selects: 150ms to 250ms
- Modals and sheet drawers: 200ms to 400ms
- Keep functional UI under 300ms. Reserve 600ms to 1400ms for editorial storytelling.

Completion criterion. Custom cubic-bezier tokens and duration budgets assigned without `ease-in`.

### Step 6. Accessibility and SSR hydration verification

Include accessibility and pointer checks in all delivered animation styles:
```css
@media (prefers-reduced-motion: reduce) {
  [data-motion-enter], .element {
    animation: none !important; transition: none !important;
    transform: none !important; opacity: 1 !important;
  }
}
@media (hover: hover) and (pointer: fine) {
  .element:hover { transform: scale(1.04); }
}
```

Never branch conditionally on `useReducedMotion()` in JSX before hydration. Use identical DOM trees with attribute contracts and CSS `!important` overrides. Defer mobile focus past transition completion.

Completion criterion. Styles include `@media (prefers-reduced-motion: reduce)` overrides without conditional JSX tag branching.

## Execution invariants

Avoid these core failure modes:
1. **Animating elements that must stay static.** The frequency gate intentionally produces zero code when motion degrades utility. Deliver instant state toggle instead.
2. **Using incorrect motion properties.** Avoid `ease-in` on entrances, `scale(0)` on mounting, or durations above 300ms on functional UI.
3. **Approximating motion values.** Take every curve and duration from reference tables. Never invent arbitrary cubic-bezier coordinates.
4. **Altering source code during audits.** When auditing codebases, generate structured reports without mutating source files.
5. **Animating bulk historical data during initial load.** Never bind entrance animations to message histories or bulk collection renders. Render historical logs instantly without motion, and gate animations behind reactive flags (`isNew: boolean`) for live events.
6. **Tearing down ephemeral elements without exit choreography.** Never call `element.remove()` synchronously on live activity indicators (such as typing indicators). Apply an exit transition (`opacity: 0`, `translateY(4px)`) over 120ms before removing nodes from DOM.

## Quick verification checklist

| Check | Passing condition |
|---|---|
| Frequency gate | Interaction frequency verified; keyboard actions execute with 0ms delay |
| Purpose | Exactly one sanctioned purpose declared |
| Acceleration | Only `transform`, `opacity`, or documented curtain `clip-path` animated |
| Curves and timing | Custom tokens used; under 300ms for functional UI, under 1400ms for editorial |
| Historical data | Initial batch data renders instantly without animations |
| Ephemeral exit | Live activity indicators fade/slide out before unmounting |
| Accessibility | `prefers-reduced-motion` and pointer media queries included |
| Artifact deliverable | Complete animation code delivered as a Claude Artifact |
