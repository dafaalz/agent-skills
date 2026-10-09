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
| 100+ times/day (keyboard shortcuts, command palette, core nav) | Disqualify motion immediately. Use instant 0ms state toggle. |
| Tens of times/day (hover effects, list selection, frequent toggles) | Limit to subtle transitions under 160ms or disqualify. |
| Occasional (modals, sheet drawers, toasts, settings dialogs) | Eligible for standard transitions (150ms to 250ms). |
| Rare or first-time (onboarding, empty states, task completion) | Permitted for expressive transitions (up to 400ms). |

Keyboard-initiated actions disqualify animation automatically. If disqualified, output the instant 0ms state toggle and state why.

### Step 2. Declare sanctioned purpose

Declare exactly one purpose before writing code:
- **Feedback.** Confirm the interface registered user interaction.
- **Spatial consistency.** Show element origin and departure points.
- **State indication.** Make a state transition legible.
- **Preventing a jarring change.** Bridge content that would otherwise jump instantaneously.
- **Delight.** Permitted only for rare or first-time interactions.

If no purpose applies, do not write animation code. Data tables and reading content must remain stationary.

### Step 3. Tool selection

Select the cheapest capable tool:
1. Hover, press, color, class toggle: **CSS transition**
2. Entry animation on mount without JS: **CSS `@starting-style`**
3. Predetermined loop running off main thread: **CSS `@keyframes`**
4. Programmatic control with zero dependencies: **Web Animations API (`element.animate()`)**
5. Springs, layout animations, gestures: **Motion (`motion.dev` / Framer Motion)**

Consult `references/recipes.md` for pre-built component patterns and `references/physics-and-gestures.md` for velocity handoffs and spring physics.

### Step 4. Hardware acceleration and property scoping

- **Animate `transform` and `opacity` exclusively.** They skip layout recalculation and paint passes. Properties like `width`, `height`, `margin`, `padding`, `top`, and `left` cause layout thrashing. Allow `height` only on accordions.
- **Never use `scale(0)`.** Start entry transitions from `scale(0.95)` with `opacity: 0`.
- **Set `transform-origin` at the trigger.** Anchor popovers, dropdowns, and tooltips to trigger coordinates. Modals remain centered.
- **In Framer Motion, specify full transform strings** under heavy load: `<motion.div animate={{ transform: "translateX(100px)" }} />` to stay on GPU compositor.

### Step 5. Easing curves and duration budget

Use these custom tokens instead of standard browser easings:

```css
--ease-out: cubic-bezier(0.23, 1, 0.32, 1);    /* strong ease-out for UI entries */
--ease-in-out: cubic-bezier(0.77, 0, 0.175, 1); /* strong ease-in-out for movement */
--ease-drawer: cubic-bezier(0.32, 0.72, 0, 1);  /* iOS drawer curve */
```

Rules:
- Never use `ease-in` on interactive UI entries. It delays visual response and feels sluggish.
- Use `ease-out` as default for entering elements.
- Keep functional UI animations under 300ms:
  - Button press feedback: 100ms to 160ms
  - Tooltips & small popovers: 125ms to 200ms
  - Dropdowns & selects: 150ms to 250ms
  - Modals & sheet drawers: 200ms to 300ms

### Step 6. Accessibility & reduced motion verification

Always include accessibility overrides:

```css
@media (prefers-reduced-motion: reduce) {
  [data-motion-enter], .element {
    animation: none !important;
    transition: none !important;
    transform: none !important;
    opacity: 1 !important;
  }
}

@media (hover: hover) and (pointer: fine) {
  .element:hover {
    transform: scale(1.04);
  }
}
```

Never branch conditionally on `useReducedMotion()` in JSX before hydration (prevents React 19 hydration mismatch). Use CSS overrides.

### Step 7. Deliverable format

- **Motion code:** Output verified, copy-pasteable CSS, Tailwind utility classes, or Motion component code inside a **Claude Artifact**.
- **Audit / Review requests:** Present findings using the Before, After, and Why table:

| Before | After | Why |
|---|---|---|
| `transition: all 300ms` | `transition: transform 180ms var(--ease-out)` | Animate GPU properties exclusively; avoid style recalc |
| `transform: scale(0)` | `transform: scale(0.95); opacity: 0` | Physical objects never emerge from zero |
| `ease-in` on modal open | `cubic-bezier(0.23, 1, 0.32, 1)` | `ease-in` feels sluggish and unresponsive |

## Never ship checklist

| Never | Instead |
|---|---|
| `transition: all` | Name exact properties (`transform`, `opacity`) |
| `transform: scale(0)` entrance | `scale(0.95)` with zero opacity |
| `ease-in` on interactive UI | `ease-out` or custom cubic-bezier token |
| Animation on keyboard actions or shortcuts | Instant 0ms state toggle |
| Functional UI duration over 300ms | 150ms to 250ms |
| Animating `width`, `height`, `margin`, `padding` | Animate `transform` and `opacity` |
| Ungated hover motion on touchscreens | Wrap in `@media (hover: hover) and (pointer: fine)` |
| Missing `prefers-reduced-motion` | Fallback preserving opacity with 0ms transform |
| Everything entering simultaneously | 30ms to 80ms stagger |

## Quick verification checklist

| Check | Passing condition |
|---|---|
| Frequency gate | Keyboard actions execute with 0ms delay; frequent actions under 160ms |
| Purpose | Exactly one sanctioned purpose declared |
| Acceleration | Only `transform` and `opacity` animated |
| Curves & timing | Custom cubic bezier tokens used, durations under 300ms |
| Artifact delivery | Complete, copy-pasteable code delivered in a Claude Artifact |
