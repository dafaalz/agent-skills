# Deconstructing Motion, Micro-interactions, and Canvas Physics

Technical manual for reverse-engineering animation timing curves, scroll-driven dynamics, magnetic button physics, WebGL shader execution, and GPU-composited 60fps performance.

## Motion Deconstruction Principles

High-end digital experiences rely on precise motion curves, tactile micro-feedback, and hardware-accelerated rendering. Reverse engineering these effects requires isolating physics parameters in browser inspection tools rather than estimating transitions by eye.

The following eight authoritative sources define motion engineering and inspection:

### 1. Inspect Animations with Chrome DevTools
Author: Chrome DevTools Team (Google).
Official source: https://developer.chrome.com/docs/devtools/animations/

Details workflow tools for capturing, slowing, and modifying animated UI elements.

Inspection methodology:
* Open the Animations drawer (`Cmd + Shift + P` then type `Show Animations`).
* Trigger animations on the live page through clicks, viewport scrolling, or state toggles. DevTools records animated elements into an Animation Group thumbnail.
* Slow playback speed to 10 percent or 25 percent to inspect frame-by-frame position changes.
* Drag timeline scrubber playheads to analyze start delays and staging sequences.
* Click the cubic-bezier curve icon on keyframe bars to launch the visual Bezier curve editor and copy four-point coordinates directly.

### 2. An Interactive Guide to CSS Transitions
Author: Josh W. Comeau.
Official source: https://www.joshwcomeau.com/animation/css-transitions/

Establishes mathematical foundations for transition curves and physical interface states.

Inspection methodology:
* Force element pseudo-states (`:hover`, `:active`, `:focus-within`) in the DevTools Styles pane to inspect transition styles.
* Examine easing functions: entering elements require decelerating ease-out curves, while elements moving between persistent coordinates use ease-in-out curves.
* Verify `transform-origin` coordinates. Contextual elements like dropdowns and tooltips must anchor to their triggering element bounds rather than the default 50 percent center point.
* Avoid declaring `transition: all`. Blanket declarations force browsers to calculate transitions for unintended properties, triggering unnecessary paint cycles.

### 3. Great Animations and 7 Practical Animation Tips
Author: Emil Kowalski (animations.dev).
Official source: https://emilkowal.ski/ui/great-animations

Details motion duration budgets and tactile physical micro-feedback.

Inspection methodology:
* Measure duration budgets. Functional utility animations must complete within 150ms to 250ms to keep interfaces responsive.
* Inspect tactile click feedback. Primary buttons should apply subtle compression, such as `transform: scale(0.97)` over 100ms to 140ms on active press states.
* Test accessible reduced motion. Open the DevTools Rendering drawer, enable `prefers-reduced-motion: reduce`, and confirm animations replace spatial movement with soft opacity fades.

### 4. Lenis Smooth Scroll Documentation and Architecture
Author: Darkroom Engineering.
Official source: https://lenis.darkroom.engineering/

Defines modern smooth scrolling that preserves native browser accessibility and event handling.

Inspection methodology:
* Inspect global window scope for active Lenis instances (`window.lenis`).
* Verify native browser behavior. Test `Cmd + F` text search, keyboard arrow navigation, and anchor jumps. Compliant smooth scroll implementations keep these functions intact.
* Profile requestAnimationFrame execution. Open the Performance tab and verify that the scroll loop executes in under 16.6ms per frame without blocking user interaction threads.

### 5. GSAP ScrollTrigger Plugin Architecture
Author: GreenSock (Jack Doyle).
Official source: https://gsap.com/docs/v3/Plugins/ScrollTrigger/

Controls timeline execution, scrubbing, and pinning based on viewport scroll progress.

Inspection methodology:
* Run `ScrollTrigger.getAll()` in the browser console to list active trigger objects.
* Inspect trigger configurations, including `start`, `end`, `scrub`, and `pin` parameters.
* Visualize trigger boundaries live by injecting visual markers:
```javascript
ScrollTrigger.getAll().forEach(trigger => { trigger.vars.markers = true; trigger.init(); });
```
* Inspect pinned containers in the DOM. GSAP inserts temporary `pin-spacer` wrapper elements to hold normal document flow during fixed pinning stages.
* Ensure instances are removed when unmounting components to prevent memory leaks.

### 6. Magnetic Buttons and Interactive UI Effects
Author: Manoela Ilic, Codrops (Tympanus).
Official source: https://tympanus.net/codrops/2021/01/26/magnetic-buttons/

Calculates relative cursor tracking physics and dual-layer parallax movement.

Inspection methodology:
* Inspect `mousemove`, `mouseenter`, and `mouseleave` event listeners registered on target buttons.
* Deconstruct coordinate math: calculate delta distances between cursor coordinates (`clientX`, `clientY`) and element bounding box centers retrieved from `getBoundingClientRect()`.
* Measure damping coefficients. Magnetic buttons multiply cursor distance by damping factors (typically 0.2 to 0.4) and update position using smooth interpolations.
* Inspect double parallax layering: internal button labels or icons translate farther than outer container frames to produce visual depth.
* Guard magnetic tracking behind `@media (hover: hover) and (pointer: fine)` to prevent broken interactions on touch screens.

### 7. WebGL Fundamentals and Shader Architecture
Author: Gregg Tavares.
Official source: https://webglfundamentals.org/

Technical guide for inspecting Canvas WebGL render loops and GLSL shaders.

Inspection methodology:
* Locate the `<canvas>` element and check rendering context (`webgl` or `webgl2`).
* Use the Spector.js browser extension to capture a live render frame.
* Inspect compiled GLSL vertex and fragment shader source code directly inside the Spector.js program viewer.
* Check time (`u_time`), mouse coordinate (`u_mouse`), and resolution (`u_resolution`) uniform variables passed to the shader.
* Confirm that device pixel ratio rendering clamps at 2 (`Math.min(window.devicePixelRatio, 2)`) to avoid GPU performance drops on high-density displays.
* Confirm that WebGL render loops pause when canvases exit the viewport via IntersectionObserver.

### 8. Stick to Compositor-Only Properties and Manage Layer Count
Authors: Paul Lewis and Sam Dutton (Google Web Developers, web.dev).
Official source: https://web.dev/articles/stick-to-compositor-only-properties-and-manage-layer-count

Techniques for isolating animation execution to GPU compositor threads.

Inspection methodology:
* Open the Performance tab and record interaction traces. Confirm animation activity runs strictly on the Compositor thread without triggering Main thread Layout or Paint operations.
* Open the Layers panel (`Cmd + Shift + P` then type `Show Layers`) to inspect visual layer promotions.
* Open the Rendering drawer and activate Paint Flashing. Green rectangle flashes during animation indicate repainting that prevents full GPU acceleration.
* Restrict continuous animation to `transform` and `opacity`. Avoid animating box model dimensions, margins, or dynamic blur filters.

---

## Motion Execution Steps

1. Capture live animation sequences using the Chrome DevTools Animations drawer.
2. Slow playback to 10 percent and copy cubic-bezier coordinates.
3. Validate that UI utility durations finish within 150ms to 250ms budgets.
4. Verify that smooth scrolling preserves keyboard navigation and page text search.
5. Audit animations with Paint Flashing to verify compositor-only execution.
6. Provide reduced-motion fallbacks for all spatial transitions.
