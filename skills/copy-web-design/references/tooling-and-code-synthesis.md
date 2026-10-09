# Tooling, Automated Extraction, and Modern Code Synthesis

Technical manual for automated DOM scraping, SVG vector sanitization, Tailwind CSS compilation, accessibility reconstruction, and Core Web Vitals performance validation.

## Automated Extraction Pipelines

Translating inspected web interfaces into production code requires automated tooling to capture computed styles, sanitize vector assets, restore accessibility landmarks, and compile clean components.

The following eight authoritative sources define extraction tooling and code synthesis:

### 1. Chrome DevTools Protocol DOMSnapshot and Accessibility Domains
Author: Chrome DevTools Team (The Chromium Authors).
Official source: https://chromedevtools.github.io/devtools-protocol/tot/DOMSnapshot/

Enables headless browsers to capture flattened layout trees, computed styles, and accessibility trees in a single programmatic call.

Workflow:
* Launch Playwright with a CDP session (`page.context().newCDPSession()`).
* Execute `DOMSnapshot.captureSnapshot` with `includeDOMRects: true`, `includePaintOrder: true`, and a whitelist of computed properties (`display`, `flex-direction`, `grid-template-columns`, `color`, `background-color`, `font-family`, `padding`, `margin`, `border-radius`).
* Simultaneously call `Accessibility.getFullAXTree` to extract computed roles, states, and accessible names directly from the browser accessibility tree.
* Map flat snapshot records back to hierarchical tree models using `backendNodeId` child relationships.

### 2. Evaluating JavaScript and Accessibility Testing Guide
Author: Microsoft Playwright Team.
Official source: https://playwright.dev/docs/evaluating

Guides headless browser execution for DOM traversal and interaction emulation.

Workflow:
* Emulate target viewports (such as 390px mobile and 1440px desktop).
* Await network idle with `page.waitForLoadState('networkidle')`.
* Execute in-page traversal scripts in a single batch using `page.evaluate()` to harvest computed styles without round-trip serialization overhead.
* Capture snapshot states using `page.accessibility.snapshot()`.

### 3. SingleFile Core DOM Serialization Engine Architecture
Author: Gildas Lormeau.
Official source: https://github.com/gildas-lormeau/SingleFile

Freezes live DOM states into deterministic visual archives.

Workflow:
* Traverse stylesheets, `@import` targets, and font declarations in the live DOM.
* Download binary assets and inline them as Base64 data URIs.
* Strip tracking scripts and analytics tags to preserve layout stability without runtime interference.
* Unpack inline Base64 data URIs into structured project asset directories (`public/assets/images`, `public/assets/fonts`) during component synthesis.

### 4. Essential Image Optimization and Responsive Delivery Guide
Author: Addy Osmani (Google Chrome Team).
Official source: https://images.guide/

Techniques for modern image encoding, responsive distribution, and Core Web Vitals optimization.

Workflow:
* Detect `<img>`, `<picture>`, and CSS background images in extracted DOM trees.
* Process master images through Sharp to output AVIF and WebP formats.
* Generate Low Quality Image Placeholders (LQIP) or 16-pixel BlurHash strings.
* Target Next.js `next/image` with `placeholder="blur"` and assign `priority` to the Largest Contentful Paint (LCP) hero candidate.
* For vanilla HTML outputs, use semantic `<picture>` tags with `<source type="image/avif">` and `<source type="image/webp">` fallbacks.

### 5. DOMPurify Security Engine and SVGO Specification
Authors: Mario Heiderich (Cure53) and SVGO Community.
Official source: https://github.com/cure53/DOMPurify

Sanitizes raw SVG vectors to prevent XSS injection attacks and optimizes vector paths.

Workflow:
* Extract inline SVG strings and `<symbol>` definitions from DOM snapshots.
* Sanitize SVG payloads with DOMPurify using profile `{ svg: true, svgFilters: true }` to strip script tags, foreignObjects, and inline event handlers (`onload`, `onclick`).
* Run SVGO to remove editor metadata, normalize `viewBox` coordinates, and clean path definitions.
* Replace hardcoded `fill` and `stroke` hex attributes with `currentColor` so icons inherit CSS color rules dynamically.

### 6. Tailwind CSS Architecture and Utility Compilation Spec
Author: Adam Wathan (Tailwind Labs).
Official source: https://tailwindcss.com/docs/styling-with-utility-classes

Compiles computed CSS properties into structured utility classes.

Workflow:
* Parse computed CSS property declarations into abstract syntax trees using PostCSS.
* Deconstruct shorthand properties into atomic declarations (such as splitting `padding: 12px 16px` into individual edges).
* Map absolute pixel metrics to standard Tailwind spacing and font scales (16px becomes `p-4`, 8px becomes `p-2`).
* Use arbitrary utility values (`p-[13px]`) only when custom values deviate beyond a 1px tolerance from standard theme scales.
* Deduplicate utility class collisions using `clsx` and `tailwind-merge` in React environments.

### 7. Google Chrome Web Vitals and Lighthouse Architecture
Authors: Philip Walton and Addy Osmani (Google Chrome Team).
Official source: https://developer.chrome.com/docs/lighthouse/overview/

Quality gates for validating performance, interactivity, and visual stability.

Workflow:
* Run headless Lighthouse audits against synthesized component output.
* Verify Largest Contentful Paint (LCP): load hero images with `<link rel="preload">` or `priority` attributes.
* Verify Interaction to Next Paint (INP): eliminate blocking main thread script tasks and prune DOM tree depths to under 32 levels.
* Verify Cumulative Layout Shift (CLS): enforce explicit `aspect-ratio` containers across all media wrappers.

### 8. WAI-ARIA Authoring Practices Guide (APG)
Author: W3C Web Accessibility Initiative.
Official source: https://www.w3.org/WAI/ARIA/apg/

Standards for keyboard navigation, focus management, and accessible component roles.

Workflow:
* Audit extracted components against Axe-core accessibility rules (`@axe-core/playwright`).
* Replace scraped division buttons with native `<button>` tags or unstyled Radix UI primitives (`@radix-ui/react-dialog`, `@radix-ui/react-dropdown-menu`).
* Reconstruct keyboard navigation: trap focus inside modal dialogs and restore focus to trigger buttons on dismiss.
* Apply visible focus outlines using Tailwind utilities (`focus-visible:ring-2 focus-visible:outline-none`) or native CSS `:focus-visible`.

---

## Dual Code Synthesis Targets

Synthesize extracted designs to one of two target stacks based on project constraints:

### Target A. Modern React Component Stack (Default)
* Framework: Next.js (App Router) or React 19.
* Styling: Tailwind CSS v4 utilizing the `@theme` block for custom design tokens.
* Icons: Lucide React with `currentColor` inheritance.
* Components: Radix UI unstyled primitives for modals, dropdowns, and tabs.
* Media: `next/image` with BlurHash placeholders.

### Target B. Pure Semantic HTML5 and Modern CSS
* Structure: Semantic HTML5 landmark tags (`<header>`, `<nav>`, `<main>`, `<article>`, `<section>`, `<aside>`, `<footer>`).
* Styling: CSS Custom Properties in `:root` with CSS Grid, CSS Subgrid, Flexbox, and `@container` queries.
* Media: Native `<picture>` tags with AVIF and WebP sources, reinforced by CSS `aspect-ratio`.
* JavaScript: Vanilla ES Modules with zero runtime framework dependencies.

### Target C. Standalone Single-File HTML Mirrors
* Script CDN mapping: map dynamic npm dependencies to equivalent public CDN script tags placed in `<head>` before the inline application script.
* DOM coordinate bindings: replace reactive state hooks (`useLayoutEffect`, `useState`) with direct element measurement properties (`offsetLeft`, `offsetTop`, `offsetWidth`, `offsetHeight`) and register dynamic repositioning callbacks to `window.resize`.
* Scroll containment: add `data-lenis-prevent="true"` to dialog elements and call `lenisInstance.stop()` on modal show, followed by `lenisInstance.start()` on modal dismiss.
* Automation safety: avoid running inline shell strings containing unescaped `${...}` JavaScript template expressions. Use quoted heredocs (`python3 - << 'EOF'`) or write standalone script files to prevent shell variable substitution.
* Syntax audit: validate standalone HTML `<script>` contents using `node -e` parsing before declaring task completion.

---

## Synthesis Execution Steps

1. Run the headless CDP scraper or console extractor script to capture DOM snapshots and computed styles.
2. Sanitize all extracted vector SVG graphics through DOMPurify and SVGO.
3. Map absolute computed measurements to design token scales or Tailwind classes.
4. Replace raw div elements with semantic HTML5 tags or Radix UI headless primitives.
5. Run Lighthouse and Axe-core audits to confirm passing Core Web Vitals and accessibility criteria.
