---
name: ui-motion
description: "Use when designing, implementing, or polishing CSS transitions, FLIP animations, gesture feedback, spring physics, or delight choreography. Don't use for layout styling (use frontend-design), accessibility audits (use ui-ux-review), interactive mockups (use prototype), React render optimization (use react), or multi-task execution plans (use agent-planning)."
---

# UI motion engineering

Design, build, audit, and optimize hardware-accelerated user interface motion.

## Overview

UI motion engineering delivers hardware-accelerated, physically grounded interface motion that preserves utility, improves spatial orientation, and avoids decorative bloat. Motion copies nature to establish spatial consistency (an internal map of where intangible things live in software). Because physical nature is slow, high-frequency actions demand restraint: keyboard shortcuts execute in 0ms, ease-out curves front-load velocity, gestures remain interruptible mid-flight, and state feedback persists even when motion is disabled. Consult deep reference documents in `references/` for recipes, gesture physics, platform standards, and audit playbooks.

## Modes

Select an execution mode before Step 1:
- Author mode (default). Implement choreographies, transitions, and gesture physics.
- Audit mode. Inspect animation performance, check frame drops, and verify reduced-motion compliance without editing styles.

## Workflow router

Identify user intent and route execution immediately:

1. **Authoring animations from scratch.** Follow the build sequence below to gate necessity, select tools, and pick exact tokens. Consult [references/recipes.md](references/recipes.md) for pre-built component patterns.
2. **Mental models, time perception, and personality.** Consult [references/mental-models-and-perception.md](references/mental-models-and-perception.md) for spatial continuity, the Wise artificial delay paradox, Android touch prediction, personality calibration, and the Pokémon state feedback invariant.
3. **Refining tactile micro-interactions.** Add active press feedback, anchor popovers to trigger coordinates, eliminate secondary tooltip delays, apply context menu blink exits, and format reviews using the Before, After, Why table.
4. **Fluid gestures and spring physics.** Consult [references/physics-and-gestures.md](references/physics-and-gestures.md) for Apple momentum decay projection, rubber band boundaries, pointer capture, mid-flight retargeting, and velocity handoffs.
5. **Codebase audits and refactor planning.** When called with an audit request (e.g. `/ui-motion audit <target>`), follow [references/audit-and-plans.md](references/audit-and-plans.md) to inspect the repository against motion failure modes and generate structured refactor plans under `plans/` without mutating source files.
6. **Mobile web and native platform motion.** Consult [references/mobile-web-and-native.md](references/mobile-web-and-native.md) for mobile Safari viewport sizing (`100dvh`), 300ms tap delay elimination, 16px input auto-zoom prevention, touch overscroll boundaries, and React Native Reanimated worklet UI thread isolation.
7. **Translating informal animation vocabulary.** Consult [references/vocabulary.md](references/vocabulary.md) when the user describes an animation informally or by sensation rather than technical names.
8. **Browser compositor and Google rendering standards.** Consult [references/google-standards.md](references/google-standards.md) when diagnosing Chromium layer explosion, auditing Core Web Vitals (INP and CLS) frame budgets, adopting Material Design 3 motion tokens, or implementing Android physics-based fling and spring animations.
9. **Desktop native and platform motion.** Consult [references/desktop-and-platform.md](references/desktop-and-platform.md) for Windows 11 DWM compositor tokens, Mica backdrop rules, macOS AppKit `NSAnimationContext` atomic batching, Electron and Tauri non-client title bar dragging without IPC loop latency, and Linux Wayland buffer sync.
10. **Kinetic typography and shimmer.** Consult [references/kinetic-typography-and-shimmer.md](references/kinetic-typography-and-shimmer.md) for character stagger sequences, blur filter boundaries, text-clip gradient shimmer, webfont loading synchronization, and CDP visual test capture timing.
11. **Creative and editorial storytelling.** Consult [references/creative-and-editorial.md](references/creative-and-editorial.md) for RAF LERP pointer inertia, dynamic spotlight cards, windowed parallax, clip-path curtain wipes, dimensional multi-plane hero layering, and SVG grain.
12. **Canvas scrubbing and smooth scroll.** Consult [references/canvas-and-scroll-scrubbing.md](references/canvas-and-scroll-scrubbing.md) for Lenis synchronization, 2D canvas frame sequences, dense GOP video scrub encoding, DPR capping, predictive caching, and sliding pill tabs.

## Reference quick routing

| Motion domain | Reference module | Scope |
|---|---|---|
| Animation & delight | [references/animation-and-delight.md](references/animation-and-delight.md) | Micro-interactions, spring physics, & delight choreography |
| Component recipes | [references/recipes.md](references/recipes.md) | Pre-built component animations & transitions |
| Physics & gestures | [references/physics-and-gestures.md](references/physics-and-gestures.md) | Apple momentum decay, rubber-banding, & gestures |
| Mobile & native | [references/mobile-web-and-native.md](references/mobile-web-and-native.md) | Mobile Safari viewport, 100dvh, & touch latency |
| Desktop & platform | [references/desktop-and-platform.md](references/desktop-and-platform.md) | Windows Mica, macOS AppKit, & Electron frame timing |
| Google standards | [references/google-standards.md](references/google-standards.md) | Material 3 motion tokens & Core Web Vitals INP/CLS |
| Kinetic typography | [references/kinetic-typography-and-shimmer.md](references/kinetic-typography-and-shimmer.md) | Character stagger sequences & gradient shimmer |
| Canvas & scroll | [references/canvas-and-scroll-scrubbing.md](references/canvas-and-scroll-scrubbing.md) | Smooth scroll sync & canvas frame scrubbing |
| Creative & editorial | [references/creative-and-editorial.md](references/creative-and-editorial.md) | RAF LERP pointer inertia, spotlight cards, & wipes |
| Mental models | [references/mental-models-and-perception.md](references/mental-models-and-perception.md) | Spatial continuity & time perception calibration |
| Vocabulary | [references/vocabulary.md](references/vocabulary.md) | Informal motion descriptions to technical tokens |
| Audit playbooks | [references/audit-and-plans.md](references/audit-and-plans.md) | Performance inspection & non-destructive audit plans |

## Execution invariants

Avoid these core failure modes:

1. **Animating elements that must stay static.** The frequency gate below intentionally produces zero lines of code when motion degrades utility. Deliver an instant state toggle instead.
2. **Animating keyboard-initiated actions.** Never animate actions triggered by keyboard shortcuts (`Cmd+Space`, `Esc`, `Tab`). Users know the outcome; animation forces waiting. Deliver an instant 0ms state change.
3. **Dropping state feedback when motion is disabled (The Pokémon principle).** Never eliminate state registration when animations are turned off. Preserve instant tactile or visual cues (selection blinks, high-contrast flashes; never use shake as shake is a vestibular trigger).
4. **Locking user input during animation.** Transitions must remain interruptible and retargetable mid-flight. Never apply `pointer-events: none` to transforming elements.
5. **Using instant transitions on high-stakes operations (The Wise paradox).** Completing financial or irreversible actions in 0ms induces user distrust. Use an artificial 350ms to 450ms confirmation animation to close the perception delta.
6. **Using incorrect motion properties.** Avoid `ease-in` on interactive entrances, `scale(0)` on mounting elements, keyframes on rapidly triggered elements, or sluggish durations above 300ms.
7. **Approximating motion values.** Take every curve, duration, and spring parameter from the reference tables. Never invent arbitrary cubic-bezier coordinates.
8. **Altering source code during audits.** When auditing repositories, generate structured plans under `plans/` without mutating source files.
9. **Animating bulk historical data during initial load.** Never bind entrance animations to message histories or bulk collection renders. Render historical logs instantly without motion, and gate animations behind reactive flags (`isNew: boolean`) for live events.
10. **Tearing down ephemeral elements without exit choreography.** Never call `element.remove()` synchronously on live activity indicators. Apply an exit transition (`opacity: 0`, `scale(0.95)`) over 120ms before removing nodes from the DOM.

## The build sequence

### Step 1. Frequency gate

Evaluate interaction frequency before writing motion code:

| Frequency | Decision |
| --- | --- |
| 100+ times per day (keyboard shortcuts, command palette, core navigation) | Disqualify motion immediately. Use an instant 0ms state toggle. |
| Context menus and right-click actions | Open instantly in 0ms; animate selection blink and 120ms fade-out on exit only. |
| Tens of times per day (hover effects, list navigation, frequent toggles) | Limit to subtle transitions under 160ms or disqualify. |
| Occasional (modals, drawers, toasts, settings dialogs) | Eligible for standard transitions (150ms to 250ms). |
| Rare or high-stakes (onboarding, task completion, financial settlement) | Permitted for expressive feedback or artificial trust confirmation (up to 450ms). |

If the request fails this gate, state the decision directly and do not write animation code. Deliver the non-motion alternative instead.

Completion criterion. The interaction frequency is classified and confirmed eligible for motion, or disqualified in favor of an instant 0ms state toggle.

### Step 2. Sanctioned purpose selection

Name exactly one sanctioned purpose before writing code:

- **Feedback.** Confirm that the interface registered user interaction.
- **Spatial consistency.** Show element origin and departure points to build an internal map of where controls live.
- **State indication.** Make a state transition legible.
- **Preventing a jarring change.** Bridge content that would otherwise jump instantaneously.
- **Explanation.** Demonstrate how an onboarding or marketing flow operates.
- **Trust calibration.** Bridge the perception delta during instantaneous high-stakes operations (such as payments or deletions).
- **Delight.** Permitted only at the rare or first-time tier.

If no purpose applies, halt and do not write animation code. Data tables, financial graphs, and reading content must remain stationary.

Completion criterion. Exactly one sanctioned purpose declared before writing animation code.

### Step 3. Tool selection

Walk down this table in order and select the first matching tool:

| Need | Tool |
| --- | --- |
| Hover, press, color, class toggle | CSS transition |
| Mount/exit animation without JS runtime | CSS `@starting-style` + `transition-behavior: allow-discrete` |
| Shared-element & DOM state morphs | `document.startViewTransition(() => flushSync(fn))` with dynamic `view-transition-name` cleanup |
| Scroll-tied reveal or progress | CSS Scroll-driven animations (`animation-timeline: view()`) |
| Predetermined motion off main thread | CSS animation |
| Programmatic interrupts with CSS performance | WAAPI (`element.animate()`) with `composite: "add"` (commitStyles + cancel on finish; cap at 8 instances) |
| Springs, layout transitions, exit animations, gestures | Motion (`motion.dev`) |

Never run two animation engines on the exact same property simultaneously.

Completion criterion. The cheapest capable tool is selected with compositor CSS transitions prioritized over JavaScript animation libraries.

### Step 4. Hardware acceleration and property scoping

- **Animate `transform` and `opacity` exclusively; never animate `width`, `height`, `margin`, `padding`, `top`, or `left`.** Transforms and opacity run directly on the compositor thread without layout recalculation. Accordions use `grid-template-rows: 0fr -> 1fr` or `interpolate-size: allow-keywords`. Allow `clip-path: inset()` on creative editorial curtain reveals.
- **Start entry transitions from `scale(0.95)` with zero opacity; never use `scale(0)`.**
- **Set `transform-origin` with fallback at the trigger.** Anchor popovers, dropdowns, and tooltips using `var(--transform-origin, center)` with trigger coordinates. Modals remain exempt and stay centered via `margin: auto`.
- **Provide tactile press feedback on all touch and pointer surfaces.** Gate `:hover` strictly by `@media (hover: hover) and (pointer: fine)`. Apply `:active` `transform: scale(0.97)` with `touch-action: manipulation` directly to pressable targets.
- **Mount and exit orchestration:** Use `@starting-style` for mount frames. Gate exit unmounting on `transitionend` (verifying `e.target === e.currentTarget`), `transitioncancel`, and a deterministic `(duration + 34ms)` fallback watchdog timer.
- **View Transitions pseudo-elements:** Set `pointer-events: none` on `::view-transition-group(*)`. Lock `height: 100%` and `object-fit: none` on `::view-transition-old/new` during container aspect-ratio morphs. Scope unique `view-transition-name` tokens dynamically to active elements only and remove on completion.

Completion criterion. Motion styles animate `transform` and `opacity` exclusively with valid trigger-anchored transform origins and orchestrated exit transitions.

### Step 5. Easing curves, spring physics, and ProMotion synchronization

```css
--ease-out: cubic-bezier(0.23, 1, 0.32, 1); /* strong ease-out front-loading velocity for UI entries */
--ease-in: cubic-bezier(0.32, 0, 0.67, 0); /* fast acceleration for UI exits */
--ease-in-out: cubic-bezier(0.77, 0, 0.175, 1); /* on-screen repositioning and curtain wipes */
--ease-drawer: cubic-bezier(0.32, 0.72, 0, 1); /* iOS drawer curve */
--ease-quintic: cubic-bezier(0.22, 1, 0.36, 1); /* weighted editorial presentations, hero entries */
--ease-expo: cubic-bezier(0.16, 1, 0.3, 1); /* kinetic text stagger, high-velocity reveals */
```

Apply these easing and personality selection rules:
- Use `ease-out` for entering elements. Exits may use `ease-in` to accelerate off-screen. Never use `ease-in` on interactive entrances or press feedback.
- Use `ease-in-out` for elements already on screen changing position or morphing.
- Use `linear` for scroll timelines (`animation-timeline: view()`) and hold-to-confirm progress indicators.
- Calibrate springs: UI uses `{ stiffness: 300, damping: 30 }` (critically damped, zero bounce); active press uses `{ stiffness: 400, damping: 17 }`.
- Mid-flight retargeting mutates the target coordinate on a single stateful solver inheriting live instantaneous velocity `v(t)` and position `x(t)` without resetting state.
- Gesture flick velocity filtering computes release velocity across samples in a rolling 40ms ring buffer, zeros velocity if idle over 45ms, and clamps release velocity to `[-3500, 3500]` px/s.
- ProMotion RAF loops integrate physics via timestamp deltas clamped to `dt <= 0.032s` with `4ms` (240Hz) internal sub-stepping to prevent tunneling or explosion after tab throttling.

Follow this duration budget reference:

| Element | Target duration |
| --- | --- |
| Button press feedback | 100 to 160ms |
| Tooltips and small popovers | 125 to 200ms |
| Dropdowns and selects | 150 to 250ms |
| Modals and sheet drawers | 200 to 400ms |
| High-stakes trust confirmation | 350 to 450ms |
| Creative editorial storytelling | 600 to 1400ms |

Keep functional UI animations under 300ms. Reserve 600 to 1400ms for creative editorial entrances.

Completion criterion. Custom cubic bezier tokens and duration budgets assigned without using `ease-in` on entrances.

### Step 6. Accessibility, fallback feedback, and SSR hydration

```css
@media (prefers-reduced-motion: reduce) {
  *, ::before, ::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
@media (hover: hover) and (pointer: fine) {
  .element:hover { transform: scale(1.04); }
}
```

Never branch conditionally on `useReducedMotion()` in JSX before initial hydration. Tag swapping triggers React 19 hydration mismatches and traps server-rendered `opacity: 0` in permanent invisibility. Use identical DOM trees with `[data-motion-enter]` attribute contracts and CSS `!important` overrides.

Disable spatial motion deltas without overriding structural layout transforms (`translate3d(x,y,0)` and `translate(-50%, -50%)`). Never apply `transform: none !important` globally under reduced motion because it breaks positioning transforms. Collapse animation durations and replace spatial entrances with opacity fades.

Preserve state feedback under reduced motion (The Pokémon principle). Replace spatial motion with an instant border flash, selection blink, or background tint pulse so users register state changes without motion sickness. Never preserve shake; shake is a vestibular trigger.

Defer mobile focus past transition completion. Delay `.focus({ preventScroll: true })` until the entry transition completes (duration + 10ms). Never auto-focus text inputs on touch viewports (`pointer: coarse` or `< 640px`) to prevent virtual keyboard layout jumps. Focus the container or close button instead.

Completion criterion. Styles include `@media (prefers-reduced-motion: reduce)` overrides with preserved non-motion feedback and zero conditional JSX tag branching.

## Boundary isolation

Confine animation rules strictly to motion timing, CSS transforms, and gesture hooks. Never alter core application state logic, backend API calls, or accessibility roles in the name of animation.

## Review format

When reviewing or proposing UI micro-interaction changes, format findings using an exact table with Before, After, and Why columns:

| Before | After | Why |
| --- | --- | --- |
| `transition: all 300ms` | `transition: transform 200ms ease-out` | Specify exact properties to avoid expensive style recalculations |
| `transform: scale(0)` | `transform: scale(0.95); opacity: 0` | Physical objects never emerge from absolute zero |
| `ease-in` on dropdown entrance | `ease-out` with custom curve | `ease-in` on entrance delays initial motion and feels sluggish |
| Missing active press feedback | `transform: scale(0.97)` on active press | Pressable targets must provide immediate tactile feedback |
| `transform-origin: center` on popover | `var(--transform-origin, center)` | Popovers scale from trigger origin, while dialog modals remain centered |
| 400ms enter on keyboard shortcut | Instant 0ms toggle | Keyboard actions reflect deliberate user intent and require zero waiting |
| Removing state feedback on reduced motion | Instant border flash or selection blink | Retain state impact proof when motion is disabled (The Pokémon principle) |

## Quick audit checklist

Verify code against this checklist before delivering. Every item represents an automatic rejection:

| Never | Instead |
| --- | --- |
| `transition: all` | Name the exact properties (`transform`, `opacity`) |
| `transform: scale(0)` entrance | `scale(0.95)` with zero opacity |
| `ease-in` on interactive entrances | `ease-out` token (exits may use `ease-in`) |
| Built-in `ease-out` on deliberate UI | `cubic-bezier(0.23, 1, 0.32, 1)` |
| Animation on keyboard actions or shortcuts | Instant 0ms state toggle |
| Context menu entrance animation | Instant 0ms entry, selection blink, 120ms exit fade |
| Eliminating state feedback when motion is off | Retain instant blink, border pulse, or color flash; never shake |
| Non-interruptible animation or blocked pointer events | Retarget live presentation transforms mid-flight |
| 0ms transition on high-stakes operations | 350ms to 450ms confirmation to close perception delta |
| Functional UI duration over 300ms | 150 to 250ms |
| `transform-origin` without fallback | `var(--transform-origin, center)` |
| Keyframes on rapidly triggered elements | CSS transitions or springs |
| Animating `width`, `height`, `margin`, `padding`, `top`, or `left` | `transform` and `opacity` (accordions use grid rows or interpolate-size) |
| Non-accelerated JS transform loops | WAAPI compositor execution or CSS transitions |
| Ungated hover motion | `@media (hover: hover) and (pointer: fine)` |
| Global `transform: none !important` under reduced motion | Collapse durations to 0.01ms; preserve structural centering transforms |
| Unmounting without transitionend guard or fallback | Filter `e.target === e.currentTarget`, listen to `transitioncancel`, watchdog timer |
| Unclamped delta-time in RAF physics loops | Clamp `dt <= 0.032s` with 4ms internal sub-stepping |
| Duplicate `view-transition-name` tokens | Scope tokens dynamically during active transition and clean up on finish |
