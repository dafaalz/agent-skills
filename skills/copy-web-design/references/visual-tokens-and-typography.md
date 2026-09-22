# Reverse-Engineering Visual Tokens and Typography

Technical manual for extracting OKLCH color systems, Display P3 wide-gamut palettes, variable typography, fluid spatial scales, and layered elevation shadows from modern web applications.

## Token Extraction Foundations

Reverse-engineering visual tokens requires distinguishing between raw absolute computed pixel values calculated by the browser layout engine and underlying mathematical formulas declared by designers.

The following eight authoritative sources define token reverse engineering:

### 1. High Definition CSS Color Guide
Author: Adam Argyle, Chrome for Developers (Google).
Official source: https://developer.chrome.com/docs/css-ui/high-definition-css-color-guide

Details the transition from 8-bit sRGB color spaces to Display P3 and Rec.2020 through CSS Color Module Level 4. Modern browser engines render up to 50 percent wider color gamuts using `oklch(L C H)` and `color(display-p3 r g b)` functions.

Extraction methodology:
* Inspect CSS declarations in the DevTools Styles pane to identify wide-gamut color tokens.
* Test display gamut adaptation using `@media (color-gamut: p3)`.
* Deconstruct interactive color states declared with `color-mix(in oklch, var(--primary) 80%, black)`. This approach derives hover and active states without separate color declarations.
* Check the DevTools Color Picker gamut line to verify if target colors exceed sRGB boundaries.

### 2. OKLCH in CSS: Why We Moved from RGB and HSL
Author: Andrey Sitnik, Evil Martians.
Official source: https://evilmartians.com/chronicles/oklch-in-css-why-we-moved-from-rgb-and-hsl

Highlights human visual perception flaws in standard HSL and RGB, where mathematical lightness does not match perceived brightness across hues. OKLCH provides a perceptually uniform color space.

Extraction methodology:
* Map palette shades (50 through 900) by locking the Hue angle while manipulating Lightness and Chroma values.
* Audit accessibility contrast mathematically. In OKLCH, the Lightness difference between background and text predicts readability accurately.
* Avoid gamut clipping caused by excessive Chroma. Over-saturated values clip against physical display limits, shifting hues unexpectedly.

### 3. Variable Fonts Guide
Author: MDN Web Docs (Mozilla Developer Network).
Official source: https://developer.mozilla.org/en-US/docs/Learn/CSS/Styling_text/Variable_fonts_guide

Details the OpenType Variable Fonts specification, which packs full weight, width, and slant variations into a single WOFF2 binary.

Extraction methodology:
* Filter Network requests by Font type and download `.woff2` assets.
* Inspect `@font-face` blocks to identify supported axis ranges, such as `font-weight: 100 900;`.
* Catalog registered axes: `wght` (weight), `wdth` (width), `slnt` (slant), `ital` (italic), and `opsz` (optical sizing).
* Identify custom axes defined with uppercase four-letter tags, such as `CASL` for casual variations.
* Use the Chrome DevTools Font Editor to inspect variable font sliders directly in the browser.

### 4. Meet Utopia: Designing And Building With Fluid Type And Space Scales
Authors: Trys Mudford and James Gilyead, Smashing Magazine.
Official source: https://www.smashingmagazine.com/2021/04/meet-utopia-fluid-type-space-scales/

Replaces fragmented breakpoint media queries with continuous fluid interpolation curves using `clamp()`.

Fluid curve formula:
```css
font-size: clamp(1.25rem, 1rem + 1.25vw, 2.5rem);
```

Extraction methodology:
* Measure computed `font-size` on headings across two viewports, such as 320px and 1280px.
* Calculate the modular scale ratio by dividing consecutive heading sizes (H1 by H2, H2 by H3). Common modular scale ratios include Minor Third (1.200), Major Third (1.250), and Perfect Fourth (1.333).
* Use relative `rem` units for minimum and maximum bounds to preserve browser accessibility zoom functionality.

### 5. Space in Design Systems
Author: Nathan Curtis, EightShapes.
Official source: https://medium.com/eightshapes-llc/space-in-design-systems-188bcbae0d62

Defines spatial token taxonomies built on 4px or 8px grid foundations.

Extraction methodology:
* Inspect Box Model metrics across primary UI containers to find the greatest common divisor (typically 4px or 8px).
* Classify spatial layouts into Nathan Curtis taxonomy patterns:
  1. Inset: symmetrical container padding.
  2. Squish Inset: tighter vertical padding than horizontal padding, standard for buttons and badges.
  3. Stretch Inset: taller vertical padding than horizontal padding.
  4. Stack: vertical rhythm between stacked sibling elements.
  5. Inline: horizontal spacing between adjacent inline elements.

### 6. Designing Beautiful Shadows in CSS
Author: Josh W. Comeau.
Official source: https://www.joshwcomeau.com/css/designing-shadows/

Deconstructs natural light physics into multi-layered box-shadow declarations.

Extraction methodology:
* Realistic elevation requires stacking two to four shadow layers.
* The first layer (umbra) provides sharp, high-opacity contact definition with minimal blur. Secondary layers (penumbra) provide broad, soft ambient diffusion with high blur and lower opacity.
* Apply chromatic shadow tinting by blending dark accents of the background or primary brand color instead of flat black `rgba(0, 0, 0, 0.25)`.

Layered shadow structure:
```css
box-shadow:
  0 1px 2px oklch(0.2 0.04 260 / 0.08),
  0 4px 8px oklch(0.2 0.04 260 / 0.06),
  0 12px 24px oklch(0.2 0.04 260 / 0.04);
```

### 7. How to Get All Custom Properties on a Page in JavaScript
Author: Tyler Gaw, CSS-Tricks.
Official source: https://css-tricks.com/how-to-get-all-custom-properties-on-a-page-in-javascript/

Provides JavaScript techniques for programmatic CSSOM traversal to extract declared CSS Custom Properties.

Extraction methodology:
* Traverse stylesheets through `document.styleSheets`.
* Filter for same-origin rules to prevent browser `SecurityError` exceptions when reading `sheet.cssRules`.
* Extract properties starting with `--` declared on `:root` and `html` selectors.
* Combine CSSOM rule scanning with `getComputedStyle(document.documentElement)` to capture resolved runtime values.

### 8. CSS Features Reference and Inspection
Author: Chrome for Developers (Google).
Official source: https://developer.chrome.com/docs/devtools/css

Technical reference for the Blink layout and rendering engine.

Extraction methodology:
* Distinguish between authored CSS in the Styles pane and resolved computed values in the Computed pane. Avoid copying static computed pixel metrics when elements rely on fluid expressions.
* Use CSS variable drill-down by hovering over `var(--token)` to trace fallback definitions and jump to declaration scopes.
* Run the CSS Coverage panel (`Cmd + Shift + P` then type `Show Coverage`) to prune unused class definitions and dormant tokens from production dumps.

---

## Token Extraction Execution Steps

1. Run the token extraction script in the browser console to gather declared custom properties and computed values.
2. Group extracted tokens into colors, typography, spacing scales, elevation shadows, and border radii.
3. Convert legacy hex values to OKLCH Display P3 definitions for wide-gamut monitors.
4. Document fluid typography formulas using `clamp()` expressions with modular scale steps.
5. Export clean tokens into a Tailwind CSS v4 `@theme` block or standard modern `:root` stylesheet.
