---
name: build-awwwards-quality-sites
description: Use when building, art-directing, or auditing motion-heavy marketing sites, interactive portfolios, GSAP or Three.js WebGL scenes, and smooth-scroll interfaces.
---

# Build Awwwards-quality sites

Implement cohesive marketing, editorial, portfolio, and landing websites. Treat award benchmarks strictly as technical acceptance bars rather than marketing claims.

## Workflow

Follow these four steps in sequence:

### Step 1. Baseline direction and technical bounds

Inspect reference materials and define architectural boundaries before writing code.

- Read project assets, reference URLs, and existing stylesheets. Extract hierarchy, pacing, color contrast, and motion narrative.
- Generate original layouts, copy, and visual identities. Never copy reference code, clone layouts directly, or trace reference screenshots.
- Select at most one smooth-scroll engine between Lenis and Locomotive Scroll. Never install or run both engines concurrently.
- Formulate a written technical spec before implementation. State the hero focal element, typography scale, palette tokens, smooth-scroll engine, WebGL responsibilities, and asset licensing sources.

**Completion criterion.** A written technical direction specifying typography, palette tokens, motion engine, and asset provenance.

### Step 2. Semantic structure and honest assets

Construct accessible markup and authentic visual components.

- Author complete semantic page layouts with navigation, structured section flows, accessible forms, primary callouts, and footer regions.
- Use genuine photographs for all personnel or testimonial avatars. Reject generic AI headshots, faceless silhouette placeholders, or initials.
- Use transparent PNG cutouts for illustrative imagery. Never generate model-authored SVG illustration blobs, CSS shapes, or canvas drawings.
- Use Solar icons through Iconify for interface controls. Reserve brand SVG marks strictly for authentic integration partners, and omit logo walls when authentic proof does not exist.
- Build resilient fallbacks. Every interactive or visual asset must remain readable and functional when JavaScript, WebGL, or media streams fail to load.

**Completion criterion.** Valid semantic markup rendering complete static content with zero missing assets or unverified proof components.

### Step 3. Motion choreography and WebGL integration

Choreograph section transitions and runtime canvas resources with performance constraints.

- Use GSAP as the primary motion runtime. Bind ScrollTrigger instances directly to the selected smooth-scroll engine.
- Animate visual elements exclusively using transform and opacity. Never animate layout dimensions, padding, or margins.
- Under prefers-reduced-motion, disable smooth-scroll engines and jump scrubbed timelines immediately to their final frames.
- When staggering heading text, retain the unsplit text inside an accessible wrapper for screen readers. Hide split decorative characters from assistive trees using aria-hidden.
- For Three.js canvases, cap the device pixel ratio at 2. Pause rendering loops when the canvas scrolls out of the viewport or when the document becomes hidden via the Page Visibility API.
- Dispose geometries, materials, textures, render targets, and event listeners on component unmount or view transitions.

**Completion criterion.** ScrollTrigger integrates directly with the single smooth-scroll engine, and WebGL render loops pause when offscreen.

### Step 4. Pre-flight verification and audit

Audit the completed interface against quality, accessibility, and performance invariants.

- Execute the production build command and resolve all compilation errors.
- Verify full layout functionality across both desktop and mobile viewports.
- Confirm keyboard navigation order and verify clear focus rings surround interactive controls.
- Confirm that only one smooth-scroll engine runs and that all canvas resources clean up on unmount.
- Verify that the rendered site contains no placeholder text, fake statistics, or unverified claims.

**Completion criterion.** Production build passes with zero errors, clean memory teardown on unmount, and keyboard navigation confirmed.

## Quick audit checklist

Run this check before declaring implementation complete:

| Check | Passing condition |
|---|---|
| Frontmatter | Contains kebab-case name and trigger-only description starting with "Use when" |
| Length | SKILL.md remains concise and well under 250 lines |
| Anti-slop | Zero banned vocabulary, zero em dashes, and colons appear only before lists or tables |
| Scroll engine | Exactly one smooth-scroll engine selected and configured |
| Motion invariants | Transforms and opacity animated exclusively, with reduced motion fallbacks |
| WebGL lifecycle | Render loops pause when offscreen and all WebGL resources dispose on unmount |
| Completion criteria | Every step defines a binary, checkable completion criterion |
