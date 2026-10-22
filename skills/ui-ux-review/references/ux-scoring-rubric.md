### Purpose

Resolve one stable target, run two independent assessments, synthesize a design critique, persist a snapshot, and ask the user what to improve next. The chat response is the primary deliverable; the snapshot is an archive of that run.

### Hard Invariants

- Assessment A (design review) and Assessment B (detector/browser evidence) are both required, except on a native platform (see Assessment Orchestration).
- Assessment A and B MUST run as two isolated sub-agents whenever a sub-agent/Task tool is exposed. Running them inline in this context is "possible" but is NOT permitted; it is a degraded run. Inline is allowed ONLY when no sub-agent tool exists (or the user declined, on harnesses that ask). Native platforms run A alone (see Assessment Orchestration).
- If you degrade for any reason, the report's first line MUST be a banner: `⚠️ DEGRADED: single-context (<reason>)`. A silent degraded critique is a failed critique.
- Assessment A must finish before detector findings enter the parent synthesis context. Detector output is deterministic, but it still anchors judgment.
- A skipped detector is a failed critique run unless `impeccable detect` is missing or crashes after a real attempt, or the platform is native (see Assessment Orchestration).
- Viewable targets require browser inspection when available.
- Any local server started only for critique visualization must run in the background, have a recorded stop method, and be stopped before final reporting unless the user asks to keep it.
- Do not claim a user-visible overlay exists unless script injection succeeded and the detector ran in the page.
- The question is the LAST thing in the response. Write the entire report out first, then ask; nothing follows the question. Prose emitted after a structured question is withheld until the user answers it, so a report written after the question reads as if the critique never ran.
- A run that ends with neither the targeted questions nor a literal `Questions skipped: <reason>` line is an incomplete run. The report is not the finish; the close is.

### Setup

1. **Resolve the target** to a concrete file path or URL. Prefer a source path over a dev-server URL when both identify the same surface; ports drift, paths do not.
   - "the homepage" -> `site/pages/index.astro` or `index.html`
   - "the settings modal" -> the primary component file
   - "this page" -> the current URL or source file
2. **Confirm the target slugs cleanly**:
   ```bash
   .agents/skills/impeccable/scripts/impeccable critique-storage slug "<resolved-path-or-url>"
   ```
   Every later command also accepts the resolved target directly and derives the same slug internally; never hand-write a slug. If this exits non-zero, skip persistence and trend for this run, but continue the critique.
3. **Read `.impeccable/critique/ignore.md`** if it exists. Drop matching findings silently; it is the only prior-run input critique consumes.

### Assessment Orchestration

**Native platforms** (`ios` / `android` / `adaptive`): Assessment B does not apply, because `impeccable detect` and the browser overlay read only web markup. Run Assessment A alone in this context and skip both sub-agent gates below, the Codex permission question included: with no B there is nothing to isolate A from, so this is the complete native method and carries no degraded banner. Do not run `impeccable detect` on native source; its empty result reads as clean.

Delegate Assessment A and Assessment B to separate sub-agents. They must not see each other's output. Do not show findings to the user until synthesis.

Sub-agent gate (all harnesses):
- Unless a harness-specific gate below overrides this, spawn A and B as two isolated, parallel sub-agents whenever a sub-agent/Task tool is exposed. This is the default and is mandatory; do not run them inline because it is faster.
- Desktop apps (see **Desktop apps** under Assessment B) are the one exception to parallel: both sub-agents would drive the app's single window at once. Seed the window, spawn A, wait until it has finished and put the window back, then spawn B. They are still two isolated sub-agents, so this is not the degraded path.
- "Unavailable" means exactly one thing: no sub-agent/Task tool is exposed in this session (or, on harnesses that ask, the user declined). It does not mean inconvenient.
- If and only if sub-agents are unavailable, fall back sequentially: finish and record Assessment A, then run Assessment B, then synthesize, and emit the degraded banner.
- Whichever path you take, declare it in the report header (see Report header provenance). Skipping sub-agents without the banner is the most common failure of this command.

Codex sub-agent gate (overrides the default above; Codex's permission model requires asking before spawning):
- Asking is the normal path, not a degradation. Approving and spawning is the dual-agent path; do not emit the degraded banner just for asking.
- If `spawn_agent` is exposed and the user explicitly allowed sub-agents, delegation, or parallel agent work, spawn A and B immediately (for a desktop app, A first and B once A has finished, as the default gate above says).
- If `spawn_agent` is exposed but the user did not explicitly allow sub-agents, ask exactly once: "Impeccable critique is designed to run two independent sub-agents for an unanchored assessment. May I use sub-agents for this critique?" Then stop until the user answers.
- If allowed, spawn A and B (in sequence for a desktop app). If declined, run sequentially and lead the report with `⚠️ DEGRADED: single-context (sub-agents declined by user)`.
- If `spawn_agent` is not exposed, do not ask; run sequentially and lead with `⚠️ DEGRADED: single-context (spawn_agent unavailable in this session)`.
- If spawning fails after permission, run sequentially and lead with `⚠️ DEGRADED: single-context (sub-agent spawn failed: <exact error>)`.
Prefer `fork_context: false` with self-contained prompts containing cwd, target, live URL, references, product context, and output contract. If using `fork_context: true`, omit `agent_type`, `model`, and `reasoning_effort`.

If browser automation is available, each assessment creates its own new tab. Never reuse an existing tab, even if it is already at the right URL. Desktop apps are the exception (see **Desktop apps** under Assessment B).

### Assessment A: Design Review

Read relevant source files and visually inspect the live page when browser automation is available. Think like a design director.

Evaluate:
- **Design specificity**: Is the composition, interaction, and visual language grounded in this product, or could an unrelated product use it unchanged? Make this judgment before seeing detector output.
- **Holistic design**: hierarchy, IA, emotional fit, discoverability, composition, typography, color, accessibility, states, copy, and edge cases.
- **Cognitive load**: consult the [Cognitive Load Assessment](#cognitive-load-assessment) section below; report checklist failures and decision points with >4 visible options.
- **Emotional journey**: peak-end rule, emotional valleys, reassurance at high-stakes moments.
- **Nielsen heuristics**: consult the [Heuristics Scoring Guide](#heuristics-scoring-guide) section below; score all 10 heuristics 0-4, marking any heuristic the mode-applicability rule allows as `n/a` instead of forcing a number.

Return: design-specificity verdict, heuristic scores, cognitive load, emotional journey, 2-3 strengths, 3-5 priority issues, persona red flags, minor observations, and provocative questions.

### Assessment B: Detector + Browser Evidence

Run the bundled detector and browser visualization evidence. On web, Assessment B is mandatory and must remain isolated from Assessment A until both are complete.

CLI scan:
```bash
.agents/skills/impeccable/scripts/impeccable detect --json [target]
```

- Pass markup files/directories as `[target]`; do not pass CSS-only files.
- For URLs, skip CLI scan and use browser visualization.
- For very large trees (500+ scannable files), narrow scope or ask.
- Exit code 0 = clean; 2 = findings.
- If the detector entrypoint is missing or fails to load, report deterministic scan unavailable and continue with browser/manual review.

Browser visualization is required for a viewable target when browser automation is available. Use a localhost dev/static URL for local files; avoid `file://` unless the available browser explicitly supports this workflow. Overlay flow:

1. Create a fresh tab and navigate. Prefer the harness's native/browser-canvas screenshot path before hand-rolling a Playwright/Puppeteer script; only fall back to a custom script when no native browser tool is exposed.
2. Preflight mutable injection by setting `document.title` and appending a `<script>` tag. Read-only evaluate APIs do not count.
3. If mutation is unavailable, skip live server, browser presentation, and injection; report fallback signal.
4. If mutation is available, start `.agents/skills/impeccable/scripts/impeccable live-server --background`, present the browser if supported, label `[Human]`, scroll top, inject `http://localhost:PORT/detect.js`, wait 2-3 seconds, read `impeccable` console messages, then run `.agents/skills/impeccable/scripts/impeccable live-server stop --keep-inject`. The overlay went in through the browser, so the project's HTML has no script tag to strip; a bare `stop` also runs `live-inject --remove` against the project's entry file, an edit a read-only critique should not make.
5. For multi-view targets, inject on 3-5 representative pages.

**Desktop apps** (Electron, NW.js, CEF, WebView2): there is no URL to open, so Assessment B attaches to the running app instead.

1. Launch the app with a local DevTools port: `--remote-debugging-port=9222` (Electron, NW.js, CEF), or `WEBVIEW2_ADDITIONAL_BROWSER_ARGUMENTS=--remote-debugging-port=9222` for WebView2. Keep the port on 127.0.0.1 and never expose it beyond this machine; prefer a test profile and test data.
2. Seed the state under review (route, open panel, theme, data). The scan reads the window as it stands. Keep the window on screen: a minimized or hidden window scans without the pixel contrast reads.
3. Run `.agents/skills/impeccable/scripts/impeccable detect --cdp 9222 --target <part of the page URL or title> --json`. It returns the same JSON as a URL scan and leaves the page as found. With several pages open it fails and lists them; rerun with a `--target` that names one.
4. Take screenshots through the harness's CDP tooling (`Page.captureScreenshot` on the same target). Skip the live-server overlay: there is no `[Human]` tab.

The app has one window, so the assessments take turns in it instead of opening tabs (A, then B; see the sub-agent gate), and each must leave it as found: put back any route, scroll, theme, or panel it changed. Tauri on macOS (WKWebView) and on Linux (WebKitGTK) expose no CDP: run Assessment A and the source scan only, and say so in Run Notes.

Codex Browser note: Use the Browser skill. Do not spend a Browser attempt on `file://`. Only call `visibility.set(true)` after mutable script injection is confirmed for the `[Human]` overlay path; verify with `get()`. Use `tab.dev.logs({ filter: "impeccable" })` for console results. Its Playwright `evaluate(...)` surface is read-only; do not rely on it for mutation.

Return: CLI findings JSON/counts, browser console findings if applicable, false positives, and skipped/failed browser steps with concrete reasons.

After Assessment B returns usable CLI findings, reuse them. Do not rerun `impeccable detect` in the parent unless Assessment B failed, was truncated, or omitted count, rule names, or file locations.

Codex failure accounting: final Run Notes must include target slug, ignore list, assessment independence, CLI detector, browser visibility, overlay injection, live-server cleanup, temp-file cleanup, and any fallback signal used. Do not run repo status checks, late API spelunking, or unrelated verification after the report is assembled.

### Generate Combined Critique Report

Synthesize both assessments into a single report. Do not simply concatenate. Weave the findings together, noting where the LLM review and detector agree, where the detector caught issues the LLM missed, and where detector findings are false positives.

The chat response is the primary user-facing deliverable. Present the full structured critique below in chat; do not replace it with a summary and a link. The persisted snapshot is an archive of that run.

Codex final-answer note: `$impeccable critique` produces a report artifact, so the final chat response should intentionally exceed the usual concise close-out style. Do not title the final response "Critique Summary" unless the user explicitly asked for a summary.

Structure your feedback as a design director would:

#### Report header provenance

The report's first line MUST declare how the assessments were run, so a degraded run is never silent:
- Dual-agent: `Method: dual-agent (A: <agent-id> · B: <agent-id>)`
- Degraded: `⚠️ DEGRADED: single-context (<reason, e.g. no sub-agent tool exposed>)`
- Native: `Method: design review only (detector not applicable, native platform)`

#### Design Health Score
> *Consult the [Heuristics Scoring Guide](#heuristics-scoring-guide) section below.*

Present the Nielsen's 10 heuristics scores as a table:

| # | Heuristic | Score | Key Issue |
|---|-----------|-------|-----------|
| 1 | Visibility of System Status | ? | [specific finding or "n/a" if solid] |
| 2 | Match System / Real World | ? | |
| 3 | User Control and Freedom | ? | |
| 4 | Consistency and Standards | ? | |
| 5 | Error Prevention | ? | |
| 6 | Recognition Rather Than Recall | ? | |
| 7 | Flexibility and Efficiency | ? | |
| 8 | Aesthetic and Minimalist Design | ? | |
| 9 | Error Recovery | ? | |
| 10 | Help and Documentation | ? | |
| **Total** | | **??/[applicable max]** | **[Rating band]** |

The applicable maximum is 4 times the number of heuristics you actually scored: **/40** when all ten apply, **/32** when two are `n/a`. Never print `/40` over a partial set.

Be honest with scores. A 4 means genuinely excellent. Most real interfaces score 20-32 out of 40.

**Mode applicability**: heuristics 7 (Flexibility and Efficiency) and 10 (Help and Documentation) may be scored `n/a` on Persuade and Experience surfaces (landing pages, campaigns, portfolios, bodies of work), as may any other heuristic that genuinely cannot apply to the surface under review. Write `n/a` in the Score cell with a one-line reason, and renormalize the total to the applicable maximum (e.g. **24/32** when two heuristics are n/a) so the rating band stays proportional. The persisted snapshot must record the applicable maximum and which heuristics were scored n/a.

#### Design Specificity Verdict

**Start here.** Does the result feel authored for this product, or category-interchangeable?

**LLM assessment**: Your unanchored evaluation of design specificity. Cover overall coherence, structural sameness, category-interchangeable choices, and missed opportunities for product character.

**Deterministic scan**: Summarize what the automated detector found, with counts and file locations. Note any additional issues the detector caught that you missed, and flag any false positives. On a native platform, write `not applicable (native platform)` instead.

**Visual overlays** (if injection succeeded): Tell the user that overlays are now visible in the **[Human]** tab in their browser, highlighting the detected issues. Summarize what the console output reported. If browser visualization was attempted but injection failed, say that no reliable user-visible overlay is available and report the fallback signal instead.

