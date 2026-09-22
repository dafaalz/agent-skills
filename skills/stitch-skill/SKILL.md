---
name: stitch-design-taste
description: Use when generating or reviewing Google Stitch screen designs, crafting DESIGN.md design system specifications, or translating visual direction into semantic UI constraints.
---

# Stitch design taste

Generate deterministic `DESIGN.md` specifications for Google Stitch screen generation and coding agents.

## Overview

This skill produces a canonical `./DESIGN.md` file in the workspace root. The document translates visual intent into concrete semantic design rules, precise color tokens, typography stacks, and interaction physics.

For the base document layout, consult `references/design-template.md`.

## Workflow

Follow these four steps in sequence:

### Step 1. Scope and style dial calibration

Evaluate project intent across four numerical dials:
- Creativity (1 to 10). Set to 1 for minimal monochrome. Set to 10 for expressive editorial layouts. Default is 8.
- Density (1 to 10). Set to 1 for airy whitespace. Set to 10 for compact data screens. Default is 4.
- Variance (1 to 10). Set to 1 for symmetric repetition. Set to 10 for asymmetric layouts. Default is 8.
- Motion intent (1 to 10). Set to 1 for static interfaces. Set to 10 for choreographed spring motion. Default is 6.

Completion criterion. Defined numeric rating for each of the four dials recorded in project notes.

### Step 2. Token architecture and palette selection

Select color tokens and typography pairings based on dial ratings:
- Palette. Select one neutral base (Zinc or Slate). Pick exactly one accent color with saturation below 80%. Never use pure black (`#000000`); use Zinc-950 or Charcoal Ink (`#18181B`).
- Typography. Select Display font (`Geist`, `Satoshi`, `Cabinet Grotesk`, or `Outfit`), Body font at weight 400, and Monospace font (`Geist Mono` or `JetBrains Mono`).
- Font restrictions. Do not use `Inter`. Do not use generic serif fonts (`Times New Roman`, `Georgia`, `Garamond`). When density exceeds 7, render all numbers in monospace.

Completion criterion. A complete token inventory specifying hex codes, functional roles, and font families with zero banned fonts.

### Step 3. Component behavior and layout synthesis

Load `references/design-template.md` and populate each section with project-specific rules:
- Hero section. Embed inline contextual images between headline words. Separate elements into distinct grid zones without text overlapping. Ban centered layouts when variance exceeds 4. Limit actions to one primary button.
- Components. Apply tactile push feedback (`-1px translateY` or `scale(0.98)`) to active buttons. Use skeletal shimmer loaders instead of circular spinners.
- Responsive layout. Enforce single column collapse below 768px, minimum 44px tap targets, `clamp()` typography scaling, and zero horizontal scrolling. Use `min-h-[100dvh]` instead of `h-screen`.
- Motion specs. Set spring physics (`stiffness: 100, damping: 20`). Restrict hardware acceleration to `transform` and `opacity`.

Completion criterion. A complete draft of `./DESIGN.md` containing all nine template sections populated.

### Step 4. Anti-pattern verification and file export pass

Audit the synthesized draft against the anti-pattern table below. Verify that the document contains zero banned items, then write the finished file to `./DESIGN.md` in the current workspace root.

Completion criterion. File `./DESIGN.md` exists on disk and satisfies every check in the anti-pattern audit table with zero violations.

## Anti-pattern audit checklist

Audit the output against these rules before finishing:

| Category | Banned practice | Passing requirement |
|---|---|---|
| Emojis | Emojis in UI copy, labels, or attributes | Zero emojis anywhere in UI text or code |
| Fonts | Inter or generic system serifs | Geist, Satoshi, Cabinet Grotesk, or modern serif |
| Neutrals | Pure black (`#000000`) | Off-Black, Zinc-950, or Charcoal |
| Glows | Neon borders or glowing drop shadows | Diffused shadow (`rgba(0,0,0,0.05)`) |
| Cards | Three equal-width cards in a row | Two-column zig-zag, bento grid, or scroll gallery |
| Hero | Centered hero when variance exceeds 4 | Split screen, left-aligned, or asymmetric layout |
| Overlap | Text overlapping on images | Separate spatial cells for all text and media |
| Copywriting | AI puffery like "Seamless" or "Elevate" | Plain action copy and verified metrics |
| Metrics | Fabricated round figures (`99.99%`, `50%`) | Organic data values (such as `47.2%`) |
| Height | Fixed `100vh` or `h-screen` | Dynamic viewport height `min-h-[100dvh]` |
