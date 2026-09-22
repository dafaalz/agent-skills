# Visual companion guide

Browser-based visual brainstorming companion for showing mockups, diagrams, and options.

## When to use

Decide per-question, not per-session. The test is whether the user understands this better by seeing it than reading it.

**Use the browser** when the content itself is visual:

- **UI mockups.** Wireframes, layouts, navigation structures, and component designs.
- **Architecture diagrams.** System components, data flow, and relationship maps.
- **Side-by-side visual comparisons.** Comparing two layouts, two color schemes, or two design directions.
- **Design polish.** Questions about look, feel, spacing, and visual hierarchy.
- **Spatial relationships.** State machines, flowcharts, and entity relationships rendered as diagrams.

**Use the terminal** when the content is text or tabular:

- **Requirements and scope.** Defining features, inputs, outputs, and system boundaries.
- **Conceptual choices.** Picking between approaches described in words.
- **Tradeoff lists.** Pros, cons, and comparison tables.
- **Technical decisions.** API design, data modeling, and architectural approach selection.
- **Clarifying questions.** Questions answered with words rather than visual preferences.

A question about a UI topic is not automatically a visual question. Asking what kind of wizard the user wants is conceptual, so use the terminal. Asking which of two wizard layouts looks right is visual, so use the browser.

## How it works

The server watches a directory for HTML files and serves the newest one to the browser. Write HTML content to `screen_dir`. The user sees it in their browser and clicks to select options. Selections are recorded to `state_dir/events` for inspection on the next turn.

**Content fragments vs full documents.** If your HTML file starts with `<!DOCTYPE` or `<html`, the server serves it as-is and injects the helper script. Otherwise, the server automatically wraps your content in the frame template, adding the header, CSS theme, selection indicator, and interactive infrastructure. Write content fragments by default. Only write full documents when you need complete control over the page.

## Starting a session

```bash
# Start server with persistence
scripts/start-server.sh --project-dir /path/to/project

# Returns: {"type":"server-started","port":52341,"url":"http://localhost:52341",
#           "screen_dir":"/path/to/project/.superpowers/brainstorm/12345-1706000000/content",
#           "state_dir":"/path/to/project/.superpowers/brainstorm/12345-1706000000/state"}
```

Save `screen_dir` and `state_dir` from the response. Direct the user to open the URL.

**Finding connection info.** The server writes startup JSON to `$STATE_DIR/server-info`. If you launched the server in the background and did not capture stdout, read that file to get the URL and port. When using `--project-dir`, check `<project>/.superpowers/brainstorm/` for the session directory.

**Persistence note.** Pass the project root as `--project-dir` so mockups persist in `.superpowers/brainstorm/` across server restarts. Without it, files go to `/tmp` and get cleaned up. Remind the user to add `.superpowers/` to `.gitignore` if not already present.

**Launching the server by platform.**

**Claude Code on macOS and Linux:**
```bash
# Default mode backgrounds the server directly
scripts/start-server.sh --project-dir /path/to/project
```

**Claude Code on Windows:**
```bash
# Windows runs in foreground mode. Use background tool execution so the server survives.
scripts/start-server.sh --project-dir /path/to/project
```
Read `$STATE_DIR/server-info` on the next turn to get the URL and port.

**Codex:**
```bash
# Script auto-detects CODEX_CI and runs in foreground mode
scripts/start-server.sh --project-dir /path/to/project
```

**Gemini CLI:**
```bash
# Run with foreground flag in background task execution
scripts/start-server.sh --project-dir /path/to/project --foreground
```

**Other environments.** The server must keep running across conversation turns. If your environment reaps detached processes, use `--foreground` and launch the command with your background execution tool.

If the URL is unreachable, bind a non-loopback host:

```bash
scripts/start-server.sh \
  --project-dir /path/to/project \
  --host 0.0.0.0 \
  --url-host localhost
```

Use `--url-host` to control what hostname is printed in the returned URL JSON.

## The loop

1. **Check server status and write HTML.** Check that `$STATE_DIR/server-info` exists before each write. If missing or if `$STATE_DIR/server-stopped` exists, restart with `start-server.sh`. The server auto-exits after 30 minutes of inactivity. Use semantic filenames like `platform.html` or `layout.html`. Never reuse filenames, because each screen requires a fresh file. Use the write file tool instead of shell heredocs.
2. **Tell user what to expect and end turn.** Remind the user of the URL on every step. Give a brief text summary of what is on screen. Ask them to inspect and respond in chat.
3. **Handle feedback on next turn.** Read `$STATE_DIR/events` if it exists. This file contains user clicks and selections as JSON lines. Merge event data with user text. The user message is the primary feedback, while `state_dir/events` provides structured choices.
4. **Iterate or advance.** When feedback changes the current screen, write a new file like `layout-v2.html`. Move to the next question only after validating the current step.
5. **Unload when returning to terminal.** When the next step does not need the browser, push a waiting screen to clear stale content:

   ```html
   <!-- filename: waiting.html -->
   <div style="display:flex;align-items:center;justify-content:center;min-height:60vh">
     <p class="subtitle">Continuing in terminal...</p>
   </div>
   ```

   This prevents the user from staring at a resolved choice while conversation continues. When the next visual question arrives, push a new content file as usual.
6. Repeat until brainstorming finishes.

## Writing content fragments

Write only the content that goes inside the page body. The server wraps it in the frame template automatically.

**Minimal example.**

```html
<h2>Which layout works better?</h2>
<p class="subtitle">Consider readability and visual hierarchy</p>

<div class="options">
  <div class="option" data-choice="a" onclick="toggleSelect(this)">
    <div class="letter">A</div>
    <div class="content">
      <h3>Single Column</h3>
      <p>Clean, focused reading experience</p>
    </div>
  </div>
  <div class="option" data-choice="b" onclick="toggleSelect(this)">
    <div class="letter">B</div>
    <div class="content">
      <h3>Two Column</h3>
      <p>Sidebar navigation with main content</p>
    </div>
  </div>
</div>
```

## CSS classes available

The frame template provides these CSS classes:

### Options for choices

```html
<div class="options">
  <div class="option" data-choice="a" onclick="toggleSelect(this)">
    <div class="letter">A</div>
    <div class="content">
      <h3>Title</h3>
      <p>Description</p>
    </div>
  </div>
</div>
```

**Multi-select.** Add `data-multiselect` to the container to let users select multiple options. Each click toggles the item. The indicator bar shows the count.

```html
<div class="options" data-multiselect>
  <!-- option markup where users can select multiple -->
</div>
```

### Cards for visual designs

```html
<div class="cards">
  <div class="card" data-choice="design1" onclick="toggleSelect(this)">
    <div class="card-image"><!-- mockup content --></div>
    <div class="card-body">
      <h3>Name</h3>
      <p>Description</p>
    </div>
  </div>
</div>
```

### Mockup container

```html
<div class="mockup">
  <div class="mockup-header">Preview: Dashboard Layout</div>
  <div class="mockup-body"><!-- your mockup HTML --></div>
</div>
```

### Split view for comparisons

```html
<div class="split">
  <div class="mockup"><!-- left --></div>
  <div class="mockup"><!-- right --></div>
</div>
```

### Pros and cons

```html
<div class="pros-cons">
  <div class="pros"><h4>Pros</h4><ul><li>Benefit</li></ul></div>
  <div class="cons"><h4>Cons</h4><ul><li>Drawback</li></ul></div>
</div>
```

### Mock elements for wireframes

```html
<div class="mock-nav">Logo | Home | About | Contact</div>
<div style="display: flex;">
  <div class="mock-sidebar">Navigation</div>
  <div class="mock-content">Main content area</div>
</div>
<button class="mock-button">Action Button</button>
<input class="mock-input" placeholder="Input field">
<div class="placeholder">Placeholder area</div>
```

### Typography and sections

- `h2`. Page title.
- `h3`. Section heading.
- `.subtitle`. Secondary text below title.
- `.section`. Content block with bottom margin.
- `.label`. Small uppercase label text.

## Browser events format

When the user clicks options in the browser, interactions are recorded to `$STATE_DIR/events` with one JSON object per line. The file clears automatically when you push a new screen.

```jsonl
{"type":"click","choice":"a","text":"Option A (Simple Layout)","timestamp":1706000101}
{"type":"click","choice":"c","text":"Option C (Complex Grid)","timestamp":1706000108}
{"type":"click","choice":"b","text":"Option B (Hybrid)","timestamp":1706000115}
```

The event stream shows the user exploration path. The last `choice` event represents the final selection, though earlier clicks can reveal hesitation or preferences worth clarifying.

If `$STATE_DIR/events` does not exist, the user did not interact with the browser. Rely on their terminal text.

## Design tips

- **Scale fidelity to the question.** Wireframes for layout, polish for visual styling.
- **Explain the question on each page.** State clear evaluation criteria.
- **Iterate before advancing.** Write a new version when feedback modifies a screen.
- **Limit choices.** Present 2 to 4 options maximum per screen.
- **Use real content.** Realistic text and images avoid misleading impressions.
- **Keep mockups focused.** Prioritize structure and layout over pixel-perfect detailing.

## File naming

- Use semantic names like `platform.html`, `visual-style.html`, or `layout.html`.
- Never reuse filenames. Each screen requires a new file.
- For iterations, append version suffixes like `layout-v2.html`.
- The server serves the newest file by modification time.

## Cleaning up

```bash
scripts/stop-server.sh $SESSION_DIR
```

If the session used `--project-dir`, mockup files persist in `.superpowers/brainstorm/` for future reference. Only `/tmp` sessions get deleted on stop.

## Reference

- Frame template CSS reference in `scripts/frame-template.html`
- Client helper script in `scripts/helper.js`
