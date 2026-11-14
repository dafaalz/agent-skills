---
name: ui-motion
description: Use when designing, implementing, or auditing CSS transitions, FLIP animations, View Transitions, gesture physics, or reduced-motion fallbacks. Don't use for static layout styling (use frontend-design), full WCAG accessibility audits (use ui-ux-review), React render memoization (use react), or prose editing (use unslop).
---

# UI motion engineering

Design, implement, and audit compositor-accelerated interface motion with deterministic timing, interruptible physics, and reduced-motion state preservation.

<HARD-GATE>
Write-Target Boundary. In Author mode, write only to component stylesheets, motion tokens, and animation hooks explicitly targeted by the user, plus state artifacts under `.agents/state/ui-motion/`. In Audit mode, write only to `.agents/state/ui-motion/audit-findings.md` and `docs/superpowers/plans/ui-motion-plan.md`. Never modify backend calls, state reducers, or ARIA roles. Any change to existing `prefers-reduced-motion` handlers requires explicit user confirmation.
</HARD-GATE>

## Modes

Declare the active operating mode before executing Step 1:
- `author` (default). Execute Steps 1 through 6 sequentially to produce motion styles and hooks.
- `audit`. Execute Steps 1, 2, 5, and 6 in read-only inspection mode against target files, write `.agents/state/ui-motion/audit-findings.md` and `docs/superpowers/plans/ui-motion-plan.md`, and halt without mutating source files.

## Reference quick routing

| Motion domain | Reference module | Scope |
|---|---|---|
| Animation & delight | [references/animation-and-delight.md](references/animation-and-delight.md) | Micro-interactions, spring physics, & delight choreography |
| Spring tokens | [references/springs.md](references/springs.md) | Spring physics tokens & branded compositor target |
| Concurrency & budget | [references/slots.md](references/slots.md) | Surface registry, React 19 starvation, & budget |
| Pointer & haptics | [references/pointer.md](references/pointer.md) | Pencil latch, hover suppression, & haptics |
| 43 transitions catalog | [references/catalog.md](references/catalog.md) | Micro-distances & 43 interaction transitions |
| Subgrid & skeletons | [references/integration.md](references/integration.md) | Subgrid isolation, portal contracts, & skeletons |
| Transitions index | [references/transitions-and-micro-distances.md](references/transitions-and-micro-distances.md) | Index mapping to all 5 motion modules |
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

1. **Zero-latency keyboard execution.** Keyboard shortcuts, command palettes, and focus navigation (`Cmd+K`, `Esc`, `Tab`, `Arrow`) execute in `0ms` without entrance transitions.
2. **Vestibular safety and preserved state feedback.** Never eliminate state feedback under `prefers-reduced-motion`. Replace spatial motion with a single-shot high-contrast border highlight or background tint (`<= 1` transition, never oscillating). Never use `shake` animations because horizontal oscillation triggers vestibular distress.
3. **Mid-flight interruptibility.** Never apply `pointer-events: none` to interactive transforming elements. Mutate target coordinates on stateful springs while preserving live velocity `v(t)` and position `x(t)`.
4. **High-stakes trust calibration.** Irreversible actions (payments, deletions, deployments) require a `350ms` to `450ms` confirmation transition to prevent user distrust from instantaneous state flips.
5. **Bulk historical data stillness.** Render initial collection loads and message histories in `0ms`. Gate entrance transitions behind reactive flags (`isNew === true`) for newly appended items only.
6. **SSR hydration parity.** Never branch JSX element tags on `useReducedMotion()` prior to client hydration. Render identical DOM structures using `data-motion` attributes and CSS `@media (prefers-reduced-motion: reduce)` overrides.

## The build sequence

### Step 1. Frequency gate

Classify the target interaction frequency and record the decision in `.agents/state/ui-motion/gate.json`:

| Interaction tier | Motion budget |
| --- | --- |
| High-frequency utility (`100+` daily triggers, keyboard shortcuts, command palettes, data tables) | Disqualified (`0ms` instant state toggle). |
| Context menus and list selection | `0ms` open; `120ms` opacity exit fade only. |
| Frequent micro-interactions (`10` to `99` daily triggers, buttons, switches, hover states) | `100ms` to `160ms` compositor transition. |
| Occasional overlays (modals, drawers, popovers, toasts) | `150ms` to `300ms` compositor transition. |
| High-stakes or narrative (payments, deletions, onboarding, hero curtain reveals) | `350ms` to `450ms` trust confirmation; `600ms` to `1400ms` editorial reveals. |

If disqualified, emit the `0ms` non-animated implementation and skip Steps 2 through 5.

Completion criterion. `.agents/state/ui-motion/gate.json` exists on disk with `"mode"`, `"frequency_tier"`, `"eligible"`, and `"max_duration_ms"`.

### Step 2. Sanctioned purpose selection

Assign exactly one sanctioned purpose to `.agents/state/ui-motion/gate.json` under `"purpose"` before writing code: `feedback`, `spatial-consistency`, `state-indication`, `jarring-prevention`, `explanation`, `trust-calibration`, or `delight` (permitted only for rare or first-time triggers). If no purpose applies, set `"eligible": false` and emit static markup.

Completion criterion. `.agents/state/ui-motion/gate.json` contains a non-empty `"purpose"` field matching the sanctioned enum and `jq -e '.purpose' .agents/state/ui-motion/gate.json` exits with status `0`.

### Step 3. Tool selection

Select the lowest-overhead capable primitive from this ordered table:

| Mechanism | Primitive |
| --- | --- |
| Hover, press, opacity, or transform toggle | CSS `transition` |
| Mount and exit without JS runtime | CSS `@starting-style` with `transition-behavior: allow-discrete` (with `transitionend` fallback) |
| Shared-element DOM morphs | `document.startViewTransition()` with dynamic `view-transition-name` cleanup |
| Scroll-linked reveal or progress | CSS `animation-timeline: view()` |
| Programmatic interruptible compositor motion | WAAPI `element.animate()` with `composite: "add"`, `commitStyles()`, and `cancel()` on finish (`<= 8` active instances) |
| Continuous pointer physics or gesture springs | Stateful `requestAnimationFrame` solver or `motion.dev` |

Completion criterion. `.agents/state/ui-motion/gate.json` records `"primitive"` matching one table entry and zero dual-engine property conflicts exist in target files.

### Step 4. Hardware acceleration and property scoping

- **Compositor-only properties.** Animate `transform` and `opacity` exclusively. Never animate `width`, `height`, `margin`, `padding`, `top`, or `left`. Accordions use `grid-template-rows: 0fr` to `1fr`. Editorial curtain reveals may animate `clip-path: inset()`.
- **Non-zero entry scale.** Start scale entrances at `scale(0.95)` with `opacity: 0`; never use `scale(0)`.
- **Trigger-anchored origin.** Anchor popovers and tooltips with `transform-origin: var(--transform-origin, center)`. Keep centered modals on `margin: auto`.
- **Tactile press and hover gating.** Wrap `:hover` rules in `@media (hover: hover) and (pointer: fine)`. Apply `:active { transform: scale(0.97); }` and `touch-action: manipulation` to pressable controls.
- **Exit unmount watchdog.** Gate DOM removal on `transitionend` (`e.target === e.currentTarget`), `transitioncancel`, and a `setTimeout` watchdog at `duration + 34ms`.
- **View Transition isolation.** Set `pointer-events: none` on `::view-transition-group(*)`, lock `height: 100%; object-fit: none` on `::view-transition-old/new`, and delete `view-transition-name` in `transition.finished`.

Completion criterion. Target stylesheets pass `grep -En 'transition:\s*all|scale\(0\)|:\s*(width|height|margin|padding|top|left)'` with exit status `1` (zero layout-thrashing animations).

### Step 5. Easing curves, spring physics, and ProMotion synchronization

```css
--ease-out: cubic-bezier(0.23, 1, 0.32, 1);
--ease-in: cubic-bezier(0.32, 0, 0.67, 0);
--ease-in-out: cubic-bezier(0.77, 0, 0.175, 1);
--ease-drawer: cubic-bezier(0.32, 0.72, 0, 1);
--ease-quintic: cubic-bezier(0.22, 1, 0.36, 1);
--ease-expo: cubic-bezier(0.16, 1, 0.3, 1);

```



- Apply `--ease-out` or `--ease-expo` to entrances. Reserve `--ease-in` strictly for exits. Use `--ease-in-out` for on-screen morphs and `linear` for scroll timelines.
- Calibrate UI springs to `{ stiffness: 300, damping: 30 }` and tactile press springs to `{ stiffness: 400, damping: 17 }`.
- Filter gesture flick velocity over a rolling `40ms` ring buffer, zero velocity after `45ms` idle, and clamp to `[-3500, 3500]` px/s.
- Clamp `requestAnimationFrame` delta-time to `dt = Math.min((now - prev) / 1000, 0.032)` and integrate physics in `0.004` (`4ms`, `240Hz`) sub-steps so background tab wakes never explode spring energy.

Completion criterion. Target files define explicit `--ease-*` tokens or `{ stiffness, damping }` constants, zero `ease-in` entrances, and `0.032` delta clamping on every `requestAnimationFrame` loop.

### Step 6. Accessibility, fallback feedback, and SSR hydration

```css
@media (prefers-reduced-motion: reduce) {
 *, ::before, ::after {
   animation-duration: 0.01ms !important;
   animation-iteration-count: 1 !important;
   transition-duration: 0.01ms !important;
   scroll-behavior: auto !important;
 }
  [data-motion-feedback="active"] {
    outline: 2px solid currentColor;
    outline-offset: 2px;
  }
}
@media (hover: hover) and (pointer: fine) {
 .interactive-target:hover { transform: scale(1.02); }
}

```




- Render identical DOM structures across SSR and client hydration; never swap JSX tags via `useReducedMotion()`.
- Never declare global `transform: none !important` inside `prefers-reduced-motion`, which breaks structural centering transforms such as `translate(-50%, -50%)`.
- Preserve non-kinetic state feedback via `[data-motion-feedback]` outline or tint highlights; never emit `shake` keyframes.
- Defer `.focus({ preventScroll: true })` until `duration + 10ms` after entry completion, and never auto-focus text inputs on `pointer: coarse` viewports.

Completion criterion. Target files contain `@media (prefers-reduced-motion: reduce)` with `[data-motion-feedback]`, zero global `transform: none !important`, and `python3 skills/review-a-skill/scripts/lint_skill.py skills/ui-motion` exits with status `0`.

## Boundary isolation

Confine edits strictly to motion tokens, CSS transitions, keyframes, View Transition pseudo-elements, and pointer/RAF hooks. Never alter business logic, API payloads, database queries, or semantic ARIA roles.

## Anti-patterns

| ID | Title | Pattern description | Why it fails | Concrete fix |
|---|---|---|---|---|
| UIM-01 | Transition all | Uses `transition: all` shorthand in stylesheets | Animates layout and paint properties and causes frame drops | Name the exact properties (`transform`, `opacity`) |
| UIM-02 | Scale-zero mount | Starts entrance transitions at `transform: scale(0)` | Collapses element to a dimensionless point and exaggerates travel | Use `scale(0.95)` paired with zero opacity |
| UIM-03 | Ease-in entrance | Applies `ease-in` to interactive element entrances | Delays initial velocity and makes controls feel unresponsive | Use `ease-out` token (reserve `ease-in` strictly for exits) |
| UIM-04 | Keyboard motion delay | Animates shortcuts, command palettes, or arrow navigation | Forces deliberate keyboard users to wait on visual choreography | Apply instant 0ms state toggle |
| UIM-05 | Vestibular shake | Uses horizontal `shake` keyframes for error or reduced motion | Triggers vestibular nausea and violates accessibility safety | Retain instant blink, border pulse, or color flash; never shake |
| UIM-06 | Feedback erasure | Strips all visual state cues under `prefers-reduced-motion` | Leaves users uncertain whether an action registered | Retain instant blink, border pulse, or color flash; never shake |
| UIM-07 | Input pointer lock | Sets `pointer-events: none` on active interactive elements | Blocks mid-flight retargeting and traps user input | Retarget live presentation transforms mid-flight |
| UIM-08 | Zero-ms high stakes | Completes payments or destructive actions in `0ms` | Induces distrust from lack of perceptible system processing | Use 350ms to 450ms confirmation to close perception delta |
| UIM-09 | Layout property tween | Animates `width`, `height`, `margin`, `padding`, `top`, or `left` | Forces main-thread layout recalculation on every frame | Animate `transform` and `opacity` (accordions use grid rows) |
| UIM-10 | Unclamped RAF delta | Integrates physics using raw `requestAnimationFrame` timestamp delta | Explodes spring velocity when a background tab wakes up | Clamp `dt <= 0.032s` with 4ms internal sub-stepping |
| UIM-11 | Ungated touch hover | Applies `:hover` transforms outside pointer media queries | Sticks hover states after tap on touch devices | Wrap in `@media (hover: hover) and (pointer: fine)` |
| UIM-12 | Global transform reset | Declares `transform: none !important` in reduced-motion media query | Destroys structural positioning transforms like `translate(-50%, -50%)` | Collapse durations to 0.01ms; preserve structural transforms |
| UIM-13 | Unguarded DOM unmount | Removes exiting nodes without `transitioncancel` or timeout fallback | Leaks orphaned DOM nodes when transitions abort mid-flight | Filter `e.target === e.currentTarget`, listen to `transitioncancel` |
| UIM-14 | Static view-transition | Hardcodes identical `view-transition-name` across list items | Throws duplicate name error and aborts the entire view transition | Scope tokens dynamically during active transition |
| UIM-15 | Hydration tag branch | Swaps JSX tags using `useReducedMotion()` during initial render | Causes React hydration mismatches and stuck `opacity: 0` elements | Use identical DOM trees with attribute contracts and CSS overrides |
| UIM-16 | Bulk history stagger | Animates initial render of historical lists or message logs | Stalls initial paint and delays access to existing data | Render historical logs instantly; gate motion behind `isNew: boolean` |

## Quick audit checklist

| Check | Passing condition |
|---|---|
| Frequency gate | Interaction frequency classified; keyboard/context actions execute in 0ms |
| Hardware acceleration | Only `transform` and `opacity` animated; zero layout property tweens |
| Reduced motion | Non-vestibular feedback preserved without `transform: none !important` or JSX branch |
| Physics stability | RAF timestamp delta clamped to `dt <= 0.032s` with 4ms internal sub-steps |
| State machine exit | Binary completion criteria verified on designated state and target files |
