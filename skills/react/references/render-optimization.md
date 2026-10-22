### React/Framework Optimization

**React-specific**:
- Use `memo()` for expensive components
- `useMemo()` and `useCallback()` for expensive computations
- Virtualize long lists
- Code split routes
- Avoid inline function creation in render
- Use React DevTools Profiler

**Framework-agnostic**:
- Minimize re-renders
- Debounce expensive operations
- Memoize computed values
- Lazy load routes and components

### Network Optimization

**Reduce Requests**:
- Combine small files
- Use SVG sprites for icons
- Inline small critical assets
- Remove unused third-party scripts

**Optimize APIs**:
- Use pagination (don't load everything)
- GraphQL to request only needed fields
- Response compression (gzip, brotli)
- HTTP caching headers
- CDN for static assets

**Optimize for Slow Connections**:
- Adaptive loading based on connection (navigator.connection)
- Optimistic UI updates
- Request prioritization
- Progressive enhancement

## Core Web Vitals Optimization

### Largest Contentful Paint (LCP < 2.5s)
- Optimize hero images
- Inline critical CSS
- Preload key resources
- Use CDN
- Server-side rendering

### Interaction to Next Paint (INP < 200ms)
- Break up long tasks
- Defer non-critical JavaScript
- Use web workers for heavy computation
- Reduce JavaScript execution time

### Cumulative Layout Shift (CLS < 0.1)
- Set dimensions on images and videos
- Don't inject content above existing content
- Use `aspect-ratio` CSS property
- Reserve space for ads/embeds
- Avoid animations that cause layout shifts

```css
/* Reserve space for image */
.image-container {
  aspect-ratio: 16 / 9;
}
```

## Performance Monitoring

**Tools to use**:
- Chrome DevTools (Lighthouse, Performance panel)
- WebPageTest
- Core Web Vitals (Chrome UX Report)
- Bundle analyzers (webpack-bundle-analyzer)
- Performance monitoring (Sentry, DataDog, New Relic)

**Key metrics**:
- LCP, INP, CLS (Core Web Vitals; INP replaced FID in March 2024)
- Time to Interactive (TTI)
- First Contentful Paint (FCP)
- Total Blocking Time (TBT)
- Bundle size
- Request count

Measure on real devices with real network conditions. Desktop Chrome on a fast connection isn't representative.

**Avoid**:
- Optimize without measuring (premature optimization)
- Sacrifice accessibility for performance
- Break functionality while optimizing
- Use `will-change` everywhere (creates new layers, uses memory)
- Lazy load above-fold content
- Optimize micro-optimizations while ignoring major issues (optimize the biggest bottleneck first)
- Forget about mobile performance (often slower devices, slower connections)

## Verify Improvements

Test that optimizations worked:

- **Before/after metrics**: Compare Lighthouse scores
- **Real user monitoring**: Track improvements for real users
- **Different devices**: Test on low-end Android, not just flagship iPhone
- **Slow connections**: Throttle to 3G, test experience
- **No regressions**: Ensure functionality still works
- **User perception**: Does it *feel* faster?

When the user-facing numbers move, hand off to `$impeccable polish` for the final pass.
