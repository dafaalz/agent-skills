# Canvas image sequence and scroll scrubbing

High-performance frame scrubbing, smooth scroll synchronization, predictive image caching, and layout morphing indicators.

## 1. Smooth scroll loop consolidation

Never run smooth scroll engines in detached background intervals. Consolidate Lenis or custom virtual scroll into the application central `requestAnimationFrame` loop to guarantee identical tick execution across scroll offsets, canvas scrubbers, and DOM transforms.

```javascript
import Lenis from "lenis";

const isReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
const lenis = !isReducedMotion ? new Lenis({ lerp: 0.09, autoRaf: false }) : null;

function mainTick(time) {
  if (lenis) lenis.raf(time);

  const scrollY = window.scrollY;
  // Execute canvas scrubbing and parallax calculations with identical scrollY
  updateScrubbers(scrollY);

  requestAnimationFrame(mainTick);
}
requestAnimationFrame(mainTick);
```

When opening full-screen modals, halt smooth scroll with `lenis.stop()` and restore on dismiss with `lenis.start()`.

## 2. Canvas sequence scrubbing versus video tag scrubbing

Scrubbing HTML5 `<video>` tags via `video.currentTime` fails during rapid reverse scrolling due to browser hardware video decoder I-frame seeking latency.

Canvas image sequence scrubbing eliminates dropped frames by drawing preloaded WebP or JPEG frames directly into a 2D canvas context.

```javascript
const canvas = document.querySelector("#sequence-canvas");
const ctx = canvas.getContext("2d", { alpha: false }); // Skip expensive alpha blending passes
const totalFrames = 240;
const frameCache = new Map();
let currentFrameIndex = 0;

// High-DPI clamp to avoid mobile GPU memory spikes
function resizeCanvas() {
  const dpr = Math.min(window.devicePixelRatio || 1, 2);
  const rect = canvas.getBoundingClientRect();
  canvas.width = (rect.width * dpr) | 0;
  canvas.height = (rect.height * dpr) | 0;
  drawFrame(frameCache.get(currentFrameIndex));
}
window.addEventListener("resize", resizeCanvas);
```

### Predictive caching and batch preloading
Load the initial frame immediately to populate the screen. Stream subsequent frames in micro-batches to protect network saturation.

```javascript
function loadFrame(i) {
  if (frameCache.has(i)) return Promise.resolve(frameCache.get(i));
  return new Promise((resolve) => {
    const img = new Image();
    img.onload = () => {
      frameCache.set(i, img);
      resolve(img);
    };
    img.onerror = () => resolve(null);
    img.src = `/sequence/frame_${String(i + 1).padStart(3, "0")}.webp`;
  });
}

// Scrub dispatcher with forward and backward predictive cache
function scrubTo(targetIndex) {
  currentFrameIndex = targetIndex;
  const cachedImg = frameCache.get(targetIndex);

  if (cachedImg) {
    drawFrame(cachedImg);
  } else {
    loadFrame(targetIndex).then((img) => {
      if (img && Math.abs(currentFrameIndex - targetIndex) < 5) {
        drawFrame(img);
      }
    });
  }

  // Preload immediate neighbor frames ahead and behind
  [-3, -2, -1, 1, 2, 3].forEach((offset) => {
    const neighbor = targetIndex + offset;
    if (neighbor >= 0 && neighbor < totalFrames && !frameCache.has(neighbor)) {
      loadFrame(neighbor);
    }
  });
}
```

## 3. Dynamic sliding pill tab indicators

Morphing navigation indicators track active buttons by transferring bounding coordinates without hardcoded CSS widths.

```html
<div class="tab-list" role="tablist">
  <div class="sliding-pill" id="tab-pill"></div>
  <button type="button" role="tab" class="tab-btn" aria-selected="true">All (12)</button>
  <button type="button" role="tab" class="tab-btn" aria-selected="false">Design</button>
  <button type="button" role="tab" class="tab-btn" aria-selected="false">Engineering</button>
</div>
```

```css
.tab-list {
  position: relative;
  display: flex;
  align-items: center;
  background: #0a100c;
  border-radius: 99px;
  padding: 0.4rem;
}

.sliding-pill {
  position: absolute;
  border-radius: 99px;
  pointer-events: none;
  background: #10b981;
  transition: all 0.4s cubic-bezier(0.22, 1, 0.36, 1);
}
```

```javascript
function movePill(pillElement, activeButton) {
  if (!activeButton) return;
  pillElement.style.cssText = `
    left: ${activeButton.offsetLeft}px;
    top: ${activeButton.offsetTop}px;
    width: ${activeButton.offsetWidth}px;
    height: ${activeButton.offsetHeight}px;
    opacity: 1;
  `;
}
```

## 4. Forced layout reflow for animation re-triggering

When filtering dynamic grids, re-triggering entrance animations on existing DOM nodes requires clearing keyframes and forcing a layout reflow.

```javascript
function retriggerGridAnimation(cards) {
  let index = 0;
  cards.forEach((card) => {
    card.style.animation = "none";
    // Trigger layout reflow to register style invalidation
    void card.offsetWidth;
    card.style.animation = `card-pop 0.65s cubic-bezier(0.22, 1, 0.36, 1) ${index++ * 60}ms backwards`;
  });
}
```

## 5. Dense GOP video encoding for timeline scrubbing

When requirements mandate native `<video>` elements instead of 2D canvas frame sequences, standard streaming video files fail because long keyframe intervals (60 to 120 frames) stall hardware video decoders during reverse scrubbing.

### FFmpeg encoding recipe

Re-encode video assets with dense keyframe intervals (Group of Pictures of 1 or 2 frames), zero B-frames (`-bf 0`) to prevent bidirectional decoder stalls, and stripped audio:

```bash
ffmpeg -i source.mp4 \
  -c:v libx264 \
  -preset slow \
  -crf 20 \
  -g 2 \
  -keyint_min 2 \
  -bf 0 \
  -an \
  -pix_fmt yuv420p \
  -movflags +faststart \
  scrub_optimized.mp4
```

### Critical flags explained

- `-g 2` and `-keyint_min 2`. Places an intra-coded frame (I-frame) every 2 frames. The browser decoder never seeks backward through more than one delta frame.
- `-bf 0`. Eliminates bidirectional predictive B-frames. Enforces pure forward prediction to avoid reverse-scrub decode buffer thrashing.
- `-an`. Strips the audio stream. Prevents browser audio buffer desynchronization and autoplay permission rejections during rapid scroll direction changes.
- `-movflags +faststart`. Relocates the `moov` atom header to the beginning of the file, allowing immediate seek operations before the entire media payload finishes downloading.

### Scrub controller synchronization

Clamp currentTime updates inside `requestAnimationFrame`, prevent decoder queue overflow using a seeking guard, and check `video.readyState >= 2` before seeking:

```javascript
const video = document.querySelector("#scrub-video");
let targetTime = 0;
let rafId = null;

function renderScrubFrame() {
  if (video.readyState >= 2 && !video.seeking) {
    if ("fastSeek" in video) {
      video.fastSeek(targetTime);
    } else {
      video.currentTime = targetTime;
    }
  }
  rafId = null;
}

function updateVideoScrub(progress) {
  if (!video.duration) return;
  const p = Math.max(0, Math.min(1, progress));
  targetTime = p * video.duration;

  if (!rafId) {
    rafId = requestAnimationFrame(renderScrubFrame);
  }
}
```
