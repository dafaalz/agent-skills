# Fluid gestures and spring physics

Complete mathematical reference for tactile gestures, momentum projection, spring mechanics, and compositor-level hardware acceleration.

## 1. Input latency and tactile response

Visual feedback must register on contact. Latency degrades directness.

- **Trigger feedback on pointer down.** Update visual state on `pointerdown` rather than waiting for `pointerup` or click events.
- **Eliminate input delays.** Strip tap delays, hover delays, and debounces from gesture paths.
- **Update transforms synchronously.** During continuous drag interactions, update element coordinates synchronously within `pointermove` or `requestAnimationFrame` handlers rather than deferring to transition completion.

```css
.button:active {
  transform: scale(0.97);
  transition: transform 100ms ease-out;
}
```

## 2. Direct manipulation and pointer tracking

Pointer coordinates and element position must match throughout the gesture.

- Lock pointer tracking using `setPointerCapture` so drag events continue uninterrupted when the cursor leaves element boundaries.
- Record the initial touch offset relative to the element origin. Maintain this offset during dragging instead of snapping the element center to the cursor.
- Ignore secondary touches while dragging to prevent coordinate jumps.

```js
let isDragging = false;
let grabOffsetY = 0;
let dragStartTime = 0;
let lastY = 0;

element.addEventListener('pointerdown', (event) => {
  if (isDragging) return;
  isDragging = true;
  dragStartTime = performance.now();
  element.setPointerCapture(event.pointerId);
  grabOffsetY = event.clientY - element.getBoundingClientRect().top;
});
```

## 3. Momentum projection and decay

Do not snap elements purely based on raw release coordinates. Project the resting position using exponential decay, then select the nearest snap point.

Apple deceleration decay formula:

```js
function project(initialVelocity, decelerationRate = 0.998) {
  return (initialVelocity / 1000) * decelerationRate / (1 - decelerationRate);
}

const projectedEndpoint = currentPosition + project(releaseVelocity);
const target = nearestSnapPoint(projectedEndpoint);
animateSpringTo(target, { velocity: releaseVelocity });
```

### Velocity-based dismissal calculation

Never force users to drag past a fixed distance threshold. Check flick velocity upon release:

```js
const elapsedTime = performance.now() - dragStartTime;
const velocity = Math.abs(dragDistance) / elapsedTime;

if (Math.abs(dragDistance) >= SWIPE_DISTANCE_THRESHOLD || velocity > 0.11) {
  dismissElement();
}
```

A quick flick with high velocity must dismiss the element even when the physical drag distance is small.

## 4. Progressive boundary resistance (rubber banding)

Boundaries must yield with increasing resistance rather than stopping abruptly. Calculate overshoot displacement with the Apple rubber band formula:

```js
function rubberband(overshoot, dimension, constant = 0.55) {
  return (overshoot * dimension * constant) / (dimension + constant * Math.abs(overshoot));
}
```

Parameters:
- `overshoot`. The raw displacement beyond the natural boundary in pixels.
- `dimension`. The corresponding viewport or container dimension (width or height).
- `constant`. The Apple resistance constant, calibrated to 0.55.

## 5. Interruptibility and velocity handoff

Interactions must remain interruptible at every frame. A user must be able to catch an element in flight and redirect its trajectory without waiting for previous animations to settle.

- **Keep input active during animation.** Never set `pointer-events: none` on transitioning elements.
- **Sample live presentation coordinates.** Query the active transform from computed styles or motion engine state before starting a new trajectory. Do not animate from logical target values.
- **Pass release velocity into the spring solver.** Transfer pointer velocity directly to the solver on gesture completion to eliminate visual hitches.
- **Blend velocity on reversals.** Preserve current momentum when targeting a new endpoint mid-flight.
- **Separate spatial axes.** Animate horizontal and vertical coordinates using independent spring solvers to avoid artificial diagonal coupling.

```js
import { animate } from 'motion';

animate(element, { y: targetY }, {
  type: 'spring',
  velocity: releaseVelocity,
  bounce: 0,
  duration: 0.4
});
```

When an animation solver requires relative velocity, normalize by remaining displacement:

```text
relativeVelocity = gestureVelocity / (targetValue - currentValue)
```

### WAAPI gesture interruption with commitStyles

Calling `animation.cancel()` on an active Web Animations API instance resets the element instantly to its stylesheet baseline, causing an abrupt jump. Preserve the live presentation geometry by invoking `commitStyles()` immediately before cancellation:

```js
function interruptAnimation(animation, element) {
  // 1. Snapshot live computed styles directly into inline style attributes
  animation.commitStyles();

  // 2. Cancel the animation player cleanly without visual snapback
  animation.cancel();

  // 3. Query the retained transform coordinate for continuous retargeting
  const currentTransform = element.style.transform;
}
```

## 6. Spring physics calibration

Use spring physics rather than fixed-duration easing curves for interactive UI components. Configure springs with damping ratio and response duration.

- **Damping ratio.** Controls oscillation and overshoot. A value of `1.0` is critically damped and settles without bounce. Values between `0.7` and `0.85` allow controlled overshoot suitable for momentum flicks.
- **Response.** The duration of an undamped oscillation cycle in seconds. Lower values produce snappier movement.

Production parameter reference:

| Interaction | Damping ratio | Response (seconds) |
| --- | --- | --- |
| Repositioning and picture-in-picture | 1.0 | 0.4 |
| Drawers and bottom sheets | 0.8 to 1.0 | 0.3 |
| Momentum flick or card swipe | 0.8 | 0.4 |

Spring configuration alternatives across platforms:

```js
/* Web (Motion) */
{ type: "spring", duration: 0.4, bounce: 0.15 }

/* iOS SwiftUI */
.spring(response: 0.35, dampingFraction: 0.85, blendDuration: 0.15)

/* Android Jetpack Compose */
spring(dampingRatio = 0.8f, stiffness = 380f)

/* Windows 11 Composition (WinUI 3) */
springAnimation.DampingRatio = 0.8f;
springAnimation.Period = TimeSpan.FromMilliseconds(250);

/* Linux Libadwaita (GTK4) */
adw_spring_params_new(1.0, 1.0, 1.0) /* mass 1.0, stiffness 1.0, damping 1.0 (critically damped) */

/* Flutter */
SpringSimulation(SpringDescription(mass: 1, stiffness: 100, damping: 15), start, end, velocity)
```

Keep bounce values between 0.1 and 0.3. Avoid heavy bounce in standard forms, data tables, or dashboards. Reserve bounce for playful actions or swipe dismissals.

## 7. Compositor performance and hardware acceleration

### Stick to GPU accelerated properties

Limit continuous gesture animations exclusively to `transform` and `opacity`.

- `transform` and `opacity` skip layout recalculation and paint cycles, running directly on the GPU compositor thread.
- Animating `height`, `width`, `margin`, or `padding` forces document relayout on every frame, causing dropped frames on mid-range devices.

### CSS custom property inheritance trap

Updating a CSS variable on a parent element causes style recalculation for all descendants:

```js
/* Bad: triggers style recalculation across every child element */
parentContainer.style.setProperty('--drag-offset', `${offset}px`);

/* Good: isolates transform updates directly to the targeted DOM node */
targetNode.style.transform = `translateY(${offset}px)`;
```

Update inline transforms directly on the moving element during continuous gestures.

### Framer Motion transform string optimization

Framer Motion shorthand properties (`x`, `y`, `scale`) calculate values on the main thread using `requestAnimationFrame`. When the main thread experiences heavy CPU workload, animation frames drop.

Enforce GPU compositor acceleration by providing explicit transform strings:

```jsx
/* Main thread bound: may drop frames during background rendering */
<motion.div animate={{ x: 120 }} />

/* Compositor accelerated: remains smooth under heavy CPU workload */
<motion.div animate={{ transform: "translateX(120px)" }} />
```

### Pre-rendered CSS versus JavaScript under load

Pre-rendered CSS transitions execute off the main thread. When the browser hydrates large React trees or parses heavy payloads, CSS motion stays smooth while JavaScript based animation libraries stutter. Use CSS for predetermined paths, reserving JavaScript for dynamic physics simulations or interactive gestures.

### Programmatic control with zero dependencies via WAAPI

The Web Animations API combines the flexibility of JavaScript with the performance of CSS compositor animations:

```js
element.animate(
  [
    { clipPath: "inset(0 100% 0 0)" },
    { clipPath: "inset(0 0 0 0)" }
  ],
  {
    duration: 300,
    fill: "forwards",
    easing: "cubic-bezier(0.23, 1, 0.32, 1)"
  }
);
```

WAAPI requires zero external runtime libraries, supports cancellation, and allows dynamic parameter injection.

## 8. Material translucency and layout depth

Translucent surfaces reveal underlying content while maintaining visual hierarchy.

- **Floating panels.** Combine `backdrop-filter: blur(...)` with semi-transparent backgrounds so underlying content shows through during scroll.
- **Avoid stacking translucent surfaces.** Layering multiple blurs degrades text contrast and increases GPU fill rate.
- **Scale blur with surface area.** Use stronger blur radii and deeper drop shadows on large modal sheets. Use tighter blurs on compact toolbars.
- **Dynamic scroll chrome.** Activate borders and blur treatments only when scrollable content passes underneath.
- **Keep transition blurs under 20px.** Heavy blur filters degrade rendering performance significantly, particularly in Safari.

```css
.toolbar {
  background: rgba(255, 255, 255, 0.75);
  backdrop-filter: blur(16px) saturate(180%);
  border-bottom: 1px solid rgba(255, 255, 255, 0.3);
}

@media (prefers-reduced-transparency: reduce) {
  .toolbar {
    background: #ffffff;
    backdrop-filter: none;
  }
}
```

## 9. Quick reference summary

| Requirement | Technique | Parameter or formula |
| --- | --- | --- |
| Default UI spring | Critically damped, zero overshoot | Damping `1.0`, response `0.3` to `0.4` |
| Momentum or flick | Under-damped, subtle bounce | Damping `0.8`, response `0.3` to `0.4` |
| Relative velocity | Normalized speed by displacement | `gestureVelocity / (target - current)` |
| Flick projection | Exponential decay resting point | `current + (v / 1000) * d / (1 - d)`, `d = 0.998` |
| Boundary resistance | Apple rubber band curve | `(x * d * 0.55) / (d + 0.55 * Math.abs(x))` |
| Interruptible motion | Sample live coordinate on interrupt | Query computed live transform |
| Direct manipulation | Pointer lock during drag | `element.setPointerCapture(event.pointerId)` |
| Multi-touch safety | Ignore secondary touch points | Early return if `isDragging` |
| GPU isolation | Animate compositor properties only | `transform` and `opacity` |
| Reduced motion | Opacity fade instead of translation | `@media (prefers-reduced-motion: reduce)` |
