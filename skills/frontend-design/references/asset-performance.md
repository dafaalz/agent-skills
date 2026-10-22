Performance is a feature. Identify the actual bottleneck for THIS interface, fix it, then measure. Don't optimize what isn't slow.

## Assess Performance Issues

Understand current performance and identify problems:

1. **Measure current state**:
   - **Core Web Vitals**: LCP, INP, CLS scores
   - **Load time**: Time to interactive, first contentful paint
   - **Bundle size**: JavaScript, CSS, image sizes
   - **Runtime performance**: Frame rate, memory usage, CPU usage
   - **Network**: Request count, payload sizes, waterfall

2. **Identify bottlenecks**:
   - What's slow? (Initial load? Interactions? Animations?)
   - What's causing it? (Large images? Expensive JavaScript? Layout thrashing?)
   - How bad is it? (Perceivable? Annoying? Blocking?)
   - Who's affected? (All users? Mobile only? Slow connections?)

Measure before and after. Optimizing without a measurement spends effort on things that do not matter.

## Optimization Strategy

Create systematic improvement plan:

### Loading Performance

**Optimize Images**:
- Use modern formats (WebP, AVIF)
- Proper sizing (don't load 3000px image for 300px display)
- Lazy loading for below-fold images
- Responsive images (`srcset`, `picture` element)
- Compress images (80-85% quality is usually imperceptible)
- Use CDN for faster delivery

```html
<img 
  src="hero.webp"
  srcset="hero-400.webp 400w, hero-800.webp 800w, hero-1200.webp 1200w"
  sizes="(max-width: 400px) 400px, (max-width: 800px) 800px, 1200px"
  loading="lazy"
  alt="Hero image"
/>
```

**Reduce JavaScript Bundle**:
- Code splitting (route-based, component-based)
- Tree shaking (remove unused code)
- Remove unused dependencies
- Lazy load non-critical code
- Use dynamic imports for large components

```javascript
// Lazy load heavy component
const HeavyChart = lazy(() => import('./HeavyChart'));
```

**Optimize CSS**:
- Remove unused CSS
- Critical CSS inline, rest async
- Minimize CSS files
- Use CSS containment for independent regions

**Optimize Fonts**:
- Use `font-display: swap` or `optional`
- Subset fonts (only characters you need)
- Preload critical fonts
- Use system fonts when appropriate
- Limit font weights loaded

```css
@font-face {
  font-family: 'CustomFont';
  src: url('/fonts/custom.woff2') format('woff2');
  font-display: swap; /* Show fallback immediately */
  unicode-range: U+0020-007F; /* Basic Latin only */
}
```

**Optimize Loading Strategy**:
- Critical resources first (async/defer non-critical)
- Preload critical assets
- Prefetch likely next pages
- Service worker for offline/caching
- HTTP/2 or HTTP/3 for multiplexing

### Rendering Performance

**Avoid Layout Thrashing**:
```javascript
// ❌ Bad: Alternating reads and writes (causes reflows)
elements.forEach(el => {
  const height = el.offsetHeight; // Read (forces layout)
  el.style.height = height * 2; // Write
});

// ✅ Good: Batch reads, then batch writes
const heights = elements.map(el => el.offsetHeight); // All reads
elements.forEach((el, i) => {
  el.style.height = heights[i] * 2; // All writes
});
```

**Optimize Rendering**:
- Use CSS `contain` property for independent regions
- Minimize DOM depth (flatter is faster)
- Reduce DOM size (fewer elements)
- Use `content-visibility: auto` for long lists
- Virtual scrolling for very long lists (react-window, TanStack Virtual)

**Reduce Paint & Composite**:
- Use `transform` and `opacity` for reliable movement, but allow blur, filters, masks, clip paths, shadows, and color shifts when they create meaningful polish
- Avoid casual animation of layout-driving properties (`width`, `height`, `top`, `left`, margins)
- Use `will-change` sparingly for known expensive operations
- Bound expensive paint areas for blur/filter/shadow effects (smaller and isolated is faster)

### Animation Performance

**GPU Acceleration**:
```css
/* ✅ GPU-accelerated (fast) */
.animated {
  transform: translateX(100px);
  opacity: 0.5;
}

/* ❌ CPU-bound (slow) */
.animated {
  left: 100px;
  width: 300px;
}
```

**Smooth 60fps**:
- Target 16ms per frame (60fps)
- Use `requestAnimationFrame` for JS animations
- Debounce/throttle scroll handlers
- Use CSS animations when possible
- Avoid long-running JavaScript during animations

**Intersection Observer**:
```javascript
// Efficiently detect when elements enter viewport
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      // Element is visible, lazy load or animate
    }
  });
});
```

