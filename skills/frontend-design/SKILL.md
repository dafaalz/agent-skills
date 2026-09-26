---
name: frontend-design
description: Use when building frontend interfaces, styling layouts with Tailwind CSS, establishing visual tokens, generating DESIGN.md, or selecting UI libraries.
---

# Frontend design

Author high-craft visual interfaces, establish token architectures, and eliminate default AI styling patterns.

## Overview

Frontend design provides a unified engineering runbook for visual craft, token architecture, component mechanics, and anti-slop safeguards. It replaces generic AI defaults such as neon gradients, generic serif headings on dashboards, centered three-card rows, and fabricated metrics with intentional design systems. Every interface must feature authentic content, stable layout structure, accessible interaction models, and verified production libraries.

Consult reference documents in references/ on demand for deep implementation patterns.

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
- Body copy. Use the same sans family at weight 400 with relaxed line height between 1.6 and 1.65. Restrict line length to a maximum of 65 characters for readability.
- Monospace tokens. Use Geist Mono or JetBrains Mono for code blocks, terminal snippets, technical tags, and timestamps. When Density exceeds level 7, render all numbers in monospace.
- Prohibited typography. Never use Inter for display or body text. Never use generic system serifs like Times New Roman, Georgia, or Garamond on dashboards. Reserve modern editorial serifs exclusively for long-form literary publications.

### 2. Color token architecture

Anchor layouts to neutral bases with at most one restrained accent color.

- Neutral foundation. Anchor interfaces to Zinc or Slate. Never use pure black (#000000); use Zinc-950 or Charcoal Ink (#18181B) for deep surfaces and high-contrast text.
- Single accent rule. Pick at most one accent color per project (Emerald, Electric Blue, Deep Rose, or Amber). Keep accent saturation strictly below 80% to eliminate neon glows.
- Systematic color spaces. Construct palette steps using OKLCH scales for uniform perceived lightness across tints and shades. Consult references/custom-theme.md.
- Surface elevation. Differentiate elevation layers using discrete surface lightness steps and subtle borders. Never stack semi-transparent white overlays or neon drop shadows.

### 3. Layout structure

Construct responsive structural grids with modern CSS and dynamic viewport units.

- CSS Grid architecture. Use CSS Grid multi-column arrangements instead of manual percentage calculations or flexbox math. Consult references/structure.md.
- Viewport stability. Set full-height hero screens and root wrappers to min-h-[100dvh] instead of h-screen or 100vh to eliminate mobile scroll jumping.
- Mobile collapse threshold. When Variance exceeds level 4, collapse asymmetric desktop grids into a clean single column below 768px (w-full px-4). Consult references/responsive.md.
- Layout anti-patterns. Avoid centered three-card feature rows. Use staggered two-column pairs, bento layouts, horizontal scrolls, or index directories. Consult references/anti-patterns.md.
- Concentric corner geometry. Maintain proportional nested radii where inner radius equals outer radius minus container padding and border thickness. Never use identical radii on nested cards.

### 4. Honest copy and authentic assets

Deliver verifiable production content with authentic brand media.

- Zero fabricated metrics. Never invent placeholder percentages, uptime stats, speed multipliers, or fake testimonial quotes. If exact metrics are absent, use organic real-world samples or structural illustrations.
- Genuine brand marks. Use verified SVG or PNG logos for authentic integrations. Omit partner logo walls entirely when authentic proof is unavailable.
- Authentic photography. Use real team photos or transparent PNG cutouts. Never use generic AI-generated faces or faceless avatars.
- Zero fake device chrome. Never hand-code simulated browser URL bars, traffic-light window controls, or faux smartphone frames. Let UI content speak for itself.
- Visual icon sets. Use Phosphor, Radix, or Solar SVG icons with unified stroke weight. Never render raw unicode emojis in user interface labels or copy.

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

Completion criterion. Interface satisfies all checklist checks with scores of 3 or higher across all evaluation criteria.

## Specialized workflow pointers

Route execution to dedicated reference runbooks based on task requirements:

1. Generating ./DESIGN.md. Follow references/design-template.md to author a canonical specification covering dials, palette tokens, typography rules, component specs, and anti-patterns.
2. Curated UI primitives and libraries. Consult references/recommended-libraries.md to map functional requirements to verified single-purpose packages like Base UI, cmdk, Sonner, input-otp, NumberFlow, Virtuoso, Zustand, and CVA.
3. Creative Awwwards-style WebGL and GSAP scenes. Consult references/creative-motion-webgl.md when choreographing smooth scroll, GSAP ScrollTrigger timelines, and Three.js canvas lifecycles with offscreen pause constraints.
4. Pre-built UI components and macrostructures. Browse references/components/ for tested component patterns (navbars, bento cards, hero callouts, footer statements) and references/macrostructures/ for full-page templates.
5. Micro-interactions and gesture physics. Consult references/ui-patterns.md for button press feedback, bento card mechanics, and cursor interactions. For spring physics, gesture tracking, and frame rate audits, activate the ui-motion skill.

## Pre-flight anti-slop audit checklist

Verify all items before declaring frontend implementation complete:

| Check | Passing condition |
|---|---|
| Dials | Creativity, Density, Variance, and Motion dial ratings calibrated |
| Typography | High-character sans paired with mono, roman headings without italics, zero Inter or generic serifs |
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
