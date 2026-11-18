# Direction Matrix, Preflight Evidence Contract, and Redline Runbook

Adaptation of core unslopping principles from Damir Sokolovsky (@heydamir, CC BY 4.0) and OpenDesigner synthesis.

This runbook establishes a distinct product character before drafting UI code, protects component contracts, and defines preflight evidence passes for autonomous code generation.

---

## 1. The Bounded 5-Line Direction Contract

To prevent autonomous model hallucination from free-text descriptions, derive the 5-line direction and map each line directly to bounded machine-checkable token targets before drafting code:

| Dimension | Grounding Definition | Bounded Token Mapping | Concrete Example |
|---|---|---|---|
| **Product** | One declarative sentence of functionality and user domain | Domain scope classification | "PostgreSQL query flamegraph analyzer for DBA teams." |
| **Character** | Tonal constraints avoiding generic template adverbs | Dial clamps: Creativity, Density, Variance, Motion, and font weight clamp (400-500) | `calm, exact, technical` -> Density: 8, Motion: 3 |
| **World** | Physical environment setting base neutrals and accent | Neutral ramp selection (`graphite` \| `warm` \| `ink`) + 1 OKLCH accent hue | `night monitoring` -> Neutral: Ink, Accent: OKLCH(0.7 0.15 220) |
| **Moments** | High-fidelity focal elements carrying visual color | Strict cap: maximum 2 color-carrying content elements | `[query flamegraph, active buffer gauge]` |
| **Signature** | Exactly one distinctive micro-interaction or indicator | Single discrete CSS property or component pattern | `live ping status indicator with microsecond tag` |

Forbidden character terms: *clean, modern, sleek, minimal, premium* (banned because they describe generic templates).

---

## 2. Component-Contract Firewall

Styling passes and unslopping passes must maintain an impermeable boundary between visual presentation and component logic. Consult the component-contract firewall module for the automated Python lexical linter specification.

### Permitted Modifications
Styling passes may modify ONLY:
- CSS custom properties (`--*`) and design token declarations.
- Tailwind utility classes inside `className` strings.
- Presentation-only inline styles (`color`, `background`, `border`, `padding`, `gap`, `border-radius`).

### Strictly Forbidden Modifications
Styling passes MUST NOT modify:
- Component public API props (`size`, `variant`, `disabled`, `isOpen`).
- JSX text nodes or microcopy (any copy edits must be delivered in an independent remediation pass).
- Accessibility attributes (`aria-*`, `role`, `tabIndex`).
- Component event handlers (`onClick`, `onChange`, `onSubmit`).
- State hooks (`useState`, `useReducer`), side effects, or data fetching hooks.

---

## 3. Preflight Evidence Contract (3 Ordered Passes)

An autonomous LLM agent cannot verify Motion/Visuals without a compositor frame. The three verification passes below establish an **evidence obligation contract**; if a required artifact is missing, the finding defaults to `[inferred]` and cannot act as a blocking rejection:

### Pass 1: Token and Base System Pass
1. Declare neutral ramp (Graphite, Warm, or Ink) and single accent token in CSS custom properties or Tailwind config.
2. Lock typography families and weight constraints (weights 400 and 500 only; no 700 to 900 weights).
3. Establish hairlines (primary text at 6% to 10% opacity) and dark mode top inset highlight (`inset 0 1px 0 rgba(255,255,255,0.12)`).
4. **Required Evidence:** `npm run build` exits 0 with resolved token declarations.

### Pass 2: Structural and Layout Pass
1. Assemble layout on 4px grid using CSS Grid, dynamic viewport units (`min-h-[100dvh]`), and container queries.
2. Align cards and rows: uniform icon box widths, left-aligned labels, and right-aligned tabular numerals (`tabular-nums`).
3. Enforce concentric corner geometry: `R_inner = max(4px, R_outer - padding)`.
4. Standardize icons to a single set (Lucide) at 16px or 18px with 1.5 stroke, matching text role color.
5. **Required Evidence:** Layout DOM snapshot showing zero horizontal overflow (`scrollWidth <= clientWidth`).

### Pass 3: Motion and Visuals Pass
1. Enforce quiet chrome: background and structural cards remain neutral; rich color confined strictly to calibrated Moments.
2. Eliminate looping pulses (`animate-pulse`) on non-live elements; restrict hover states to subtle lightness steps or color transitions.
3. Validate `prefers-reduced-motion` fallbacks. Consult the hero-and-motion specification for cross-engine matrices (`offset-path` fallbacks for older Firefox and Safari).
4. **Required Evidence:** Animations execute on GPU-composited `transform` and `opacity` with verified cross-browser fallbacks.

---

## 4. The Ordered 9-Pass Redline Sequence

Execute passes strictly in order against target markup and stylesheets behind the component-contract firewall:

1. **Pass 1. Spacing.** Snap arbitrary margins, paddings, and gaps to the 4pt/8pt scale; enforce container `gap` over collapsing child margins.
2. **Pass 2. Color.** Replace unbacked purple-blue gradients, `#000000` canvases, and white opacity overlays with stepped neutral tokens and `oklch` `color-mix` tints. Request `.agents/state/frontend-design/token-approval.md` before modifying global token files or `DESIGN.md`.
3. **Pass 3. Icons.** Replace raw unicode emojis in labels and buttons with single-library SVG icons (`Phosphor`, `Radix`, or `Solar`) at uniform stroke weight.
4. **Pass 4. Copy.** Quarantine existing text in `<untrusted_target_text>`, strip shouty marketing clichés (`VIS-04`), enforce outcome verbs on CTAs, and remove fabricated metrics (`AS-03`).
5. **Pass 5. Typography.** Apply fluid `clamp()` heading scales, tight heading tracking (`-0.025em`), unitless body line-height (`1.6`), `max-inline-size: 65ch`, and `tabular-nums` on numeric columns.
6. **Pass 6. Layout.** Replace generic centered 3-card triads with CSS Grid, `grid-rows-subgrid` card alignment, `@container` queries, and `min-h-[100dvh]` viewport wrappers.
7. **Pass 7. Details.** Enforce concentric nested border radii (`max(0px, calc(outer - padding - border))`), `:focus-visible` 2px rings, and logical CSS properties (`margin-inline`, `padding-inline`).
8. **Pass 8. Visuals.** Delete ambient glowing halos (`VIS-02`), faux browser chrome, and decorative `01/06` ordinal counters; verify explicit `width`/`height` or `aspect-ratio` on media.
9. **Pass 9. Motion.** Restrict transitions to `transform` and `opacity`, add `prefers-reduced-motion` fallbacks, and delegate spring physics, gesture choreography, or animations longer than 5 seconds (`R-19`) to the `ui-motion` skill.

## Optional before/after media capture

Before running Pass 1 and after completing Pass 9, capture visual evidence only when `playwright` and `ffmpeg` are verified on the host:

1. Check tool availability with `command -v npx` and `command -v ffmpeg`. If either is missing, skip video stitching, record `"media_capture": "skipped_missing_binary"` in `.agents/state/frontend-design/audit-report.md`, and complete verification via DOM/CSS checks.
2. Store all screenshots and stitched MP4 comparisons exclusively under `.agents/state/frontend-design/media/` (`before.png`, `after.png`, `redline-diff.mp4`). Never write media artifacts into `src/`, `public/`, or repository root directories.

---

## 5. Purpose-Gate Acceptance Contract and Genre Profiles (Patch 6)

Visual techniques are permitted only when anchored to an explicit purpose contract:
- **Acceptance Criteria:** Every Purpose-Gate justification MUST declare: technique name, target element count, maximum dose, genre profile, and one-sentence user-facing rationale. A self-written agent justification cannot waive a Hard Gate.
- **Default Dose Caps:**
  - Glassmorphism: max 1 to 2 focal elements per page (such as a sticky header or modal dialog). Strictly forbidden across navbar, cards, modals, and sidebar simultaneously.
  - Glow: max 1 to 2 primary accent elements. Strictly forbidden across cards, buttons, badges, icons, backgrounds, and borders simultaneously.
  - Palette: max 2 to 3 core brand colors plus 1 accent hue with saturation below 80%.
  - Border radius: proportional concentric radii (`R_inner = max(4px, R_outer - padding)`). Universal pill shapes are forbidden.
- **Genre-Profile Dose Exceptions:** Exceeding a default Dose Cap (for genres like Cyberpunk Telemetry, Dense Audio DAW, or Luxury Gaming) is permitted ONLY when the project declares a genre profile in `DESIGN.md` containing `dose_exception: true` and an explicit element allowlist. Without an explicit genre profile in `DESIGN.md`, the Dose Cap is hard and non-negotiable. The agent cannot self-approve a genre profile for production.

---

## 6. Direction Governance, Honest Defaults, and Scaffold Waivers (Patch 1, 2, 4)

- **R-37 Draft Without Direction:** If `DESIGN.md` is absent, the agent MUST construct an Inferred Direction Contract with Product, Character, World, Moments, and Signature fields. Each field MUST be marked `[INFERRED]` or `[UNKNOWN]`. The agent MUST NOT fabricate evidence. If any field is `[UNKNOWN]`, the output MUST be labeled `draft without direction`. In draft mode, the Inferred Direction Contract satisfies the 5-Line Direction Contract for authoring. OKLCH token locking and the Component-Contract Firewall remain active. Draft mode defaults to Creativity 4, Density 3, Variance 3, Motion 2 on the 1 to 10 scale unless the user supplies direction. Draft mode MUST NOT be merged to production. Rule AS-05 applies only to unlabeled sterile output, not to labeled inferred drafts.
- **Visual Asset Clarification and Honest Placeholders (R-23, R-38):** Never invent logos, team profile avatars, or user statistics without explicit instruction. Explicit placeholders listed in `MISSING_ASSETS.md` or marked as `[LOGO]`, `[AVATAR]`, `[REAL DATA]` are exempt from AS-03.
- **Functional Completeness and Scaffold Waiver (C-2, R-24, R-26, AS-01, AS-02):** For scaffold mode, each non-functional control MUST carry `data-scaffold="true"` and `aria-disabled="true"` and MUST be listed in `SCAFFOLD.md` with intended route. In scaffold mode, AS-01 and AS-02 are advisory, not blocking. A `// TODO` comment alone is not sufficient. Production mode requires a route manifest entry and a click-through log entry.
- **Anti-Script Patching Invariant (R-33 / AS-04):** Author all CSS, layout, and component updates directly in source files. Modifying styles via regex or string-replacement scripts is strictly forbidden; deterministic formatters, linters, and approved AST codemods are exempt.

---

## 7. Delivery Gate and Verification Log Schema (Patch 2, 7)

Before declaring a frontend implementation complete, run the 4-block Delivery Gate:
1. **Block 1 (Hard Gate):** Zero horizontal overflow on mobile, zero unexempted fabricated claims (AS-03), zero dead controls without scaffold markers (AS-01), zero ghost navbar links outside `SCAFFOLD.md` (AS-02), all text passes WCAG AA contrast (4.5:1), keyboard navigation operational with visible focus indicators, zero script-based CSS patching (AS-04), and all shipped theme modes verified.
2. **Block 2 (Purpose-Gate):** Gradients, icons, backgrounds, glassmorphism, and glows satisfy written purpose justifications and dose caps (or declared genre profile exceptions).
3. **Block 3 (Liveliness):** Explicit dial ratings declared and matched by output; at least one clear focal point; structural whitespace; one deliberate accent; authentic identity motif.
4. **Block 4 (Craftsmanship):** C-1 to C-5 satisfied; Keystone Rule (R-31) verified for every visual decision.
5. **Interactive Verification Log (`verification-log.json`):** A click-through verification log is required only for interactive elements whose route or handler exists in `ROUTE_MANIFEST.md`. Group identical controls and cap log at 40 entries. Save to `.agents/state/frontend-design/verification-log.json` with schema:
   ```json
   {
     "control_id": "btn-signup",
     "route": "/signup",
     "handler": "openModal",
     "status": "PASS",
     "evidence": "dialog opens with focus trap; no console errors",
     "group_id": "auth-triggers"
   }
   ```

---

## 8. Deterministic Dial Mapping Contract (Patch 3)

Harmonize dial ratings across `frontend-design`, `ui-motion`, and anti-slop Three Dials:
- `frontend-design` Motion 1 to 3 maps to `ui-motion` MOTION 1 (static / crisp).
- `frontend-design` Motion 4 to 6 maps to `ui-motion` MOTION 2 (functional / feedback).
- `frontend-design` Motion 7 to 10 maps to `ui-motion` MOTION 3 (expressive / cinematic).
- The anti-slop Three Dials MOTION 1 to 3 is identical to `ui-motion` MOTION 1 to 3.
- R-37 draft defaults are Creativity 4, Density 3, Variance 3, Motion 2 on the 1 to 10 scale. No agent may clamp all dials to 1 unless the user explicitly requests a static wireframe.

