---
name: redesign-existing-projects
description: Use when auditing or updating an existing website, web app, or frontend UI to replace generic AI patterns, fix typography and layout issues, or improve polish without changing tech stacks.
---

# Redesigning existing projects

Audit and upgrade existing web interfaces by eliminating generic patterns, improving hierarchy, and polishing interactions within the active tech stack.

## Workflow

Follow these four steps in sequence:

### Step 1. Stack and convention scan

Inspect the codebase before editing any visual files:

- Identify the framework, styling solution (Tailwind, vanilla CSS, CSS modules, styled-components), and existing component library.
- Check package versions in `package.json` or project manifests (for example, Tailwind CSS v3 versus v4) to prevent syntax incompatibilities.
- Audit existing color tokens, fonts, and responsive breakpoint conventions.

Completion criterion. A recorded inventory of the project styling stack, active color tokens, and package dependencies.

### Step 2. Gap analysis and pattern audit

Read `references/design-audit.md` to evaluate target pages against concrete design standards:

- Audit typography, color palettes, surface textures, grid layouts, interactive states, and content quality.
- Record every detected issue along with its exact file path and CSS selector or class name.
- Note components that already follow clean patterns to prevent regressions during edits.

Completion criterion. A written audit report mapping detected flaws directly to file paths and selectors.

### Step 3. Phased refinement execution

Consult `references/upgrade-techniques.md` for concrete replacement patterns:

- Apply modifications strictly according to the fix priority list below.
- Keep changes incremental and reviewable. Modify existing component templates rather than rewriting them from scratch.
- Preserve existing application logic, state handlers, and routing.

Completion criterion. Incremental styling changes applied to target files without broken imports or altered business logic.

### Step 4. Visual and regression verification

Verify changes across viewports and interaction states:

- Test responsive layout behavior at mobile (375px), tablet (768px), and desktop (1280px) widths.
- Confirm keyboard focus indicators, hover feedback, and pressed states function as intended.
- Run project build or test commands to confirm that no syntax or styling errors were introduced.

Completion criterion. Build and test commands pass with zero errors, and all modified components render without visual defects.

## Fix priority

Apply changes in this sequence to deliver maximum visual improvement with minimal regression risk:

1. Font selection and display hierarchy
2. Color palette cleanup and accent consolidation
3. Hover, active, and keyboard focus states
4. Layout constraints, grid structure, and whitespace
5. Component pattern replacements (cards, badges, navigation)
6. Loading, empty, and error feedback states
7. Typography fine-tuning (tracking, line-height, text-wrap)

## Core rules

- Work within the existing stack. Never migrate frameworks or introduce alternate styling libraries without explicit instructions.
- Preserve existing functionality. Test behavior after every change.
- Verify dependency existence in package manifests before adding imports.
- Default to vanilla CSS if the project does not use a CSS framework.
- Keep modifications small, focused, and reviewable.

## Quick reference checklist

Run this check before completing any redesign task:

| Check | Passing condition |
|---|---|
| AI vocabulary | Zero promotional buzzwords (elevate, unleash, next-gen, delve, tapestry) in interface copy |
| Dash punctuation | Zero em dashes, en dashes, or hyphens acting as dashes in documentation and UI text |
| Focus rings | High-contrast focus indicators present on every keyboard-focusable element |
| Viewport stability | Layout renders without horizontal overflow or breakage at 375px viewport width |
| Contrast ratio | Text meets WCAG AA 4.5:1 contrast against its background surface |
| Framework integrity | Existing tech stack preserved without introducing unauthorized dependencies |
