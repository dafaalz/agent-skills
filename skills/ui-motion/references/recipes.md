# Component recipes and interaction patterns

Ready-to-build implementations for common interface components. Start from the matching recipe, then adapt to codebase tokens instead of writing motion styles from scratch.

Curves match `--ease-out`, `--ease-in-out`, and `--ease-drawer` design tokens.

---

## 1. Responsive button press

Pressable targets must react instantly to user touch or click. Apply subtle scaling on the `:active` pseudo-class:

```css
.button {
  transition: transform 160ms var(--ease-out);
}

.button:active {
  transform: scale(0.97);
}
```

Keep scale values between 0.95 and 0.98. Scaling applies proportionally to typography, icons, and badges without altering surrounding layout geometry.

No hover gating is required here because `:active` is a genuine physical press on touch screens. Gate any `:hover` styling separately.

---

## 2. Dropdown, popover, menu, select

Scales out of its trigger, not out of thin air:

```css
.popover {
  transform-origin: var(--transform-origin); /* Headless UI primitives supply this */
  transition:
    opacity 200ms var(--ease-out),
    transform 200ms var(--ease-out);
}

.popover[data-starting-style],
.popover[data-ending-style] {
  opacity: 0;
  transform: scale(0.95);
}
```

The `transform-origin` property is the critical detail. The panel must appear anchored to the clicked trigger.

---

## 3. Tooltip with consecutive hover skip

Tooltips require an initial delay to avoid visual noise during cursor travel. However, once any tooltip opens, hovering adjacent controls should reveal tooltips immediately:

```css
.tooltip {
  transform-origin: var(--transform-origin);
  transition:
    transform 125ms var(--ease-out),
    opacity 125ms var(--ease-out);
}

.tooltip[data-starting-style],
.tooltip[data-ending-style] {
  opacity: 0;
  transform: scale(0.97);
}

/* Once one tooltip is open, neighboring tooltips open without delay */
.tooltip[data-instant] {
  transition-duration: 0ms;
}
```

Skipping both the delay and the animation on subsequent hovers makes an entire toolbar feel instant and light.

---

## 4. Modal dialog

Modals represent the one overlay that stays centered in the viewport:

```css
.modal {
  transform-origin: center; /* exempt, anchored to the viewport center */
  transition:
    opacity 250ms var(--ease-out),
    transform 250ms var(--ease-out);
}

.modal[data-starting-style],
.modal[data-ending-style] {
  opacity: 0;
  transform: scale(0.96);
}

.modal-backdrop {
  transition: opacity 250ms var(--ease-out);
}
```

Animate the backdrop opacity simultaneously so modal and backdrop read as a single coherent surface.

---

## 5. Drawer and bottom sheet

```css
.drawer {
  transform: translateY(0);
  transition: transform 500ms var(--ease-drawer);
}

.drawer[data-closed] {
  transform: translateY(100%);
}
```

For gesture-driven drawers with drag to dismiss, see the drag recipe below.

---

## 6. Toast notification

Use standard CSS transitions or `@starting-style` rather than keyframes. This ensures new entries and unmounting toasts retarget smoothly during list reflows:

```css
.toast {
  opacity: 1;
  transform: translateY(0);
  transition:
    opacity 350ms ease,
    transform 350ms ease;

  @starting-style {
    opacity: 0;
    transform: translateY(100%);
  }
}
```

If `@starting-style` is not supported, fall back to a mount state flag:

```jsx
const [mounted, setMounted] = useState(false);
useEffect(() => { setMounted(true); }, []);
// <div data-mounted={mounted} />
```

---

## 7. Accordion and collapsible content

Keep duration short. This animation triggers layout recalculations on every frame, so long durations feel sluggish and cost performance:

```css
.accordion-wrapper {
  display: grid;
  grid-template-rows: 0fr;
  transition: grid-template-rows 200ms var(--ease-out);
}

.accordion-wrapper[data-expanded="true"] {
  grid-template-rows: 1fr;
}

.accordion-content {
  overflow: hidden;
}
```

Native CSS grid interpolation eliminates the need for manual JavaScript height measurements.

---

## 8. Staggered group entrances

Permitted for milestone screens, onboarding, or dashboard cards the user visits occasionally, but never for lists the user scrolls all day:

```css
.stagger-item {
  opacity: 0;
  transform: translateY(8px);
  animation: fadeIn 300ms var(--ease-out) forwards;
}

.stagger-item:nth-child(2) { animation-delay: 40ms; }
.stagger-item:nth-child(3) { animation-delay: 80ms; }
.stagger-item:nth-child(4) { animation-delay: 120ms; }

@keyframes fadeIn {
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
```

Stagger timing must stay between 30ms and 80ms per item. It must never block user interaction while playing.

---

## 9. Hold to confirm or delete

Use for destructive actions where an accidental click causes data loss. Pair a deliberate, linear press duration with a rapid ease-out snap back on early release:

```css
.action-overlay {
  clip-path: inset(0 100% 0 0);
  transition: clip-path 200ms var(--ease-out); /* snappy reset on release */
}

.action-button:active .action-overlay {
  clip-path: inset(0 0 0 0);
  transition: clip-path 1800ms linear;         /* slow, deliberate press */
}

.action-button:active {
  transform: scale(0.97);
}
```

The `linear` curve is mandatory during the hold phase because progress bars should not accelerate or decelerate arbitrarily.

---

## 10. Active tab indicator with clip path

Interpolating separate colors across active and inactive tabs often results in muddy crossfades. Clip a duplicate layer instead:

Duplicate the tab labels in markup. Style the duplicate layer with active colors. Apply `clip-path` to the duplicate layer so only the current tab index is visible, then transition the clip boundaries on click:

```css
.tabs-active-layer {
  clip-path: inset(0 60% 0 20%); /* dynamically updated to active tab bounds */
  transition: clip-path 250ms var(--ease-in-out);
}
```

Typography and background colors change in perfect synchronization because they belong to one revealed surface rather than separate color interpolations.

---

## 11. Viewport image reveal

Marketing surfaces only. Never apply scroll reveals to functional interfaces visited daily:

```css
.reveal-image {
  clip-path: inset(0 0 100% 0);
  transition: clip-path 600ms var(--ease-in-out);
}

.reveal-image[data-visible="true"] {
  clip-path: inset(0 0 0 0);
}
```

Trigger using `IntersectionObserver` or Motion's `useInView` with `{ once: true }`. Fire once only. Re-animating elements every time they scroll into view disrupts reading.

---

## 12. Momentary blur for jarring state swaps

When crossfading between two text labels, counts, or icons creates clunky ghosting, apply a momentary 2px blur during the swap:

```css
.morph-content {
  transition:
    filter 180ms ease,
    opacity 180ms ease;
}

.morph-content.is-transitioning {
  filter: blur(2px);
  opacity: 0.7;
}
```

Blur blends intermediate rendering artifacts into a single transformation. Keep blur values under 15px to avoid Safari GPU degradation.

---

## 13. Drag to dismiss

Combine pointer capture with spring physics:

```js
const timeTaken = performance.now() - dragStartTime;
const velocity = Math.abs(currentOffset) / timeTaken;

if (Math.abs(currentOffset) >= SWIPE_THRESHOLD || velocity > 0.11) {
  dismiss();
} else {
  // Settle back to origin using spring physics
  animate(element, { y: 0 }, { type: "spring", duration: 0.4, bounce: 0.15 });
}
```

Key rules:
- Call `element.setPointerCapture(event.pointerId)` on start.
- Update `element.style.transform` directly, never via parent CSS custom properties.
- Apply elastic boundary resistance if pulled beyond normal constraints.

---

## 14. Sonner component design rules

Core principles for production notification components:
- **Zero configuration DX.** Work immediately with reasonable defaults without wrapper boilerplate.
- **Opinionated defaults.** Supply tested easing curves and typography out of the box.
- **Invisible edge handling.** Pause auto-dismiss timers when document visibility changes to hidden. Fill layout gaps with pseudo-elements to preserve hover continuity across stacked items.
- **Asymmetric timing.** Keep user inputs deliberate and system feedback immediate.
- **Slow motion review.** Inspect component transitions at 10% or 25% speed in browser DevTools to catch opacity and layout bounds clipping.
