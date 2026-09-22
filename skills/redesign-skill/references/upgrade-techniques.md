# Upgrade techniques

Apply these implementation techniques to replace generic interface patterns with deliberate visual styling.

## Typography upgrades

Use these techniques to create intentional typographic hierarchy:

- Variable font weight interpolation. Interpolate `font-weight` or `font-stretch` across scroll progress or pointer movement. This adds fluid responsive weight shifts to display titles.
- Outlined-to-fill text transitions. Render text initially with `-webkit-text-stroke: 1px currentColor` and transparent fill. Transition `color` to fill on scroll trigger or hover.
- Text mask reveals. Use `background-clip: text` combined with high-contrast imagery or looping video behind display headers. Ensure fallback text colors remain legible when background assets fail to load.

## Layout upgrades

Use these techniques to structure content beyond repetitive card grids:

- Asymmetric grids. Break rigid column constraints by assigning irregular column spans (`grid-column: span 7` next to `grid-column: span 5`). Offset adjacent columns vertically using margin offsets.
- Whitespace expansion. Increase negative space around primary focal points. Isolate critical actions by doubling surrounding padding and margins.
- Sticky stacking cards. Position cards with `position: sticky; top: 5rem;` so succeeding cards physically stack over preceding items during vertical scrolling.
- Split-screen viewports. Divide viewports into two distinct panels that respond independently to scroll progress or contain contrasting graphic and textual information.

## Motion upgrades

Use these techniques to implement responsive, physics-based interactions:

- Inertia scrolling. Use lightweight momentum-based scroll smoothing when building narrative landing pages to decouple movement from abrupt wheel clicks.
- Staggered entry transitions. Stagger the entry of list items and card grids by combining `opacity` and `transform: translateY(12px)` with incremental transition delays (`transition-delay: 50ms, 100ms, 150ms`). Never animate all elements simultaneously.
- Spring physics motion. Replace linear CSS easing curves with cubic bezier curves that simulate physical spring mass, such as `cubic-bezier(0.16, 1, 0.3, 1)`.
- Scroll-driven reveals. Tie element scaling, rotation, or clipping paths directly to scroll progress using CSS scroll timelines or intersection observers.

## Surface treatments

Use these techniques to add visual depth to flat containers:

- Layered glassmorphism. Combine `backdrop-filter: blur(12px)` with a 1px semi-transparent inner border (`border: 1px solid rgba(255, 255, 255, 0.1)`) and a subtle inset box shadow (`box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.15)`).
- Cursor-tracking spotlight borders. Update CSS custom properties (`--x`, `--y`) on pointer move to render a radial gradient highlight directly beneath the cursor along component borders.
- Grain and noise overlays. Add a fixed, pointer-events-none overlay element containing a tiled SVG noise filter at low opacity (around 3 to 5 percent) to break flat digital surfaces.
- Tinted shadows. Derive shadow colors from the hue of the underlying container or background color rather than applying generic black shadows. For instance, use `box-shadow: 0 10px 25px -5px rgba(15, 23, 42, 0.25)` on slate surfaces.
