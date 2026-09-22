# Component mechanics, tactile polish, and modern CSS

Audit component anatomy, concentric corner geometry, native popovers, anchor positioning, relational selectors, and micro-interaction tactile feedback.

## Authoritative sources

| Source | Author or organization | Domain | Official URL |
| --- | --- | --- | --- |
| CSS Backgrounds and Borders Module Level 3 (§5.3 Corner Shaping) | W3C CSS Working Group | Corner curvature mathematics | https://www.w3.org/TR/css-backgrounds-3/#corner-shaping |
| Human Interface Guidelines: Controls and Views | Apple Inc. | Platform component standards | https://developer.apple.com/design/human-interface-guidelines/buttons |
| Material Design 3 Components System | Google Design | Component states and tokens | https://m3.material.io/components/buttons/overview |
| Material Design 3 Motion Guidelines | Google Design | Standard UI easings | https://m3.material.io/styles/motion/easing-and-duration |
| Popover API Specification and Guide | MDN Web Docs / Open Web Docs | Native top-layer popovers | https://developer.mozilla.org/en-US/docs/Web/API/Popover_API |
| CSS Anchor Positioning Module Level 1 | W3C CSS Working Group | Floating tether positioning | https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_anchor_positioning |
| CSS @starting-style and Discrete Transitions | W3C CSS Working Group | Zero-JS entry and exit motion | https://developer.mozilla.org/en-US/docs/Web/CSS/@starting-style |
| CSS Selectors Level 4: The :has() Relational Selector | W3C CSS Working Group | Parent and contextual styling | https://developer.mozilla.org/en-US/docs/Web/CSS/:has |
| CSS Media Queries Level 4: Pointer and Hover Features | W3C CSS Working Group | Hardware pointer detection | https://developer.mozilla.org/en-US/docs/Web/CSS/@media/hover |
| Cumulative Layout Shift Prevention and Layout Stability | Google Chromium Team, web.dev | Dimensional containment | https://web.dev/articles/cls |

## 1. Concentric border radii geometry

Nesting rounded elements requires concentric curvature. When a child container shares an identical `border-radius` with its parent, the inner corner appears visually pinched and deformed.

### The concentric formula
The inner radius must equal the outer radius minus the intervening padding and border thickness:

`R_inner = max(0, R_outer - (padding + border_width))`

Boundary conditions:
- If padding is equal to or greater than the outer radius, the inner corner must be set to 0.
- When padding differs across X and Y axes, declare elliptical radii using CSS `calc()`:

```css
.card {
  --card-padding: 16px;
  --card-radius: 24px;
  --border-width: 1px;

  padding: var(--card-padding);
  border: var(--border-width) solid rgba(255, 255, 255, 0.1);
  border-radius: var(--card-radius);
}

.card-badge {
  border-radius: max(0px, calc(var(--card-radius) - var(--card-padding) - var(--border-width)));
}
```

## 2. Native HTML Popover API and CSS Anchor Positioning

Modern web engines provide native top-layer popovers and anchor tethering, eliminating third-party JavaScript floating positioning libraries:

### Popover API
Declare `popover="auto"` on floating dialogs and link them via `popovertarget`:
- Renders directly in the browser top layer, eliminating `z-index` stacking conflicts and parent `overflow: hidden` clipping.
- Provides native light-dismiss on outside clicks and handles the `Escape` key automatically.

```html
<button popovertarget="action-menu" style="anchor-name: --menu-trigger;">
  Actions
</button>

<div id="action-menu" popover="auto" class="anchor-popover">
  <p>Menu content</p>
</div>
```

### CSS Anchor Positioning
Tether floating menus directly to their trigger using `position-anchor`:

```css
.anchor-popover {
  position: fixed;
  position-anchor: --menu-trigger;
  top: anchor(bottom);
  left: anchor(start);
  margin-top: 8px;
  position-try-fallbacks: flip-block, flip-inline;
  background: #1e1e24;
  color: #ffffff;
  border-radius: 8px;
  padding: 12px;
}
```

## 3. Discrete transitions and `@starting-style`

Eliminate JavaScript `setTimeout` hacks when animating modals, dialogs, and top-layer popovers entering or leaving `display: none`:

```css
dialog[open] {
  opacity: 1;
  transform: scale(1);
  display: block;
  transition: opacity 0.2s cubic-bezier(0.16, 1, 0.3, 1),
              transform 0.2s cubic-bezier(0.16, 1, 0.3, 1),
              display 0.2s allow-discrete,
              overlay 0.2s allow-discrete;
}

@starting-style {
  dialog[open] {
    opacity: 0;
    transform: scale(0.96);
  }
}

dialog {
  opacity: 0;
  transform: scale(0.96);
  transition: opacity 0.15s cubic-bezier(0.4, 0, 1, 1),
              transform 0.15s cubic-bezier(0.4, 0, 1, 1),
              display 0.15s allow-discrete,
              overlay 0.15s allow-discrete;
}
```

## 4. Relational selectors (`:has()`) in UI mechanics

The `:has()` selector enables contextual parent styling based on child states, eliminating manual JavaScript class synchronization:

```css
/* Disable submit button if form contains invalid inputs */
form:has(:invalid) button[type="submit"] {
  opacity: 0.5;
  pointer-events: none;
}

/* Style field group when internal input receives focus */
.input-group:has(input:focus-visible) {
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.2);
}
```

## 5. Tactile micro-interaction feedback

Interactive components must communicate state transitions with tactile precision:

### Active press duration and scale
- Keep button press feedback duration between 100ms and 160ms. Durations exceeding 200ms feel sluggish.
- Compression scale during `:active` states must stay between `scale(0.97)` and `scale(0.98)`. Compressing below 0.95 makes controls feel unstable.

### Pointer safety barrier
Hover effects must never trigger on touch devices, where sticky hover states degrade interactions:

```css
.button-action {
  transition: transform 120ms cubic-bezier(0.16, 1, 0.3, 1),
              background-color 120ms ease;
  user-select: none;
}

@media (hover: hover) and (pointer: fine) {
  .button-action:hover {
    transform: translateY(-1px);
  }
}

.button-action:active {
  transform: scale(0.97);
  transition-duration: 80ms;
}
```

### Accessible motion fallback
All transform and spatial transitions must respect user motion preferences:

```css
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

## 6. Skeleton screen mechanics

Skeleton loaders must reserve layout dimensions without inducing Cumulative Layout Shift:
- Declare explicit `aspect-ratio` or fixed dimensions matching the final rendered component.
- Apply linear shimmer gradients with cycle durations between 1.2 and 1.5 seconds.
- Mark skeleton containers with `aria-hidden="true"` and provide screen-reader announcements via `.sr-only` text.

```css
.skeleton-card {
  inline-size: 100%;
  aspect-ratio: 16 / 9;
  border-radius: 12px;
  background: linear-gradient(
    90deg,
    rgba(255, 255, 255, 0.04) 0%,
    rgba(255, 255, 255, 0.12) 50%,
    rgba(255, 255, 255, 0.04) 100%
  );
  background-size: 200% 100%;
  animation: shimmer 1.4s infinite linear;
}

@keyframes shimmer {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}
```
