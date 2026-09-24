---
name: hallmark
description: Use when building greenfield pages, auditing UI quality, redesigning interfaces, or extracting design tokens from URLs and screenshots.
---

# Hallmark

Anti-slop design system for software engineering agents. Enforces structural variety, typography purity, and honest copy across greenfield builds, audits, redesigns, and design extraction.

Hallmark eliminates generic AI visual defaults. Two pages designed for different briefs should never share the same layout rhythm, feature cards, or color templates. Consult `references/structure.md` for macro-structural patterns.

## Workflow verbs

Identify the active verb from the user request:

| Invocation | Action |
|---|---|
| *(default)* | Build or design a new page or application. Follow the Design flow below. |
| `hallmark audit <target>` | Inspect target against anti-patterns and return a punch list. Do not edit. Read `references/verbs/audit.md`. |
| `hallmark redesign <target>` | Redesign visual structure within existing implementation boundaries. Read `references/verbs/redesign.md`. |
| `hallmark study <target>` | Extract design tokens, type pairings, and macrostructure from a URL or screenshot. Read `references/study.md`. |
| Component brief | When the brief targets a single element (button, modal, card), follow `references/component-scope.md`. |

Safety invariant. Never delete production files or route trees without explicit user confirmation.

## Core design disciplines

Apply these seven disciplines across all verbs:

1. **Pre-emit self-critique.** Score output 1 to 5 on Philosophy, Hierarchy, Execution, Specificity, Restraint, and Variety. Scores under 3 require revision. Stamp scores at the artifact header. Consult `references/slop-test.md`.
2. **Honest copy without fabricated content.** Never invent metrics, testimonials, customer counts, or speed multipliers. Use verified numbers, explicit placeholders, or alternative layouts. Consult `references/anti-patterns.md`.
3. **Locked tokens without improvisation.** Declare colors and typography as CSS custom properties. Reference named tokens exclusively in component code. Never inline arbitrary color values. Consult `references/custom-theme.md`.
4. **No fake browser or device chrome.** Do not hand-build faux URL bars, traffic-light window dots, or simulated phone frames. Present content cleanly on its own.
5. **Verified mobile responsiveness.** Test layouts at 320px, 375px, 414px, and 768px. Ensure horizontal scroll is clipped, text wraps cleanly, and click targets never break across two lines. Consult `references/responsive.md`.
6. **Typography purity without italic headers.** Keep headings upright and roman. Emphasize heading words using font weight, color, or underlines, never italics. Reserve italics for running body prose.
7. **Real brand assets over synthetic placeholders.** Brand identity lives in authentic assets, not arbitrary hex codes or CSS shapes. Source authentic SVG or PNG logos, real device photography for hardware, and verified UI screenshots for software. Never substitute hand-drawn CSS silhouettes or colored rectangles for real product imagery.

## Design flow

Follow these eight steps in sequence:

### Step 0. Pre-flight scan

Inspect existing project configurations before proposing design changes:
- Read `package.json`, `tailwind.config.*`, or active CSS files to extract existing typography and color variables.
- Detect existing design tokens and framework constraints to avoid stomping on current brand rules.
- Answer four positioning checks before declaring tokens: Narrative role (hero, transition, data, pull-quote, closing), viewing distance (phone, monitor, projector), visual temperature (quiet, energized, authoritative, warm, playful), and capacity check (evaluate whether content density fills the layout naturally without artificial padding).

Completion criterion. Existing repository styles, tokens, and frameworks documented with zero unverified assumptions.

### Step 1. Context gate and genre detection

Classify the project into one of four visual genres:
- Editorial, modern minimal, atmospheric, or playful.
- Identify creative intent signals such as brand colors or specific mood keywords.

Completion criterion. A confirmed genre and confirmed creative-intent signals recorded in working notes.

### Step 2. Macrostructure selection

Select a distinct page layout macrostructure before writing code:
- Choose an arrangement from `references/macrostructures.md` that fits the content density.
- Do not repeat default hero-feature-cta templates.

Completion criterion. A macrostructure selected and mapped to the user brief.

### Step 3. Theme route and token locking

Establish the palette and typography tokens:
- Pick a curated theme from `references/themes/` or construct an OKLCH palette following `references/custom-theme.md`.
- Define typography with one display face, one body face, and an optional mono face.

Completion criterion. Complete CSS custom properties defined for all primary, neutral, and accent tokens.

### Step 4. Hero enrichment decision

Determine the hero section layout and focal element:
- Select an enrichment pattern from `references/hero-enrichment.md` (interactive demo, technical schematic, or focused headline).
- Keep hero copy concise and directly tied to the primary user action.

Completion criterion. Hero layout pattern selected with confirmed visual asset boundaries.

### Step 5. Multi-section preview

Present a structural outline or draft layout to the user:
- Show section rhythm, typography pairings, and interaction models before building deep implementation code.
- Confirm direction with the user.

Completion criterion. The user explicitly approves the layout outline.

### Step 6. Production code build

Synthesize complete production components matching project standards:
- Assemble components using semantic HTML5, CSS Grid, and project styling libraries.
- For component patterns, consult `references/component-cookbook.md` and `references/components/`.

Completion criterion. Complete, functional code delivered with zero placeholder comments or omitted blocks.

### Step 7. Slop test verification

Audit generated code against anti-slop rules before completion:
- Verify zero banned AI design clichés, proper color contrast, and correct responsive behavior.
- Run checks defined in `references/slop-test.md`.

Completion criterion. The artifact passes all slop test gates with zero violations.

## Quick reference checklist

Run this check before delivering UI designs:

| Check | Passing condition |
|---|---|
| Token discipline | All colors and fonts reference named tokens with zero inline arbitrary values |
| Copy integrity | Zero fabricated statistics, metrics, or false customer claims |
| Chrome purity | Zero fake browser frames, device mockups, or decorative window dots |
| Responsive floor | Flawless rendering verified across mobile and desktop breakpoints |
| Typography rules | Roman headings without italics, paired with appropriate body type |
| Anti-slop gate | Completed design passes all checks in references/slop-test.md |
