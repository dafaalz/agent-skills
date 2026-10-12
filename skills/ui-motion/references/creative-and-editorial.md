# Creative and editorial motion engineering

Hardware-accelerated techniques for narrative landing pages, editorial layouts, continuous pointer physics, dynamic lighting, and curtain reveal masks.

## 1. Scope and dual-layer architecture

Separate motion engineering into two distinct operational layers:

- **Functional UI layer.** Transactable controls, forms, inputs, dropdowns, tooltips, dialogs, and command palettes. Restricted to under 300ms, strict cubic bezier tokens, and zero decorative overhead. Keyboard shortcuts execute with 0ms transition.
- **Creative and editorial layer.** Hero sections, brand storytelling, portfolio galleries, and narrative transitions. Durations from 600ms to 1400ms are explicitly sanctioned when paired with asymmetric high-velocity curves (`cubic-bezier(0.16, 1, 0.3, 1)` or `cubic-bezier(0.22, 1, 0.36, 1)`).

Never apply functional UI speed caps to narrative editorial scenes, and never apply editorial long-decay physics to transactional app workflows.

## 2. Continuous pointer physics and RAF LERP damping

Direct pointer tracking without damping introduces harsh jitter. Smooth camera inertia uses Linear Interpolation (LERP) inside a dedicated `requestAnimationFrame` loop.

Apply the linear interpolation formula `current = current + (target - current) * factor`.

```javascript
const hero = document.querySelector("#hero");
let mx = 0, my = 0;
let x = 0, y = 0;
const damping = 0.06; // 94% frame inertia retention

hero.addEventListener("pointermove", (e) => {
  // Normalize coordinates to [-0.5, 0.5] range
  mx = e.clientX / window.innerWidth - 0.5;
  my = e.clientY / window.innerHeight - 0.5;
});

hero.addEventListener("pointerleave", () => {
  mx = 0;
  my = 0;
});

function tick() {
  x += (mx - x) * damping;
  y += (my - y) * damping;

  hero.style.setProperty("--mx", x.toFixed(3));
  hero.style.setProperty("--my", y.toFixed(3));

  requestAnimationFrame(tick);
}
requestAnimationFrame(tick);
```

Consume the CSS variables across layered transforms with varying depth multipliers:

```css
.layer-deep {
  transform: translate3d(calc(var(--mx) * -40px), calc(var(--my) * -25px), 0);
}

.layer-foreground {
  transform: translate3d(calc(var(--mx) * 20px), calc(var(--my) * 15px), 0);
}
```

## 3. Dynamic cursor spotlight lighting

Render dynamic surface reflection on cards without manual Canvas overhead by pushing local coordinates to CSS custom properties.

```javascript
cardContainer.addEventListener("pointermove", (e) => {
  const card = e.target.closest(".spotlight-card");
  if (!card) return;
  const rect = card.getBoundingClientRect();
  card.style.setProperty("--sx", `${e.clientX - rect.left}px`);
  card.style.setProperty("--sy", `${e.clientY - rect.top}px`);
});
```

```css
.spotlight-card {
  position: relative;
  overflow: hidden;
  background: #0d120e;
  border: 1px solid rgba(255, 255, 255, 0.08);
  transition: transform 0.4s cubic-bezier(0.22, 1, 0.36, 1), border-color 0.4s ease;
}

.spotlight-card::after {
  content: "";
  position: absolute;
  inset: 0;
  pointer-events: none;
  opacity: 0;
  transition: opacity 0.4s ease;
  background: radial-gradient(
    280px circle at var(--sx, 50%) var(--sy, 0),
    rgba(61, 220, 132, 0.2),
    transparent 70%
  );
}

.spotlight-card:hover::after {
  opacity: 1;
}
```

## 4. Windowed parallax and clip-path curtain reveals

Editorial reveals use geometric clipping rather than standard opacity fade-ins.

### Curtain wipe reveal
Pair `clip-path: inset()` with an asymmetric ease curve:

```css
.curtain-frame {
  overflow: hidden;
  clip-path: inset(0 0 100% 0);
  transition: clip-path 1.2s cubic-bezier(0.77, 0, 0.175, 1);
}

.curtain-frame.is-revealed {
  clip-path: inset(0);
}
```

### Windowed image counter-parallax
Scale the internal image up by 12% to 15% and counter-translate against scroll progress:

```css
.curtain-frame img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transform: translate3d(0, var(--py, 0px), 0) scale(1.14);
  will-change: transform;
}
```

Calculate `--py` during the scroll tick loop using bounding client rect distance from the viewport center:

```javascript
cards.forEach((card) => {
  const rect = card.getBoundingClientRect();
  if (rect.bottom > 0 && rect.top < window.innerHeight) {
    const centerOffset = (rect.top + rect.height / 2 - window.innerHeight / 2) / window.innerHeight;
    card.style.setProperty("--py", `${(centerOffset * -28).toFixed(1)}px`);
  }
});
```

## 5. Procedural ambient texture and grain

Avoid heavy bitmap noise downloads. Generate SVG fractal grain directly via inline data URI:

```css
.noise-overlay {
  position: absolute;
  inset: -50%;
  pointer-events: none;
  z-index: 2;
  opacity: 0.08;
  mix-blend-mode: overlay;
  background: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='3'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
  animation: noise-shift 0.5s steps(2) infinite;
}

@keyframes noise-shift {
  25% { transform: translate(-3%, 2%); }
  50% { transform: translate(2%, -3%); }
  75% { transform: translate(-2%, -2%); }
}
```

## 6. Kinetic letterbox camera aperture

Cinematic entrances employ opening bars to establish visual focus:

```css
.cinema-bar {
  position: absolute;
  left: 0;
  right: 0;
  z-index: 8;
  height: 51vh;
  background: #000;
  animation: bar-reveal 2.2s 0.3s cubic-bezier(0.22, 1, 0.36, 1) forwards;
}

.cinema-bar.top { top: 0; }
.cinema-bar.bottom { bottom: 0; }

@keyframes bar-reveal {
  to { height: 8vh; }
}
```

## 7. Dimensional multi-plane hero layering

Scrollytelling compositions build spatial depth by decomposing the hero into independent visual planes that translate at differential rates during scroll.

### Physical layer sandwich

Structure the DOM hierarchy from deep background to foreground:

1. **Backplane (`z-index: 1`).** Atmospheric environment, high-resolution panorama, or subtle gradient mesh. Moves at `0.2x` scroll rate.
2. **Typography midplane (`z-index: 2`).** Display headlines and editorial statements positioned behind or partially occluded by the subject. Moves at `0.7x` scroll rate.
3. **Primary subject plane (`z-index: 3`).** Isolated product cutout, device model, or focal character with transparent background. Moves at `1.0x` baseline or pins momentarily during act transitions.
4. **Foreground framing plane (`z-index: 4`).** Environmental foreground silhouettes, lens dust, or micro-accents. Moves at `1.3x` to `1.5x` scroll rate to exaggerate camera parallax.
5. **Interactive HUD overlay (`z-index: 5`).** Navigation, chapter trackers, and CTA affordances that remain anchored to the viewport.

### Implementation recipe

Drive translation through normalized scroll progress (`0.0` to `1.0`) mapped to hardware-accelerated transforms:

```javascript
function updateHeroDepth(progress) {
  const p = Math.max(0, Math.min(1, progress));
  const baseTravel = 320; // Subject baseline (1.0x)

  backplane.style.transform = `translate3d(0, ${(p * baseTravel * 0.2).toFixed(1)}px, 0)`;
  typography.style.transform = `translate3d(0, ${(p * baseTravel * 0.7).toFixed(1)}px, 0)`;
  subject.style.transform = `translate3d(0, ${(p * baseTravel * 1.0).toFixed(1)}px, 0)`;
  foreground.style.transform = `translate3d(0, ${(p * baseTravel * 1.5).toFixed(1)}px, 0)`;
}
```

Ensure non-interactive backplane and foreground elements permit clicks and touch events to reach underlying controls:

```css
.hero-backplane,
.hero-foreground {
  pointer-events: none;
}
```

### Accessibility and reduced-motion fallback

Never collapse the visual sandwich into a flat white page under reduced-motion settings. Preserve the layered composition, visual occlusion, and typography placement statically:

```css
@media (prefers-reduced-motion: reduce) {
  .hero-plane {
    transform: none !important;
    transition: none !important;
  }

  .hero-subject {
    position: relative;
    z-index: 3;
  }

  .hero-typography {
    position: absolute;
    z-index: 2;
  }
}
```
