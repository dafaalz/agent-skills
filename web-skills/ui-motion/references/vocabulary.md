# Motion vocabulary and concept mapping

Reverse lookup glossary translating informal sensory descriptions into standard technical terms and implementation patterns.

## Concept mapping table

Use this table to map user descriptions to concrete animation patterns:

| User description | Technical term | Definition | Recommended implementation |
| --- | --- | --- | --- |
| Panel or menu grows out of the clicked button | Origin-aware animation | The entering surface expands from the trigger coordinates rather than viewport center | Set `transform-origin: var(--transform-origin)` supplied by headless primitives |
| Scroll resists and snaps back when pulled past boundaries | Rubber-banding | Elastic resistance increases progressively beyond bounds before settling via springs | Calculate displacement with Apple rubber band formula `(x * d * 0.55) / (d + 0.55 * Math.abs(x))` |
| Cards or list items cascade into view one by one | Stagger | Sequential entrance delays across sibling elements | Apply 30ms to 80ms increments via `animation-delay` or Motion stagger helpers |
| Tab indicator changes background and text color cleanly | Clip path transition | A duplicate active styled layer is revealed through an animated rectangular boundary | Duplicate tab list, apply `clip-path: inset()` to the top copy, transition bounds |
| Dynamic Island or card changing dimensions smoothly | Morph or layout animation | Element preserves spatial identity while changing geometry across states | Use Motion layout props or Web Animations API with presentation transforms |
| Quick button recoil on press | Tactile press feedback | Interactive target scales down slightly on active touch | Apply `transform: scale(0.97)` on `:active` pseudo-class with 120ms to 160ms ease-out |
| Long press fill before executing destructive action | Hold to confirm | Deliberate linear progress animation paired with fast snap back upon premature release | Animate `clip-path` over 2s linear on press, snap back in 200ms ease-out on release |
| Element follows finger and flies away on quick flick | Momentum dismissal | Drag gesture resolves based on release velocity rather than fixed distance thresholds | Calculate `Math.abs(distance) / elapsedTime` and trigger exit when exceeding 0.11 px/ms |
| Crossfade between two texts looks messy or doubled | Momentary blur mask | Brief filter application during intermediate states to blend mismatched glyphs | Apply `filter: blur(2px)` and 0.7 opacity for 180ms during the swap |
| Smooth reveal of image or container on viewport entry | Scroll reveal | Content unmasks once as it enters screen viewports | Animate `clip-path: inset(0 0 100% 0)` to `inset(0 0 0 0)` once via IntersectionObserver |
| Elements snap between values without bouncing | Critically damped spring | Physical spring settling cleanly at the target endpoint without oscillating | Spring configuration with damping ratio `1.0` and response `0.3s` to `0.4s` |
| Bouncy settling on thrown objects | Under-damped spring | Physical spring exhibiting controlled overshoot after momentum handoffs | Spring configuration with damping ratio `0.8` and response `0.3s` to `0.4s` |
| Snappy task motion in enterprise dashboards | Productive motion | Minimal duration transition designed for high-frequency utility | Use 70ms to 240ms duration with asymmetric ease-out curves |
| Fluid brand transition on landing pages or modals | Expressive motion | Stylized animation guiding user attention during significant state changes | Use 350ms to 500ms duration with emphasized curves or controlled spring bounce |
| Desktop title bar dragging follows cursor with zero lag | Non-client drag region | OS window manager handles hit-testing directly without JavaScript IPC | Apply `-webkit-app-region: drag` and exclude buttons with `no-drag` |
| Toolbar tooltips open instantly after the first one is open | Warm-start tooltip | Skip delay and entrance transition when cursor travels across sibling triggers | Set `transition-duration: 0ms` while tooltip group has an active target |
| Gesture updates stay 120fps during heavy JS parsing | UI thread isolation | Touch callbacks and transforms calculate directly on platform UI thread | Use Reanimated 4 worklets, Compose graphicsLayer lambdas, or compositor transforms |
| Screen movement causes dizziness or vestibular discomfort | Optical flow conflict | Large-area motion triggers mismatch between retinal signals and inner ear | Replace 3D scaling and parallax scrolling with 2D opacity crossfades |

---

## Disambiguation guide

When multiple terms appear similar, use these structural distinctions:

### Clip path versus CSS mask

- **Clip path.** Produces sharp vector boundaries that clip raster and text content. Highly performant on the GPU compositor thread. Ideal for tabs, hold-to-confirm progress fills, and rectangular reveals.
- **CSS mask.** Utilizes alpha gradients or image assets to create soft, feathered transparency transitions. More demanding on GPU rasterization passes.

### Pop in versus Bounce

- **Pop in.** A quick scale entrance starting from `scale(0.95)` with zero opacity, settling with minimal or zero overshoot.
- **Bounce.** An under-damped spring oscillation that repeatedly crosses target boundaries. Reserved for playful brand moments or momentum flicks. Disqualified from standard enterprise forms and data grids.

### Shared element transition versus Layout animation

- **Shared element transition.** Animates an element across distinct pages or routes, creating visual continuity between thumbnail and full screen detail views.
- **Layout animation.** Animates positional and dimensional adjustments within a single view when DOM sibling nodes insert, remove, or reorder.

### Productive motion versus Expressive motion

- **Productive motion.** Applied to everyday task workflows, dropdowns, buttons, toggles, and data tables. Keeps durations under 240ms, avoids overshoot, and prioritizes efficiency.
- **Expressive motion.** Applied to landmark transitions, milestone celebrations, modal dialogues, and onboarding. Uses durations between 300ms and 500ms with spatial trajectory and subtle spring dynamics.

### Off-Main-Thread Animation (OMTA) versus Main-thread animation

- **OMTA.** Animations running exclusively on the browser GPU compositor thread (transforms and opacity). Immune to JavaScript thread freezes or heavy DOM rendering.
- **Main-thread animation.** Animations modifying layout properties (`width`, `height`, `top`, `left`, `margin`) or driven by JavaScript intervals. Vulnerable to dropped frames under CPU workload.

---

## Verification checklist

When communicating animation concepts, verify against these criteria:

| Check | Passing condition |
| --- | --- |
| Grounding | Every informal term maps to a concrete CSS property, WAAPI call, or Motion parameter |
| Restraint | Decorative terms are gated against the frequency table before recommending code |
| Clarity | Explanations distinguish between hardware-accelerated compositor properties and layout-affecting properties |
