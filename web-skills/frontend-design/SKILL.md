---
name: frontend-design
description: Use when building frontend interfaces, styling layouts with Tailwind CSS, establishing visual tokens, generating DESIGN.md, or designing React/HTML components. Don't use for backend API implementation, database migrations, or server configuration.
---

# Frontend Design for Claude Web

Author high-craft visual interfaces, establish token architectures, and eliminate default AI styling patterns on Claude Web.

<initiative_and_scope>
When asked to build or style an interface, deliver the complete, fully coded component or layout with real content. Stop and report when done. Do not add unrequested backend models, fake API servers, or unrelated pages. If the user asks for design options, dials, or layout directions first, present 2 to 3 distinct visual directions and stop to wait for user selection before writing code.
</initiative_and_scope>

<claude_web_environment>
Operate within the Claude Web interface.
- Output complete UI components (React JSX/TSX with Tailwind, Lucide/Radix icons, or standalone HTML/Tailwind) as previewable Claude Artifacts (`application/vnd.ant.code` or `text/html`).
- Output design token systems or `DESIGN.md` documentation as Markdown Claude Artifacts (`text/markdown`).
- In the chat body, provide only a high-level summary of dial calibration, typography pairing, and color token choices.
</claude_web_environment>

## Baseline dial calibration

Calibrate interface constraints across four numerical dials on a 1 to 10 scale before drafting layouts or tokens:

| Dial | Default | Low (1 to 3) | Mid (4 to 7) | High (8 to 10) |
|---|---|---|---|---|
| Creativity | 8 | Minimal monochrome, strict conventions | Balanced personality, subtle accents | Expressive editorial, inline imagery, asymmetry |
| Density | 4 | Airy gallery whitespace, wide gaps | Balanced application spacing | Cockpit dense, 1px borders, tabular mono numbers |
| Variance | 8 | Symmetrical grids, uniform cards | Subtle offsets, mixed ratios | Asymmetric masonry, varied rhythms, non-repeating blocks |
| Motion | 6 | Static CSS transitions on hover | Smooth easing, staggered entrances | Coordinated spring physics, gesture tracking |

Calibrate dial settings with four positioning checks:
1. Narrative role: Identify if the section acts as hero, transition, data display, pull-quote, or closing action.
2. Viewing distance: Optimize typography and density for mobile, desktop, or dashboard displays.
3. Visual temperature: Align color temperature as quiet, energized, authoritative, warm, or playful.
4. Capacity check: Ensure authentic content fills the layout naturally without artificial spacers or empty cards.

## Core disciplines

### 1. Typography stacks
Pair high-character sans with monospaced accents. Keep headings upright and roman without italics:
- Display and headings: Use high-character sans families such as Geist, Satoshi, Outfit, or Cabinet Grotesk. Track tight (-0.025em), set fluid clamp scales, and compress line height between 1.1 and 1.2.
- Body copy: Use the same sans family at weight 400 with relaxed line height between 1.6 and 1.65. Restrict line length to a maximum of 65 characters (`max-w-prose` or `max-inline-size: 65ch`).
- Monospace tokens: Use Geist Mono or JetBrains Mono for code blocks, terminal snippets, technical tags, and timestamps. When Density exceeds level 7, render all numbers in monospace with `tabular-nums`.
- Prohibited typography: Never use Inter for display or body text. Never use generic system serifs like Times New Roman, Georgia, or Garamond on dashboards. Reserve modern editorial serifs exclusively for long-form literary publications.

### 2. Color token architecture
Anchor layouts to neutral bases with at most one restrained accent color:
- Neutral foundation: Anchor interfaces to Zinc or Slate. Never use pure black (`#000000`); use Zinc-950 or Charcoal Ink (`#18181B`) for deep surfaces and high-contrast text.
- Single accent rule: Pick at most one accent color per project (Emerald, Electric Blue, Deep Rose, or Amber). Keep accent saturation strictly below 80% to eliminate neon glows.
- Systematic color spaces: Construct palette steps using OKLCH scales for uniform perceived lightness across tints and shades. Consult `references/custom-theme.md`.
- Surface elevation: Differentiate elevation layers using discrete surface lightness steps and subtle borders. Never stack semi-transparent white overlays or neon drop shadows.

### 3. Layout structure
Construct responsive structural grids with modern CSS and dynamic viewport units:
- CSS Grid architecture: Use CSS Grid multi-column arrangements instead of manual percentage calculations or flexbox math.
- Viewport stability: Set full-height hero screens and root wrappers to `min-h-[100dvh]` instead of `h-screen` or `100vh` to eliminate mobile scroll jumping.
- Mobile collapse threshold: When Variance exceeds level 4, collapse asymmetric desktop grids into a clean single column below 768px (`w-full px-4`).
- Layout anti-patterns: Avoid centered three-card feature rows. Use staggered two-column pairs, bento layouts, horizontal scrolls, or index directories. Consult `references/anti-patterns.md`.
- Concentric corner geometry: Maintain proportional nested radii where `R_inner = max(0, R_outer - (padding + border))`. Never use identical radii on nested cards.

### 4. Honest copy and authentic assets
Deliver verifiable production content with authentic brand media:
- Zero fabricated metrics: Never invent placeholder percentages, uptime stats, speed multipliers, or fake testimonial quotes. If exact metrics are absent, use organic real-world samples or structural illustrations.
- Genuine brand marks: Use verified SVG or PNG logos. Omit partner logo walls entirely when authentic proof is unavailable.
- Authentic photography: Use real team photos or transparent PNG cutouts. Never use generic AI-generated faces or faceless avatars.
- Zero fake device chrome: Never hand-code simulated browser URL bars, traffic-light window controls, or faux smartphone frames. Let UI content speak for itself.
- Visual icon sets: Use Phosphor, Radix, or Lucide SVG icons with unified stroke weight. Never render raw unicode emojis in user interface labels or copy.

## Macrostructures and visual genres

Select an intentional macrostructure that matches project content density and narrative role:
1. Bento grid: Multi-cell asymmetric dashboard or product overview combining stat callouts, interactive previews, and feature callouts.
2. Split studio: High-contrast two-column arrangement with sticky media preview alongside scrolling explanatory narrative.
3. Marquee hero: Expansive typographic header paired with flowing preview ribbons or ticker metrics.
4. Long document: Structured editorial layout with margin notes, fluid typography, and sticky table of contents.
5. Workbench cockpit: Dense utility layout with collapsible side rails, command bar, and tabular data panes.
6. Ecosystem index: Categorized directory grid designed for extensibility, plugins, or large asset libraries.

Classify aesthetic direction into one of four visual genres:
- Editorial: High typographic contrast, generous white space, restrained palettes, and literary discipline.
- Modern minimal: Precision geometry, crisp monochrome tones, subtle micro-borders, and high functional density.
- Atmospheric: Deep dark surfaces, diffused backdrops, focused illumination, and tactile depth.
- Playful: Expressive type, tactile physical feedback, bold accents, and organic rounded forms.

## Component mechanics and interaction states

Implement full lifecycle interaction states and tactile feedback for all components:
1. Tactile press feedback: Apply tactile physical displacement (`active:scale-[0.98]` or `active:translate-y-[1px]`) to buttons and interactive cards.
2. Skeleton loaders: Match placeholder skeleton geometries to expected layout dimensions. Avoid generic circular spinners for primary content blocks.
3. Form validation timing: Delay error messages until input blur, then validate live on subsequent input. Position validation messages directly adjacent to invalid fields.
4. Hardware-accelerated motion: Animate exclusively via `transform` and `opacity`. Restrict spring physics transitions to motion-enabled elements and respect `prefers-reduced-motion` queries.
5. Asynchronous network resilience: Handle race conditions with AbortController, and provide optimistic mutations with rollback. Consult `references/api-resilience.md`.

## Execution workflow

### Step 1. Dial calibration and genre selection
Examine the user prompt and project requirements:
- Establish numeric ratings for Creativity, Density, Variance, and Motion dials.
- Select visual genre (Editorial, Modern Minimal, Atmospheric, Playful) and macrostructure (Bento, Split Studio, Workbench, etc.).

### Step 2. Token locking and typography setup
Declare colors, spacing, and typography as structured tokens:
- Pick curated theme from `references/themes/` or construct OKLCH scales.
- Lock display, body, and monospace font families.
- Establish semantic surface lightness steps for light and dark modes.

### Step 3. Component assembly in Claude Artifact
Assemble the complete, self-contained component or view:
- Use React with Tailwind CSS or standalone HTML/Tailwind.
- Render the complete implementation inside a Claude Artifact (`application/vnd.ant.code` or `text/html`) so that it can be previewed directly in the Artifact pane.
- Include full interaction states (hover, active, focus-visible, skeleton/loading, empty states).

### Step 4. Pre-flight verification and slop-test scoring
Evaluate output against anti-slop criteria before completing work:
- Confirm zero uninstalled packages, zero fake metrics, and zero banned fonts.
- Confirm full-height wrappers use `min-h-[100dvh]`.
- Confirm nested card containers satisfy concentric border-radius geometry.

## Pre-flight anti-slop audit checklist

| Check | Passing condition |
|---|---|
| Dials | Creativity, Density, Variance, and Motion dial ratings calibrated |
| Typography | High-character sans paired with mono, roman headings without italics, zero Inter or generic serifs |
| Color tokens | Single accent under 80% saturation, Zinc or Slate neutral, zero pure black (`#000000`) |
| Elevation | Differentiated lightness steps and subtle borders, zero neon glow shadows |
| Viewport height | Full-height wrappers use `min-h-[100dvh]` instead of `h-screen` |
| Mobile collapse | Asymmetric grids collapse to single column below 768px |
| Concentric radii | Inner radii match outer radii minus padding and border offset |
| Copy integrity | Zero fabricated metrics, zero promotional buzzwords or exaggerated claims |
| Asset authenticity | Real SVG or PNG assets, genuine photography, zero faux browser frames |
| Emojis | Zero raw unicode emojis used in UI labels, copy, or markup |
| Deliverable | Complete component rendered inside a previewable Claude Artifact |
