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

Permitted for milestone screens, onboarding, or dashboard cards the user visits occasionally, but never for lists the user scrolls all day.

Dynamic Motion variants pattern for interruptible stagger:

```jsx
const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.05,
      delayChildren: 0.02,
    },
  },
};

const itemVariants = {
  hidden: { opacity: 0, y: 8 },
  visible: {
    opacity: 1,
    y: 0,
    transition: { duration: 0.25, ease: [0.16, 1, 0.3, 1] },
  },
};

export function StaggerList({ items }) {
  return (
    <motion.ul variants={containerVariants} initial="hidden" animate="visible">
      {items.map((item) => (
        <motion.li key={item.id} variants={itemVariants}>
          {item.name}
        </motion.li>
      ))}
    </motion.ul>
  );
}
```

Declarative CSS pattern with custom properties for dynamic list lengths:

```css
.stagger-item {
  opacity: 1;
  transform: translateY(0);
  transition:
    opacity 250ms var(--ease-out),
    transform 250ms var(--ease-out);
  transition-delay: calc(var(--stagger-index, 0) * 40ms);

  @starting-style {
    opacity: 0;
    transform: translateY(8px);
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

Apply these drag interaction rules:
- Call `element.setPointerCapture(event.pointerId)` on start.
- Update `element.style.transform` directly, never via parent CSS custom properties.
- Apply elastic boundary resistance if pulled beyond normal constraints.

---

## 14. Sonner component design rules

Follow these production notification principles:
- **Zero configuration DX.** Work immediately with reasonable defaults without wrapper boilerplate.
- **Opinionated defaults.** Supply tested easing curves and typography out of the box.
- **Invisible edge handling.** Pause auto-dismiss timers when document visibility changes to hidden. Fill layout gaps with pseudo-elements to preserve hover continuity across stacked items.
- **Asymmetric timing.** Keep user inputs deliberate and system feedback immediate.
- **Slow motion review.** Inspect component transitions at 10% or 25% speed in browser DevTools to catch opacity and layout bounds clipping.

---

## 15. Direct DOM ref mutation for continuous React updates

Updating React component state during continuous gestures or scroll events forces full component re-rendering on every animation frame, dropping frame rates under CPU workload.

Mutate DOM node inline styles directly via refs:

```jsx
import { useRef } from 'react';

export function GestureDraggable() {
  const elementRef = useRef(null);

  function handlePointerMove(offset) {
    if (!elementRef.current) return;
    elementRef.current.style.transform = `translate3d(0, ${offset}px, 0)`;
  }

  return <div ref={elementRef} className="draggable-card" />;
}
```

This isolates style updates strictly to the target DOM node without running React reconciliation passes.

---

## 16. Selective GPU layer promotion

Applying `will-change: transform` indiscriminately consumes GPU memory and degrades scrolling performance across pages.

Apply `will-change: transform` only when an element exhibits a 1px subpixel snapping jump at the moment animation begins:

```css
.card-with-subpixel-jump {
  will-change: transform;
}
```

Remove `will-change` once the animation settles, or omit it completely when motion renders without initial subpixel shifts.

---

## 17. Headless ecosystem and library matching

Rely on tested headless libraries for complex interactive primitives rather than hand-rolling unaccessible custom components:

| Need | Recommended library | Reason |
| --- | --- | --- |
| Popovers, dialogs, selects, dropdowns | Base UI (`@base-ui-components/react`) | Native support for `var(--transform-origin)` trigger anchors and ARIA focus management |
| Command palette (⌘K) | cmdk | Instant 0ms keyboard filtering without open or close motion delays |
| Stacked toast notifications | Sonner | Opinionated default curves, auto-pause on hidden document, and gesture dismissal |
| Number tickers and counter stats | NumberFlow | Formatted digit morphing without layout reflows |
| Virtualized long lists and data grids | Virtuoso | Smooth 60fps scrolling for lists exceeding 100 items without DOM bloat |
| General springs, layout morphs, gestures | Motion (`motion.dev`) | Native spring solvers, interruptibility, and presentation transform tracking |

---

## 18. SSR-safe entrance motion with attribute contract

Direct branching on `useReducedMotion()` during server-side rendering (SSR) causes hydration mismatches in React 19. The server renders `<motion.div>` with inline `opacity: 0`, while the client swaps to `<div>`, abandoning hydration and locking the element into permanent invisibility.

Preserve identical DOM tree structure between server and client. Apply `data-motion-enter` as an explicit contract, and enforce reduced motion overrides via high-specificity CSS:

```jsx
import * as React from 'react';
import * as motion from 'motion/react-client';

export function MotionEnter({ children }: { children: React.ReactNode }) {
  return (
    <motion.div
      data-motion-enter
      initial={{ opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.25, ease: [0.16, 1, 0.3, 1] }}
    >
      {children}
    </motion.div>
  );
}
```

Companion global CSS stylesheet rule:

```css
@media (prefers-reduced-motion: reduce) {
  [data-motion-enter] {
    opacity: 1 !important;
    transform: none !important;
    transition: none !important;
    animation: none !important;
  }
}
```

Apply these hydration rules:
* Never return alternate JSX node tags before initial client hydration settles.
* The `!important` rule overrides inline styles at the browser compositor level immediately, preventing flash of invisible content even before JavaScript executes.

---

## 19. Tactile spring pill tab indicator

Floating pill indicator that glides between active tabs using layout projection and physical damping:

```jsx
import * as React from 'react';
import { motion } from 'motion/react';

export function TabBar({ tabs, activeId, onSelect }: TabBarProps) {
  return (
    <div className="flex gap-1 p-1 bg-neutral-100 rounded-lg relative">
      {tabs.map((tab) => {
        const isActive = tab.id === activeId;
        return (
          <button
            key={tab.id}
            onClick={() => onSelect(tab.id)}
            className="relative px-3 py-1.5 text-sm font-medium transition-colors z-10"
          >
            {isActive && (
              <motion.div
                layoutId="activeTabPill"
                className="absolute inset-0 bg-white rounded-md shadow-sm -z-10"
                transition={{
                  type: 'spring',
                  stiffness: 400,
                  damping: 32,
                  mass: 0.8
                }}
              />
            )}
            {tab.label}
          </button>
        );
      })}
    </div>
  );
}
```

Apply these spring physics rules:
* Keep mass under 1.0 to prevent sluggish pill dragging.
* Use `layoutId` across sibling elements to trigger compositor hardware projection automatically.

---

## 20. Tactile swipe dismiss with velocity exit

Card dismiss gesture with resistance and velocity-based threshold:

```jsx
import * as React from 'react';
import { motion, useMotionValue, useTransform } from 'motion/react';

export function SwipeCard({ onDismiss, children }: SwipeCardProps) {
  const x = useMotionValue(0);
  const opacity = useTransform(x, [-150, 0, 150], [0, 1, 0]);

  return (
    <motion.div
      style={{ x, opacity }}
      drag="x"
      dragConstraints={{ left: 0, right: 0 }}
      dragElastic={0.6}
      onDragEnd={(_, info) => {
        if (Math.abs(info.offset.x) > 120 || Math.abs(info.velocity.x) > 500) {
          onDismiss();
        }
      }}
      transition={{ type: 'spring', stiffness: 350, damping: 28 }}
    >
      {children}
    </motion.div>
  );
}
---

## 21. Enterprise productive and expressive timing tokens

Enterprise platforms divide motion into two explicit tiers:

```css
:root {
  /* Productive motion tokens (data grids, menus, dropdowns, forms) */
  --duration-fast-01: 70ms;
  --duration-fast-02: 110ms;
  --duration-moderate-01: 150ms;
  --duration-moderate-02: 240ms;
  --ease-productive: cubic-bezier(0.2, 0, 0.38, 0.9);

  /* Expressive motion tokens (modals, landing page cards, milestone toasts) */
  --duration-slow-01: 400ms;
  --duration-slow-02: 700ms;
  --ease-expressive: cubic-bezier(0, 0, 0.3, 1);
}
```

Apply productive tokens to repetitive daily workflow components. Reserve expressive tokens for infrequent milestone events.

---

## 22. Safe reduced-motion duration collapse (0.01ms)

Setting `animation: none !important` or `transition: none !important` suppresses browser `transitionend` and `animationend` events. When asynchronous JavaScript libraries or modal dialogs wait on `transitionend` promises before unmounting or resolving state, `transition: none` hangs the application logic indefinitely.

Collapse the duration to a sub-millisecond value instead of canceling the event:

```css
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

This guarantees `transitionend` and `animationend` events fire immediately on the next event loop tick, resolving async promises without visual motion.

---

## 23. Off-thread vector animation runtime (dotLottie and Rive)

Complex vector graphics, interactive brand illustrations, and animated micro-icons consume significant CPU memory when rendered on the main DOM thread.

Transfer vector rendering to an isolated Web Worker via `OffscreenCanvas`:

```jsx
import * as React from 'react';
import { DotLottieWorker } from '@lottiefiles/dotlottie-web';

export function WorkerVectorIcon({ src }: { src: string }) {
  const canvasRef = React.useRef<HTMLCanvasElement>(null);

  React.useEffect(() => {
    if (!canvasRef.current) return;

    const dotLottie = new DotLottieWorker({
      canvas: canvasRef.current,
      src,
      autoplay: true,
      loop: true,
      renderConfig: {
        devicePixelRatio: Math.min(window.devicePixelRatio, 2),
      },
    });

    return () => {
      dotLottie.destroy();
    };
  }, [src]);

  return <canvas ref={canvasRef} width={120} height={120} className="w-12 h-12" />;
}
```

Worker canvas rendering offloads parsing and rasterization passes from the browser main thread, preserving 60Hz and 120Hz frame rates during background React reconciliations.

---

## 24. Consecutive warm-start tooltips

When hovering across a toolbar, the first tooltip requires a deliberate delay (300ms) to avoid visual flicker. Once any tooltip opens, adjacent tooltips must appear immediately without open delay or entrance motion:

```jsx
import * as React from 'react';

const TooltipGroupContext = React.createContext<{
  hasActiveTooltip: boolean;
  setHasActiveTooltip: (active: boolean) => void;
}>({
  hasActiveTooltip: false,
  setHasActiveTooltip: () => {},
});

export function TooltipGroup({ children }: { children: React.ReactNode }) {
  const [hasActiveTooltip, setHasActiveTooltip] = React.useState(false);
  const timeoutRef = React.useRef<NodeJS.Timeout | null>(null);

  function handleStateChange(isOpen: boolean) {
    if (isOpen) {
      if (timeoutRef.current) clearTimeout(timeoutRef.current);
      setHasActiveTooltip(true);
    } else {
      timeoutRef.current = setTimeout(() => {
        setHasActiveTooltip(false);
      }, 400); // 400ms grace period before resetting initial delay
    }
  }

  return (
    <TooltipGroupContext.Provider value={{ hasActiveTooltip, setHasActiveTooltip: handleStateChange }}>
      <div className="flex gap-1">{children}</div>
    </TooltipGroupContext.Provider>
  );
}
```

In the tooltip item, conditionally set entrance duration to 0ms when `hasActiveTooltip` is true. This makes toolbar exploration instantaneous while protecting the interface against accidental hover triggers.

---

## 25. Right-click context menu with selection blink and exit fade

Context menus serve repetitive workflows and must display in 0ms without entrance animation. Upon item selection, trigger a rapid visual blink on the selected target before fading out over 120ms:

```css
.context-menu {
  /* 0ms entrance: display immediately without motion delay */
  opacity: 1;
  transform: none;
}

.context-menu-item.is-selected {
  animation: context-menu-blink 80ms ease-out forwards;
}

.context-menu.is-closing {
  opacity: 0;
  transition: opacity 120ms var(--ease-out);
}

@keyframes context-menu-blink {
  0% { background-color: var(--color-accent-subtle); }
  50% { background-color: var(--color-accent); color: var(--color-accent-contrast); }
  100% { background-color: var(--color-accent-subtle); }
}
```

This delivers instant utility on invocation while giving visual confirmation of the chosen action before the menu unmounts.

---

## 26. High-stakes trust confirmation (The Wise pattern)

Completing asynchronous operations in 0ms can induce user anxiety during irreversible or financial workflows. When operations complete instantaneously, insert a synthetic 350ms to 450ms confirmation sequence to close the perception delta:

```jsx
import * as React from "react";
import { motion } from "motion/react";

export function TrustTransferConfirmation({ isComplete, onFinish }: TrustConfirmationProps) {
  React.useEffect(() => {
    if (!isComplete) return;
    // Artificial 400ms duration to allow perception of completed settlement
    const timer = setTimeout(() => {
      onFinish();
    }, 450);
    return () => clearTimeout(timer);
  }, [isComplete, onFinish]);

  return (
    <div className="relative flex items-center justify-center p-4">
      <motion.div
        initial={{ scale: 0.9, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        exit={{ scale: 0.95, opacity: 0 }}
        transition={{ duration: 0.2, ease: [0.23, 1, 0.32, 1] }}
        className="flex items-center gap-2 text-sm font-medium text-emerald-600"
      >
        <svg className="w-5 h-5 text-emerald-500 animate-checkmark" viewBox="0 0 24 24">
          <circle cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="2" fill="none" />
          <path d="M7 13l3 3 7-7" stroke="currentColor" strokeWidth="2" fill="none" />
        </svg>
        <span>Payment confirmed</span>
      </motion.div>
    </div>
  );
}
```

This prevents user panic and repeated click attempts caused by instant invisible state settlement.

---

## 27. State feedback fallback under disabled motion (The Pokémon pattern)

Disabling animations via user preference or frequency gating must never eliminate state change confirmation. When motion is disqualified, replace spatial translation with instant tactile or visual feedback (such as a 30-frame screen shake or high-contrast border flash):

```css
/* Screen shake fallback for critical impacts when standard animations are disabled */
.damage-container[data-impact="true"] {
  animation: state-shake 200ms ease-out;
}

@keyframes state-shake {
  0% { transform: translateX(0); }
  25% { transform: translateX(-4px); }
  50% { transform: translateX(4px); }
  75% { transform: translateX(-2px); }
  100% { transform: translateX(0); }
}

@media (prefers-reduced-motion: reduce) {
  /* Replace spatial shake with an instantaneous high-contrast border flash */
  .damage-container[data-impact="true"] {
    animation: state-flash 160ms ease-out;
    transform: none !important;
  }
}

@keyframes state-flash {
  0% { outline: 2px solid var(--color-error); }
  100% { outline: 2px solid transparent; }
}
```

This preserves state registration without forcing vestibular motion upon users.

---

## 28. Hardware-anchored spatial volume slider (The Pixel pattern)

Anchor transient software controls directly to the physical hardware input location. When triggering volume adjustments, animate the slider horizontally out of the screen edge adjacent to the physical rocker button:

```css
.volume-overlay {
  position: fixed;
  right: 0;
  top: var(--hardware-button-offset-y, 25%);
  transform-origin: right center;
  transform: translateX(100%);
  opacity: 0;
  transition:
    transform 180ms var(--ease-out),
    opacity 180ms var(--ease-out);
}

.volume-overlay[data-visible="true"] {
  transform: translateX(0);
  opacity: 1;
}
```

Anchoring the software surface to the physical hardware button reinforces the user mental map of control ownership.

