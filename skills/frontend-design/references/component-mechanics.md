# Component mechanics and interaction states

Implement full lifecycle interaction states and tactile feedback for all components:

1. Tactile press feedback. Apply tactile physical displacement (`-translate-y-[1px]` or `scale-[0.98]`) to active buttons and interactive chips.
2. Skeleton loaders. Match placeholder skeleton geometries to expected layout dimensions. Avoid generic circular spinners for primary content blocks.
3. Form validation timing. Delay error messages until input blur, then validate live on subsequent input. Position validation messages directly adjacent to invalid fields.
4. Concentric card nesting. Ensure nested badges, buttons, and preview containers use mathematically concentric radii to prevent visual pinching. Formula: `max(0px, calc(outer - padding - border))`.
5. Hardware-accelerated motion. Animate exclusively via `transform` and `opacity`. Restrict spring physics transitions to motion-enabled elements and respect `prefers-reduced-motion` media queries.
6. Asynchronous network resilience. Handle race conditions with `AbortController`, retry idempotent requests with exponential backoff, and provide optimistic mutations with rollback.
7. Target size minimum and keyboard focus. Guarantee interactive elements meet WCAG 2.2 SC 2.5.8 with a minimum hit area of 24x24px, with recommended 44px touch targets. Configure visible focus indicators on all interactive targets using `focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:outline-none`.
8. Top layer and discrete transitions. Use native `dialog` or Popover API for modals, command palettes, and drawer surfaces to activate browser focus trapping and top-layer stacking. Animate entry and exit states using `@starting-style` with `transition-behavior: allow-discrete` for display, opacity, and transform transitions without JavaScript animation libraries.
9. Relational container focus. Configure parent card boundaries to reflect keyboard focus of interior interactive links or buttons using `:has(a:focus-visible)` and `:has(button:focus-visible)` without JavaScript event listeners.
10. Composite hit targets. Expand primary card links via `after:absolute after:inset-0`, and isolate secondary interactive buttons or menus with relative `z-10` to prevent nested click collisions.
