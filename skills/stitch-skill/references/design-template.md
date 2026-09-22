# Design system: [Project title]

## Configuration

Adjust these dials before using this design system. They control output creativity, density, and animation.

| Dial | Level | Description |
|---|---|---|
| Creativity | 8 | 1 = Minimal and monochrome. 5 = Balanced with personality. 10 = Expressive, experimental typography, inline headline images, strong asymmetry. Default is 8. |
| Density | 4 | 1 = Airy gallery whitespace. 5 = Balanced sections. 10 = Cockpit dense and data heavy. Default is 4. |
| Variance | 8 | 1 = Symmetric grids. 5 = Subtle offsets. 10 = Asymmetric layouts where no two sections repeat. Default is 8. |
| Motion intent | 6 | 1 = Static. 5 = Subtle hover and entrance cues. 10 = Coordinated orchestration on every component. Default is 6. |

At creativity levels 1 to 3, the output produces clean, restrained layouts. At creativity levels 7 to 10, the output includes inline image typography, high scale contrast, and editorial asymmetry.

---

## 1. Visual theme and atmosphere

A restrained interface with asymmetric layouts and fluid spring physics. Density is balanced (Level 4), variance runs high (Level 8) to avoid symmetrical patterns, and motion remains fluid without theatrical delays (Level 6).

## 2. Color palette and roles

- **Canvas White** (`#F9FAFB`). Primary background surface. Warm neutral, never clinical blue-white.
- **Pure Surface** (`#FFFFFF`). Card and container fill with diffused shadow for elevation.
- **Charcoal Ink** (`#18181B`). Primary text, Zinc-950 depth, never pure black.
- **Steel Secondary** (`#71717A`). Body text, descriptions, and metadata.
- **Muted Slate** (`#94A3B8`). Tertiary text, timestamps, and disabled states.
- **Whisper Border** (`rgba(226,232,240,0.5)`). Card borders and structural 1px lines.
- **Diffused Shadow** (`rgba(0,0,0,0.05)`). Card elevation with 40px blur and -15px offset.

### Accent selection

Pick one accent per project:
- **Emerald Signal** (`#10B981`). Growth, success, and positive metrics.
- **Electric Blue** (`#3B82F6`). Developer tools, productivity apps, and software platforms.
- **Deep Rose** (`#E11D48`). Creative, editorial, and design-led products.
- **Amber Warmth** (`#F59E0B`). Community, social, and warm utility products.

### Banned colors

- Purple or violet neon gradients
- Pure black (`#000000`). Use Off-Black or Zinc-950 instead.
- Oversaturated accents above 80% saturation
- Fluctuating between warm and cool grays within one project

## 3. Typography rules

- **Display.** `Geist`, `Satoshi`, `Cabinet Grotesk`, or `Outfit`. Track tight (`-0.025em`), fluid scale, weight-driven hierarchy (700 to 900), compressed leading (`1.1`).
- **Body.** Same family at weight 400. Relaxed leading (`1.65`), 65 character line maximum, Steel Secondary color.
- **Mono.** `Geist Mono` or `JetBrains Mono`. Code blocks, metadata, and timestamps. When density exceeds level 7, render all numbers in monospace.
- **Scale.** Display at `clamp(2.25rem, 5vw, 3.75rem)`. Body at `1rem` to `1.125rem`. Mono metadata at `0.8125rem`.

### Banned fonts

- `Inter`. Banned in display and body text.
- Generic serif fonts (`Times New Roman`, `Georgia`, `Garamond`, `Palatino`). If serif is required for editorial work, use modern serifs such as `Fraunces`, `Gambarino`, `Editorial New`, or `Instrument Serif`. Serif fonts remain banned in dashboards and software interfaces.

## 4. Component stylings

- **Buttons.** Flat surface without outer glows. Primary buttons use accent fill with white text. Secondary buttons use ghost or outline styling. Active state uses `-1px translateY` or `scale(0.98)` for tactile push feedback. Hover state shifts background shade without adding drop shadows.
- **Cards and containers.** Rounded corners (`2.5rem`), pure white fill, whisper border (`1px` semi-transparent), and diffused shadow (`0 20px 40px -15px rgba(0,0,0,0.05)`). Internal padding spans `2rem` to `2.5rem`. Use cards only when elevation communicates hierarchy. In high density layouts, replace cards with `border-top` dividers or negative space.
- **Inputs and forms.** Label positioned above input, optional helper text, and error text below in Deep Rose. Focus ring uses accent color with `2px` offset. Do not use floating labels. Keep a standard `0.5rem` gap in the label-input-error stack.
- **Navigation.** Sticky header with horizontal layout and generous item spacing. Icons scale slightly on hover. Desktop navigation must not collapse into a hamburger menu.
- **Loaders.** Skeletal shimmer matching container dimensions and corner radius. Do not use circular spinners.
- **Empty states.** Composed illustration or icon layout paired with actionable copy. Do not output bare text like "No data found".
- **Error states.** Inline contextual container with red accent border and an explicit recovery button.

## 5. Hero section

- **Inline image typography.** Embed small contextual images directly between words in the headline. Images sit inline at text height with rounded corners, functioning as visual punctuation.
- **Spatial separation.** Never overlap text on images or other text. Every element occupies its own grid cell or layout zone. Do not use z-index stacking for text over media.
- **Zero filler text.** Do not include "Scroll to explore", "Swipe down", scroll arrows, or bouncing chevrons.
- **Asymmetric structure.** Centered hero layouts are banned when variance exceeds 4. Use 50/50 split screen, left-aligned text with right-side visual, or asymmetric whitespace layouts.
- **Call to action restraint.** Maximum one primary button. Do not add secondary links or micro-copy under the headline.

## 6. Layout principles

- **Grid first.** Use CSS Grid for all major sections. Do not use flexbox percentage calculations such as `calc(33% - 1rem)`.
- **Feature sections.** Do not use three equal cards in a horizontal row. Use a two-column zig-zag, an asymmetric bento grid (such as `2fr 1fr 1fr`), or a horizontal scroll gallery.
- **Containment.** Center all content inside `max-width: 1400px`. Apply horizontal padding of `1rem` on mobile, `2rem` on tablet, and `4rem` on desktop.
- **Full height sections.** Use `min-height: 100dvh`. Do not use `height: 100vh` to avoid mobile browser address bar jumps.
- **Bento structure.** For feature grids, use Row 1 with 3 columns and Row 2 with 2 columns (70/30 split).

## 7. Responsive rules

- **Mobile collapse (< 768px).** Multi-column grids collapse to a single column with `width: 100%`, `padding: 1rem`, and `gap: 1.5rem`.
- **Zero horizontal scroll.** Horizontal overflow on mobile is an absolute defect. All content must fit inside viewport width.
- **Typography scaling.** Headlines scale via `clamp()`. Body text remains `1rem` minimum and never drops below `14px`.
- **Touch targets.** Interactive elements must meet a minimum `44px` tap target. Buttons expand to full width on mobile.
- **Image behavior.** Inline headline images stack underneath the headline on mobile viewports rather than sitting inline.
- **Navigation.** Desktop navigation collapses to a drawer menu or full screen sheet on mobile.
- **Testing viewports.** Verify designs at `375px`, `390px`, `768px`, `1024px`, and `1440px`.

## 8. Motion and interaction

- **Physics engine.** Spring-based curves exclusively (`stiffness: 100, damping: 20`). Do not use linear easing.
- **Micro-interactions.** Active dashboard components include continuous states: pulse on status dots, typewriter on search inputs, float on feature icons, and shimmer on loaders.
- **Staggered entry.** Mount lists and card groups with cascade delays (`animation-delay: calc(var(--index) * 100ms)`). Do not reveal all items simultaneously.
- **Hardware acceleration.** Animate only `transform` and `opacity`. Never animate `top`, `left`, `width`, or `height`. Place grain or noise overlays on fixed pseudo-elements with `pointer-events: none`.
- **Performance.** Isolate CPU-intensive animations in leaf components so parent trees do not re-render. Maintain 60 frames per second.

## 9. Banned anti-patterns

- Emojis anywhere in UI text, code, or image attributes
- `Inter` font in display or body text
- Generic serif fonts (`Times New Roman`, `Georgia`, `Garamond`)
- Pure black (`#000000`)
- Neon glows or outer box-shadow glows
- Accent saturation above 80%
- Gradient text across large headers
- Custom mouse cursor overrides
- Overlapping elements or text stacked on images
- Three equal width cards in a row
- Centered hero layouts when variance exceeds 4
- Instructional filler copy: "Scroll to explore", "Swipe down", "Discover more below"
- Generic placeholder names: "John Doe", "Sarah Chan", "Acme", "Nexus", "SmartFlow"
- Fabricated round metrics: `99.99%`, `50%`, `1234567`. Use realistic figures like `47.2%`.
- Promotional AI copy: "Elevate", "Seamless", "Unleash", "Next-Gen", "Revolutionize"
- Broken placeholder image links. Use `picsum.photos/seed/{id}/800/600` or SVG avatars.
- Uncustomized default component libraries
- Layer index clutter. Reserve z-index for navigation, dialogs, and overlays.
- Viewport unit `h-screen`. Use `min-h-[100dvh]`.
- Circular loading spinners. Use skeletal shimmer states.
