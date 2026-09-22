---
name: design-taste-frontend
description: Use when building frontend interfaces, styling layouts with Tailwind CSS, animating with Framer Motion, or fixing generic AI interface designs.
---

# Design taste frontend

Construct high-quality frontend interfaces, correct default AI layout biases, and enforce hardware-accelerated animations.

## Baseline configuration

Apply these baseline dial values unless the user explicitly requests different settings in chat prompts:

- `DESIGN_VARIANCE`: 8 (on a 1 to 10 scale, where 1 is symmetrical grid and 10 is asymmetric layout)
- `MOTION_INTENSITY`: 6 (on a 1 to 10 scale, where 1 is static CSS and 10 is spring physics)
- `VISUAL_DENSITY`: 4 (on a 1 to 10 scale, where 1 is airy gallery and 10 is compact dashboard)

## Workflow

Follow these four steps in sequence:

### Step 1. Environment and dependency audit

Inspect the target project configuration before drafting UI code.

- Inspect `package.json` before importing third-party libraries such as `framer-motion`, `@phosphor-icons/react`, or `@radix-ui/react-icons`. If a package is missing, output the installation command before writing code.
- Detect the active Tailwind CSS version. Use Tailwind v4 plugins (`@tailwindcss/postcss` or Vite plugin) only in v4 projects. Keep v3 configuration files in v3 projects.
- Isolate interactive components. In Next.js and React Server Component environments, mark leaf components containing motion, hooks, or browser events with `'use client'` at the top of the file. Keep layout wrappers as static server components.

Completion criterion. Target dependencies and runtime boundaries are verified against `package.json` with zero uninstalled package imports.

### Step 2. Layout, typography, and color scaffolding

Establish typography scales, geometric layout structures, and color bounds.

- Select high-character sans-serif fonts (`Geist`, `Satoshi`, `Outfit`, or `Cabinet Grotesk`) paired with monospace fonts (`Geist Mono` or `JetBrains Mono`). Avoid serif fonts for software dashboards.
- Use CSS Grid (`grid grid-cols-1 md:grid-cols-3 gap-6`) for multi-column structures instead of manual flexbox percentage math.
- Set full-height sections to `min-h-[100dvh]` instead of `h-screen` to prevent layout jumping on mobile viewports.
- When `DESIGN_VARIANCE` exceeds 4, collapse asymmetric desktop grids into a single-column layout (`w-full px-4`) on viewports under 768px.
- Limit accents to at most one color with saturation below 80%. Use neutral bases (Zinc or Slate). Avoid purple or neon gradient glow buttons. Maintain consistent color temperature across the entire interface.
- Render icons using Phosphor or Radix SVG components with standardized stroke widths (such as 1.5 or 2.0). Do not render unicode emojis in code, markup, or text.

Completion criterion. Layout and color variables adhere to viewport stability rules, single-accent constraints, and font pairing requirements.

### Step 3. State, motion, and interaction choreography

Implement full lifecycle interaction states and performance-safe motion.

- Implement complete interaction states for every user action:
  1. Skeleton loaders matching final layout geometry.
  2. Empty states with guidance on how to populate data.
  3. Inline validation error messages below input fields.
  4. Tactile press feedback on buttons using `-translate-y-[1px]` or `scale-[0.98]`.
- Configure Framer Motion transitions with spring physics (`type: "spring", stiffness: 100, damping: 20`). Avoid linear easing.
- Animate position and dimension changes using Framer Motion `layout` and `layoutId` props.
- Animate exclusively via `transform` and `opacity`. Never animate `top`, `left`, `width`, or `height`.
- Apply background grain filters exclusively to fixed, `pointer-events-none` pseudo-elements.
- Isolate perpetual animation loops into memoized client components to avoid triggering re-renders in parent layouts.
- For complex layouts, bento grid implementations, and magnetic cursor attraction, consult `references/ui-patterns.md`.

Completion criterion. All interactive components support loading, empty, and active states while animating exclusively hardware-accelerated CSS properties.

### Step 4. Pre-flight verification

Evaluate completed code against the verification checklist before presenting results.

Completion criterion. Code passes every item on the checklist with zero violations.

## Dial definitions

| Dial | Level 1 to 3 | Level 4 to 7 | Level 8 to 10 |
|---|---|---|---|
| `DESIGN_VARIANCE` | Symmetrical 12-column grids, centered alignments | Overlapping sections, offset cards, mixed aspect ratios | Asymmetric masonry, fractional CSS Grid splits, single-column mobile fallback |
| `MOTION_INTENSITY` | Static CSS transitions on `:hover` and `:active` | Smooth transitions via `cubic-bezier(0.16, 1, 0.3, 1)`, load-in cascades | Dynamic Framer Motion spring physics, layout transitions, animated bento cards |
| `VISUAL_DENSITY` | Generous whitespace, large section gaps | Standard web application spacing | Dense data tables, 1px divider lines, monospace numbers |

## Pre-flight checklist

Run this check before finishing any frontend generation task:

| Check | Passing condition |
|---|---|
| Dependencies | Every imported package exists in `package.json` or includes an install command |
| Viewport stability | Full-height sections use `min-h-[100dvh]` instead of `h-screen` |
| Mobile safety | Asymmetric layouts collapse to single column below 768px |
| Typography | Headline scale uses high-character font stack without serif on dashboards |
| Color saturation | At most one accent color with saturation below 80% and zero neon purple glows |
| Icons | Phosphor or Radix SVG icons used with zero unicode emojis |
| Component boundaries | Client hooks and animations isolated in `'use client'` leaf components |
| Hardware acceleration | Animations modify only `transform` and `opacity` |
| Interaction states | Empty, loading skeleton, and inline error states provided |
