# Springs, FLIP projection, and tactile gesture physics

## 1. Zero-JS CSS `linear()` spring tokens

Use multi-stop `linear()` curves for tactile button snaps, badge pops, and segmented pill transitions without loading a JS spring runtime. Always wrap in `@supports` so older engines fall back to `--ease-out`:

```css
:root {
  --spring-snappy: var(--ease-out);
}

@supports (animation-timing-function: linear(0, 1)) {
  :root {
    --spring-snappy: linear(
      0, 0.009, 0.035 2.1%, 0.141, 0.281 6.7%, 0.723 12.9%, 0.938 16.7%,
      1.017, 1.077, 1.121, 1.149 24.3%, 1.159, 1.163, 1.161, 1.154 29.9%,
      1.129 32.8%, 1.051 39.6%, 1.017 43.1%, 0.991, 0.977 51%, 0.974 53.8%,
      0.975 57.1%, 0.997 69.8%, 1.003 76.9%, 1.004 83.8%, 1
    );
  }
}
```

## 2. FLIP layout projection with inverse child scale compensation

1. **First.** Read `first = element.getBoundingClientRect()` synchronously before state mutation.
2. **Last.** Commit DOM state and read `last = element.getBoundingClientRect()` inside `useLayoutEffect` before browser paint. Abort if `last.width <= 0 || last.height <= 0`.
3. **Invert.** Compute `dx = first.left - last.left`, `dy = first.top - last.top`, `sx = first.width / last.width`, and `sy = first.height / last.height` with `transform-origin: 0 0`.
4. **Play.** Sample `N = 16` keyframes along cubic ease-out progress `p` so parent scale `sp = s + (1 - s) * p` and child scale `1 / sp` remain exact reciprocals on every frame, running WAAPI `element.animate()` and `inner.animate()` with `composite: "replace"` and no persistent `fill: "forwards"`.

## 3. Velocity-projected detent snapping and rubber-band damping

- **Decisiveness projection.** Evaluate sheet or carousel snap targets using `projectedOffset = currentOffset + releaseVelocity * 0.12` from a `40ms` rolling velocity ring buffer so a brisk `1600px/s` flick over `25px` advances to the next detent.
- **Asymptotic rubber-banding.** When dragging past min or max scroll bounds by `overscroll` pixels across a container of size `dim`, compute damped displacement via:

$$\text{damped} = \text{dim} \left(1 - \frac{1}{\frac{|\text{overscroll}| \cdot 0.55}{\text{dim}} + 1}\right)$$
