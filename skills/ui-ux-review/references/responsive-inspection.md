### Navigation Adaptation

- Transform complex nav to hamburger/drawer on mobile
- Bottom nav bar for mobile apps
- Persistent side navigation on desktop
- Breadcrumbs on smaller screens for context

Test on real devices. DevTools emulation is a useful first pass but misses real touch, performance, and browser chrome.

**Avoid**:
- Hide core functionality on mobile (if it matters, make it work)
- Assume desktop = powerful device (consider accessibility, older machines)
- Use different information architecture across contexts (confusing)
- Break user expectations for platform (mobile users expect mobile patterns)
- Forget landscape orientation on mobile/tablet
- Use generic breakpoints blindly (use content-driven breakpoints)
- Ignore touch on desktop (many desktop devices have touch)

## Verify Adaptations

Test thoroughly across contexts:

- **Real devices**: Test on actual phones, tablets, desktops
- **Different orientations**: Portrait and landscape
- **Different browsers**: Safari, Chrome, Firefox, Edge
- **Different OS**: iOS, Android, Windows, macOS
- **Different input methods**: Touch, mouse, keyboard
- **Edge cases**: Very small screens (320px), very large screens (4K)
- **Slow connections**: Test on throttled network

**Custom controls** (sliders, drag surfaces, scrollable control strips): a before/after slider can pass every width check above and still refuse to drag on iOS, so exercise each one in scope in the same batched round as the checks above:

- **Primary gesture**: Tap it and confirm it responds as designed, then drag it with the target input method; the drag must complete, not just start
- **Scroll across it**: A swipe along the page's scroll axis across the control scrolls the page or container without activating it; a drag that starts on the control along its axis moves the control, not the page. Neither failure throws an error, so try both
- **Evidence**: Say what produced the evidence: an emulated viewport, synthesized touch input through a browser tool, which engine ran it (Chromium is not Safari), or a physical device. Screenshots and resized viewports verify layout, never a gesture. Name what stayed untested and move on; unreachable hardware is a reported gap, not a blocker

When the adaptation feels native to each context, hand off to `$impeccable polish` for the final pass.

---

## Reference Material

The sections below were previously `responsive-design.md` and live inline now so the adapt flow has its deep responsive reference in one place.

### Responsive Design

#### Mobile-First: Write It Right

Start with base styles for mobile, use `min-width` queries to layer complexity. Desktop-first (`max-width`) means mobile loads unnecessary styles first.

#### Breakpoints: Content-Driven

Don't chase device sizes; let content tell you where to break. Start narrow, stretch until design breaks, add breakpoint there. Three breakpoints usually suffice (640, 768, 1024px). Use `clamp()` for fluid values without breakpoints.

#### Detect Input Method, Not Just Screen Size

**Screen size doesn't tell you input method.** A laptop with touchscreen, a tablet with keyboard. Use pointer and hover queries:

```css
/* Fine pointer (mouse, trackpad) */
@media (pointer: fine) {
  .button { padding: 8px 16px; }
}

/* Coarse pointer (touch, stylus) */
@media (pointer: coarse) {
  .button { padding: 12px 20px; }  /* Larger touch target */
}

/* Device supports hover */
@media (hover: hover) {
  .card:hover { transform: translateY(-2px); }
}

/* Device doesn't support hover (touch) */
@media (hover: none) {
  .card { /* No hover state - use active instead */ }
}
```

**Critical**: Don't rely on hover for functionality. Touch users can't hover.

#### Safe Areas: Handle the Notch

Modern phones have notches, rounded corners, and home indicators. Use `env()`:

```css
body {
  padding-top: env(safe-area-inset-top);
  padding-bottom: env(safe-area-inset-bottom);
  padding-left: env(safe-area-inset-left);
  padding-right: env(safe-area-inset-right);
}

/* With fallback */
.footer {
  padding-bottom: max(1rem, env(safe-area-inset-bottom));
}
```

**Enable viewport-fit** in your meta tag:
```html
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
```

#### Responsive Images: Get It Right

##### srcset with Width Descriptors

```html
<img
  src="hero-800.jpg"
  srcset="
    hero-400.jpg 400w,
    hero-800.jpg 800w,
    hero-1200.jpg 1200w
  "
  sizes="(max-width: 768px) 100vw, 50vw"
  alt="Hero image"
>
```

**How it works**:
- `srcset` lists available images with their actual widths (`w` descriptors)
- `sizes` tells the browser how wide the image will display
- Browser picks the best file based on viewport width AND device pixel ratio

##### Picture Element for Art Direction

When you need different crops/compositions (not just resolutions):

```html
<picture>
  <source media="(min-width: 768px)" srcset="wide.jpg">
  <source media="(max-width: 767px)" srcset="tall.jpg">
  <img src="fallback.jpg" alt="...">
</picture>
```

#### Layout Adaptation Patterns

**Navigation**: Three stages: hamburger + drawer on mobile, horizontal compact on tablet, full with labels on desktop. **Tables**: Transform to cards on mobile using `display: block` and `data-label` attributes. **Progressive disclosure**: Use `<details>/<summary>` for content that can collapse on mobile.

#### Testing: Don't Trust DevTools Alone

DevTools device emulation is useful for layout but misses:

- Actual touch interactions
- Real CPU/memory constraints
- Network latency patterns
- Font rendering differences
- Browser chrome/keyboard appearances

**Test on at least**: One real iPhone, one real Android, a tablet if relevant. Cheap Android phones reveal performance issues you'll never see on simulators.

---

**Avoid**: Desktop-first design. Device detection instead of feature detection. Separate mobile/desktop codebases. Ignoring tablet and landscape. Assuming all mobile devices are powerful.
