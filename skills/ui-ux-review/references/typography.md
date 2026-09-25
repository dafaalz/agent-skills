# Typography, readability, and font mechanics

Audit typographic hierarchy, measure, leading proportions, modular scales, font loading mechanics, and rendering stability.

## Authoritative sources

| Source | Author or organization | Domain | Official URL |
| --- | --- | --- | --- |
| The Elements of Typographic Style Applied to the Web | Richard Rutter and Robert Bringhurst | Web typography principles | https://webtypography.net/ |
| Web Design is 95% Typography (2006) | Oliver Reichenstein, iA | Text-centric design manifesto | https://ia.net/topics/the-web-is-all-about-typography-period |
| Flexible Typesetting (2018) | Tim Brown, A Book Apart | Responsive typographic systems | https://abookapart.com/products/flexible-typesetting |
| More Meaningful Typography | Tim Brown, A List Apart | Musical intervals and scale | https://alistapart.com/article/more-meaningful-typography/ |
| Modular Scale Calculator | Scott Kellum and Tim Brown | Proportional ratio calculation | https://www.modularscale.com/ |
| CSS Text Module Level 4: text-wrap | W3C CSS Working Group | Line breaking and wrapping | https://www.w3.org/TR/css-text-4/ |
| CSS Fonts Module Level 4 | W3C CSS Working Group | Variable fonts and OpenType | https://www.w3.org/TR/css-fonts-4/ |
| Understanding WCAG 2.2: Visual Presentation (SC 1.4.8) | W3C Web Accessibility Initiative | Line length and spacing rules | https://www.w3.org/WAI/WCAG22/Understanding/visual-presentation.html |
| Understanding WCAG 2.2: Text Spacing (SC 1.4.12) | W3C Web Accessibility Initiative | Spacing override standards | https://www.w3.org/WAI/WCAG22/Understanding/text-spacing.html |
| Avoid Invisible Text During Font Loading | Google Chrome Team, web.dev | Font loading and FOUT mitigation | https://web.dev/articles/font-display |

## 1. Typographic theory and structural hierarchy

### Bringhurst and Rutter web typography doctrines
Robert Bringhurst established that typography exists to guide the reader's eye without demanding conscious attention. Richard Rutter translated these classical rules to digital CSS layout, emphasizing measure, proportional leading, vertical baseline rhythm, and character wrapping.

### Oliver Reichenstein on 95 percent typography
Oliver Reichenstein articulated that 95 percent of all interface communication on the web consists of written text. Interface design is fundamentally typographic engineering, dividing into macro-typography (content hierarchy, structural whitespace) and micro-typography (tracking, kerning, leading, and tabular alignment).

### Tim Brown modular scale
A modular scale establishes an interrelated hierarchy of font sizes based on a fixed mathematical ratio:
- **Minor Third (1.200).** Compact scale suited for dense data grids and mobile screens.
- **Major Third (1.250).** Standard balanced scale for general web applications.
- **Perfect Fourth (1.333).** Expressive scale suited for marketing and editorial content.
- **Golden Ratio (1.618).** High-contrast scale for large display headlines.

Size calculation formula: `Size_n = Base_Size * (Ratio ^ n)`.

Scale progression using a 16px (1rem) base with a Major Third (1.250) ratio:
- Body text (Step 0): `1.000rem` (16px)
- Heading 4 (Step 1): `1.250rem` (20px)
- Heading 3 (Step 2): `1.563rem` (25px)
- Heading 2 (Step 3): `1.953rem` (31.25px)
- Heading 1 (Step 4): `2.441rem` (39.06px)

### Measure and line length
Measure represents the horizontal width of a text block:
- Optimal reading comfort falls between 45 and 75 characters per line (CPL), with 66 CPL as the empirical ideal.
- WCAG 1.4.8 mandates an absolute maximum of 80 characters per line for body copy.
- Lines exceeding 80 characters cause eye fatigue and scanning failures during return saccades. Lines shorter than 40 characters fragment sentence structure.
- Constrain reading containers using `max-inline-size: 65ch;`.
- Apply `text-wrap: balance;` to display headings to eliminate lonely orphan words.
- Apply `text-wrap: pretty;` to body copy to prevent orphan words on paragraph ending lines.

### Leading and vertical rhythm
Leading (`line-height`) must scale inversely with font size:
- Body copy (16px to 20px): Requires a line height between 1.45 and 1.6.
- Large display headings (32px and above): Requires tight leading between 1.1 and 1.25. Loose leading on large text fragments headings into disconnected lines.
- Captions and labels (11px to 13px): Requires leading between 1.35 and 1.45 to maintain character legibility.
- Never declare fixed units (`px`, `pt`, `em`) for `line-height`. Always specify unitless values (such as `line-height: 1.5;`) so leading inherits proportionally across child elements.

## 2. Modern font mechanics and rendering performance

### Variable fonts
Variable fonts encapsulate multiple weights, widths, and optical sizes into a single WOFF2 file. This replaces dozens of individual font requests, reducing HTTP requests and payload weights:

```css
@font-face {
  font-family: 'Inter Variable';
  src: url('/fonts/Inter-Variable.woff2') format('woff2');
  font-weight: 100 900;
  font-display: swap;
}
```

### Tabular numbers
Proportional numerical glyphs possess varying widths. In data tables, financial reports, clocks, and animated counters, proportional numbers produce horizontal layout jitter when values change. Always declare tabular figures:

```css
.numeric-data {
  font-variant-numeric: tabular-nums;
  font-feature-settings: "tnum" 1;
}
```

### Font loading strategies with FOUT versus FOIT
- Avoid Flash of Invisible Text (FOIT) by rejecting `font-display: block`.
- Use `font-display: swap` for body text to show fallback fonts immediately while web fonts download.
- Use `font-display: optional` for non-critical decorative fonts to enforce a 100ms download window, eliminating layout shift if the network is constrained.
- Preload critical fonts in the HTML document `<head>`:

```html
<link rel="preload" href="/fonts/inter.woff2" as="font" type="font/woff2" crossorigin>
```

- Mitigate Flash of Unstyled Text (FOUT) layout shift using `@font-face` metric overrides on local fallback fonts:

```css
@font-face {
  font-family: 'Fallback-Arial';
  src: local('Arial');
  ascent-override: 90%;
  descent-override: 22%;
  size-adjust: 105%;
}
```

## 3. Quantitative typography audit rules

### Fluid typography clamp formula
Interpolate font size linearly between minimum and maximum viewport boundaries without media query snapping:

`font-size: clamp(MIN_SIZE, INTERCEPT + SLOPE * 1vw, MAX_SIZE)`

Mathematical calculation:
- Minimum size: 16px (1rem) at 320px (20rem) viewport.
- Maximum size: 20px (1.25rem) at 1280px (80rem) viewport.
- Size difference: `20 - 16 = 4px`.
- Viewport difference: `1280 - 320 = 960px`.
- Slope: `4 / 960 = 0.004167` (equivalent to `0.4167vw`).
- Intercept: `16 - (0.004167 * 320) = 14.667px` (equivalent to `0.9167rem`).

Resulting CSS declaration:

```css
body {
  font-size: clamp(1rem, 0.9167rem + 0.4167vw, 1.25rem);
}
```

### Synthetic font disabling
Browsers automatically generate artificial bold and slanted glyphs if an explicit weight or italic font file is missing, producing distorted letterforms:

```css
html {
  font-synthesis: none;
}
```

### Root font size accessibility
Never overwrite the root font size with static pixels (`html { font-size: 16px; }`). Hardcoded pixel root sizes override user browser zoom preferences, violating accessibility standards. Always declare relative root sizing:

```css
html {
  font-size: 100%;
}
```

## 4. Typography anti-patterns and solutions

### Unbounded body text
```css
/* Bad: Reading lines stretch endlessly across large viewports */
.article-text {
  inline-size: 100%;
}

/* Good: Measure constrained to readable character count */
.article-text {
  max-inline-size: 65ch;
  text-wrap: pretty;
}
```

### Justified text without hyphenation
Raw justified text produces uneven spacing gaps (typographic rivers) because web engines lack micro-spacing typography algorithms.

```css
/* Bad: Causes rivers of white space across paragraphs */
p {
  text-align: justify;
}

/* Good: Natural left alignment */
p {
  text-align: start;
}
```

### Proportional numbers in data grids
```css
/* Bad: Numbers shift horizontally as digits change */
.balance-table td {
  font-variant-numeric: normal;
}

/* Good: Equal character widths across all digits */
.balance-table td {
  font-variant-numeric: tabular-nums;
}
```
