# Frontend UI patterns reference

Reference catalog for high-variance layouts, bento grid archetypes, and micro-interactions. Consult this guide when designing complex interfaces or interactive components.

## Bento grid archetypes

Modern feature grids use structured visual hierarchy and physics-based motion. Apply these specifications when building bento layouts.

### Container specifications

- Palette: Page background `#f9fafb`. Cards use `#ffffff` with a 1px border `border-slate-200/50`.
- Geometry: Corner radius `rounded-3xl` or `rounded-[2.5rem]`. Internal padding `p-8` or `p-10`.
- Shadows: Use diffusion shadows (`shadow-[0_20px_40px_-15px_rgba(0,0,0,0.05)]`) rather than dark drop shadows.
- Typography: Headers use `tracking-tight` with high-contrast font stacks (`Geist` or `Satoshi`).
- Text placement: Place primary titles and descriptive copy outside and below cards to keep surfaces uncluttered.

### Motion engine rules

- Spring physics: Configure Framer Motion transitions with `type: "spring", stiffness: 100, damping: 20`. Avoid linear easing.
- State transitions: Apply `layout` and `layoutId` props to animate container resizing and shared element position changes.
- Component isolation: Wrap animated loops inside isolated React client components marked with `'use client'`. Wrap list containers in `React.memo` to prevent re-renders in parent layouts.

### Five bento card implementations

1. Intelligent list
   - Structure: Vertical stack of task or metric items.
   - Behavior: Items re-order automatically at fixed intervals. Use Framer Motion `layoutId` on list items to animate position changes smoothly.

2. Command input
   - Structure: Centered search bar featuring a monospaced input field and an animated cursor.
   - Behavior: Cycle through sample queries using a character-by-character typewriter loop. Display a loading shimmer badge during simulated processing transitions.

3. Live status indicator
   - Structure: System metric badge with a pulsing status dot.
   - Behavior: Combine an ambient pulse on the status dot with a floating notification pill that springs into view, pauses for 3 seconds, and exits cleanly.

4. Wide data stream
   - Structure: Horizontal row of metric cards spanning the full width of the parent container.
   - Behavior: Translate the container along the x-axis continuously from `0%` to `-100%` inside an overflow-hidden wrapper. Set the animation to loop indefinitely with a constant duration.

5. Contextual focus mode
   - Structure: Document block containing a floating toolbar.
   - Behavior: Highlight a target text segment on load, then reveal the floating toolbar with spring physics.

## Layout variations

Use these structural alternatives to avoid generic centered rows.

### Asymmetric hero sections

- Align headline copy to the left or right edge of the viewport.
- Place visual assets or data cards on the opposite side using an unequal column split (`grid-cols-1 md:grid-cols-12` with column spans `md:col-span-7` and `md:col-span-5`).
- On screens under 768px, collapse the grid into a single column (`w-full px-4`).

### Split screen scroll

- Split the viewport into two equal 50% columns.
- Keep one column fixed while the other column scrolls through supporting sections, or scroll both columns in opposite directions.

### Sticky scroll stacks

- Position a sequence of cards inside a parent container with relative positioning.
- Set each card to `sticky top-24` with increasing z-index values so cards stack over each other as the user scrolls down the page.

### Masonry grids

- Use CSS column count (`columns-1 md:columns-3 gap-6`) or CSS Grid with auto-rows to render cards with varied aspect ratios without leaving uneven vertical gaps.

## Micro-interactions and physics

### Magnetic cursor attraction

Apply attraction physics to key interactive buttons:

```tsx
import { motion, useMotionValue, useTransform } from "framer-motion";
import { useRef } from "react";

export function MagneticButton({ children }: { children: React.ReactNode }) {
  const ref = useRef<HTMLButtonElement>(null);
  const x = useMotionValue(0);
  const y = useMotionValue(0);

  const handleMouseMove = (e: React.MouseEvent<HTMLButtonElement>) => {
    const rect = ref.current?.getBoundingClientRect();
    if (!rect) return;
    const centerX = rect.left + rect.width / 2;
    const centerY = rect.top + rect.height / 2;
    x.set((e.clientX - centerX) * 0.25);
    y.set((e.clientY - centerY) * 0.25);
  };

  const handleMouseLeave = () => {
    x.set(0);
    y.set(0);
  };

  return (
    <motion.button
      ref={ref}
      style={{ x, y }}
      onMouseMove={handleMouseMove}
      onMouseLeave={handleMouseLeave}
      transition={{ type: "spring", stiffness: 150, damping: 15 }}
      className="px-6 py-3 rounded-full bg-zinc-900 text-white font-medium"
    >
      {children}
    </motion.button>
  );
}
```

Do not store cursor coordinates in React `useState`. Always use `useMotionValue` outside the React render cycle.

### Refraction panels

When building frosted glass panels, combine backdrop blur with inner specular highlights:

```html
<div class="backdrop-blur-md bg-white/70 border border-white/20 shadow-[inset_0_1px_0_rgba(255,255,255,0.4)] rounded-2xl p-6">
  <!-- Content -->
</div>
```

The 1px inner border and subtle inset box shadow create a physical glass edge without heavy drop shadows.

### Skeleton shimmer

Implement loading states that match final layout dimensions. Animate a gradient highlight across the placeholder surface:

```html
<div class="relative overflow-hidden rounded-lg bg-zinc-200 h-6 w-48">
  <div class="absolute inset-0 -translate-x-full animate-[shimmer_1.5s_infinite] bg-gradient-to-r from-transparent via-white/40 to-transparent"></div>
</div>
```

Define `@keyframes shimmer` in CSS with `transform: translateX(100%)`.
