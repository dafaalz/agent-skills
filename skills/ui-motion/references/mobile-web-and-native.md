# Mobile web and React Native motion engineering

Engineering guidelines for mobile web platform quirks, touch interactions, and native Expo or React Native motion runtimes.

## 1. Web on mobile platform layer

Most mobile interface defects originate in browser defaults rather than motion engines. Apply these platform fixes before implementing animations.

### Viewport and layout sizing

Standard `100vh` calculates height using the largest viewport state where browser address bars collapse. On initial page load, this causes vertical overflows.

- Use `100dvh` on app shells, drawers, and fixed containers to dynamically track address bar visibility changes.
- Use `100svh` on hero sections to guarantee content fits without shifting layout as the user scrolls.

```css
.app-shell {
  height: 100dvh;
}

.hero-section {
  min-height: 100svh;
}
```

### Touch feedback and tap delays

Browsers introduce an artificial 300ms delay to detect double taps when double-tap zoom is possible.

- Add `touch-action: manipulation` to all interactive controls to eliminate the 300ms tap delay.
- Remove the gray tap highlight painted by mobile Safari and Chrome by setting `-webkit-tap-highlight-color: transparent`.
- Trigger press styling on the `:active` pseudo-class or on `pointerdown` events instead of waiting for `click` or `pointerup`.

```css
html {
  -webkit-tap-highlight-color: transparent;
}

button,
a,
[role="button"],
.interactive-target {
  touch-action: manipulation;
}

.interactive-target:active {
  transform: scale(0.97);
  transition: transform 120ms var(--ease-out);
}
```

### Input auto-zoom prevention

iOS Safari zooms the viewport when focus moves into an input field with a font size below 16px. This zoom disrupts layouts permanently until manual zoom resets.

Set input text size to at least 16px on touch devices instead of disabling user zoom:

```css
@media (pointer: coarse) {
  input,
  textarea,
  select {
    font-size: 16px;
  }
}
```

### Overscroll and scroll chaining

Overscrolling past boundaries triggers full-page rubber banding in iOS Safari or pull-to-refresh in Android Chrome.

- Apply `overscroll-behavior: none` to the document root in standalone web applications.
- Apply `overscroll-behavior: contain` to internal scroll containers, such as drawers and sidebars, to preserve native bounce while stopping scroll events from propagating to parent layers.

```css
html,
body {
  overscroll-behavior: none;
}

.sheet-scroll-container {
  overflow-y: auto;
  overscroll-behavior: contain;
}
```

### Axis disambiguation on gesture surfaces

Horizontal swipes on carousels conflict with vertical document scrolling. Declare allowed browser actions explicitly:

- Set `touch-action: pan-y` on horizontal tracks so vertical scrolling stays with the browser while horizontal gestures remain with the component.
- Set `touch-action: pan-x` on vertical bottom sheet drag handles.
- Set `touch-action: none` strictly on elements that completely manage 2D gestures.

```css
.horizontal-carousel {
  touch-action: pan-y;
}

.bottom-sheet-handle {
  touch-action: pan-x;
}
```

### Text selection on interactive controls

Prolonged touch on buttons triggers text selection or copy callout overlays.

```css
button,
[role="button"],
.tab-trigger,
.drag-handle {
  user-select: none;
  -webkit-user-select: none;
  -webkit-touch-callout: none;
}
```

Do not apply `user-select: none` to readable content or body text.

### Edge-to-edge layout and safe areas

Mobile displays with notches and home indicator bars require explicit viewport configurations to enable edge-to-edge rendering:

```html
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover, interactive-widget=resizes-content" />
```

Pad content away from physical obstructions using CSS environment variables:

```css
.fixed-header {
  padding-top: env(safe-area-inset-top, 0px);
}

.fixed-bottom-bar {
  padding-bottom: calc(1rem + env(safe-area-inset-bottom, 0px));
}
```

### Mobile drawer transitions and focus orchestration

Mobile drawers, bottom sheets, and slide-over panels present distinct timing challenges between visibility changes, CSS transitions, and browser focus management.

#### Engine isolation

Never mix CSS transition utility classes such as `transition` or `duration-300` with JavaScript animation libraries or touch drag scripts on the same element. Mixing both engines creates conflicting property mutations and frame drops. Assign full transform control either to CSS classes or to JavaScript transforms.

#### Reflow flush requirement

When revealing an off-screen element, removing `hidden` or `display: none` in the same execution turn as removing `translate-y-full` skips the transition in WebKit and Blink. Browsers coalesce DOM mutations and apply final visible coordinates without animating the entry.

Scheduling class changes via `requestAnimationFrame` remains unreliable under heavy main thread load. Force an immediate synchronous layout calculation between removing `hidden` and releasing the transform offset class. Evaluating `void element.offsetHeight` forces the rendering engine to recalculate geometry so subsequent transform class removals animate smoothly from off-screen coordinates.

#### State retention on exit

When dismissing a drawer, retain the off-screen transform class after hiding the element. Never strip dismissal classes when applying `hidden`. Keeping dismiss classes on hidden elements guarantees subsequent open operations start from their off-screen baseline rather than flashing into view.

#### Focus timing and virtual keyboard layout shifts

Focusing interactive elements while a drawer moves across the viewport causes visual defects because browsers scroll moving elements into view and jump the viewport. Auto-focusing a text input on mobile devices triggers the virtual software keyboard immediately. The keyboard shrinks visual viewport height (`100dvh`) and disrupts the entrance animation.

Enforce these focus rules on mobile drawers:
1. Defer calling `.focus()` until the entry transition completes fully. Add 10ms of buffer past the CSS transition duration.
2. Always pass `{ preventScroll: true }` into `.focus()` to prevent browsers from scrolling the window during focus assignment.
3. On touch viewports matching `(pointer: coarse)` or screen widths below 640px, never auto-focus text inputs. Focus the modal container or the close button instead. Allow users to tap input fields explicitly when ready.

#### Standard reference implementation

```javascript
class MobileDrawer {
  constructor(element, durationMs = 300) {
    this.element = element;
    this.durationMs = durationMs;
    this.focusTimer = null;
  }

  open() {
    clearTimeout(this.focusTimer);

    // 1. Reveal element while keeping parked off-screen coordinates
    this.element.classList.remove('hidden');

    // 2. Force layout reflow before releasing offset classes
    void this.element.offsetHeight;

    // 3. Trigger transition by removing off-screen class
    this.element.classList.remove('translate-y-full');

    // 4. Orchestrate focus after animation completes
    const isTouch = window.matchMedia('(pointer: coarse)').matches || window.innerWidth < 640;
    this.focusTimer = setTimeout(() => {
      if (isTouch) {
        // Focus container or close button to protect virtual keyboard viewport
        const closeBtn = this.element.querySelector('[data-drawer-close]');
        if (closeBtn) {
          closeBtn.focus({ preventScroll: true });
        } else {
          this.element.focus({ preventScroll: true });
        }
      } else {
        // Desktop viewports can focus the first interactive control
        const input = this.element.querySelector('input, textarea, select, button');
        if (input) {
          input.focus({ preventScroll: true });
        }
      }
    }, this.durationMs + 10);
  }

  close() {
    clearTimeout(this.focusTimer);

    // 1. Move back off-screen using hardware acceleration
    this.element.classList.add('translate-y-full');

    // 2. Hide element after transition completes and retain parked coordinates
    setTimeout(() => {
      this.element.classList.add('hidden');
    }, this.durationMs);
  }
}
```

---

## 2. React Native and Expo motion architecture

Mobile animation requires strict separation between JavaScript application logic and the UI rendering thread.

### Two runtimes and worklet isolation

React Native executes application logic in the JavaScript runtime. Reanimated executes worklets directly on the native UI thread. Touching the JavaScript runtime during a gesture drops frames under CPU load.

Rules for UI thread isolation:
1. Never execute `setState` inside gesture or scroll event handlers. Use `useSharedValue` combined with `useAnimatedStyle`.
2. Do not schedule calls back to the React Native runtime inside `onUpdate` handlers. In Reanimated 4, avoid calling `scheduleOnRN` or deprecated `runOnJS` on every frame. Execute JS callbacks only in `onEnd` or via `useAnimatedReaction` when values cross a threshold.
3. Mark functions called from worklets with the `'worklet'` directive on line one.
4. Read and write shared values via `.get()` and `.set()` methods for full compatibility with React Compiler. Do not mutate `.value` directly.
5. Never read or write shared values during component render passes. Access shared values only inside worklets, handlers, or lifecycle hooks.

```jsx
import { useSharedValue, useAnimatedStyle, withSpring } from 'react-native-reanimated';
import { Gesture, GestureDetector } from 'react-native-gesture-handler';

export function DraggableBox() {
  const translateY = useSharedValue(0);

  const panGesture = Gesture.Pan()
    .onUpdate((event) => {
      'worklet';
      translateY.set(event.translationY);
    })
    .onEnd((event) => {
      'worklet';
      translateY.set(
        withSpring(0, {
          duration: 400,
          dampingRatio: 0.8,
          velocity: event.velocityY,
        })
      );
    });

  const animatedStyle = useAnimatedStyle(() => ({
    transform: [{ translateY: translateY.get() }],
  }));

  return (
    <GestureDetector gesture={panGesture}>
      <Animated.View style={[styles.box, animatedStyle]} />
    </GestureDetector>
  );
}
```

### Threshold triggers without polling

When actions fire upon reaching a physical displacement point, evaluate conditions on the UI thread:

```jsx
const armed = useSharedValue(false);

useAnimatedReaction(
  () => pullDistance.get() > REFRESH_THRESHOLD,
  (isArmed, wasArmed) => {
    if (isArmed !== wasArmed) {
      armed.set(isArmed);
      scheduleOnRN(Haptics.impactAsync, Haptics.ImpactFeedbackStyle.Light);
    }
  }
);
```

### Hardware acceleration and layout properties in React Native

Properties like `width`, `height`, `margin`, `padding`, `top`, and `left` trigger the Yoga layout engine across child and sibling elements on every frame.

- Animate `transform` and `opacity` arrays exclusively.
- Position translate before scale inside the transform array such as `transform: [{ translateY }, { scale }]` to avoid scaling spatial offsets.
- Animate opacity of a static shadowed layer instead of animating Android `elevation`.
- Avoid animating `BlurView` intensity dynamically on Android because each frame forces blur re-renders. Crossfade static blurred surfaces instead.

### Haptic feedback integration

Haptic pulses confirm physical interactions when properly calibrated:

| Interaction | API call |
| --- | --- |
| Detent tick, segmented slider step | `Haptics.selectionAsync()` |
| Sheet detent lock, snap completion | `Haptics.impactAsync(ImpactFeedbackStyle.Light)` |
| Destructive action trigger, heavy collision | `Haptics.impactAsync(ImpactFeedbackStyle.Medium)` |
| Operation success or failure confirmation | `Haptics.notificationAsync(NotificationFeedbackType.Success)` |

Three requirements govern haptic implementation:
1. Fire haptics on the exact frame the visual change occurs.
2. Limit haptics to one pulse per committed user action. Never fire haptics continuously during scroll or per-frame movement.
3. Never use haptics as the sole confirmation signal. Visual affordances must remain fully informative without vibration.

### High refresh rate displays

Enable 120Hz ProMotion support on iOS devices by configuring `app.json`:

```json
{
  "expo": {
    "ios": {
      "infoPlist": {
        "CADisableMinimumFrameDurationOnPhone": true
      }
    }
  }
}
```

This configuration lowers the per-frame execution budget from 16ms to 8ms.

### Keyboard synchronisation

Synchronize UI position directly with software keyboards on the UI thread using `react-native-keyboard-controller` instead of React Native default keyboard listeners:

```jsx
import { useKeyboardHandler } from 'react-native-keyboard-controller';

const height = useSharedValue(0);

useKeyboardHandler({
  onMove: (event) => {
    'worklet';
    height.set(event.height);
  },
});
```

---

## 3. Jetpack Compose and Flutter Impeller native pipelines

### Jetpack Compose draw-phase isolation

Reading animated state in Compose during composition triggers recomposition of the entire composable tree on every frame.

Isolate animated properties to the Draw phase using the lambda version of `Modifier.graphicsLayer`:

```kotlin
// Bad: triggers full recomposition on every animation frame
val translationY by animateFloatAsState(targetValue)
Box(modifier = Modifier.translationY(translationY))

// Good: isolates updates strictly to the RenderNode draw phase
val translationY = remember { Animatable(0f) }
Box(
    modifier = Modifier.graphicsLayer {
        this.translationY = translationY.value
    }
)
```

Never read animated state values inside the parent composable body. Confining state reads inside `graphicsLayer { ... }` skips Recomposition and Layout passes, sending transforms directly to the hardware rendering pipeline.

### Flutter Impeller rendering pipeline and VSYNC synchronization

Flutter Impeller replaces Skia by pre-compiling all shaders ahead of time to eliminate runtime shader compilation jank:
- **Avoid unbounded `saveLayer` calls.** Every `saveLayer` invocation creates a temporary offscreen framebuffer texture. Stacking multiple `BackdropFilter` widgets or dynamic opacity groups saturates mobile GPU fill rate.
- **VSYNC synchronization.** Bind custom physics simulations to `TickerProvider` to synchronize calculations with the native display frame clock (16.67ms on 60Hz, 8.33ms on 120Hz).
- **Direct momentum injection.** Pass pointer velocity directly to `SpringSimulation` when releasing drag gestures without artificial deceleration clamps.

---

## 4. Operating system accessibility flag synchronization

Native mobile runtimes expose system accessibility preferences that must gate animations across native code:

| Platform | Native API check | Recommended action |
|---|---|---|
| iOS | `UIAccessibility.isReduceMotionEnabled` | Substitute spatial transforms with alpha crossfades |
| Android | `ValueAnimator.areAnimatorsEnabled()` | Check `Settings.Global.TRANSITION_ANIMATION_SCALE`, collapse durations when 0 |
| Windows | `UISettings.AnimationsEnabled` | Listen to `AnimationsEnabledChanged` event and disable decorative transitions |

When bridging native preferences to web views or hybrid shells, query these APIs during application bootstrap and forward status flags to JavaScript via root attributes (`data-reduce-motion="true"`).

---

## 5. Verification criteria

Validate mobile implementations against this checklist:

| Check | Passing condition |
| --- | --- |
| Tap delay | `touch-action: manipulation` applied to interactive nodes |
| Viewport sizing | Layout containers use `dvh` or `svh` units without horizontal or vertical drift |
| Input zoom | Input text size is at least 16px on coarse pointer devices |
| Tap highlight | WebKit tap highlight color is transparent |
| Runtime thread | Gesture handlers trigger zero React re-renders and invoke no JS callbacks per frame |
| Compose phase | Animated values read inside `Modifier.graphicsLayer { ... }` lambda |
| Flutter Impeller | Zero unbounded `saveLayer` calls during interactive scroll or drag |
| OS motion flag | Native `isReduceMotionEnabled` or `areAnimatorsEnabled()` checked and synchronized |
| Haptics | Vibrations fire on the visual state frame and execute at most once per user gesture |
| Native feel | Tested on physical hardware rather than browser responsive emulation |
| Drawer transitions | Layout reflow flushed with `void el.offsetHeight` before removing offset classes |
| Focus timing | Focus deferred past transition duration with `{ preventScroll: true }` |
| Virtual keyboard | No auto-focusing text inputs on coarse pointer viewports |
