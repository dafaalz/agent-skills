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

### 3. Layout structure and modern CSS
Construct responsive structural grids with modern CSS and dynamic viewport units:
- CSS Grid architecture: Use CSS Grid multi-column arrangements instead of manual percentage calculations or flexbox math.
- Viewport stability: Set full-height hero screens and root wrappers to `min-h-[100dvh]` instead of `h-screen` or `100vh` to eliminate mobile scroll jumping.
- Mobile collapse threshold: When Variance exceeds level 4, collapse asymmetric desktop grids into a clean single column below 768px (`w-full px-4`).
- Centered measure for chat feeds: Always constrain conversational logs, messaging lists, and message input bars to `max-w-3xl mx-auto w-full` to eliminate eye strain across wide monitors.
- Concentric corner geometry: Maintain proportional nested radii where `R_inner = max(0, R_outer - (padding + border))`. Never use identical radii on nested cards.
- Target size compliance: Ensure all interactive controls satisfy WCAG 2.2 AA target size (minimum 24x24px, recommended 44x44px).

### 4. Honest copy and anti-patterns
Deliver verifiable production content and eliminate AI defaults:
- Zero fabricated metrics: Never invent placeholder percentages, uptime stats, speed multipliers, or fake testimonial quotes.
- Genuine brand marks and photography: Use verified SVG or PNG logos and authentic images. Never use generic AI faces or faceless avatars.
- Zero fake device chrome: Never hand-code simulated browser URL bars, traffic-light window controls, or faux smartphone frames.
- Dynamic text in whitespace-pre: Never separate opening and closing HTML tags with source newlines when wrapping dynamic text in `whitespace-pre-*`. Write `>${escapedText}<` flush against tag boundaries to avoid rendering literal source indentation.
- State guards: Target empty states with explicit unique semantic identifiers (`#chat-empty-placeholder`) or data attributes (`[data-state="empty"]`), never styling tokens (`.text-muted-foreground`).
- Clear the design fingerprint gate: When building multiple views, diverge from prior views on at least 4 of 6 structural dimensions (macrostructure, nav treatment, hero device, section rhythm, closing pattern, interactive signature move). Consult `references/anti-patterns.md`.

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
- Confirm chat/conversational containers are constrained to `max-w-3xl mx-auto`.

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
| Target size | Minimum 24x24px bounding box for all touch/click targets |
| Chat measure | Feeds and inputs constrained to `max-w-3xl mx-auto w-full` |
| Bubble flush | Dynamic text in `whitespace-pre-*` written flush against tag boundaries |
| Copy integrity | Zero fabricated metrics, zero promotional buzzwords or exaggerated claims |
| Asset authenticity | Real SVG or PNG assets, genuine photography, zero faux browser frames |
| Emojis | Zero raw unicode emojis used in UI labels, copy, or markup |
| Deliverable | Complete component rendered inside a previewable Claude Artifact |
