---
name: copy-web-design
description: Use when reverse-engineering, deconstructing, benchmarking, or replicating web designs, design tokens, layout structures, animations, or components from URLs or screenshots.
---

# Copy Web Design

Deterministic runbook for reverse-engineering and replicating web designs while preserving legal boundaries, extracting design tokens, deconstructing layouts, profiling animations, and synthesizing production code.

## Progressive Disclosure

This runbook defines sequential execution steps. Read detailed reference manuals when executing specific phases:
- Legal doctrines, AFC test, trade dress, and clean-room protocol: `references/legal-and-ethics.md`
- OKLCH colors, variable typography, fluid clamp scales, and shadow layering: `references/visual-tokens-and-typography.md`
- Semantic landmarks, CSS Grid, CSS Subgrid, and container queries: `references/layout-and-dom-decomposition.md`
- DevTools animation timelines, easing curves, scroll dynamics, and WebGL: `references/motion-and-microinteractions.md`
- CDP extraction, SVG sanitization, Tailwind compilation, and Core Web Vitals: `references/tooling-and-code-synthesis.md`
- Browser console token extraction helper: `scripts/extract_tokens.js`

## Workflow

Follow these five phases in sequence:

### Phase 1. Legal and Ethical Triage

Verify target eligibility and establish intellectual property boundaries before inspecting code:

1. Confirm public access. Never inspect pages behind authentication walls, paywalls, or encrypted client sessions.
2. Filter protected content. Strip all narrative marketing copy, brand logos, trademarks, and client photography. Replicate only uncopyrightable functional layout wireframes and user interaction flows.
3. Establish clean-room isolation. Document target behavior as an abstract specification. Build implementation code without copying vendor minified bundles.
4. Verify trade dress differentiation. Ensure the target brand identity, unique color trademarks, and logos are replaced with distinct project assets.

Completion criterion. An abstract specification listing wireframe regions, user flows, and placeholder asset requirements with zero vendor text or trade dress elements.

### Phase 2. Visual Tokens and Typography Ingestion

Extract design tokens and typography metrics from the live page:

1. Extract custom properties. Run `scripts/extract_tokens.js` in the browser console to gather declared CSS custom properties.
2. Ingest color systems. Identify primary, neutral, and accent colors. Convert hex values to OKLCH Display P3 definitions. Derive interactive hover and active states using `color-mix()`.
3. Ingest typography scales. Inspect `@font-face` declarations for variable font axes (`wght`, `wdth`, `slnt`, `opsz`). Measure heading font sizes across mobile (320px) and desktop (1280px) viewports to extract modular scale ratios and fluid `clamp()` formulas.
4. Measure spatial rhythm. Determine the base grid multiplier (4px or 8px). Classify padding and gaps into Inset, Squish, Stack, and Inline patterns.
5. Deconstruct elevation shadows. Identify layered umbra and penumbra tiers, applying chromatic tinting from the background color.

Completion criterion. A written design token catalog defining OKLCH colors, variable font rules, fluid clamp formulas, spatial scales, and shadow tiers.

### Phase 3. Structural Layout Decomposition

Deconstruct the DOM tree into semantic landmarks and modern CSS layout primitives:

1. Strip DOM nesting. Discard framework wrapper divisions. Map visual regions to HTML5 landmarks (`<header>`, `<nav>`, `<main>`, `<article>`, `<section>`, `<aside>`, `<footer>`).
2. Construct macro layout. Implement page-level arrangements using CSS Grid with named template areas. Avoid rigid 12-column row wrappers.
3. Align components with Flexbox and Subgrid. Use Flexbox for one-dimensional component alignment. Use CSS Subgrid on card grids to align nested titles and footers across siblings.
4. Implement container queries. Add `container-type: inline-size` to modular components. Define internal responsive variations with `@container` queries rather than global viewport media queries.
5. Eliminate layout shifts. Assign explicit `aspect-ratio` properties to all media elements to guarantee zero Cumulative Layout Shift.

Completion criterion. A semantic HTML5 component skeleton verified in the browser Accessibility Tree with zero layout shift during rendering.

### Phase 4. Motion and Physics Deconstruction

Deconstruct animations, micro-interactions, and scroll dynamics:

1. Profile animation curves. Open Chrome DevTools Animations drawer (`Cmd + Shift + P` then `Show Animations`). Trigger animations, slow playback to 10 percent, and copy four-point cubic-bezier coordinates.
2. Enforce duration budgets. Confirm functional UI transitions complete within 150ms to 250ms. Restrict active button compression to `transform: scale(0.97)` over 100ms to 140ms.
3. Profile scroll architecture. Identify whether scroll dynamics use native CSS scroll-driven animations, Lenis smooth scrolling, or GSAP ScrollTrigger. Verify that page search (`Cmd + F`) and keyboard navigation remain functional.
4. Isolate compositor execution. Run the DevTools Performance panel and enable Paint Flashing. Confirm transitions use only `transform` and `opacity` without triggering main-thread repaints.
5. Provide reduced-motion fallbacks. Ensure every spatial animation falls back to a clean opacity fade when `prefers-reduced-motion: reduce` is active.

Completion criterion. Recorded cubic-bezier values, confirmed compositor-only execution with zero paint flashes, and verified reduced-motion fallbacks.

### Phase 5. Code Synthesis and Quality Gates

Synthesize the final production code into the target framework:

1. Select synthesis target.
   - For Modern React: synthesize to Next.js or React 19, Tailwind CSS v4 `@theme` tokens, Radix UI headless primitives, and `next/image`.
   - For Pure Web: synthesize to semantic HTML5, modern CSS with custom properties and CSS Grid, native `<picture>` tags, and vanilla ES modules.
2. Sanitize vector assets. Process all inline SVGs through DOMPurify and SVGO, replacing fixed fills with `currentColor`.
3. Audit accessibility. Run Axe-core checks. Verify keyboard tab order, modal focus traps, and visible focus rings (`:focus-visible`).
4. Validate performance. Run automated Lighthouse audits. Confirm zero Cumulative Layout Shift, passing Largest Contentful Paint, and low Interaction to Next Paint.

Completion criterion. Working production components passing all Axe-core accessibility checks and Core Web Vitals performance gates.

## Quick Audit Checklist

Run this check before completing any replication task:

| Check | Passing condition |
|---|---|
| Legal bounds | Zero scraped marketing copy, zero proprietary logos, and clean-room isolation verified |
| Token accuracy | Colors converted to OKLCH, typography fluid via clamp, and base grid documented |
| DOM semantics | Converted from divitis to HTML5 landmarks with verified accessibility tree |
| Layout stability | Explicit aspect-ratio on all media elements with zero Cumulative Layout Shift |
| Motion budgets | Durations under 250ms, compositor-only GPU properties, and reduced-motion supported |
| Quality gates | Zero console errors, passing Axe-core accessibility tests, and clean code formatting |
