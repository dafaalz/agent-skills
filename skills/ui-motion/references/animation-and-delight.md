> **Additional context needed**: performance constraints.

Use motion to explain state, relationship, and hierarchy, or to create one authored moment the surface has earned. Decoration without purpose is animation debt.

---

## Visitor mode

- **Persuade + Experience:** motion may carry the voice. Prefer one rehearsed focal sequence to repeated section reveals.
- **Operate + Read:** motion serves feedback, state, and continuity. Keep routine transitions fast and do not make users wait through page-load choreography.
- **Native (`ios` / `android` / `adaptive`):** follow the Motion section of native iOS or Android guidelines, including the platform's Reduce Motion behavior. Do not apply the web tooling below.

## Find the job

Inspect the existing motion language, interaction states, target devices, and performance budget. Find only the places where motion would:

- acknowledge an action;
- make a state change or spatial relationship legible;
- preserve continuity through navigation or layout change;
- direct attention at a meaningful moment;
- embody the selected visual world.

Ask only when a material constraint cannot be inferred. Do not animate a static area merely because it exists.

## Set the motion thesis

Write a short plan before implementation:

- **Focal moment:** the one sequence or interaction that deserves authorship, if any.
- **Continuity:** the state, layout, or navigation changes that need explanation.
- **Feedback:** the controls and outcomes that need acknowledgment.
- **Budget:** which effects may be expensive and how often they run.

The focal moment must come from this product and surface concept. A generic fade-and-rise, hover lift, parallax layer, or scroll reveal is not a thesis.

## Choose material by meaning

Transform and opacity are reliable foundations, not the entire palette. Choose properties for what the transition communicates:

- **Continuity and relationship:** shared-element motion, FLIP-style transforms, view transitions, or deliberate spatial movement.
- **Focus and depth:** bounded blur, filter, backdrop, light, or shadow changes.
- **Reveal and composition:** masks, clip paths, cropping, or controlled occlusion.
- **Material and energy:** color, gradient position, texture, distortion, or shader effects when the world and runtime support them.
- **State and feedback:** the smallest change that makes cause and result unmistakable.

Do not stack techniques for spectacle. One strong material idea, carried through the focal sequence and quiet supporting states, is usually enough.

Sibling stagger is appropriate when a list appears as a list. Cap the total delay, and never reinterpret every scrolled section as a staggered list.

## Timing and easing

Timing should express distance and consequence:

| Duration | Typical use |
|---|---|
| 100–150 ms | immediate feedback |
| 150–300 ms | routine state change |
| 300–500 ms | layout, overlay, or view transition |
| 500–800 ms | a deliberately authored focal entrance |

Exit faster than entrance. Use natural deceleration such as `cubic-bezier(0.16, 1, 0.3, 1)` for confident arrivals; do not use bounce or elastic curves by reflex. Long feedback feels like latency.

## Implement to the runtime

- Use CSS transitions and keyframes for declarative state and bounded sequences.
- Use Web Animations API or the project's existing motion library for interruption, sequencing, and dynamic values.
- Use View Transitions or shared-element techniques when continuity across states is the point.
- Use scroll-driven motion only when the scroll relationship itself carries meaning, with a robust fallback.
- Do not add a dependency for an effect the existing stack can express cleanly.

Keep content visible in the default state so failed scripts do not hide the page. Avoid casually animating layout-driving properties such as `width`, `height`, `top`, `left`, and margins; use FLIP, transforms, or grid techniques when appropriate. Bound blur, filter, shadow, canvas, and shader work to isolated regions. Apply `will-change` only during known animation. Measure on target viewports and devices rather than assuming transform means fast.

## Accessibility and control

Respect autoplay and sound preferences. Any nonessential loop must stop when offscreen or hidden.

Every web animation needs a `prefers-reduced-motion` path with an intentional alternative. Remove or reduce spatial movement while preserving opacity, color, and state transitions that carry meaning. Reduced motion means fewer and gentler animations, not disabling all motion; feedback that confirms an action should remain legible.

## Verify

- The focal motion is specific to the selected world and surface.
- Every supporting animation explains feedback, state, or relationship.
- Interruption and repeated use behave correctly.
- Desktop, mobile, and keyboard paths remain usable.
- The `prefers-reduced-motion` path reduces movement without erasing meaningful feedback or state changes.
- Expensive effects stay smooth on the target device.
- Removing an animation would lose meaning or authored character, not merely decoration.

When motion earns its place, hand off to `$impeccable polish` for the final pass.
> **Additional context needed**: the brand's emotional range.

Make the experience memorable at moments that earn it. Delight is not a layer of generic whimsy; it is product character revealed through a useful interaction, a humane response, or an unexpectedly considered detail.

---

## Visitor mode

- **Persuade + Experience:** personality may run through voice, composition, motion, and discovery, provided the artifact remains the focus.
- **Operate + Read:** concentrate delight at meaningful moments such as first use, completion, recovery, or mastery. Reliability carries everything else.

## Find the opportunity

Inspect the target, DESIGN.md, product voice, repeated-use frequency, and emotional context. Look for:

- effort worth acknowledging;
- waiting that can become informative;
- an empty or first-use state that can orient;
- an error or recovery moment that needs empathy;
- an interaction whose physical or verbal response could express the brand;
- a useful capability people might enjoy discovering.

Do not manufacture a celebration for an ordinary click. Ask only when the brand's emotional range or the stakes cannot be inferred.

## Define one delight thesis

State in one sentence what the user should feel and why that feeling belongs to this product. Then choose the smallest system that can deliver it:

- a distinctive response to a meaningful action;
- product-specific language that clarifies while carrying voice;
- an interaction or transition with a recognizable material behavior;
- an illustration, sound, haptic, or environmental detail grounded in the product world;
- a discovery reward that reveals real utility.

Derive the treatment from product mechanism and visual world, not a stock catalog.

## Build for the emotional moment

- **Success:** match the response to the effort and consequence. Major milestones can expand; routine saves should simply feel certain.
- **Waiting:** show truthful progress, useful context, or product-specific activity. Never fake work or delay completion to stage a flourish.
- **Empty and first use:** make the next action clear before adding personality.
- **Error and recovery:** lead with the problem and recovery. Warmth may reduce stress; jokes must not trivialize loss, money, privacy, or blocked work.
- **Repeated interaction:** keep the response satisfying after the hundredth use. Variation is useful only when it remains coherent and predictable enough to trust.
- **Discovery:** reward curiosity without hiding required functionality.

Copy must use the product's language. Generic whimsy is worse than neutral clarity.

## Protect the experience

Delight must not:

- delay, block, or obscure the primary task;
- override platform conventions or accessibility;
- add unrequested factual claims;
- play sound without consent or ignore mute settings;
- become mandatory, unskippable, or exhausting on repeat;
- add a dependency or asset cost disproportionate to the moment.

For authored motion, follow the animation principles above. Respect screen readers, keyboard use, touch, localization, and cultural context. Nonessential loops stop when hidden. Make celebration intensity proportional to frequency and consequence.

## Verify

- The moment is specific enough that a neighboring product could not use it unchanged.
- It improves comprehension, confidence, motivation, or emotional recovery.
- The interface remains fast and obvious without the flourish.
- Repetition does not turn charm into friction.
- Muted, keyboard, touch, and localized paths work.
- The result feels like the selected world, not a generic “delight” treatment.

When the personality feels earned, hand off to `$impeccable polish` for the final pass.
