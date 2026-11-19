---
name: ui-motion
description: Use when designing, implementing, or auditing CSS transitions, @starting-style, WAAPI, FLIP morphs, View Transitions, scroll-driven animations, gesture physics, Core Web Vitals motion impact, landing choreography, or reduced-motion fallbacks. Don't use for static layout styling (use frontend-design), full WCAG audits (use ui-ux-review), prose editing (use unslop), or general architecture scoping (use brainstorming).
---

# UI motion engineering

Design, implement, and audit compositor-accelerated interface and editorial motion with deterministic timing, interruptible physics, and reduced-motion state preservation.

<HARD-GATE>
Write-Target Boundary. In Author mode, write only to component stylesheets, motion tokens, animation hooks, and motion-related JSX attributes (`data-motion`, `data-motion-feedback`, `data-motion-editorial`, `data-motion-ambient`, `data-motion-spinner`, `data-revealed`, `data-direction`, `style`, `ref`, `onTransitionEnd`, `onTransitionCancel`, `onPointerDown`, `onPointerMove`, `onPointerUp`, `onPointerCancel`, `onPointerLeave`, `isNew`, `aria-label`, `aria-hidden`) in user-targeted files, plus state artifacts under `.agents/state/ui-motion/`. In Audit mode, write only to `.agents/state/ui-motion/audit-findings.md` and `docs/superpowers/plans/ui-motion-plan.md`, leaving all application source files untouched. Never modify business logic, API calls, state reducers, or semantic ARIA roles. Before overwriting pre-existing `prefers-reduced-motion` blocks in Author mode, record `"reduced_motion_confirm": "required"` in `.agents/state/ui-motion/gate.json` and request user approval.
</HARD-GATE>

## Modes

Declare the active operating mode before executing Step 1:
- `author` (default). Execute Steps 1 through 6 sequentially (skipping Steps 2 through 4 when Step 1 marks `"eligible": false`) to produce motion styles, hooks, and attribute bindings.
- `audit`. Execute Steps 1 through 6 in non-mutating inspection mode against target files, record findings in `.agents/state/ui-motion/audit-findings.md` and `docs/superpowers/plans/ui-motion-plan.md`, and halt without writing `.agents/state/ui-motion/gate.json` or modifying source files.

## Reference quick routing

| Motion domain | Reference module | Mutually exclusive load trigger |
|---|---|---|
| Hero, stagger, spotlights | [references/landing-and-editorial.md](references/landing-and-editorial.md) | Load for hero LCP choreography, sub-linear stagger decay, SVG `pathLength` draws, and `@property` spotlights |
| CSS springs and FLIP | [references/springs-and-flip.md](references/springs-and-flip.md) | Load for CSS `linear()` curves, sampled inverse-scale FLIP morphs, and velocity detent snapping |
| Gestures and momentum | [references/physics-and-gestures.md](references/physics-and-gestures.md) | Load for pointer capture, rubber-band boundaries, WAAPI `commitStyles()` guards, and drag physics |
| Spring token catalog | [references/springs.md](references/springs.md) | Load when referencing extended stiffness, damping, or mass presets beyond Step 4 defaults |
| Delight choreography | [references/animation-and-delight.md](references/animation-and-delight.md) | Load strictly for rare first-time `delight` celebrations |
| React 19 concurrency | [references/slots.md](references/slots.md) | Load when coordinating concurrent surface slots under React 19 |
| Pointer and haptics | [references/pointer.md](references/pointer.md) | Load for Apple Pencil, touch hover gating, or haptic triggers |
| Widget micro-distances | [references/catalog.md](references/catalog.md) | Load when selecting pixel travel budgets across standard UI controls |
| Native desktop shells | [references/desktop-and-platform.md](references/desktop-and-platform.md) | Load when targeting macOS AppKit, Windows Mica, Electron, or Tauri surfaces |
| Subgrid and skeletons | [references/integration.md](references/integration.md) | Load when animating subgrid layouts, portals, or loading skeletons |
| Component recipes | [references/recipes.md](references/recipes.md) | Load for dialogs, drawers, toasts, tabs, or accordions |
| Mobile web viewports | [references/mobile-web-and-native.md](references/mobile-web-and-native.md) | Load for Mobile Safari `100dvh` viewports or coarse-pointer latency |
| Core Web Vitals | [references/google-standards.md](references/google-standards.md) | Load when auditing INP, LCP, or CLS impact |
| Kinetic typography | [references/kinetic-typography-and-shimmer.md](references/kinetic-typography-and-shimmer.md) | Load for display character staggers (`<= 24` chars) or shimmer passes |
| Scroll and canvas scrub | [references/canvas-and-scroll-scrubbing.md](references/canvas-and-scroll-scrubbing.md) | Load for scroll-linked timelines (`view()`/`scroll()`) or canvas frame scrubbing |
| Editorial curtain wipes | [references/creative-and-editorial.md](references/creative-and-editorial.md) | Load for `clip-path` curtain wipes or pointer inertia trails |
| Spatial perception | [references/mental-models-and-perception.md](references/mental-models-and-perception.md) | Load when calibrating spatial continuity or perceived duration |
| Token vocabulary | [references/vocabulary.md](references/vocabulary.md) | Load when mapping qualitative motion requests to numeric tokens |
| Audit playbooks | [references/audit-and-plans.md](references/audit-and-plans.md) | Load when executing Audit mode inspections and remediation plans |

## Execution invariants

- **INV-01 Zero-latency keyboard execution.** Keyboard shortcuts, command palettes, and focus navigation (`Cmd+K`, `Esc`, `Tab`, `Arrow`) execute in `0ms` with synchronous `.focus({ preventScroll: true })`.
- **INV-02 Vestibular safety and state feedback.** Under `prefers-reduced-motion: reduce`, neutralize spatial travel and scroll-driven timelines (`animation-timeline: auto !important`), ban `shake` keyframes, and preserve non-kinetic inset border, tint, or `<= 150ms` opacity dissolve feedback.
- **INV-03 Mid-flight interruptibility.** Keep `pointer-events: auto` on active interactive elements and retarget live position `x(t)` and velocity `v(t)` without visual snapback.
- **INV-04 High-stakes trust calibration.** Gate irreversible actions (payments, deletions, deployments) behind a `350ms` to `450ms` confirmation transition.
- **INV-05 Bulk historical stillness.** Render initial lists and message histories in `0ms`; animate only newly appended items gated by `isNew === true`.
- **INV-06 SSR hydration parity.** Render identical JSX tags across SSR and client hydration without branching on `useReducedMotion()`; express overrides via `data-motion-*` attributes and CSS media queries.
- **INV-07 Above-the-fold LCP visibility.** Paint primary hero `<h1>` and hero media at non-zero opacity from frame zero (`0ms` delay); never gate above-the-fold LCP behind JS `IntersectionObserver` or `opacity: 0` stagger delays.
- **INV-08 Offscreen ambient suspension.** Pause infinite marquees and ambient loops via `IntersectionObserver` and `document.visibilitychange`, capping each `100dvh` viewport to at most 1 focal sequence and 1 ambient layer.
- **INV-09 Directional spatial topology.** Derive `--direction` (`1` or `-1`) from ordinal tab or step deltas along the true navigation axis.
- **INV-10 Zero-reflow counters and scroll lock.** Apply `font-variant-numeric: tabular-nums` to animated numbers and `scrollbar-gutter: stable` on `:root`.

## The build sequence

### Step 1. Frequency gate and purpose classification

Classify interaction frequency and sanctioned purpose (`feedback`, `spatial-consistency`, `state-indication`, `jarring-prevention`, `explanation`, `trust-calibration`, or `delight`). In Author mode, write `.agents/state/ui-motion/gate.json` before authoring code:

| Interaction tier | Motion budget |
|---|---|
| High-frequency utility (`100+` daily triggers, shortcuts, table cells) | Disqualified (`0ms` instant toggle; `"eligible": false`, `"primitive": "none"`) |
| Command palettes and search modals | `0ms` open or `<= 120ms` opacity dissolve; `120ms` opacity exit fade |
| Context menus and list selection | `0ms` open; `120ms` opacity exit fade only |
| Frequent micro-interactions (`10` to `99` daily triggers, buttons, switches, hovers) | `100ms` to `160ms` compositor transition |
| Occasional overlays (modals, drawers, popovers) | `150ms` to `300ms` compositor transition |
| Stacked toast notifications | `400ms` compositor settle with `ease` (`cubic-bezier(0.25, 0.1, 0.25, 1)`) |
| High-stakes or narrative (payments, deletions, hero curtains, scroll storytelling) | `350ms` to `450ms` confirmation; `600ms` to `900ms` editorial reveals |

When disqualified, record `"eligible": false`, `"max_duration_ms": 0`, and `"primitive": "none"`, emit `0ms` static markup with synchronous focus handling, skip Steps 2 through 4, and proceed directly to Step 5.

Completion criterion. In Author mode, `python3 -c 'import json; d=json.load(open(".agents/state/ui-motion/gate.json")); assert d.get("mode")=="author" and isinstance(d.get("eligible"),bool) and isinstance(d.get("max_duration_ms"),int) and d.get("frequency_tier") and d.get("purpose") and (d["eligible"] or (d["max_duration_ms"]==0 and d.get("primitive")=="none"))'` exits `0`. In Audit mode, `grep -En 'frequency_tier|Interaction tier' .agents/state/ui-motion/audit-findings.md` exits `0`.

### Step 2. Tool selection

Select the lowest-overhead capable primitive and record `"primitive"` in `.agents/state/ui-motion/gate.json` (`references/springs-and-flip.md`, `references/physics-and-gestures.md`):

| Mechanism | Primitive |
|---|---|
| Hover, press, opacity, or fixed-endpoint snap | CSS `transition` with `--ease-out` or `@supports`-gated `--spring-snappy` |
| Mount and Top Layer exit without JS runtime | CSS `@starting-style` with `transition-behavior: allow-discrete` and `overlay <dur> allow-discrete` |
| Shared-element container or pill morph | Sampled-keyframe inverse-scale FLIP (`last.width > 0` guard) or feature-detected `document.startViewTransition()` |
| Scroll-linked scrub or viewport reveal | `@supports (animation-timeline: view())` inside `prefers-reduced-motion: no-preference`, or one-shot `IntersectionObserver` |
| Programmatic compositor keyframes | WAAPI `element.animate()` (`<= 8` active), `composite: "replace"`, no persistent `fill: "forwards"`, guarded `commitStyles()` + `cancel()` |
| Continuous pointer physics or gesture springs | Fixed-timestep `requestAnimationFrame` symplectic Euler solver or `motion.dev` |

Completion criterion. In Author mode, `python3 -c 'import json; d=json.load(open(".agents/state/ui-motion/gate.json")); assert d.get("primitive") in ("none","css-transition","starting-style","flip","view-transition","scroll-timeline","intersection-observer","waapi","raf-spring","motion-dev")'` exits `0`. In Audit mode, `grep -En 'primitive|dual-engine' .agents/state/ui-motion/audit-findings.md` exits `0`.

### Step 3. Hardware acceleration and property scoping

- **Compositor properties and `will-change`.** Animate only `transform`, `opacity`, `clip-path: inset()`, SVG `stroke-dashoffset` (`pathLength="1"`), and registered `@property` `<angle>` or `<length>` tokens. Ban layout and blur tweens (`width`, `height`, `margin`, `padding`, `top`, `left`, `right`, `bottom`, `background-position`, `backdrop-filter`, `grid-template-rows`). Scope `will-change: transform` to active sequences, clear it on `transitionend`/`animationend`, and rest at `transform: none`.
- **Sticky containment and blur cap.** Use `overflow: clip` (never `overflow: hidden`) on sticky stages. Keep `backdrop-filter: blur()` static at `<= 16px` and never nest blur inside translating layers.
- **Entry scale and asymmetric exits.** Start below-the-fold scale entrances at `scale(0.95)` with `opacity: 0`; never use `scale(0)`. Run exits at `0.7x` entrance duration (`<= 8px` travel) and sequence panel swaps as `exit (90ms)` before `enter (160ms)`.
- **Origin, spotlight isolation, and hover gating.** Anchor popovers with `transform-origin: var(--transform-origin, center)`. Measure magnetic pull (`<= 8px`) and cached `DOMRect`s on a stationary outer wrapper (`ResizeObserver` + passive `scroll` + `pointerenter`, zero reads in `pointermove`). Register spotlight `--sx`/`--sy` via `@property` with `inherits: false` (or transform a dedicated child layer) and translate a `2 * radius` radial layer via `translate3d(calc(var(--sx) - var(--radius)), calc(var(--sy) - var(--radius)), 0)`. Wrap `:hover` in `@media (hover: hover) and (pointer: fine)` and apply `:active:not(:disabled):not([aria-disabled="true"]) { transform: scale(0.97); }` with `touch-action: manipulation`.
- **Exit watchdog and View Transitions.** Gate DOM unmount on `transitionend` (`e.target === e.currentTarget`), `transitioncancel`, and a `duration + 34ms` watchdog. Set `::view-transition { pointer-events: none; }`, lock `width: 100%; height: 100%; object-fit: cover;` on `::view-transition-old(*), ::view-transition-new(*)`, catch `transition.ready.catch(() => {})`, call `skipTransition()` on overlap, and clear `view-transition-name` in `finally`.

Completion criterion. In Author mode (when `eligible` is `true`), on macOS Darwin `zsh`, `grep -En 'transition(-property)?[[:space:]]*:[^;]*([:,[:space:]])(all|width|height|(margin|padding)(-[a-z]+)?|top|left|right|bottom|background-position|backdrop-filter|grid-template-rows)([[:space:],;]|$)|scale(X|Y|3d)?\([[:space:]]*0(\.0+)?[[:space:]]*[,)]' <target-files>` exits `1`. In Audit mode, `grep -En 'Compositor|will-change|layout' .agents/state/ui-motion/audit-findings.md` exits `0`.

### Step 4. Easing curves, stagger ceilings, and ProMotion synchronization

```css
--ease-out: cubic-bezier(0.23, 1, 0.32, 1);
--ease-in: cubic-bezier(0.32, 0, 0.67, 0);
--ease-in-out: cubic-bezier(0.77, 0, 0.175, 1);
--ease-drawer: cubic-bezier(0.32, 0.72, 0, 1);
--ease-quintic: cubic-bezier(0.22, 1, 0.36, 1);
--ease-expo: cubic-bezier(0.16, 1, 0.3, 1);
--spring-snappy: linear(0, 0.009, 0.035 2.1%, 0.141, 0.281 6.7%, 0.723 12.9%, 0.938 16.7%, 1.017, 1.077, 1.121, 1.149 24.3%, 1.159, 1.163, 1.161, 1.154 29.9%, 1.129 32.8%, 1.051 39.6%, 1.017 43.1%, 0.991, 0.977 51%, 0.974 53.8%, 0.975 57.1%, 0.997 69.8%, 1.003 76.9%, 1.004 83.8%, 1);

```

* Apply `--ease-out` or `--ease-expo` to entrances, `@supports`-gated `--spring-snappy` (fallback `--ease-out`) to stateless tactile snaps, `ease` (`400ms`) to stacked toasts, `--ease-in` to exits, `--ease-in-out` to morphs, and `linear` strictly to scroll-scrubbed timelines.
* Cap cumulative stagger via $D(i) = D_{\max}(1-e^{-ki})$ at $D_{\max} = 450\text{ms}, k = 0.28$ (bento/lists) or $D_{\max} = 700\text{ms}, k = 0.24$ (hero display words), assigning `0ms` to offscreen items and `0ms` delay to the LCP `<h1>`.
* Calibrate springs (`mass: 1`) to `{ stiffness: 420, damping: 41 }` (critically damped switches/tabs, $\zeta = 1.0$), `{ stiffness: 400, damping: 32 }` (tactile press/spotlight, $\zeta = 0.80$), `{ stiffness: 300, damping: 30 }` (overlays/FLIP, $\zeta = 0.87$), and `{ stiffness: 320, damping: 25 }` (flick detents, $\zeta = 0.70$).
* Filter gesture velocity over a `40ms` ring buffer, zero after `45ms` idle, clamp to `[-3500, 3500]` px/s, project snap detents via `projected = offset + velocity * 0.12`, damp boundary overscroll with `dim * (1 - 1 / ((Math.abs(overscroll) * 0.55) / dim + 1))`, and release capture on `pointerup`, `pointercancel`, and `lostpointercapture`.
* For spring/physics `rAF` loops, clamp `dt = Math.min((now - prev) / 1000, 0.032)`, integrate via semi-implicit Euler (`v += a * 0.004; x += v * 0.004;`) in `4ms` (`240Hz`) sub-steps, and cancel `rAF` once `Math.abs(target - x) < 0.01 && Math.abs(v) < 0.01`.

Completion criterion. In Author mode (when `eligible` is `true`), `grep -En -- '--ease-(out|expo|in|in-out|drawer|quintic)' <target-files>` exits `0`, and when `"primitive"` is `"raf-spring"`, `grep -En '0\.032' <target-files>` and `grep -En '0\.004' <target-files>` both exit `0`. In Audit mode, `grep -En 'easing|spring|stagger' .agents/state/ui-motion/audit-findings.md` exits `0`.

### Step 5. Accessibility, split-text parity, and SSR hydration

```css
@media (prefers-reduced-motion: reduce) {
  *, ::before, ::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    animation-timeline: auto !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
  [data-motion-feedback="active"],
  [data-state="open"],
  [aria-expanded="true"],
  [aria-pressed="true"] {
    box-shadow: inset 0 0 0 2px currentColor;
  }
  [data-motion-editorial] {
    animation: none !important;
    transition-property: opacity !important;
    transition-duration: 140ms !important;
    transform: none !important;
    clip-path: none !important;
  }
  [data-motion-ambient] {
    animation: none !important;
  }
  [data-motion-spinner] {
    animation-duration: 1600ms !important;
    animation-iteration-count: infinite !important;
  }
}

```

* Render identical SSR and client DOM tags without branching on `useReducedMotion()`.
* On split-text headlines, set the complete string in `aria-label` on the parent heading, set `aria-hidden="true"` on visual spans, and wrap words in `white-space: nowrap`.
* Scope `transform: none !important` strictly inside `[data-motion-editorial]` so structural centering transforms remain intact.
* Call `.focus({ preventScroll: true })` synchronously inside the user-activation event on open (with `inert` on background content), and restore focus to the invoking trigger on close.

Completion criterion. In Author mode, `python3 -c 'import pathlib,re,sys; txt="\n".join(pathlib.Path(p).read_text() for p in sys.argv[1:]); assert "prefers-reduced-motion" in txt; bad=[s for s,b in re.findall(r"([^{}@]+)\{([^{}]+)\}",txt) if re.search(r"transform\s*:\s*none\s*!important",b) and "data-motion-editorial" not in s]; assert not bad, bad; assert ("animation-timeline:" not in txt) or ("animation-timeline: auto" in txt or "prefers-reduced-motion: no-preference" in txt)' <target-files>` exits `0`. In Audit mode, `grep -En 'prefers-reduced-motion|vestibular|focus' .agents/state/ui-motion/audit-findings.md` exits `0`.

### Step 6. Final verification and mode exit

* In Author mode, run Step 1 and Step 5 checks unconditionally, plus Steps 2 through 4 checks when `"eligible": true` in `.agents/state/ui-motion/gate.json`.
* In Audit mode, confirm `.agents/state/ui-motion/audit-findings.md` and `docs/superpowers/plans/ui-motion-plan.md` exist with non-zero byte size and halt without mutating source files.

Completion criterion. In Author mode, `python3 -c 'import json; d=json.load(open(".agents/state/ui-motion/gate.json")); assert d.get("mode")=="author" and (d["eligible"] is False or bool(d.get("primitive")))'` exits `0` alongside all applicable step checks. In Audit mode, `test -s .agents/state/ui-motion/audit-findings.md && test -s docs/superpowers/plans/ui-motion-plan.md` exits `0`.

## Boundary isolation

All edits obey the `<HARD-GATE>` Write-Target Boundary at the top of this file. Never touch business logic, API calls, database schemas, state reducers, or semantic ARIA roles.

## Anti-patterns

| ID | Title | Pattern description | Why it fails | Concrete fix |
| --- | --- | --- | --- | --- |
| UIM-01 | Transition all | Uses `transition: all` shorthand in stylesheets | Animates layout and paint properties and drops frames | Name exact properties (`transform`, `opacity`) |
| UIM-02 | Scale-zero mount | Starts entrance transitions at `transform: scale(0)` | Collapses element to a point and exaggerates travel | Use `scale(0.95)` paired with opacity |
| UIM-03 | Ease-in entrance | Applies `ease-in` to interactive entrances | Delays initial velocity and feels unresponsive | Use `var(--ease-out)` for entrances and `var(--ease-in)` for exits |
| UIM-04 | Keyboard motion delay | Animates shortcuts, command palettes, or arrow keys | Forces keyboard users to wait on visual transitions | Apply `0ms` state toggle and synchronous `.focus({ preventScroll: true })` |
| UIM-05 | Vestibular shake | Uses horizontal `shake` keyframes for errors | Triggers vestibular nausea and violates safety | Replace oscillation with inset border highlight or tint |
| UIM-06 | Feedback erasure | Strips all state cues under `prefers-reduced-motion` | Leaves users uncertain whether input registered | Preserve inset border highlight or tint on active states |
| UIM-07 | Input pointer lock | Sets `pointer-events: none` on moving controls | Blocks mid-flight retargeting and drops input | Keep `pointer-events: auto` and retarget live state |
| UIM-08 | Zero-ms high stakes | Completes payments or deletions in `0ms` | Induces distrust from imperceptible state flips | Use `350ms` to `450ms` confirmation transition |
| UIM-09 | Layout property tween | Animates `width`, `height`, `margin`, `padding`, `top`, `left`, or `grid-template-rows` | Forces main-thread relayout every frame | Animate `transform`, `opacity`, or `clip-path: inset()` |
| UIM-10 | Unclamped RAF delta | Integrates physics with raw `rAF` delta or explicit Euler | Explodes velocity on tab wake or diverges under stiffness | Clamp `dt <= 0.032s` with `4ms` semi-implicit Euler sub-steps |
| UIM-11 | Ungated touch hover | Applies `:hover` outside pointer media queries | Sticks hover states after touch taps | Wrap in `@media (hover: hover) and (pointer: fine)` |
| UIM-12 | Global transform reset | Declares `transform: none !important` globally in reduced motion | Breaks structural positioning transforms | Scope `transform: none !important` strictly to `[data-motion-editorial]` |
| UIM-13 | Unguarded DOM unmount | Removes exiting nodes without cancel or timeout fallback | Leaks orphaned nodes on aborted transitions | Filter `e.target === e.currentTarget`, handle `transitioncancel`, set `duration + 34ms` watchdog |
| UIM-14 | Static view-transition | Hardcodes identical `view-transition-name` across items | Throws `InvalidStateError` and aborts morph | Scope tokens dynamically, catch `ready`, clear in `finally` |
| UIM-15 | Hydration tag branch | Swaps JSX tags via `useReducedMotion()` on initial render | Causes hydration mismatches and stuck `opacity: 0` | Render identical DOM trees with `data-motion-*` CSS overrides |
| UIM-16 | Bulk history stagger | Animates initial render of historical lists or logs | Stalls paint and delays access to existing data | Render initial history in `0ms`; gate new items on `isNew === true` |
| UIM-17 | Hero LCP opacity lock | Hides above-the-fold `<h1>` at `opacity: 0` behind JS or delay | Delays Largest Contentful Paint | Keep LCP text visible at frame zero with `0ms` delay |
| UIM-18 | Unbounded linear stagger | Multiplies index by fixed `60ms` to `100ms` across large sets | Stretches reveals past 2 seconds | Use $D_{\max}(1-e^{-ki})$ capped at `450ms` (grid) or `700ms` (hero) |
| UIM-19 | Overflow-hidden sticky break | Sets `overflow: hidden` on sticky scroll containers | Disables descendant `position: sticky` | Replace `overflow: hidden` with `overflow: clip` |
| UIM-20 | Inherited spotlight vars | Updates `--sx`/`--sy` without `inherits: false` or uses `50%` on oversized layers | Recalculates child styles or offsets spotlight center from cursor | Register `@property` with `inherits: false` and center a `2 * radius` layer |
| UIM-21 | Unlabeled split-text | Splits headings into `<span>` nodes without `aria-label` | Causes screen readers to spell letter by letter | Set `aria-label` on heading and `aria-hidden="true"` on spans |
| UIM-22 | Unpaused offscreen ambient | Runs infinite loops offscreen or in hidden tabs | Wastes battery and violates WCAG 2.2.2 | Gate loops with `IntersectionObserver` and `document.visibilitychange` |
| UIM-23 | Permanent `will-change` | Leaves `will-change: transform` on idle cards | Exhausts GPU VRAM and blurs text | Apply during active motion and clear on completion |
| UIM-24 | Moving-node rect read | Calls `getBoundingClientRect()` inside `pointermove` or on moving node | Causes layout thrash and pointer feedback jitter | Cache rect on stationary wrapper via `ResizeObserver` and `pointerenter` |
| UIM-25 | Naive 2-frame FLIP scale | Interpolates parent `scale(s)` and child `scale(1/s)` in 2 keyframes | Warps child glyphs mid-flight and divides by zero on collapsed nodes | Guard `last.width > 0` and sample `>= 12` reciprocal keyframes |
| UIM-26 | Overlapping panel swap | Fades outgoing and incoming panels simultaneously | Creates muddy text overlap | Exit outgoing (`90ms`) before entering incoming (`160ms`) |
| UIM-27 | Animated blur or missing gutter | Tweens `backdrop-filter: blur()` or omits `scrollbar-gutter: stable` | Triggers per-frame blur readbacks and horizontal modal jump | Keep blur static (`<= 16px`), animate `opacity`, set `scrollbar-gutter: stable` |
| UIM-28 | Numeric layout jitter | Animates counters without tabular figures | Shifts sibling geometry on every tick | Apply `font-variant-numeric: tabular-nums` |
| UIM-29 | Unstoppable scroll timeline | Uses `animation-timeline: view()` without reduced-motion reset | Scroll motion keeps running under `prefers-reduced-motion: reduce` | Gate with `prefers-reduced-motion: no-preference` and reset `animation-timeline: auto !important` |
| UIM-30 | Missing Top Layer overlay | Uses `@starting-style` with `display` but omits `overlay allow-discrete` | Clips `<dialog>` and `[popover]` exits at frame zero | Include `overlay <dur> allow-discrete` in transition list |

## Quick audit checklist

| Check | Passing condition |
| --- | --- |
| Frequency gate | Interaction tier classified; `0ms` utility skips Steps 2 to 4 and sets `"primitive": "none"` |
| Hardware acceleration | Compositor-only properties, `@property` spotlight isolation, `overlay allow-discrete` on Top Layer exits |
| Landing and FLIP craft | LCP `<h1>` visible at frame zero, sub-linear stagger cap, sampled inverse FLIP scale, cached wrapper rect |
| Reduced motion | `animation-timeline: auto !important`, scoped `[data-motion-editorial]` reset, preserved inset feedback |
| Physics stability | Clamped `dt <= 0.032s`, `4ms` semi-implicit Euler sub-steps, `pointercancel` cleanup, `0.12s` projection |
| Verification exit | Mode-aware macOS BSD `grep` and `python3` gates pass on designated artifacts |
