# Kinetic typography and shimmer animations

Patterns and rules for character-level stagger entrances, text-clipped gradient shimmers, and font loading synchronization.

## 1. Character-level stagger entrances

Split headline words into individual character nodes (`<i>` or `<span>`) to execute sequential reveals. Index each character with a CSS custom property `--i`.

```html
<h1 class="headline" aria-label="Digital Studio">
  <span class="word">
    <i style="--i: 0">D</i><i style="--i: 1">i</i><i style="--i: 2">g</i>
    <i style="--i: 3">i</i><i style="--i: 4">t</i><i style="--i: 5">a</i>
    <i style="--i: 6">l</i>
  </span>
  <span class="word">
    <i style="--i: 7">S</i><i style="--i: 8">t</i><i style="--i: 9">u</i>
    <i style="--i: 10">d</i><i style="--i: 11">i</i><i style="--i: 12">o</i>
  </span>
</h1>
```

```css
.headline .word {
  display: inline-block;
  white-space: nowrap;
}

.headline i {
  display: inline-block;
  font-style: normal;
  animation: char-rise 0.8s cubic-bezier(0.22, 1, 0.36, 1) both;
  animation-delay: calc(var(--base-delay, 0ms) + var(--i, 0) * 45ms);
}

@keyframes char-rise {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
```

Keep per-character stagger delays between 30ms and 50ms. Stagger delays above 60ms draw out sentences past acceptable attention spans.

Always supply the full phrase in `aria-label` on the parent container. Screen readers struggle with fragmented single-character elements.

## 2. The blur filter hazard on typography

Applying `filter: blur(...)` to text during stagger entrances triggers continuous CPU and GPU rasterization invalidations.

Heavy blur radius values above 12px cause these defects:
- Neighboring glyph contours merge into an ink-solid block during the first 300ms.
- Ligatures, slab serifs, or tight letterforms appear as overlapping corrupted characters.
- Headless testing or automated visual regression tools capture distorted blobs if snapshots fire before blur reaches zero.

Rules for typography blur motion:
- Cap blur radius at 6px to 8px. Never exceed 12px on text elements.
- Pair blur reduction directly with opacity ramps.
- When animating text with custom display fonts or heavy weights (700+), drop `filter: blur` entirely and rely on `opacity` and `translateY`.

```css
/* Good. Sharp entrance without ink bleed */
@keyframes char-clean-in {
  0% {
    opacity: 0;
    transform: translateY(16px);
  }
  100% {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Guarded blur. Subtle 6px boundary */
@keyframes char-soft-in {
  0% {
    opacity: 0;
    transform: translateY(16px);
    filter: blur(6px);
  }
  60% {
    opacity: 1;
    filter: blur(0);
  }
  100% {
    opacity: 1;
    transform: translateY(0);
    filter: blur(0);
  }
}
```

## 3. Text-clipped gradient shimmer

Create metallic or luminous accent text by animating a linear gradient across a clipped background.

```css
.headline .shimmer-text {
  background: linear-gradient(
    110deg,
    #10b981 35%,
    #a7f3d0 50%,
    #10b981 65%
  ) 0 0 / 300% 100%;
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent !important;
  color: transparent !important;
  text-shadow: none !important;
  animation: text-shimmer 4s linear infinite;
  animation-delay: calc(var(--entrance-duration, 1.5s) + var(--i, 0) * 60ms);
}

@keyframes text-shimmer {
  0% {
    background-position: 150% 0;
  }
  40%, 100% {
    background-position: -50% 0;
  }
}
```

Rules for text-clipped animations:
- Keep the gradient aspect wide (at least `300% 100%`) so the highlight sweeps through cleanly before resting.
- Delay infinite shimmer keyframes until after the entrance transition settles. Concurrent entrance transforms and continuous gradient recalculations cause dropped frames on mobile GPUs.
- When an inline element inside the clipped block uses a distinct font family (such as a geometric ampersand), set `display: inline-block` and `vertical-align: baseline`. This prevents baseline dropouts and keeps clipping geometry continuous.

## 4. Webfont synchronization with motion

Running entrance animations while webfonts stream over the network causes Flash of Unstyled Text (FOUT) or Flash of Transformed Text (FOYT).

When a fallback font swaps to the final webfont mid-flight:
- Glyph metrics change instantly, causing layout shifts (CLS) on animated lines.
- Transform centers recalculate abruptly, causing visible jitter.
- Contours jump between different glyph shapes while opacity or blur is animating.

Rules for font synchronization:
- Host variable webfonts locally as `.woff2` files using `font-display: swap` or `font-display: optional`.
- Strip remote CDN font stylesheets that match local font families to prevent network stylesheet races.
- If using Next.js font loaders (`next/font`), bind font classes directly to the layout container rather than relying on late `@import` statements.

## 5. Headless browser verification and automated tests

Capture screenshots of animated typography only after all keyframes reach steady state:

```javascript
// Calculate total duration before snapshot
const totalDuration = entranceDurationMs + (totalChars * staggerDelayMs) + 200;
await new Promise((resolve) => setTimeout(resolve, totalDuration));
```

Verify font rendering through Chrome DevTools Protocol (CDP) before validating visual regression tests:

```javascript
// Query exact platform font used by animated glyph
const fonts = await cdpSession.send("CSS.getPlatformFontsForNode", { nodeId });
assert.strictEqual(fonts.fonts[0].isCustomFont, true);
```
