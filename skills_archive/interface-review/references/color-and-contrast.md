# Color systems, perceptual contrast, and design tokens

Audit perceptual color contrast, design token hierarchies, modern color spaces, dark mode architectures, and system contrast modes.

## Authoritative sources

| Source | Author or organization | Domain | Official URL |
| --- | --- | --- | --- |
| Accessible Perceptual Contrast Algorithm (APCA) | Andrew Somers, Myndex Research | Perceptual contrast modeling | https://github.com/Myndex/SAPC-APCA |
| W3C Silver Visual Contrast Subgroup Documentation | W3C Accessibility Guidelines WG | Next-generation contrast rules | https://www.w3.org/WAI/GL/task-forces/silver/wiki/Visual_Contrast_Subgroup |
| Design Tokens Format Module v2025.10 | W3C Design Tokens Community Group | Standard token specifications | https://tr.designtokens.org/format/ |
| The Science of Color and Design | Google Material Design Team | Color science in software | https://m3.material.io/blog/science-of-color-design |
| Material Design 3 Color Roles and Surface Containers | Google Material Design | Surface container hierarchy | https://m3.material.io/styles/color/the-color-system/color-roles |
| Material Color Utilities Engine (CAM16 and HCT) | Google Material Foundation | Algorithmic tonal palettes | https://github.com/material-foundation/material-color-utilities |
| CSS Color Module Level 4 | W3C CSS Working Group | OKLCH and wide gamut colors | https://www.w3.org/TR/css-color-4/ |
| A Perceptual Color Space for Computer Graphics: Oklab | Björn Ottosson | Perceptually uniform color math | https://bottosson.github.io/posts/oklab/ |
| OKLCH in CSS: Why We Moved Away from RGB and HSL | Andrey Sitnik and Roman Shamin, Evil Martians | Practical OKLCH engineering | https://evilmartians.com/chronicles/oklch-in-css-why-quit-rgb-hsl |
| Styling for Windows High Contrast with Forced Colors | Melanie Richards, Microsoft Edge Team | System forced-colors standards | https://blogs.windows.com/msedgedev/2020/09/17/styling-for-windows-high-contrast-with-new-standards-for-forced-colors/ |
| Material Design Dark Theme Architecture | Google Material Design | Dark mode surface engineering | https://m2.material.io/design/color/dark-theme.html |

## 1. APCA versus WCAG 2.1 contrast modeling

WCAG 2.1 calculates contrast using the formula `(L1 + 0.05) / (L2 + 0.05)`. This formula treats contrast symmetrically across positive polarity (dark text on light background) and negative polarity (light text on dark background).

Human visual biology operates non-linearly:
- **Halation and irradiation.** In dark mode, light text emits scattered photons across astigmatic retinas, causing thin white fonts to blur into background darkness. Conversely, in light mode, bright backgrounds constrict pupils, sharpening optical edges for dark body text.
- **Spatial frequency.** Human contrast perception depends heavily on font weight and glyph size. A contrast ratio that provides legibility for bold 24px headings is illegible for thin 13px captions.
- **APCA solution.** The Accessible Perceptual Contrast Algorithm calculates Lightness Contrast (`Lc`). APCA accounts for spatial frequency, font weight, background luminance, and polarity. Body text requires at least `Lc 75` to `Lc 90`. Large headings require `Lc 60`. Non-text interface components require `Lc 45`.

## 2. W3C Design Tokens Community Group (DTCG) 3-tier architecture

Maintain strict boundary separation across three distinct token tiers:

1. **Global or primitive tokens.**
   - Encapsulate raw, context-agnostic values.
   - Examples: `--primitive-blue-500: oklch(0.55 0.20 250);`, `--primitive-neutral-100: oklch(0.98 0.005 260);`.
   - Primitive tokens must never be referenced directly inside UI component templates.
2. **Semantic or alias tokens.**
   - Bind primitive values to functional intent and theme contexts.
   - Examples: `--color-surface: var(--primitive-neutral-100);`, `--color-text-primary: var(--primitive-neutral-900);`.
   - Theme switching (light and dark mode) occurs exclusively at the semantic tier. Component templates consume semantic tokens whose references swap underneath.
3. **Component tokens.**
   - Scope styling parameters to specific component boundaries.
   - Examples: `--button-primary-bg: var(--color-action-primary-bg);`, `--card-elevation-bg: var(--color-surface-container);`.
   - Prevents tight coupling between individual UI controls and global design palettes.

## 3. Google Material Design 3 HCT and surface container hierarchy

Google engineered the HCT (Hue, Chroma, Tone) color space by pairing CAM16 color appearance models with CIELAB `L*` luminance:

- **Tone independence.** Tone ranges from 0 (pure black) to 100 (pure white). The perceptual contrast between two colors depends entirely on their Tone delta. A Tone delta of 50 points or greater guarantees WCAG AA legibility regardless of hue.
- **Discrete surface containers.** Material 3 deprecates opacity-based surface tinting (`surfaceTintColor`), replacing it with explicit container tokens:
  - `surface-container-lowest`: Deepest recessed surfaces.
  - `surface-container-low`: Baseline page canvas.
  - `surface-container`: Standard modular cards.
  - `surface-container-high`: Popovers, dropdown menus, and sheet overlays.
  - `surface-container-highest`: Prominent dialogs and floating action surfaces.

Elevation and depth communicate through discrete lightness shifts rather than semi-transparent white overlays.

## 4. Modern color spaces with OKLCH and Display P3

Legacy sRGB and HSL color spaces distort lightness across different hues. Pure yellow `hsl(60, 100%, 50%)` and pure blue `hsl(240, 100%, 50%)` share an identical 50 percent lightness declaration in HSL, yet human eye cone sensitivity perceives yellow as blindingly bright (relative luminance 0.93) and blue as dark (relative luminance 0.07).

### OKLCH advantages
`oklch(L C H)` delivers perceptual uniformity:
- `L` (Perceptual Lightness): Two colors sharing an identical `L` value (such as `0.70`) possess identical perceived brightness across all hues.
- `C` (Chroma): Saturation scales smoothly without shifting hue angles.
- `H` (Hue Angle): Continuous 360-degree color wheel without hue distortion.
- **Wide Color Gamut (Display P3).** OKLCH unlocks rich emeralds, high-chroma oranges, and saturated purples unavailable within constrained sRGB monitors.

## 5. Dark mode architecture rules

### Canvas baseline
Never apply pure black `#000000` to large surface containers. Extreme luminance contrast between pure black canvas and bright text triggers halation and rapid ocular fatigue. Declare neutral dark gray baselines (OKLCH Lightness 0.16 to 0.20, such as `#121212`). Pure black is reserved strictly for OLED battery-saving modes.

### Accent desaturation
Primary brand colors configured for light mode become intensely oversaturated on dark surfaces, inducing chromostereopsis (visual vibration and focal discomfort). Reduce Chroma by 25 to 35 percent and increase Lightness when mapping accents to dark mode:

```css
:root {
  --color-primary: oklch(0.52 0.24 260); /* Saturated for light mode */
}

@media (prefers-color-scheme: dark) {
  :root {
    --color-primary: oklch(0.72 0.14 260); /* Desaturated, lighter for dark mode */
  }
}
```

### Elevation without opacity stacking
Stacking semi-transparent white layers (`rgba(255, 255, 255, 0.08)`) produces unpredictable blending artifacts when cards nest inside dialogs. Define distinct semantic surface tokens based on explicit lightness increments:

```css
@media (prefers-color-scheme: dark) {
  :root {
    --color-surface: oklch(0.18 0.01 260);
    --color-surface-container-low: oklch(0.22 0.01 260);
    --color-surface-container: oklch(0.26 0.01 260);
    --color-surface-container-high: oklch(0.30 0.01 260);
  }
}
```

## 6. Windows Contrast Themes and forced-colors compatibility

Windows Contrast Themes (High Contrast Mode) assists users with low vision or photophobia. When active, browsers activate `@media (forced-colors: active)`:

- Browsers strip author colors (`color`, `background-color`, `box-shadow`, `border-color`).
- Flat designs that rely exclusively on drop shadows or subtle background tints lose visual boundaries entirely, becoming invisible.
- Declare transparent borders (`border: 1px solid transparent;`) on all interactive controls (buttons, inputs, cards). Forced-colors mode replaces transparent borders with system-defined outline colors, preserving component affordances.

```css
.btn-control {
  background-color: var(--color-action-bg);
  color: var(--color-action-text);
  border: 1px solid transparent;
}

@media (forced-colors: active) {
  .btn-control {
    background-color: ButtonFace;
    color: ButtonText;
    border-color: ButtonText;
  }

  .btn-control:focus-visible {
    outline: 2px solid Highlight;
    outline-offset: 2px;
  }
}
```

## 7. Color audit checklist

1. **Dual-engine contrast check.** Validate text using WCAG 2.1 (minimum 4.5:1 for body copy, 3:1 for large headings) and verify with APCA (`Lc 75` for body text).
2. **Three-tier token isolation.** Confirm components reference semantic tokens rather than raw primitive hex values.
3. **Dark mode halation check.** Verify canvas backgrounds maintain OKLCH lightness of at least 0.16.
4. **Forced-colors preservation.** Confirm buttons, cards, and input fields declare physical or transparent borders to survive high-contrast mode stripping.
