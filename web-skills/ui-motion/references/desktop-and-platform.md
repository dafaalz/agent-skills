# Desktop and platform native motion engineering

Engineering guidelines for native desktop motion across Windows 11, macOS, Linux, Electron, and Tauri.

## 1. Windows 11 Fluent motion and DWM compositor

Windows 11 motion executes directly on the Desktop Window Manager (DWM) compositor thread. Animations remain smooth even when the UI dispatcher thread experiences heavy workload.

### Standard duration tokens in WinUI 3

Windows App SDK and WinUI 3 establish standard duration resources:

| Token | Duration | Application |
|---|---|---|
| `ControlFasterAnimationDuration` | 83ms | Immediate tactile feedback, press states, ripples, hover highlights |
| `ControlFastAnimationDuration` | 167ms | Micro-interactions, checkboxes, toggles, compact control expansions |
| `ControlNormalAnimationDuration` | 250ms | Standard UI transitions, page navigation, modal dialogs, panel expansions |

Never exceed 300ms in standard desktop workflows to avoid cognitive friction during frequent navigation.

### Baseline transition curves

WinUI 3 mandates two primary cubic-bezier curves:
- **Fast Out, Slow In (Deceleration curve).** `cubic-bezier(0, 0, 0, 1)`. Mandatory baseline for UI elements entering the viewport or navigating into view. Elements arrive with high initial velocity and encounter high resistance before stopping.
- **Slow Out, Fast In (Acceleration curve).** `cubic-bezier(1, 0, 1, 1)`. Mandatory baseline for elements exiting the viewport. Elements accelerate rapidly to reach escape velocity, clearing display space quickly.

Never use linear easing for state changes. Linear motion feels mechanical and ignores physical friction.

### Backdrop materials Mica versus Acrylic

Windows 11 provides two translucent backdrop materials with contrasting performance characteristics:

| Property | Mica (`MicaBackdrop`) | Acrylic (`DesktopAcrylicBackdrop`) |
|---|---|---|
| Compositor sampling | Samples wallpaper exactly once per surface creation or wallpaper change | Samples pixels behind window continuously at 60Hz or 120Hz display refresh |
| GPU overhead | Extremely low, minimal memory bandwidth impact | High fill rate, continuous multi-pass Gaussian blur |
| Intended usage | Permanent application window backdrops and tabbed title bars | Transient, light-dismiss surfaces only (flyouts, context menus, tooltips) |
| System fallback | Automatically falls back to solid neutral background under battery saver or low-end GPU | Automatically disabled when transparency is turned off in Windows settings |

Never use Acrylic as a permanent window background. Applying continuous Gaussian blur across an entire application window saturates GPU fill rate and causes frame drops during resizing.

---

## 2. macOS AppKit and QuartzCore transactions

Desktop macOS applications orchestrate window, split-view, and toolbar animations through AppKit animation contexts and CoreAnimation (`QuartzCore`) transactions.

### Atomic transaction batching with NSAnimationContext

AppKit maintains a thread-local stack of `NSAnimationContext` instances:
- Default context duration is 0.25 seconds (250ms).
- Layout updates, frame changes, and opacity adjustments execute atomically via `NSAnimationContext.runAnimationGroup(_:completionHandler:)`.
- Accessing properties through the `animator()` proxy object triggers implicit animations if context duration is non-zero.

```swift
import AppKit
import QuartzCore

final class SidebarAnimator {
    static func resizeSidebar(view: NSView, targetWidth: CGFloat, completion: (() -> Void)? = nil) {
        NSAnimationContext.runAnimationGroup({ context in
            context.duration = 0.25
            context.timingFunction = CAMediaTimingFunction(name: .easeInEaseOut)
            context.allowsImplicitAnimation = true

            var newFrame = view.frame
            newFrame.size.width = targetWidth
            view.animator().frame = newFrame
            view.animator().alphaValue = targetWidth > 0 ? 1.0 : 0.0
        }, completionHandler: {
            completion?()
        })
    }
}
```

Never mutate layout coordinates across individual ticks during window or split-view resize. Batch mutations inside `runAnimationGroup` to prevent layout thrashing on the AppKit main thread.

---

## 3. Electron multi-process motion architecture

Electron splits execution between a single Main Process (Node.js) and multiple Renderer Processes (Chromium Blink).

### Process starvation hazard

The Main Process manages the native OS window message pump, native menus, and IPC dispatch. Blocking the Main Process with synchronous file I/O (`fs.readFileSync`) or heavy JSON parsing freezes window message loops, immediately halting window dragging, resizing, and window animations across all active windows.

Offload heavy computation to background Node.js utility processes (`utilityProcess.fork()`) or worker threads.

### Frameless window dragging with native OS delegation

Implementing custom window dragging in JavaScript via `mousedown` and `mousemove` listening combined with IPC `win.setPosition()` introduces 16ms to 33ms roundtrip latency per event. This latency causes cursor detachment, jitter, and frame drops.

Delegate window dragging directly to the host operating system window manager:

```html
<header class="custom-titlebar">
  <div class="window-drag-region">
    <span class="window-title">Desktop Application</span>
  </div>
  <div class="window-controls">
    <button id="minimize-btn" type="button" aria-label="Minimize Window">−</button>
    <button id="close-btn" type="button" aria-label="Close Window">✕</button>
  </div>
</header>

<style>
.custom-titlebar {
  display: flex;
  height: 38px;
  align-items: center;
  user-select: none;
  -webkit-app-region: drag;
}

.window-drag-region {
  flex: 1;
  padding-left: 16px;
  pointer-events: none;
}

.window-controls {
  display: flex;
  -webkit-app-region: no-drag;
}

.window-controls button {
  width: 46px;
  height: 38px;
  border: none;
  background: transparent;
  cursor: pointer;
}
</style>
```

Rules for frameless window title bars:
1. Apply `-webkit-app-region: drag` to the draggable title bar container.
2. Mark all interactive elements (buttons, inputs, menus) with `-webkit-app-region: no-drag`.
3. Apply `user-select: none` to the entire title bar to prevent selection highlighting during drag.

---

## 4. Tauri and WRY cross-platform pipelines

Tauri v2 avoids bundling Chromium, using platform-native WebViews instead:
- Windows uses Microsoft Edge WebView2 (Blink engine with DirectComposition acceleration).
- macOS uses Apple WKWebView (WebKit engine with Metal CoreAnimation hosting).
- Linux uses WebKitGTK (WebKit engine with EGL and Wayland/X11 rendering).

### IPC throughput constraints

Tauri message passing serializes data over native IPC buffers. Never send continuous high-frequency animation coordinates (60Hz or 120Hz drag positions) over Tauri Rust IPC. Compute coordinate changes entirely in the frontend animation loop and synchronize only final committed state to the Rust backend.

### Platform rendering divergence

CSS filter blur and layer promotion perform differently across desktop WebViews. Edge WebView2 handles heavy backdrop filters efficiently, whereas WKWebView and WebKitGTK drop frames when blurring large surface areas. Keep transition blur radii below 15px.

---

## 5. Linux desktop pipelines and Wayland stability

Linux desktop applications built on WebKitGTK interface with GPU drivers and display servers via the DMABUF renderer (`AcceleratedSurfaceDMABuf`).

### Wayland Protocol Error 71 mitigation

Rapid window resizing on Wayland compositors with NVIDIA proprietary drivers can trigger `Gdk-Message: Error 71 (Protocol error) dispatching to Wayland display`, crashing the application process.

Apply the explicit sync workaround in Rust before initializing the window:

```rust
fn main() {
    #[cfg(target_os = "linux")]
    {
        if std::env::var("__NV_DISABLE_EXPLICIT_SYNC").is_err() {
            std::env::set_var("__NV_DISABLE_EXPLICIT_SYNC", "1");
        }
    }

    tauri::Builder::default()
        .run(tauri::generate_context!())
        .expect("error running tauri application");
}
```

Never unconditionally set `WEBKIT_DISABLE_COMPOSITING_MODE=1`. That flag disables hardware acceleration completely, forcing CPU software rasterization and causing 100% CPU core utilization.

---

## 6. Verification checklist for desktop apps

| Check | Passing condition |
|---|---|
| Duration budget | Normal transitions stay under 250ms, fast feedback states under 167ms |
| Easing curves | Deceleration `cubic-bezier(0, 0, 0, 1)` on entrances, acceleration `cubic-bezier(1, 0, 1, 1)` on exits |
| Title bar dragging | Non-client title bar uses `-webkit-app-region: drag` with zero JavaScript IPC drag loops |
| Interactive controls | Controls inside draggable header marked `-webkit-app-region: no-drag` |
| Windows backdrop | Mica used for base window backdrops, Acrylic restricted to transient popovers |
| Main process unblocked | Zero synchronous file I/O or heavy parsing in Electron or Tauri main threads |
| Wayland sync | Explicit sync workaround configured for Linux WebKitGTK builds |
