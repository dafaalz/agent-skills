---
name: ui-motion
description: Use when adding interface animations, gestures, or auditing motion performance. Don't use for static CSS styling or general layout bugs.
---

# UI motion engineering

Design, build, audit, and optimize hardware-accelerated user interface motion.

## Overview

UI motion engineering delivers hardware-accelerated, physically grounded interface motion that preserves utility, improves spatial orientation, and avoids decorative bloat. Every motion must pass frequency gating, use the most performant execution layer, respect user accessibility preferences, and operate under strict duration budgets.

Consult deep reference documents in references/ for recipes, gesture physics, mobile native environments, vocabulary mapping, Google rendering standards, and audit playbooks.

## Workflow router

Identify user intent and route execution immediately:

1. **Authoring animations from scratch.** Follow the build sequence below to gate necessity, select tools, and pick exact tokens. Consult [references/recipes.md](references/recipes.md) for pre-built component patterns.
2. **Refining tactile micro-interactions.** Add active press feedback, anchor popovers to trigger coordinates, eliminate secondary tooltip delays, and format reviews using the Before, After, Why table.
3. **Fluid gestures and spring physics.** Consult [references/physics-and-gestures.md](references/physics-and-gestures.md) for Apple momentum decay projection, rubber band boundaries, pointer capture, and velocity handoffs.
4. **Codebase audits and refactor planning.** When explicitly called with an audit request (e.g. `/ui-motion audit <target>`), follow [references/audit-and-plans.md](references/audit-and-plans.md) to inspect the repository against motion failure modes and generate structured refactor plans under `plans/` without mutating source files.
5. **Mobile web and native platform motion.** Consult [references/mobile-web-and-native.md](references/mobile-web-and-native.md) for mobile Safari viewport sizing (`100dvh`), 300ms tap delay elimination, 16px input auto-zoom prevention, touch overscroll boundaries, and React Native Reanimated worklet UI thread isolation.
6. **Translating informal animation vocabulary.** Consult [references/vocabulary.md](references/vocabulary.md) when the user describes an animation informally or by sensation rather than technical names.
7. **Browser compositor and Google rendering standards.** Consult [references/google-standards.md](references/google-standards.md) when diagnosing Chromium layer explosion, auditing Core Web Vitals (INP and CLS) frame budgets, adopting Material Design 3 motion tokens, or implementing Android physics-based fling and spring animations.

## Execution invariants

Avoid these core failure modes:

1. **Animating elements that must stay static.** The frequency gate below intentionally produces zero lines of code when motion degrades utility. Deliver an instant state toggle instead.
2. **Using incorrect motion properties.** Avoid `ease-in` on entrances, `scale(0)` on mounting elements, keyframes on rapidly triggered elements, or sluggish durations above 300ms.
3. **Approximating motion values.** Take every curve, duration, and spring parameter from the reference tables. Never invent arbitrary cubic-bezier coordinates.
4. **Altering source code during audits.** When auditing repositories, generate structured plans under `plans/` without mutating source files.

## The build sequence

### 1. Frequency gate

Evaluate interaction frequency before writing motion code:

| Frequency                                                                 | Decision                                                        |
| ------------------------------------------------------------------------- | --------------------------------------------------------------- |
| 100+ times per day (keyboard shortcuts, command palette, core navigation) | Disqualify motion immediately. Use an instant 0ms state toggle. |
| Tens of times per day (hover effects, list navigation, frequent toggles)  | Limit to subtle transitions under 160ms or disqualify.          |
| Occasional (modals, drawers, toasts, settings dialogs)                    | Eligible for standard transitions.                              |
| Rare or first-time (onboarding, empty states, task completion)            | Permitted for expressive feedback transitions.                  |

Keyboard-initiated actions disqualify animation automatically. Raycast uses no open or close animation because users trigger it hundreds of times daily. Use instant state changes for keyboard workflows.

If the request fails this gate, state the decision directly and do not write animation code. Deliver the non-motion alternative instead.

### 2. Sanctioned purpose

Name exactly one sanctioned purpose before writing code:

- **Feedback.** Confirm that the interface registered user interaction.
- **Spatial consistency.** Show element origin and departure points.
- **State indication.** Make a state transition legible.
- **Preventing a jarring change.** Bridge content that would otherwise jump instantaneously.
- **Explanation.** Demonstrate how an onboarding or marketing flow operates.
- **Delight.** Permitted only at the rare or first-time tier.

If no purpose applies, halt and do not write animation code. Data tables, financial graphs, and reading content must remain stationary.

### 3. Cheapest tool that works

Walk down this table in order and select the first matching tool:

| Need                                                              | Tool                        |
| ----------------------------------------------------------------- | --------------------------- |
| Hover, press, color, class toggle                                 | CSS transition              |
| Entry animation on mount without JS state                         | CSS `@starting-style`       |
| Predetermined motion running off the main thread during load      | CSS animation               |
| Programmatic control with CSS performance, zero dependencies      | WAAPI (`element.animate()`) |
| Springs, layout animations, exit animations, interactive gestures | Motion (`motion.dev`)       |

CSS transitions outperform JavaScript under load because they execute on the GPU compositor thread. In contrast, `requestAnimationFrame` drops frames while the browser executes scripts or hydrates components. Reserve JavaScript for dynamic physics or interruptible gestures.

For complex headless UI primitives (toasts, drawers, command menus), rely on battle-tested libraries such as Sonner or Vaul to manage ARIA attributes and focus traps properly.

### 4. Hardware-accelerated transform and opacity

- **Animate `transform` and `opacity` exclusively.** They skip layout recalculation and paint passes, running on the compositor thread. Properties like `width`, `height`, `margin`, `padding`, `top`, and `left` force expensive layout thrashing. Allow `height` only on accordions where transform cannot match the behavior.
- **Never use `scale(0)`.** Start entry transitions from `scale(0.95)` with zero opacity.
- **Set `transform-origin` at the trigger.** Anchor popovers, dropdowns, and tooltips to their trigger using `var(--transform-origin)`. Modals remain exempt and stay centered.
- **Use percentage values in `translate()`.** A value like `translateY(100%)` scales with the element dimensions instead of a fragile pixel count.
- **In Framer Motion, specify full transform strings.** Shorthand props (`x`, `y`, `scale`) run through requestAnimationFrame on the main thread and drop frames under CPU load. Provide explicit transform strings:

```jsx
<motion.div animate={{ x: 100 }} />                          /* drops frames under load */
<motion.div animate={{ transform: "translateX(100px)" }} />  /* hardware accelerated */
```

- **Avoid parent CSS variable updates during gestures.** Setting custom properties on parent elements triggers style recalculation across all child elements. Apply inline transforms directly to the target element.

### 5. Easing curves and duration budget

Standard browser easings lack punch. Use these tokens:

```css
--ease-out: cubic-bezier(0.23, 1, 0.32, 1); /* strong ease-out for UI entries */
--ease-in-out: cubic-bezier(
  0.77,
  0,
  0.175,
  1
); /* strong ease-in-out for on-screen movement */
--ease-drawer: cubic-bezier(0.32, 0.72, 0, 1); /* iOS drawer curve */
```

Apply these easing selection rules:

- Use `ease-out` for entering or exiting elements because it starts quickly and feels responsive.
- Use `ease-in-out` for moving or morphing on screen.
- Use `ease` for hover or color changes.
- Use `linear` for constant motion such as marquees and progress indicators.
- Use `ease-out` as the default curve.

Never use `ease-in` on interactive UI elements. It delays visual response and makes interfaces feel sluggish.

Follow this duration budget reference:

| Element                             | Target duration  |
| ----------------------------------- | ---------------- |
| Button press feedback               | 100 to 160ms     |
| Tooltips and small popovers         | 125 to 200ms     |
| Dropdowns and selects               | 150 to 250ms     |
| Modals and sheet drawers            | 200 to 400ms     |
| Marketing or explanatory animations | Can exceed 400ms |

Keep functional UI animations under 300ms. A 180ms dropdown feels faster and more responsive than a 400ms dropdown.

### 6. Accessibility and SSR hydration safety

Include accessibility and pointer checks in all delivered animation styles:

```css
@media (prefers-reduced-motion: reduce) {
  [data-motion-enter],
  .element {
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

Never branch conditionally on `useReducedMotion()` in JSX before initial hydration. Tag swapping (`if (reduce) return <div>` versus `<motion.div>`) triggers React 19 hydration mismatches and traps server-rendered `opacity: 0` in permanent invisibility. Use identical DOM trees with `[data-motion-enter]` attribute contracts and CSS `!important` overrides.

## Review format

When reviewing or proposing UI micro-interaction changes, format findings using an exact table with Before, After, and Why columns:

| Before                                | After                                       | Why                                                                     |
| ------------------------------------- | ------------------------------------------- | ----------------------------------------------------------------------- |
| `transition: all 300ms`               | `transition: transform 200ms ease-out`      | Specify exact properties to avoid expensive style recalculations        |
| `transform: scale(0)`                 | `transform: scale(0.95); opacity: 0`        | Physical objects never emerge from absolute zero                        |
| `ease-in` on dropdown                 | `ease-out` with custom curve                | `ease-in` delays initial motion and feels sluggish                      |
| Missing active press feedback         | `transform: scale(0.97)` on active press    | Pressable targets must provide immediate tactile feedback               |
| `transform-origin: center` on popover | `transform-origin: var(--transform-origin)` | Popovers scale from trigger origin, while dialog modals remain centered |

## Never ship checklist

Verify code against this checklist before delivering. Every item represents an automatic rejection:

| Never                                                              | Instead                                                                 |
| ------------------------------------------------------------------ | ----------------------------------------------------------------------- |
| `transition: all`                                                  | Name the exact properties                                               |
| `transform: scale(0)` entrance                                     | `scale(0.95)` with zero opacity                                         |
| `ease-in` on interactive UI                                        | `ease-out` or a custom curve token                                      |
| Built-in `ease-out` on deliberate UI                               | `cubic-bezier(0.23, 1, 0.32, 1)`                                        |
| Animation on keyboard actions or shortcuts                         | Instant 0ms state toggle                                                |
| Functional UI duration over 300ms                                  | 150 to 250ms                                                            |
| `transform-origin: center` on anchored popover                     | `var(--transform-origin)` (dialog modals exempt)                        |
| Keyframes on rapidly triggered elements                            | CSS transitions or springs                                              |
| Animating `width`, `height`, `margin`, `padding`, `top`, or `left` | `transform` and `opacity`                                               |
| Framer Motion shorthand props under load                           | Full `transform` string                                                 |
| Ungated hover motion                                               | `@media (hover: hover) and (pointer: fine)`                             |
| Missing `prefers-reduced-motion`                                   | Gentler variant preserving opacity                                      |
| Everything entering simultaneously                                 | 30 to 80ms stagger                                                      |
| Hard stops at drag boundaries                                      | Elastic boundary resistance                                             |
| Pure distance-only swipe dismissals                                | Velocity-based dismissal calculation                                    |
| JSX branching on `useReducedMotion()`                              | Attribute contract `[data-motion-enter]` with `!important` CSS override |

## Quick verification checklist

| Check             | Passing condition                                                            |
| ----------------- | ---------------------------------------------------------------------------- |
| Frequency gate    | Interaction frequency verified, keyboard actions execute with 0ms delay      |
| Purpose           | Exactly one sanctioned purpose declared                                      |
| Acceleration      | Only `transform` and `opacity` animated (except documented accordion height) |
| Curves and timing | Custom cubic bezier or spring parameters used, durations under 300ms         |
| Origin            | Anchored popovers expand from triggers, modals expand from center            |
| Accessibility     | `prefers-reduced-motion` and pointer media queries included                  |
| Self-containment  | Output provides working code first, followed by gate result and parameters   |
