# Landing page and editorial motion choreography

## 1. Above-the-fold Hero LCP contract

1. Keep primary `<h1>` text and hero product media visible at non-zero opacity from frame zero (`0ms` delay) on initial HTML, driving entrance via pure CSS `@keyframes` (`transform` or `clip-path`) that complete within `650ms` without waiting for JS hydration.
2. Stagger hero sub-elements (eyebrow, headline, subcopy, primary CTA, product stage) with fixed CSS custom property offsets (`--stagger-index: 0..4`) capped at `700ms` total span.
3. Never attach `IntersectionObserver` to elements inside the initial `100dvh` viewport.

## 2. Sub-linear stagger formula

Linear staggers (`delay = index * stepMs`) feel brisk for the first 3 items and sluggish after item 6. Use exponential decay so early items enter crisply while trailing items compress smoothly toward the ceiling:

$$\text{delay}(i) = D_{\max} \left(1 - e^{-k \cdot i}\right)$$

- **Bento grids and feature cards.** Set $D_{\max} = 450\text{ms}$ and $k = 0.28$. Item 0 starts at `0ms`, item 3 at `256ms`, item 8 at `402ms`, and items beyond viewport fold receive `0ms`.
- **Hero display words.** Set $D_{\max} = 700\text{ms}$ and $k = 0.24$. Split by word rather than individual character for body subheads; reserve per-character staggers strictly for short display titles (`<= 24` characters).

## 3. Scroll-linked scrub vs one-shot threshold reveal

- **Scroll-scrubbed parallax and progress.** Gate `animation-timeline: view()` inside `@supports (animation-timeline: view())` and `@media (prefers-reduced-motion: no-preference)`, paired with explicit `animation-range: entry 0% cover 40%` or `contain 0% contain 100%` and `animation-timing-function: linear`.
- **One-shot section reveals.** Use `IntersectionObserver` with `threshold: 0.15` and `rootMargin: "0px 0px -8% 0px"`. Unobserve immediately after adding `data-revealed="true"` so scrolling back upward never reverses or replays the entrance.
- **Sticky narrative containment.** Apply `overflow-x: clip` (never `overflow: hidden`) on outer page wrappers so multi-screen sticky showcases remain pinned.

## 4. GPU-composited spotlights and SVG architectural draws

- **Card pointer spotlights.** Register `@property --sx` and `@property --sy` with `syntax: "<length>"; inherits: false; initial-value: -999px;` so updates never invalidate descendant styles. Render a radial layer sized to $2 \times \text{radius}$ positioned via `transform: translate3d(calc(var(--sx) - var(--radius)), calc(var(--sy) - var(--radius)), 0)` from a single `requestAnimationFrame` loop using a cached wrapper `DOMRect`.
- **SVG connector beams and underlines.** Set `pathLength="1"` directly on `<path>`, `<line>`, or `<circle>` elements in JSX/SVG, pair with `stroke-dasharray: 1` and `stroke-dashoffset: 1`, and transition `stroke-dashoffset` to `0` without calling `getTotalLength()`.
