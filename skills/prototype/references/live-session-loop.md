Interactive live variant mode: select elements in the browser, pick a design action, and get AI-generated HTML+CSS variants hot-swapped via the dev server's HMR.

## Prerequisites

A running dev server with HMR (Vite, Next.js, Bun, etc.), OR a static HTML file open in the browser. If the dev server's default port is busy, the app is very likely ALREADY running; probe the default URL before spawning a second server.

Live editing requires a local checkout; injection into deployed production sites (including HTTPS) is unsupported. For production inspection, use `.agents/skills/impeccable/scripts/impeccable detect <url>` or the browser extension, not the live helper. Do not disable browser security or weaken production CSP to enable live mode.

Codex: run live helper commands, the app dev server, and any dependency-installing setup with `sandbox_permissions: "require_escalated"` from the start; live mode depends on localhost and package-manager network access that the sandbox blocks.

## The contract (read once)

Execute in order. No step skipped, no step reordered. Every tool output in live mode may carry an `_instructions` field: it is the authoritative next step for that exact situation, with real ids and paths substituted; when it conflicts with your recollection of this document, `_instructions` wins.

1. `impeccable live`: boot. If the request names or implies a file, route, or app inside a monorepo, infer the concrete path and run `.agents/skills/impeccable/scripts/impeccable live --target <path>` instead; then run the rest of this live session from the returned `projectRoot`. The boot resolves the app root from dev-server config files and persists it in `.impeccable/live/roots.json`; every helper re-anchors to that manifest at startup (a wrong cwd cannot fork session state), PRODUCT.md / DESIGN.md are discovered upward to the git root, and relative helper args like `--file` resolve against the app root.
2. Open the app URL that serves `pageFile` (infer from `package.json`, docs, terminal output, or an open tab). Never use `serverPort`; it's the helper, not the app. **Cursor:** `browser_navigate` to that URL before polling; do not skip. **Other harnesses:** use the available browser tool; if the URL is uncertain, ask the user once.
3. Poll loop with the default long timeout (600000 ms). Run `impeccable live-poll` again immediately after every event or `--reply`; Codex runs this one-shot poll in the foreground. Never pass a short `--timeout=`. The global bar's **Impeccable mark** dims with a pulsing amber dot when nothing is polling `/poll`; restart `impeccable live-poll` to reconnect.
4. On `generate`: reuse `event.scaffold` when present; read the screenshot if present; load the action's reference; deliver variants; `--reply done`; poll again. Generate in this thread: you already hold the project's tokens and layout. The overlay preview IS the verification channel; do not screenshot, re-render, or QA variants between generate and accept. Apply craft-floor's contrast, spacing, and type floors by construction as you write; full verification runs once at accept on the chosen variant.
5. On `steer`: read the message and `pageUrl`; do the work; `--reply steer_done`; poll again. No pickup ack.
6. On `accept` / `discard`: the poll script runs `impeccable live-accept`, acknowledges delivery, and prints `_completionAck`. Plain accepts/discards are terminal immediately; carbonize accepts stay recoverable until `impeccable live-complete --id EVENT_ID` runs. Finish that cleanup before polling again.
7. If interrupted, run `impeccable live-status` or `impeccable live-resume` before guessing. The journal under `.impeccable/live/sessions/` is canonical and replays unacknowledged work after a helper restart; the injected `live.js` re-attaches when the page reopens. Fall back to the direct-edit loop only when `impeccable live-resume` reports no active session, never because disconnects felt frequent.
8. On `exit`: run the cleanup at the bottom.

Harness policy:
- **Claude Code**: run the poll as a **background task** (no short timeout); the harness notifies you on completion. Do not block the shell.
- **Cursor**: **one-shot** poll in a **background terminal** with notify on `"type":"(steer|generate|accept|discard|manual_edit_apply|variant_mount_failed|prefetch|exit)"`; handle, `--reply`, restart the poll. Do **not** use `--stream` on Cursor (measured ~5s pickup vs sub-second one-shot).
- **Codex**: default one-shot poll in a **yielded foreground exec session**. No `&`, no `--stream`, never leave Live without an active foreground poll. Starting the poll is not enough: SERVICE it (keep reading the exec session until it returns an event). Never announce "waiting for the user" and idle; a yielded poll nobody reads is a dead session, and the user's Go sits unanswered.
- **Other harnesses**: one-shot foreground unless you know stdout reliably returns when a shell exits.

Delivery policy: atomic single-edit delivery everywhere; do not switch a harness to progressive publishing unless its poll loop is known not to block on the extra calls.

Chat is overhead. No recap, no tutorial output, no pasting PRODUCT / DESIGN bodies. Spend tokens on tools and edits; on failure, one or two short sentences.

## Poll loop

```
LOOP:
  .agents/skills/impeccable/scripts/impeccable live-poll   # default long timeout; no --timeout=
  Read JSON; dispatch on "type"

  "generate"  → Handle Generate; reply done; LOOP
  "steer"     → Handle Steer; reply steer_done; LOOP
  "accept"    → Handle Accept; complete carbonize cleanup if required; LOOP
  "discard"   → Handle Discard; LOOP
  "prefetch"  → Handle Prefetch; LOOP
  "manual_edit_apply" → Handle Manual Edit Apply; reply done|partial|error; LOOP
  "variant_mount_failed" → Fix the variant files; reply done --file <path>; LOOP
  "timeout"   → LOOP
  "exit"      → break → Cleanup
```

`variant_mount_failed` means the browser could not render what you published (`variant`, module `url`, `error`). The user sees a persistent error card, not variants. Fix the variant files, then `--reply EVENT_ID done --file <manifest or source path>`; the browser retries on its own.

**Stream mode** (`--stream`, experimental, never on Cursor): one long-lived process, one JSON line per event, `--reply` from a separate command. Only for harnesses that read incremental stdout reliably.

## Start

```bash
.agents/skills/impeccable/scripts/impeccable live
```

Output JSON: `{ ok, serverPort, serverToken, pageFiles, roots, hasProduct, product, productPath, hasDesign, design, designPath, hasSurfaceBrief, surfaceBrief }`. `roots` is the resolved root manifest; `projectRoot` mirrors `roots.appRoot`. The surface brief rides along; do not shell out to `impeccable surface-brief` separately. Precedence for generation: **DESIGN.md wins on visual decisions; PRODUCT.md wins on durable product and voice decisions; the surface brief wins on this surface's strategy.** When DESIGN.md is missing, identity is **not** absent; extract it from CSS variables, computed styles, and sibling components (Step 4 Phase A). Identity preservation is the default; departure requires the user's explicit redesign intent.

`serverPort`/`serverToken` belong to the small helper HTTP server (`/live.js`, SSE, `/poll`), not your dev server; the page URL is whatever origin serves a `pageFiles` entry.

If output is `{ ok: false, error: "config_missing" | "config_invalid", path }`, this project needs one-time configuration: read the live setup guide and follow it. If the output carries a non-null `configDrift`, tell the user once which HTML files are uncovered and suggest adding them or switching `files` to a glob; never auto-edit the config.

## Recovery commands

The append-only journal under `.impeccable/live/sessions/` is canonical durable state (not project source). When the chat was interrupted, polling was missed, the helper restarted, or the browser reloaded:

```bash
.agents/skills/impeccable/scripts/impeccable live-status      # helper state, active sessions, queued events; works with the helper down
.agents/skills/impeccable/scripts/impeccable live-resume --id SESSION_ID   # active snapshot, pending event, next safe action
.agents/skills/impeccable/scripts/impeccable live-complete --id SESSION_ID # canonical manual final acknowledgement after verified cleanup
```

Server restart rule: start `impeccable live-server` again, then poll; startup requeues unacknowledged events, so never ask the user to click Go again unless `impeccable live-resume` says no active session exists.

## Handle fallback

When wrap returns `fallback: "agent-driven"`, you pick the source file yourself; the goal is unchanged: three preview variants now, and the accepted one persisted where the next build cannot wipe it.

1. **Find where the element really lives** from the error payload: `element_not_in_source` + `generatedMatch` means the served HTML is generated, so find the generator's template or partial; `element_not_found` means runtime-injected, so find the rendering component or data source; `file_is_generated` resolves the same way. A purely visual change may belong in a shared stylesheet rather than a template.
2. **Preview in the served file**: manually write the same wrapper scaffold `impeccable live-wrap` produces into the file the browser actually loaded, moving the element itself into the original slot: `<!-- impeccable-variants-start ID --><div data-impeccable-variants="ID" data-impeccable-variant-count="3" style="display: contents"><div data-impeccable-variant="original">THE ELEMENT, UNCHANGED</div><!-- Variants: insert below this line --></div><!-- impeccable-variants-end ID -->`. Insert your variant divs after the marker, then `--reply EVENT_ID done --file <served file>`. Never drop the original slot: discard restores the element from it and refuses a wrapper without one. This edit is temporary; a regen wiping it is fine.
3. **On accept, write to true source** (accept refuses generated files, so `_acceptResult.handled` is usually `false` here): structural change → template/component source; visual-only → the right stylesheet; content rendered from data → the data source or render logic. Then remove the temporary wrapper from the served file.
4. **On discard**, just remove the temporary wrapper.

## Handle `accept`

Event: `{id, variantId, _acceptResult, _completionAck}`. The poll script already ran `impeccable live-accept` deterministically and acknowledged delivery; the browser DOM is already updated.

- The accept event includes `pageUrl`; the poll script must forward it to `impeccable live-accept --page-url PAGE_URL` so accept-time cleanup only scrubs staged copy edits for the current page.
- `_completionAck.ok !== true`: do not poll yet. Run `impeccable live-status` / `impeccable live-resume`, finish cleanup manually if needed, then `impeccable live-complete --id EVENT_ID`.
- `handled: true, carbonize: false`: nothing to do; poll again.
- `handled: true, carbonize: true`: required cleanup below; `_acceptResult.todo`, `_completionAck.requiresComplete`, and the stderr banner all point at it.
- `handled: false, mode: "fallback"`: the session lived in a generated file; you already wrote true source in fallback Step 3; clean the temporary wrapper and poll.
- `handled: false, mode: "error"`: **do not hand-edit the file.** `source_locked`: rerun the same `impeccable live-accept` command (idempotent) until the publisher releases. `accept_receipt_conflict`: the session already resolved as `priorOperation`; run `impeccable live-status` and tell the user. Anything else: report briefly, run `impeccable live-status` first.
- `handled: false` without `mode`: manual cleanup: read file, find markers, edit.

### Required after accept (carbonize)

`carbonize: true` means the accepted variant is stitched into source with helper markers and inline CSS (so the browser renders with no gap). That stitch-in is temporary; rewrite it into permanent form before anything else, or dead `@scope` rules, wrapper divs, and marker comments accumulate across sessions. Five steps, synchronously, before the next poll:

1. **Locate the carbonize block** in `_acceptResult.file`: bracketed by `<!-- impeccable-carbonize-start/end SESSION_ID -->` with a `<style data-impeccable-css>` element; read the `<!-- impeccable-param-values -->` comment first when present, it drives steps 3 and 4.
2. **Move the CSS rules** into the project's real stylesheet (whichever already owns styling for the surrounding element).
3. **Bake param values while rewriting selectors**: retarget `@scope ([data-impeccable-variant="N"])` to real semantic classes; keep only the `:scope[data-p-<id>="VALUE"]` branch matching the chosen value; substitute `var(--p-<id>)` literals or update the var's default.
4. **Unwrap the accepted content**: delete the inner variant div (and on JSX the outer `data-impeccable-carbonize` div); drop `data-impeccable-params` and all `data-p-*` attributes.
5. **Delete** the inline `<style>` block, the param-values comment, both carbonize markers, and any `@scope` rules for non-accepted variants.

Then run `impeccable live-complete --id SESSION_ID` and verify `phase: "completed"` before polling again. The command is a gate, not a formality: it refuses with `error: "source_dirty"` plus findings while any live-mode leftover remains; fix and rerun (`--force` only for false positives).

## Handle `discard`

Event: `{id, _acceptResult, _completionAck}`. The poll script already restored the original and acknowledged `discarded`. Nothing to do unless `_completionAck.ok !== true`; then `impeccable live-complete --id EVENT_ID --discarded` and poll again.

## Handle `steer`

Event: `{id, message, pageUrl}`: page-level direction from the global bar's Steer control (typed or spoken), no element context, no variant cycling. Read `message`, inspect the page or files as needed, make edits or answer in prose. Reply `.agents/skills/impeccable/scripts/impeccable live-poll --reply EVENT_ID steer_done ["Optional short toast"]`, or on failure `--reply EVENT_ID error "Short reason"`, then poll immediately. No separate pickup reply; the Steer bar unlocks on `steer_done` or `error`.

## Handle `prefetch`

Event: `{pageUrl}`: fired once per route on first selection; the user is likely about to Go on a page you have not read. Resolve the route to its file (root `/` is usually the boot's `pageFile`; multi-page sites often map `/foo` to `public/foo/index.html`; SPAs map everything to one entry), read it, poll again. No `--reply`. If you cannot resolve it confidently, skip and poll.

## Handle `manual_edit_apply`

Event: `{id, pageUrl, batch: {entries}, evidencePath?, chunk?, repair?, deadlineMs}`.

The user already clicked Apply. Do not ask what to do, discard, or redirect to Go. The parent live thread keeps the foreground poll loop and sends the final `/poll --reply --data`.

When native subagents are available, delegate source edits to `impeccable_manual_edit_applier` / `impeccable-manual-edit-applier`. Pass cwd, scripts path, event id, page URL, chunk/deadline, `batch`, `evidencePath`, and the canonical JSON result schema. The subagent must not poll or reply. If unavailable, apply inline with the same contract.

If `repair` is present, the previous Apply changed source but final validation failed. Fix the current source and return the same canonical JSON result; do not roll files back yourself. The browser will ask the user before any rollback.

After source edits finish, reply exactly once with `.agents/skills/impeccable/scripts/impeccable live-poll --reply EVENT_ID done --data '{"status":"done","appliedEntryIds":["8hexid"],"failed":[],"files":["src/page.html"],"notes":[]}'`. Use `status:"partial"` or `status:"error"` with `failed[]` when not every entry applied. Then poll again. Never reply without the event id; `--reply done --file ...` is invalid for manual Apply.

## Exit

The user stops live mode by saying so in chat, closing the tab (SSE drops; poll returns `exit` after 8s), or the browser's exit button. On `exit`, kill any still-running background poll, then clean up.

## Cleanup

```bash
.agents/skills/impeccable/scripts/impeccable live-server stop
```

Stops the helper and runs `impeccable live-inject --remove` to strip the injected script (use `stop --keep-inject` to keep it for a quick restart; `.impeccable/live/config.json` persists as project config). Then search for and remove any leftover `impeccable-variants-start` wrappers and `impeccable-carbonize-start` blocks.

