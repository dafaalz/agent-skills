Start your response with:

```
──────────── ⚡ OVERDRIVE ─────────────
》》》 Entering overdrive mode...
```

Push an interface past conventional limits. This isn't just about visual effects. It's about using the full power of the browser to make any part of an interface feel extraordinary: a table that handles a million rows, a dialog that morphs from its trigger, a form that validates in real-time with streaming feedback, a page transition that feels cinematic.

Context decides what "extraordinary" means. A particle system on a creative portfolio is impressive. The same particle system on a settings page is embarrassing. But a settings page with instant optimistic saves and animated state transitions? That's extraordinary too. Understand the project's personality and goals before deciding what's appropriate.

### Propose Before Building

This command has the highest potential to misfire. Do NOT jump straight into implementation. You MUST:

1. **Think through 2-3 different directions**: consider different techniques, levels of ambition, and aesthetic approaches. For each direction, briefly describe what the result would look and feel like.
2. **Get the user's pick before writing any code.** Ask with Codex's structured user-input/question tool when available, or directly in chat if it is not, and wait for the answer before continuing. Carry each direction's description and its trade-offs (browser support, performance cost, complexity) inside the option itself, so the user is choosing between things they can read. A structured question blocks the message it rides in until the user answers, so directions written alongside the question stay invisible while the user is being asked to choose between them.
3. Only proceed with the direction the user confirms.

Skipping this step risks building something embarrassing that needs to be thrown away.

### Verify in the Browser

Ambitious effects rarely work on the first try, so verify them in the browser rather than from code: an effect that technically runs can still stutter, ease wrong, or land on the wrong frame. Aim the checks at timing, easing, and smoothness, batch the fixes between looks, and keep refining until the effect is extraordinary.

---

## Assess What "Extraordinary" Means Here

The right kind of technical ambition depends entirely on what you're working with. Before choosing a technique, ask: **what would make a user of THIS specific interface say "wow, that's nice"?**

### For visual/marketing surfaces
Pages, hero sections, landing pages, portfolios: the "wow" is often sensory: a scroll-driven reveal, a shader background, a cinematic page transition, generative art that responds to the cursor.

### For functional UI
Tables, forms, dialogs, navigation: the "wow" is in how it FEELS: a dialog that morphs from the button that triggered it via View Transitions, a data table that renders 100k rows at 60fps via virtual scrolling, a form with streaming validation that feels instant, drag-and-drop with spring physics.

### For performance-critical UI
The "wow" is invisible but felt: a search that filters 50k items without a flicker, a complex form that never blocks the main thread, an image editor that processes in near-real-time. The interface just never hesitates.

### For data-heavy interfaces
Charts and dashboards: the "wow" is in fluidity: GPU-accelerated rendering via Canvas/WebGL for massive datasets, animated transitions between data states, force-directed graph layouts that settle naturally.

**The common thread**: something about the implementation goes beyond what users expect from a web interface. The technique serves the experience, not the other way around.

## The Toolkit

Organized by what you're trying to achieve, not by technology name.

### Make transitions feel cinematic
- **View Transitions API** (same-document: all browsers; cross-document: no Firefox): shared element morphing between states. A list item expanding into a detail page. A button morphing into a dialog. This is the closest thing to native FLIP animations.
- **`@starting-style`** (all browsers): animate elements from `display: none` to visible with CSS only, including entry keyframes
- **Spring physics**: natural motion with mass, tension, and damping instead of cubic-bezier. Libraries: motion (formerly Framer Motion), GSAP, or roll your own spring solver.

### Tie animation to scroll position
- **Scroll-driven animations** (`animation-timeline: scroll()`): CSS-only, no JS. Parallax, progress bars, reveal sequences all driven by scroll position. (Chrome/Edge/Safari; Firefox: flag only; always provide a static fallback)

### Render beyond CSS
- **WebGL** (all browsers): shader effects, post-processing, particle systems. Libraries: Three.js, OGL (lightweight), regl. Use for effects CSS can't express.
- **WebGPU** (Chrome/Edge; Safari 26+; Firefox on Windows/macOS; flag only on Firefox Linux/Android): next-gen GPU compute, more powerful than WebGL. Always fall back to WebGL2.
- **Canvas 2D / OffscreenCanvas**: custom rendering, pixel manipulation, or moving heavy rendering off the main thread entirely via Web Workers + OffscreenCanvas.
- **SVG filter chains**: displacement maps, turbulence, morphology for organic distortion effects. CSS-animatable.

### Make data feel alive
- **Virtual scrolling**: render only visible rows for tables/lists with tens of thousands of items. No library required for simple cases; TanStack Virtual for complex ones.
- **GPU-accelerated charts**: Canvas or WebGL-rendered data visualization for datasets too large for SVG/DOM. Libraries: deck.gl, regl-based custom renderers.
- **Animated data transitions**: morph between chart states rather than replacing. D3's `transition()` or View Transitions for DOM-based charts.

### Animate complex properties
- **`@property`** (all browsers): register custom CSS properties with types, enabling animation of gradients, colors, and complex values that CSS can't normally interpolate.
- **Web Animations API** (all browsers): JavaScript-driven animations with the performance of CSS. Composable, cancellable, reversible. The foundation for complex choreography.

### Push performance boundaries
- **Web Workers**: move computation off the main thread. Heavy data processing, image manipulation, search indexing: anything that would cause jank.
- **OffscreenCanvas**: render in a Worker thread. The main thread stays free while complex visuals render in the background.
- **WASM**: near-native performance for computation-heavy features. Image processing, physics simulations, codecs.

### Interact with the device
- **Web Audio API**: spatial audio, audio-reactive visualizations, sonic feedback. Requires user gesture to start.
- **Device APIs**: orientation, ambient light, geolocation. Use sparingly and always with user permission.

**NOTE**: This command is about enhancing how an interface FEELS, not changing what a product DOES. Adding real-time collaboration, offline support, or new backend capabilities are product decisions, not UI enhancements. Focus on making existing features feel extraordinary.

## Implement with Discipline

### Progressive enhancement is non-negotiable

Every technique must degrade gracefully. The experience without the enhancement must still be good.

```css
@supports (animation-timeline: scroll()) {
  .hero { animation-timeline: scroll(); }
}
```

```javascript
if ('gpu' in navigator) { /* WebGPU */ }
else if (canvas.getContext('webgl2')) { /* WebGL2 fallback */ }
/* CSS-only fallback must still look good */
```

### Performance rules

- Target 60fps. If dropping below 50, simplify.
- Lazy-initialize heavy resources (WebGL contexts, WASM modules) only when near viewport.
- Pause off-screen rendering. Kill what you can't see.
- Test on real mid-range devices, not just your development machine.

### Polish is the difference

The gap between "cool" and "extraordinary" is in the last 20% of refinement: the easing curve on a spring animation, the timing offset in a staggered reveal, the subtle secondary motion that makes a transition feel physical. Don't ship the first version that works; ship the version that feels inevitable.

**NEVER**:
- Ship effects that cause jank on mid-range devices
- Use bleeding-edge APIs without a functional fallback
- Add sound without explicit user opt-in
- Use technical ambition to mask weak design fundamentals; fix those first with other commands
- Layer multiple competing extraordinary moments. Focus creates impact, excess creates noise

## Verify the Result

- **The wow test**: Show it to someone who hasn't seen it. Do they react?
- **The removal test**: Take it away. Does the experience feel diminished, or does nobody notice?
- **The device test**: Run it on a phone, a tablet, a Chromebook. Still smooth?
- **The context test**: Does this make sense for THIS brand and audience?

"Technically extraordinary" isn't about using the newest API. It's about making an interface do something users didn't think a website could do.
# Visualize: Direction Comps & Asset Production

Load this from the new-surface workflow on a comp-led build, when image generation is available (a harness-native tool or the API fallback `impeccable context` reports). A code-led contract skips this file by design, not by drift; do not load it then. PRODUCT.md is a precondition; DESIGN.md is one only on an established world, since a new or replacement world writes it at the finish. The MODE RULES block concept-seed printed for this surface (COMPS) governs these comps together with this file and wins where they conflict; with no roll this session, read the mode's file named in new-work.md. New-work has already resolved the visual world; this file must not reopen it. A surface-scope structure round that already put three visualized cards before the user (new-work.md, established world) has discharged this round: the locked card's comp is the approved comp, so record the approval and continue at After approval; generate nothing new.

A probe tests composition, narrative, hierarchy, density, focal moment, signature use, and image requirements. It is not a second identity workshop. Keep the world's palette, typography direction, material language, component character, imagery stance, and motion grammar fixed: DESIGN.md's on an established world, the chosen direction's on a new one.

## Generate three compositional options

The comp round runs inside the build's phase state: `impeccable build-phase start --direction <seed reference>` has already run (with `--decision-comp <path>` when the chosen card has a decision comp) and its `comps` phase is open before the first comp is generated; a comp rendered before that sits outside the state, and a session resumed from that point has no phases to follow. `impeccable generate-image` refuses to write under `.impeccable/mocks/` until start has run; a harness-native image tool is bound by the same order.

Render three distinct high-fidelity north-star comps of the requested surface, saved under `.impeccable/mocks/` so they survive the session. When the chosen card has a decision comp, it is option one: it stays at its path under `.impeccable/mocks/decision/`, where the gate counts it through `--decision-comp`, and is never regenerated; render the other two. Comp at the surface's own viewport: portrait at device size for a native app or mobile-first surface, desktop landscape otherwise; a phone screen comped landscape misstates the composition before anything is built against it. Comps are the build thread's own work, never delegated: the thread that writes the prompts holds the direction's full context and has seen every comp when the build starts. Open every image by its workspace-relative path; sandboxed viewers reject absolute paths, and everything under the project root has a relative one. Base the comps on real content and the surface concepts already developed with the user. On an established world, anchor every comp on the real identity: capture a screenshot of a representative existing page and pass it as a reference image (the harness image tool's input image, or `impeccable generate-image --ref`); the prompt leads with the new surface's structure while the reference carries palette, type, and component character, because DESIGN.md words alone drift where a pixel reference does not. Name what the reference contributes and what it must not: chrome, palette, type, and component character carry over; the reference page's own content does not, and a banner, hero, or card lifted verbatim is the reference leaking, not fidelity. Three is the number: one comp invites rubber-stamping; the spread between three surfaces the composition worth building. The chosen card's decision comp is the first of the three: it already renders this direction at full fidelity under this discipline, so generate two more that vary what the first held fixed, from the direction in words rather than with the first comp as an input image (a reference image anchors the layout, and three comps collapse into one composition). How comps two and three vary from the first is the mode's call, in its COMPS rules. A variant that simplifies the first into a tidier version of itself adds no choice to the round. Send all three to the approval point together. Only a round arriving with no decision comp (a degraded roll, an identity-mode page, a direction pinned without the decision round) renders all three here.

- A comp prompt is short, 150 to 300 words, and carries only what the image model cannot know. The model draws what the prompt names and stops deciding whatever the prompt pins down, so a prompt that specifies everything gets back a template. Open with the surface: the kind of screen it is (a desktop web app, a documentation page, a landing page, a native app screen at its device viewport) for the product, by name, rendered edge to edge with crisp readable text and no browser window, device, or desk around it. Then the product and the visitor's job in plain words, with the real content that answers it: names, numbers with units, the offer or the state, any claim at its honest certainty, and the next action by name. Then what leads this comp, its product concept (summary-led, timeline-led, offer-led, reference-led), and the parts the screen holds in reading order, a phrase each. Then the frame in one line: the product's mark and name, its navigation, its utility controls, and the far edge, so the comp is a finished screen, never a fragment; a page with no navigation says so instead of inventing one. Leave sizes, positions, colours, and component styling out, except a colour, typeface, or brand element the user pinned: that is content, so state it. Self-check every render: if it could hang as a poster, or reads as a photograph with some text on it, it is not a comp; regenerate.
- The look comes from the world, and from a picture wherever one exists. An established world has the screenshot reference above: it carries the look, so the prompt adds one sentence on what the reference contributes and nothing more about style. A catalog world has card images: attach its board and hero as reference images (the NEXT line names them; `impeccable generate-image --ref <board> --ref <hero>`, or the harness image tool's input images) and write one sentence, that the references are style inspiration adapted into a real working product, their layout and content not to be copied. Describing the style as well overrides the picture. A direction with no card images carries its look in two to four sentences of concrete visual law: the ground and main colours with what each does, the type voices, and the one signature that makes it recognisable. No path lists colours past the main few or describes components one by one.
- The subject must be in it. Before accepting a render, point at the subject: a render that depicts the world and nothing of the subject fails however faithful its atmosphere, and the deletion usually rides in on an exclusion list. Regenerate with the subject's content named.
- Judge a comp as the shipped screen: the visitor's job must be readable from the image alone. Name the surface's mode from the render with no caption; a render whose mode cannot be read back is art direction without a surface. Regenerate with the visitor's job as the prompt's spine.
- Commitment is depth, not performance spread across regions. The world enters through one dominant move plus the material, type, and spacing that support it; the remaining regions hold still in that material and keep their content at real reading size. A second element competing with the lead at the same scale is the comp shouting: regenerate keeping the strongest move and quieting the rest. Busy is louder, not bolder.
- When the user shortlisted multiple concepts, spread the three across them.
- When one direction is committed, vary the structural uncertainty an image can resolve: what leads the screen, topology, sequence, density, hierarchy, focal composition, or interaction framing.
- Show enough beyond the opening moment to prove the concept can govern the whole surface.
- Do not generate a palette artifact, ask new atmosphere questions, introduce a different type voice, or invent a new motif. If the committed world cannot support the concept, return to the concept shortlist rather than changing the world.

Each comp is a direction test, not a screenshot specification. Core UI text, responsive behavior, accessibility, semantics, and interaction states remain implementation responsibilities.

## One approval point

Show the three together on the decision page (`impeccable serve-question`, one option per comp with the comp as its hero), or in the harness only when it renders images inline; a text-only surface does not count as display. Ask what should carry forward, what feels false to the world, and whether the selected concept should be approved, combined, revised, or rejected. Then stop and wait. A structured simulated user counts as attended and receives the same question.

Do not begin code until the user approves a direction or explicitly delegates the choice. If they delegate, choose using the task brief, PRODUCT.md, and DESIGN.md, and state the evidence. Approval refines the task concept; it does not modify DESIGN.md.

This approval point has no substitute and no skip condition. When the structured question tool errors, fall back to the decision page; only after both fail may you treat the choice as delegated, and a delegated pick is recorded exactly as an approval is and disclosed in your first reply, not your last. The finish reviewer treats comp-round comps with no recorded approval as a material finding; decision comps under `.impeccable/mocks/decision/` are the direction round's hand, not comp-round output, and imply no approval on their own.

After approval, record the choice where tools can find it: the approved comp's path goes in the surface brief, and its prompt sidecar (the image's full file name plus `.json`: `a.png` gets `a.png.json`) gains `"approved": true` (every comp generated through `impeccable generate-image` has one; create it if a native tool didn't). The sidecar travels with the mocks folder, so the approval survives sessions and machines that never see the brief, and it is what `impeccable build-phase advance` reads to close the comps phase. Summarize the composition and the parts of the comp that must not be literalized, return to new-work.md, record the direction contract from the approved concept, and build.

## After approval: the comp becomes a spec

The approved comp is a north star for translation into semantic, responsive, accessible code, never a license to recompose: keeping the palette and mood while redrawing the topology is a second art direction. Do not rasterize core UI text or controls. Do not substitute a different visual driver after approval without asking.

What the comp shows is measured, not remembered. new-work.md section 6 runs the build as phases (`impeccable build-phase`): the spec phase turns the comp into region boxes with sampled palettes (`impeccable comp-spec`), and the medium of every region follows from what the pixels are, never from what feels buildable: a figure, a product object, machinery, any illustration with perspective, shading, or drawing skill in it, and any texture by name (woven cloth, paper grain, fabric, leather, brushed metal) is a `plate` / `image` / `texture` region and ships as a raster; text, controls, chrome, diagrams with countable elements, flat shape systems, and anything that must move, scale, or respond are semantic. Writing "CSS" for a sculpted panel's finish, or a many-vertex `clip-path` for a torn edge, is the quiet deletion of the approved design; the detector's organic-clip-path and buried-raster rules and the hero gate's region scores catch it. Dropping an image-native region is a scope decision the user makes at the approval point, never a silent flattening after it. Generated imagery is a material, not a claim: evidence rules bind assertions, specs, testimonials, and photographs presented as real, never render fidelity.

## Plates and provenance

Every raster region's plate is produced in the plates phase, before any page code, by the shipped asset producer or in the current thread (use `impeccable comp-spec --crop <id>` and save `impeccable comp-spec --plate-prompt <id>` to a prompt file; pass the crop and prompt to the harness image tool, or use `impeccable generate-image --ref <crop.png> --prompt-file <prompt.txt> --out <plate.png> --size <WxH> --quality high`). For isolated cutouts, add `--background transparent` to both the plate-prompt and API generation commands; use native PNG alpha and preserve white paint and clear gaps. Use `--background opaque` for full-frame imagery. Create output directories first and inspect alpha on light and dark grounds. Generation context is part of the asset: after generating any image with any tool, run `.agents/skills/impeccable/scripts/impeccable embed-prompt <image> --prompt "<prompt>"` with the exact string the tool received (`impeccable generate-image` does this itself), so the intent lives inside the file; `--read` recovers it, `--scan <dir>` lists rasters still missing one. The embedded prompt plus the region's row in the spec is the raster's **provenance**, and every raster the artifact references carries it; a sourced, stock, or pre-existing raster embeds its origin instead. A raster created or replaced later, in a fix batch or a reviewer's rebuild, is produced the same way; a raster a fix abandons is deleted in the same batch.

Convert images with a converter `impeccable context` reported at boot (the IMAGE_TOOLS line); probe only when it reported none, at most once per session, never per image.

Return to the new-surface workflow for the direction contract, the phased build, and the finishing pass.
