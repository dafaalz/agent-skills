# Core disciplines

Comprehensive implementation rules for typography, color tokens, layout structures, copy authenticity, and runtime performance in web interfaces.

## 1. Typography system

Construct an intentional typographic hierarchy using high-performance variable fonts and fluid scaling:
- System pairing. Choose one clear heading face and one neutral, highly legible body face from the typography catalog.
- Fluid clamp scaling. Define responsive font sizes using `clamp()` (or Tailwind arbitrary clamp values) for headers rather than jumping abruptly at breakpoint boundaries.
- Prohibited typography. Avoid unconfigured default Inter on greenfield marketing and editorial layouts. When working in an existing codebase that already configures Inter as its brand typography, adopt the existing repository font. Never use generic system serifs like Times New Roman, Georgia, or Garamond on dashboards. Reserve modern editorial serifs exclusively for long-form literary publications. Never accent a single word in a headline with isolated italics, bolding, or colored text. Never apply all-caps styling to general content labels; permit uppercase tracking-[0.06em] strictly on data-table headers, telemetry badges, and kbd hints (11px or under).
- Editorial pull quotes and marginalia. Structure pull quotes using semantic figure and blockquote containers with left accent borders and fluid clamp scaling. Compartmentalize marginalia columns into distinct structured sub-blocks separated by subtle dividers rather than monolithic paragraphs.

## 2. Color token architecture

Anchor layouts to neutral bases with at most one restrained accent color:
- Neutral foundation. Anchor interfaces to Zinc or Slate. Never use pure black (#000000); use Zinc-950 or Charcoal Ink (#18181B) for deep surfaces and high-contrast text.
- Single accent rule. Pick at most one accent color per project (Emerald, Electric Blue, Deep Rose, or Amber). Keep accent saturation strictly below 80% to eliminate neon glows.
- Systematic color spaces. Construct palette steps using OKLCH scales for uniform perceived lightness across tints and shades. Consult the custom theme guide.
- Surface elevation. Differentiate elevation layers using discrete surface lightness steps and subtle borders instead of stacking semi-transparent white overlays or neon drop shadows.
- Dynamic surface tinting. Construct state tints and subtle surface borders using color-mix in oklch space with 5% to 15% accent mix instead of stacking opacity overlays or arbitrary hex codes.
- Banned AI palette tropes. Use project-specific palette tokens grounded in brand context; avoid formulaic warm cream (#F4F1EA) paired with terracotta (#D97757) and high-contrast serifs, or near-black backgrounds paired with single acid-green or vermilion accents, unless explicitly required by brand guidelines.

## 3. Layout structure

Construct responsive structural grids with modern CSS and dynamic viewport units:
- CSS Grid architecture. Use CSS Grid multi-column arrangements instead of manual percentage calculations or flexbox math. Consult the structure guide.
- Subgrid card alignment. Align internal card zones (headers, descriptions, pricing, footers) across sibling cards in multi-column grids using `grid-template-rows: subgrid` (`grid-rows-subgrid`).
- Viewport stability. Set full-height hero screens and root wrappers to `min-h-[100dvh]` or `min-h-svh` instead of `h-screen` or `100vh` to eliminate mobile scroll jumping.
- Mobile collapse threshold. When Variance exceeds level 4, collapse asymmetric desktop grids into a clean single column below 768px (`w-full px-4`). Consult the responsive guide.
- Layout anti-patterns. Avoid centered three-card feature rows. Use staggered two-column pairs, bento layouts, horizontal scrolls, or index directories. Consult the anti-pattern catalog.
- Characteristic hero composition. Open with the most representative artifact of the domain, such as an interactive demo, canvas, or direct preview. Avoid generic hero blocks made of large isolated numbers, small labels, and gradient washes. Apply the Chanel restraint principle: pick exactly one focal anchor per view and keep secondary elements quiet.
- Clamped concentric corner geometry. Maintain proportional nested radii where inner radius equals `max(0px, calc(outer - padding - border))` using concentric geometry formulas instead of applying identical radii on nested cards.
- Container query modularity. Declare `container-type: inline-size` on portable micro-component roots without fixed descendants. Trigger internal responsive adaptations and typography clamping using container queries and `cqw` units instead of coupling components to global viewport breakpoints.
- Pre-code ASCII wireframing. Sketch a concise ASCII wireframe and spatial role before writing JSX or Tailwind classes to lock alignment, hierarchy, and column spans.
- Specificity collision guards. Use pure utility classes or scoped component selectors; avoid mixing element type selectors with component utility classes. Handle vertical section spacing with parent container padding or gap rather than child margins that collapse or cancel out.

## 4. Honest copy and authentic assets

Deliver verifiable production content with authentic brand media:
- Zero fabricated metrics. Never invent placeholder percentages, uptime stats, speed multipliers, or fake testimonial quotes. If exact metrics are absent, use organic real-world samples or structural illustrations.
- Genuine brand marks. Use verified SVG or PNG logos for authentic integrations. Omit partner logo walls entirely when authentic proof is unavailable.
- Authentic photography and illustration. Use real team photos, transparent PNG cutouts, or genuine vector art instead of generic AI clay dioramas, low-poly pastel 3D toys, or uncredited decorative mesh blobs.
- Zero synthetic ordinal counters or scroll cues. Omit decorative 01 / 06 section corner counters and animated mouse scroll indicators. Let content, hierarchy, and peeked fold boundaries guide navigation naturally.
- Zero fake device chrome. Let UI content speak for itself instead of hand-coding simulated browser URL bars, traffic-light window controls, or faux smartphone frames.
- Zero template chrome. Omit tracked-out ALL-CAPS eyebrow labels above headings, metadata strings separated by middle dots ('A · B · C'), dual-fragment headings separated by dashes, and automatic '→' characters on button text.
- Visual icon sets. Use Phosphor, Radix, or Solar SVG icons with unified stroke weight instead of rendering raw unicode emojis in user interface labels or copy.

## 5. Web performance and runtime vitals

Apply platform-level performance constraints to eliminate layout shifts, interface lag, and excessive payload transfers:
- Layout stability (CLS). Every image, video, canvas, and iframe must declare explicit width and height attributes or use Tailwind aspect-* utility classes. Reserve container dimensions for dynamic asynchronous components using skeleton placeholders or CSS `contain-intrinsic-size` to eliminate reflow when content renders.
- Main thread responsiveness (INP). Keep event handlers lightweight. Defer non-critical computations using `requestIdleCallback` or microtask splitting. Debounce high-frequency scroll and resize listeners, or handle them via passive event listeners (`{ passive: true }`) and CSS scroll-driven animations. Avoid DOM thrashing by separating batch DOM reads from batch DOM writes.
- Critical asset delivery (LCP). Preload exactly one primary hero visual element using `<link rel="preload" as="image">` with `fetchpriority="high"`. Apply `loading="lazy"` and `decoding="async"` to all below-the-fold media. Configure `font-display: swap` or `optional` on web fonts to prevent invisible text during font download.
- Bundle transfer discipline. Use granular named imports for icons and utilities; avoid importing full icon or utility libraries when only a fraction is used. Isolate heavy visualization, editor, or charting libraries behind dynamic imports (`import()`) and load them on demand.
