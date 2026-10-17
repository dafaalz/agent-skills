---
name: frontend-design
description: Use when building frontend interfaces, styling layouts with Tailwind CSS, establishing visual tokens, generating DESIGN.md, or selecting UI libraries. Don't use for backend API implementation, database migrations, or server configuration.
---

# Frontend design

Author intentional visual interfaces, establish token architectures, and eliminate default AI styling patterns.

## Overview

Frontend design provides an engineering runbook for layout structure, token architecture, component mechanics, and anti-slop safeguards. It replaces generic AI defaults such as neon gradients, generic serif headings on dashboards, centered three-card rows, and fabricated metrics with intentional design systems. Every interface must feature authentic content, stable layout structure, accessible interaction models, and verified production libraries.

Consult reference documents in references/ on demand for deep implementation patterns.

## Modes

Select an execution mode before Step 1:
- Greenfield mode (default). Author new views, generate DESIGN.md, and establish visual tokens from scratch.
- Audit and restyle mode. Inspect existing components, calculate delta scores against references/impeccable-delta.md, and present recommendations before modifying markup.

## Execution workflow

Follow these four steps in sequence:

### Step 1. Environment audit and dial calibration

Inspect package.json and project configuration before drafting UI code.

- Detect existing design tokens, Tailwind configuration version, and installed packages.
- Establish numeric ratings for Creativity, Density, Variance, and Motion dials.
- Isolate interactive components with client hooks into memoized leaf components.

Completion criterion. Target dependencies and dial values confirmed with zero unverified imports.

### Step 2. Token locking and typography setup

Declare colors, spacing, and typography as structured tokens.

- Pick a curated theme from references/themes/ or construct an OKLCH scale following references/custom-theme.md.
- Lock display, body, and monospace font families in Tailwind or CSS custom properties.
- Establish semantic surface lightness steps for light and dark modes.

Completion criterion. Complete token inventory defined in CSS custom properties with zero arbitrary color literals.

### Step 3. Layout synthesis and component assembly

Assemble complete semantic components matching project standards.

- Build multi-column layouts using CSS Grid and dynamic viewport heights (min-h-[100dvh]).
- Implement complete interaction states including skeleton loaders, empty states, and inline validation.
- Animate visual elements exclusively using transform and opacity with spring physics.

Completion criterion. Responsive layout assembled with full interaction states and hardware-accelerated transitions.

### Step 4. Pre-flight verification and slop-test scoring

Evaluate output against anti-slop criteria before completing work.

- Score implementation on Philosophy, Hierarchy, Execution, Specificity, Restraint, and Variety.
- Verify mobile responsiveness at 320px, 375px, 414px, and 768px.
- Confirm zero uninstalled packages, zero fake metrics, and zero banned fonts.
- Apply `references/impeccable-delta.md` checks 1 to 8 against project DESIGN.md and prior project views.

Completion criterion. Component markup passes responsive checks at all target breakpoints, includes skeleton loader and empty state markup, and confines animations to transform and opacity.

## Boundary isolation

Apply styling exclusively to markup, layout, and visual tokens:
- Never modify, remove, or refactor component props, state hooks (`useState`, `useReducer`), side effects (`useEffect`), event handler callbacks, or API query wiring during visual restyling passes.
- Maintain existing accessibility attributes (`aria-*`, `role`, tabindex, focus management) intact.

## Baseline dial calibration

Calibrate interface constraints across four numerical dials on a 1 to 10 scale before drafting layouts or tokens:

| Dial | Default | Low (1 to 3) | Mid (4 to 7) | High (8 to 10) |
|---|---|---|---|---|
| Creativity | 8 | Minimal monochrome, strict conventions | Balanced personality, subtle accents | Expressive editorial, inline headline imagery, asymmetry |
| Density | 4 | Airy gallery whitespace, wide gaps | Balanced application spacing | Cockpit dense, 1px borders, tabular mono numbers |
| Variance | 8 | Symmetrical grids, uniform cards | Subtle offsets, mixed ratios | Asymmetric masonry, varied section rhythms, non-repeating blocks |
| Motion | 6 | Static CSS transitions on hover | Smooth easing, staggered entrances | Coordinated spring physics, gesture tracking, layout morphs |

Calibrate dial settings with four positioning checks before locking styling rules:
1. Narrative role. Identify if the section acts as hero, transition, data display, pull-quote, or closing action.
2. Viewing distance. Optimize typography and density for mobile hand-held use, desktop displays, or wall projectors.
3. Visual temperature. Align color temperature as quiet, energized, authoritative, warm, or playful.
4. Capacity check. Ensure content fills the layout naturally without artificial spacers or empty cards.

## Core disciplines

Apply these foundational disciplines across all frontend tasks:

### 1. Typography stacks

Pair high-character sans with monospaced accents. Keep headings upright and roman without italics.

- Display and headings. Use high-character sans families such as Geist, Satoshi, Outfit, or Cabinet Grotesk. Track tight (-0.025em), set fluid clamp scales, and compress line height between 1.1 and 1.2.
- Body copy. Use the same sans family at weight 400 with relaxed line height between 1.6 and 1.65. Restrict line length to a maximum of 65 characters for readability. Give serif body copy slightly more line height than sans-serif.
- Monospace tokens. Use Geist Mono or JetBrains Mono for code blocks, terminal snippets, technical tags, and timestamps. When Density exceeds level 7, render all numbers in monospace.
- Prohibited typography. Avoid unconfigured default Inter on greenfield marketing and editorial layouts. When working in an existing codebase that already configures Inter as its brand typography, adopt the existing repository font. Never use generic system serifs like Times New Roman, Georgia, or Garamond on dashboards. Reserve modern editorial serifs exclusively for long-form literary publications. Never accent a single word in a headline with isolated italics, bolding, or colored text. Never apply all-caps styling to content labels.
- Editorial pull quotes and marginalia. Structure pull quotes using semantic figure and blockquote containers with left accent borders and fluid clamp scaling. Compartmentalize marginalia columns into distinct structured sub-blocks (formal citations, contextual notes, archive tags) separated by subtle dividers rather than monolithic paragraphs.

### 2. Color token architecture

Anchor layouts to neutral bases with at most one restrained accent color.

- Neutral foundation. Anchor interfaces to Zinc or Slate. Never use pure black (#000000); use Zinc-950 or Charcoal Ink (#18181B) for deep surfaces and high-contrast text.
- Single accent rule. Pick at most one accent color per project (Emerald, Electric Blue, Deep Rose, or Amber). Keep accent saturation strictly below 80% to eliminate neon glows.
- Systematic color spaces. Construct palette steps using OKLCH scales for uniform perceived lightness across tints and shades. Consult references/custom-theme.md.
- Surface elevation. Differentiate elevation layers using discrete surface lightness steps and subtle borders instead of stacking semi-transparent white overlays or neon drop shadows.
- Dynamic surface tinting. Construct state tints and subtle surface borders using color-mix in oklch space with 5% to 15% accent mix instead of stacking opacity overlays or arbitrary hex codes.
- Banned AI palette tropes. Avoid formulaic warm cream (#F4F1EA) paired with terracotta (#D97757) and high-contrast serifs, or near-black backgrounds paired with single acid-green or vermilion accents, unless explicitly required by brand guidelines.

### 3. Layout structure

Construct responsive structural grids with modern CSS and dynamic viewport units.

- CSS Grid architecture. Use CSS Grid multi-column arrangements instead of manual percentage calculations or flexbox math. Consult references/structure.md.
- Viewport stability. Set full-height hero screens and root wrappers to min-h-[100dvh] instead of h-screen or 100vh to eliminate mobile scroll jumping.
- Mobile collapse threshold. When Variance exceeds level 4, collapse asymmetric desktop grids into a clean single column below 768px (w-full px-4). Consult references/responsive.md.
- Layout anti-patterns. Avoid centered three-card feature rows. Use staggered two-column pairs, bento layouts, horizontal scrolls, or index directories. Consult references/anti-patterns.md.
- Characteristic hero composition. Open with the most representative artifact of the domain, such as an interactive demo, canvas, or direct preview. Avoid generic hero blocks made of large isolated numbers, small labels, and gradient washes. Apply the Chanel restraint principle: pick exactly one focal anchor per view and keep secondary elements quiet.
- Concentric corner geometry. Maintain proportional nested radii where inner radius equals outer radius minus container padding and border thickness using concentric geometry formulas instead of applying identical radii on nested cards.
- Container query modularity. Declare container-type inline-size on portable micro-component roots. Trigger internal responsive adaptations and typography clamping using container queries and cqw units instead of coupling components to global viewport breakpoints.

### 4. Honest copy and authentic assets

Deliver verifiable production content with authentic brand media.

- Zero fabricated metrics. Never invent placeholder percentages, uptime stats, speed multipliers, or fake testimonial quotes. If exact metrics are absent, use organic real-world samples or structural illustrations.
- Genuine brand marks. Use verified SVG or PNG logos for authentic integrations. Omit partner logo walls entirely when authentic proof is unavailable.
- Authentic photography and illustration. Use real team photos, transparent PNG cutouts, or genuine vector art instead of generic AI clay dioramas, low-poly pastel 3D toys, or uncredited decorative mesh blobs.
- Zero synthetic ordinal counters or scroll cues. Omit decorative 01 / 06 section corner counters and animated mouse scroll indicators. Let content, hierarchy, and peeked fold boundaries guide navigation naturally.
- Zero fake device chrome. Let UI content speak for itself instead of hand-coding simulated browser URL bars, traffic-light window controls, or faux smartphone frames.
- Zero template chrome. Omit tracked-out ALL-CAPS eyebrow labels above headings, metadata strings separated by middle dots ('A · B · C'), dual-fragment headings separated by dashes, and automatic '→' characters on button text.
- Visual icon sets. Use Phosphor, Radix, or Solar SVG icons with unified stroke weight instead of rendering raw unicode emojis in user interface labels or copy.

## Macrostructures and visual genres

Select an intentional macrostructure that matches project content density and narrative role:

1. Bento grid. Multi-cell asymmetric dashboard or product overview combining stat callouts, interactive previews, and feature callouts.
2. Split studio. High-contrast two-column arrangement with sticky media preview alongside scrolling explanatory narrative.
3. Marquee hero. Expansive typographic header paired with flowing preview ribbons or ticker metrics.
4. Long document. Structured editorial layout with margin notes, fluid typography, and sticky table of contents.
5. Workbench cockpit. Dense utility layout with collapsible side rails, command bar, and tabular data panes.
6. Ecosystem index. Categorized directory grid designed for extensibility, plugins, or large asset libraries.

Classify aesthetic direction into one of four visual genres:
- Editorial. High typographic contrast, generous white space, restrained palettes, and literary discipline.
- Modern minimal. Precision geometry, crisp monochrome tones, subtle micro-borders, and high functional density.
- Atmospheric. Deep dark surfaces, diffused backdrops, focused illumination, and tactile depth.
- Playful. Expressive type, tactile physical feedback, bold accents, and organic rounded forms.

## Component mechanics and interaction states

Implement full lifecycle interaction states and tactile feedback for all components:

1. Tactile press feedback. Apply tactile physical displacement (-translate-y-[1px] or scale-[0.98]) to active buttons and interactive chips.
2. Skeleton loaders. Match placeholder skeleton geometries to expected layout dimensions. Avoid generic circular spinners for primary content blocks.
3. Form validation timing. Delay error messages until input blur, then validate live on subsequent input. Position validation messages directly adjacent to invalid fields.
4. Concentric card nesting. Ensure nested badges, buttons, and preview containers use mathematically concentric radii to prevent visual pinching.
5. Hardware-accelerated motion. Animate exclusively via transform and opacity. Restrict spring physics transitions to motion-enabled elements and respect prefers-reduced-motion queries.
6. Asynchronous network resilience. Handle race conditions with AbortController, retry idempotent requests with exponential backoff, and provide optimistic mutations with rollback. Consult `references/api-resilience.md`.
7. Target size minimum and keyboard focus. Guarantee interactive elements meet WCAG 2.2 SC 2.5.8 with a minimum hit area of 24x24px, with recommended 44px touch targets (min-h-[44px] or adequate padding and gap spacing). Configure visible focus indicators on all interactive targets using focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:outline-none.
8. Top layer and discrete transitions. Use native dialog or Popover API for modals, command palettes, and drawer surfaces to activate browser focus trapping and top-layer stacking. Animate entry and exit states using @starting-style with transition-behavior allow-discrete for display, opacity, and transform transitions without JavaScript animation libraries.
9. Relational container focus. Configure parent card boundaries to reflect keyboard focus of interior interactive links or buttons using :has(a:focus-visible) and :has(button:focus-visible) without JavaScript event listeners.

## Specialized workflow pointers

Route execution to dedicated reference runbooks based on task requirements:

1. Generating ./DESIGN.md. Follow references/design-template.md to author a canonical specification covering dials, palette tokens, typography rules, component specs, and anti-patterns.
2. Curated UI primitives and libraries. Consult references/recommended-libraries.md to map functional requirements to verified single-purpose packages like Base UI, cmdk, Sonner, input-otp, NumberFlow, Virtuoso, Zustand, and CVA.
3. Kinetic WebGL and GSAP scenes. Consult references/creative-motion-webgl.md when choreographing smooth scroll, GSAP ScrollTrigger timelines, and Three.js canvas lifecycles with offscreen pause constraints.
4. Pre-built UI components and macrostructures. Browse references/components/ for tested component patterns (navbars, bento cards, hero callouts, footer statements) and references/macrostructures/ for full-page templates.
5. Micro-interactions and gesture physics. Consult references/ui-patterns.md for button press feedback, bento card mechanics, and cursor interactions. For spring physics, gesture tracking, and frame rate audits, activate the ui-motion skill.

## Reference index

Consult these runbooks on demand for deep implementation detail:

- Core disciplines. `references/typography.md`, `references/color.md`, `references/layout-and-space.md`, `references/copy.md`, `references/motion.md`, `references/interaction-and-states.md`, `references/microinteractions.md`.
- Media and assets. `references/assets.md`, `references/imagery-kit.md`, `references/hero-enrichment.md`, `references/custom-craft.md`.
- Composition. `references/component-cookbook.md`, `references/macrostructures.md`, `references/floating-nav.md`.
- Genre runbooks. `references/genres/editorial.md`, `references/genres/modern-minimal.md`, `references/genres/atmospheric.md`, `references/genres/playful.md`.
- Workflow commands. `references/verbs/audit.md`, `references/verbs/redesign.md`.
- Process and output. `references/study.md`, `references/component-scope.md`, `references/preview-examples.md`, `references/design-md.md`, `references/export-formats.md`, `references/contract.md`, `references/slop-test.md`.

## Quick audit checklist

Verify all items before declaring frontend implementation complete:

| Check | Passing condition |
|---|---|
| Dials | Creativity, Density, Variance, and Motion dial ratings calibrated |
| Typography | High-character sans paired with mono, roman headings without italics, zero generic serifs |
| Color tokens | Single accent under 80% saturation, Zinc or Slate neutral, zero pure black (#000000) |
| Elevation | Differentiated lightness steps and subtle borders, zero neon glow shadows |
| Viewport height | Full-height wrappers use min-h-[100dvh] instead of h-screen |
| Mobile collapse | Asymmetric grids collapse to single column below 768px |
| Concentric radii | Inner radii match outer radii minus padding and border offset |
| Copy integrity | Zero fabricated metrics, zero promotional buzzwords or exaggerated claims |
| Asset authenticity | Real SVG or PNG assets, genuine photography, zero faux browser frames |
| Emojis | Zero raw unicode emojis used in UI labels, copy, or markup |
| Libraries | Selected single-purpose packages verified against package.json |
| Motion bounds | Animations restricted to transform and opacity, reduced-motion fallbacks included |
| Target sizes | Interactive elements maintain minimum 24x24px target size with 44px touch bounds |
| Keyboard focus | Visible focus indicators configured via focus-visible:ring-2 focus-visible:ring-offset-2 |
| Editorial quotes | Pull quotes use semantic figure or blockquote with structured multi-tier marginalia |
| Container queries | Portable micro-components declare container-type inline-size and scale via @container |
| Native dialogs | Modals use native dialog or popover with @starting-style discrete transitions |
| Relational focus | Container cards reflect child keyboard focus via :has(:focus-visible) |
| Surface tinting | Dynamic states use color-mix in oklch rather than stacked opacity overlays |
| Fingerprint divergence | Layout diverges from prior project views on at least 4 of 6 structural dimensions |
| Section ordinality | Zero decorative 01 / 06 corner counters and zero animated mouse scroll cues |
| AI visual clichés | Zero template chrome (ALL-CAPS eyebrows, middle dots, single-word accents, or automatic '→' glyphs) |
| AI palette tropes | Zero formulaic warm cream with terracotta or near-black with acid-green unless project-mandated |
| Hero composition | Hero opens with subject-matter artifact or interactive moment instead of default stat-plus-gradient block |
| Boldness focus | Exactly one memorable focal element per view, with secondary elements visually disciplined |
