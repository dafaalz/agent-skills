# Mental models, time perception, and animation engineering

Engineering principles governing spatial continuity, perception of time, interaction restraint, and personality calibration in user interfaces.

## 1. The five core rules of interface motion

### Rule 1. Spatial consistency and copying nature

Human visual systems evolved to interpret physical reality where objects possess mass, momentum, and persistent spatial coordinates. Software lacks physical constraints. Elements can appear or vanish instantaneously, breaking spatial orientation. Interface motion re-establishes physical intuition through spatial consistency.

Motion creates an internal map of where intangible software entities live.

- **Hardware and software continuity.** Anchor digital controls to physical inputs. The Google Pixel volume slider expands outward from the physical volume rocker. Tapping an icon or the Apple Dynamic Island expands the application surface out of the physical or digital container, establishing that the app lives within that spatial anchor.
- **Hinge and multi-screen continuity.** Dual-screen devices (such as Microsoft Surface Duo) sample hinge angle sensors at 60Hz. The compositor tilts the active viewport around a 3D center axis, applying progressive blur that strengthens toward the fold accompanied by edge vignetting. Both displays remain active concurrently to preserve spatial continuity.
- **Collapsible panels.** When collapsing a navigation sidebar or drawer in a productivity tool, animate the exit off-screen. This informs the user that the controls persist in off-screen space and remain retrievable.
- **Disney principles adapted to software.** Frank Thomas and Ollie Johnston documented the 12 principles of animation in 1981. In 1993, researchers adapted slow in and slow out into cubic-bezier easing curves for graphical user interfaces. Squash and stretch principles govern modern elastic surfaces, liquid glass, and rubber-band boundary collisions.

### Rule 2. Restraint and frequency gating

Physical motion is slow. Applying real-world physics to high-frequency digital workflows introduces friction. When an interface element serves daily work, prioritize speed over physical simulation.

- **Keyboard-initiated actions.** Never animate keyboard-initiated actions. Keyboard shortcuts (`Cmd+Space`, `Esc`, `Tab`, command palette triggers) reflect deliberate user intent where the user already knows the outcome. An animation teaches spatial origin on first exposure. By the hundredth trigger, animation forces unnecessary waiting. Raycast executes launcher open and close states in 0ms, while Spotlight delays interaction with a 400ms entrance animation.
- **Context menus.** Right-click context menus must open in 0ms without entrance animation. Upon item selection, trigger a rapid background blink on the selected row, followed by a 120ms fade-out. Provide zero motion on entry and micro-motion on exit.
- **Tooltip warm-start.** Enforce a 300ms hover delay on the initial tooltip to avoid visual noise during cursor transit. Once any tooltip opens, adjacent triggers must display tooltips in 0ms without delay or animation because user inspection intent is active.
- **Decoupling backend latency.** In drag-and-drop workflows (such as video editors or file managers), open the target viewport immediately on drop. Do not block the interface transition on backend database record creation.
- **Interruptibility and retargeting.** Never lock pointer events during animations. A user swiping a sheet downward must retain the ability to catch the surface mid-flight and reverse the swipe upward. Query live presentation transforms and retarget the spring solver dynamically.

### Rule 3. Speed calibration and front-loaded velocity

Duration alone does not determine perceived speed. The distribution of velocity across time governs how responsive an interaction feels.

| Easing curve | Velocity distribution | Impact on user perception | Permitted usage |
| --- | --- | --- | --- |
| Linear | Constant speed throughout | Mechanical, unnatural, robotic | Marquees, steady progress bars, hold-to-confirm fills |
| Ease-in | Slow start, accelerating end | Sluggish, delayed feedback, heavy | Prohibited for UI entrances and exits |
| Ease-out | High initial velocity, gentle deceleration | Snappy, responsive, immediate reaction | Entrances, exits, dropdowns, dialogs, popovers |
| Ease-in-out | Slow start, fast middle, slow end | Smooth, balanced, weighted | Elements already on screen changing position or morphing |

Ease-out curves feel faster than linear or ease-in transitions with identical millisecond durations. Ease-out front-loads 70% to 80% of total travel distance into the first 30% of elapsed time. The human eye registers immediate reaction to input, while the remaining deceleration settles smoothly.

Mobile platforms replace fixed durations with spring physics. Defining physical parameters (stiffness and damping) allows the animation to absorb incoming gesture velocity and resolve naturally.

### Rule 4. Time perception engineering

Perceived time differs from elapsed clock time. Use motion to manage human perception during state changes and system latency.

- **Buying startup time.** Expanding an application window out of its launch icon occupies the user's visual attention for 200ms to 400ms. Operating systems draw an initial frame or display a static launch screen during this window, concealing cold boot latency.
- **Synthetic touch delays and trajectory prediction.** The Android input pipeline introduces a deliberate 5ms touch buffer while predicting finger position up to 80ms ahead. This mathematical extrapolation aligns pointer coordinates with display VSYNC intervals, eliminating visual jitter during continuous scrolling.
- **The Wise paradox (artificial delay for trust).** Completing complex operations in 0ms can trigger user anxiety and distrust. When Wise reduced cross-border bank transfer times to near-zero, users suspected the transaction had failed because moving money felt instantaneous. Introducing a 400ms confirmation animation displaying settlement progress increased user trust and satisfaction. Use artificial delay on high-stakes operations (financial transfers, irreversible deletions, cryptographic signing) where instantaneous completion undermines credibility.

### Rule 5. Personality calibration

Calibrate motion dynamics to the product domain:

| Product profile | Motion characteristics | Spring configuration | Typical duration |
| --- | --- | --- | --- |
| High-productivity tool (Linear, IDEs) | Rigid, minimal, predictable, zero bounce | Critically damped (damping ratio 1.0) | 100ms to 200ms |
| Playful consumer app (Duolingo) | Bouncy, elastic, expressive overshoot | Under-damped (damping ratio 0.65 to 0.8) | 250ms to 400ms |
| Premium luxury brand | Fluid, deliberate, weighted, elegant | Critically damped with custom ease-in-out | 400ms to 800ms |

- **Adding bounce.** Bouncy motion overshoots the target coordinate before pulling back into place. Overshoot introduces personality and lightheartedness. Avoid bounce in enterprise data grids, financial entry fields, or dense navigation trees.
- **Frame rate modulation.** In character animation (such as Miles Morales in Spider-Verse moving on twos at 12fps before transitioning to ones at 24fps), frame rates communicate skill level and confidence. Interfaces can vary stagger cadences and step timing to contrast draft states from confirmed states.
- **Regulatory limits on gamified motion.** Celebratory animations (such as confetti on milestone achievements) reinforce user progress. In financial trading platforms, gamified animations can violate consumer protection regulations. In 2024, Massachusetts regulators fined Robinhood 7.5 million dollars and required permanent removal of confetti animations to curb gamified trading behavior.

## 2. The state feedback invariant (The Pokémon principle)

In early game engineering (such as Pokémon Red and Blue), disabling battle animations disabled attack sequences but retained a 30-frame screen shake upon taking damage. Without screen shake, players could not register health depletion.

When motion is disqualified by the frequency gate or disabled via `prefers-reduced-motion`:
- Never drop state confirmation.
- Replace spatial motion with instantaneous visual indicators: row selection blinks, high-contrast border flashes, subtle background color pulses, or badge updates.
- Ensure every interaction delivers immediate proof of state registration within 16ms of input.

## 3. Interruptibility and retargeting implementation

Interfaces must remain interruptible at every frame. If an element is transitioning between State A and State B, an incoming interaction must retarget the motion toward State C from its current presentation position.

```javascript
import { animate } from 'motion';

let currentAnimation = null;

function moveTo(element, targetY, initialVelocity = 0) {
  // Read live computed transform from presentation layer
  const style = window.getComputedStyle(element);
  const matrix = new DOMMatrixReadOnly(style.transform);
  const currentY = matrix.m42;

  if (currentAnimation) {
    currentAnimation.stop();
  }

  currentAnimation = animate(
    element,
    { y: [currentY, targetY] },
    {
      type: 'spring',
      stiffness: 400,
      damping: 35,
      velocity: initialVelocity,
    }
  );
}
```

This prevents visual teleportation when interrupting transitions in flight.
