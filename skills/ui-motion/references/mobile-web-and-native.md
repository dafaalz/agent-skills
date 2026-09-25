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

## 3. Verification criteria

Validate mobile implementations against this checklist:

| Check | Passing condition |
| --- | --- |
| Tap delay | `touch-action: manipulation` applied to interactive nodes |
| Viewport sizing | Layout containers use `dvh` or `svh` units without horizontal or vertical drift |
| Input zoom | Input text size is at least 16px on coarse pointer devices |
| Tap highlight | WebKit tap highlight color is transparent |
| Runtime thread | Gesture handlers trigger zero React re-renders and invoke no JS callbacks per frame |
| Haptics | Vibrations fire on the visual state frame and execute at most once per user gesture |
| Native feel | Tested on physical hardware rather than browser responsive emulation |
