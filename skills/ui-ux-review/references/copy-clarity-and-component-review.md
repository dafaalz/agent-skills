> **Additional context needed**: audience knowledge and emotional state.

Rewrite unclear interface text so users understand what happened, what matters, and what to do next. Preserve factual meaning, product terminology, and brand voice.

## Audit the language

Read the entire interaction path, not isolated strings. Identify:

- ambiguous nouns, verbs, and actions;
- internal jargon or assumed knowledge;
- vague labels, outcomes, and system states;
- missing consequences, recovery, or timing;
- inconsistent terminology and capitalization;
- redundant headings, intros, helper text, and confirmations;
- text that breaks at realistic widths or in translation;
- tone that ignores stress, risk, success, or urgency.

Infer audience and task from product context and surrounding UI. Ask before changing factual claims, legal meaning, or a term that may be domain-specific.

## Set the message hierarchy

For each state, decide:

1. the one fact the user needs now;
2. the action available next;
3. supporting context that changes the decision;
4. the appropriate tone for this moment.

Say each idea once. If the heading already explains the state, the introduction should add new information or disappear.

## Rewrite by function

### Actions and navigation

Use a specific verb and object when the outcome is not already obvious. Labels should describe what will happen, not the gesture used to trigger it. Keep the same noun and verb for the same concept throughout the product.

For destructive actions, name the object and consequence. Prefer undo over confirmation when recovery is safe. When confirmation is necessary, name the action on both the message and button instead of using `Yes`, `No`, `OK`, or `Submit`.

### Forms

Use persistent labels; placeholders are examples, not labels. Put format and eligibility requirements before submission. Explain why information is requested only when it is not obvious. Required and optional treatment should be consistent.

Validation says what needs attention and how to correct it without blaming the user. Keep related instructions near the field and announce errors accessibly.

### Errors and permissions

An actionable error answers:

1. what failed;
2. why, when known and useful;
3. how to recover or what alternative remains.

Do not expose internal codes as the primary message. Do not promise a cause or resolution the system cannot know. Treat privacy, payment, deletion, access loss, and blocked work seriously; warmth is welcome, jokes are not.

### Loading, empty, and success states

Loading text names the real operation and sets an honest expectation when the wait is meaningful. Show determinate progress when available; never invent progress.

An empty state distinguishes first use, no results, filters, permissions, and failure. Explain the state and provide the next useful action.

Success confirms the completed outcome and mentions the next consequence only when it changes what the user should do. Routine success should be brief.

### Help and instructional text

Helper text answers an implicit question instead of restating the control. Use progressive disclosure for uncommon detail. Link text must make sense out of context; icon-only controls need accessible names.

## Voice, accessibility, and localization

Voice stays consistent; tone adapts to the moment. Use plain language without flattening terminology the audience genuinely knows.

- Write complete translatable messages rather than concatenated fragments.
- Keep variables and numbers structured so translators can reorder them.
- Allow expansion instead of abbreviating prematurely.
- Make alt text convey the image's information; use empty alt for decoration.
- Keep screen-reader names aligned with visible labels and outcomes.
- Do not rely on punctuation, color, or iconography to carry the message alone.

Maintain a short terminology glossary when inconsistency spans the product. Do not vary words for literary effect in an interface.

## Verify

Read the flow in context and test:

- comprehension without hidden product knowledge;
- actionability at errors, empty states, and decision points;
- factual accuracy and consistent terminology;
- scanability at target widths and 200% zoom;
- long names, localization expansion, pluralization, and dynamic values;
- accessible names and announced state changes;
- tone appropriate to consequence and emotional context.

The final copy is as short as it can be without removing meaning or recovery.

When the language reads cleanly, hand off to `$impeccable polish` for the final pass.
# Plan and asset review

Use this checkpoint on comp-led builds once every raster region has its plate and the plates gate has scored them, before any page code exists. The approved comp is the reference. The user reviews two things: the plates that will ship, and the production plan for everything else, meaning which regions code draws. A painted region planned as code is the most expensive mistake a comp-led build makes, and this is where the user catches it. Text, controls and chrome are judged later, in the assembled first viewport.

## Plan, capture, serve

Run `.agents/skills/impeccable/scripts/impeccable component-review plan`. It writes `.impeccable/review/components.json` from the measured spec, the comp and the plate files, and refuses, naming each one, while any raster region lacks its plate. Never write or edit that file for this stage: the packet is derived from the spec, so every change belongs in the regions file.

If the harness exposes `component_review`, call it with `manifest_path` set to `.impeccable/review/components.json`. The host captures, presents the review and returns the user's decisions. A suspended request is waiting for the user; it is not a failed build or an approval.

Otherwise run `.agents/skills/impeccable/scripts/impeccable component-review capture --manifest .impeccable/review/components.json`, then start `.agents/skills/impeccable/scripts/impeccable component-review serve --session <returned session>` in the background. Open the URL it prints in the available browser and wait for the user; `serve` exits 0 once they submit. Read the decisions with `.agents/skills/impeccable/scripts/impeccable component-review status --session <id>`; `.agents/skills/impeccable/scripts/impeccable component-review verify --manifest .impeccable/review/components.json` confirms approval and refuses pending, needs-work and stale input. Never submit the page or write a receipt on the user's behalf.

`serve` exits 2 when this session has no browser (the same signal as the decision page) and 4 when it closes after 30 idle minutes without a decision. Either way no one is reviewing: stop waiting, do not approve anything yourself, and do not build past this checkpoint. End the run and report the plan and asset review as pending with its session ID, so the user can resume it. A waiting review is pending work, not a completed build.

## Act on the receipt

Apply the user's decisions as given, never your own favorable verdict in their place.

- **approve**: once every item is approved and the inventory is confirmed, advance to the hero.
- **revise** (a plate): regenerate that plate at the same path with the user's feedback.
- **revise with split** (an asset): replace that region in the regions file with its layers: a frame plate with a transparent opening (kind `plate`, same box), the content as its own `image` region at the opening's box, and each moving part (a shutter, a door) as its own plate. Name each layer after the original region, as `<id>-frame`, `<id>-view` or `<id>-shutter-left`, so the next round shows it as part of the user's request. Rerun `.agents/skills/impeccable/scripts/impeccable comp-spec --comp <comp.png> --regions <regions.json>` and produce the plates.
- **revise** (a plan item): change the regions file as the feedback says (resize or extend a raster region, split material into its own plate region, or adjust the code region), rerun `.agents/skills/impeccable/scripts/impeccable comp-spec --comp <comp.png> --regions <regions.json>`, and produce any new plates.
- **reclassify** (a code region): in the regions file, change that region's `kind` to the one the user chose and rewrite its `note` to describe the material. Rerun `.agents/skills/impeccable/scripts/impeccable comp-spec --comp <comp.png> --regions <regions.json>`, then produce the new plates, with the asset producer when subagents are available.
- **missing**: add the region to the regions file, rerun `.agents/skills/impeccable/scripts/impeccable comp-spec --comp <comp.png> --regions <regions.json>`, and produce its plate if it is raster.

Then run `plan`, `capture` and `serve` again. Unchanged decisions carry over, so the user sees only what changed. Any spec change, or a plate replaced after acceptance, needs a new round; the build-phase gate stays closed until the review of the current spec is accepted.

## Assemble and review

Build the first viewport from the approved plates and plan, and run the hero gate. Human review does not waive its integrity checks. After three failed hero attempts, or three failed responsive attempts before any first viewport is accepted, stop iterating and present the first-viewport review with the current build; the user's eye settles what the readings could not.

Present a second manifest at `.impeccable/review/hero.json`. You write this one, and its shape is fixed:

```json
{
  "schemaVersion": 2,
  "stage": "hero",
  "id": "hero",
  "title": "First viewport",
  "comp": {"path": ".impeccable/mocks/comp.png", "width": 1536, "height": 1024},
  "components": [{
    "id": "first-viewport",
    "name": "First viewport",
    "medium": "HTML / CSS",
    "note": "Assembled first viewport",
    "box": {"x": 0, "y": 0, "w": 1, "h": 1},
    "preview": {"kind": "page", "path": "index.html"},
    "dependencies": ["styles.css", "assets/plates/sky.png", "fonts/display.woff2"]
  }]
}
```

- `schemaVersion` is 2. Version 3 is the plan review packet and requires stage `components`. `codeRegions` and `specSha256` exist only in version 3 and are refused here. `reviewGroup` is refused too: version 3 rejects it, and any other version accepts it only on a page preview in a `components`-stage manifest, never in a hero manifest.
- `comp.path` is the `comp` value in `.impeccable/build/spec.json`, and `width` and `height` are that PNG's pixel size.
- Exactly one component, with `box` exactly `{"x": 0, "y": 0, "w": 1, "h": 1}` and `name`, `medium` and `note` as strings.
- `preview.path` is the page entry the build gates (`artifact` in `.impeccable/build/state.json`).
- `dependencies` lists every other file the page loads (stylesheets, scripts, plates, images, fonts) as bare strings. Every path, here and above, is project-relative and plain: no leading `./` or `/`, no `..`, no URL, no `?`, `#`, `%`, `:` or backslash. A request to a file missing from this list, or to another host, fails the capture.

The reference stays the approved comp. Call the same host review tool, or run `capture`, `serve` and `verify` with this manifest. Needs-work feedback starts another assembly round.

Acceptance closes human review for this build: never request plan, asset or assembly approval again. While the page renders what the user accepted, the hero score, the palette check and every numeric reading are advisories; material vetoes still hold (a missing or unreferenced plate, an SVG illustration, an organic clip, a clipped plate, invented ink, failed rendered presence). A text, control or chrome region the accepted screenshot also lacks is settled by the acceptance; a plate it lacks is a question for the user that the gate's reason spells out: do not move off what they accepted on your own, but carry out their answer, including placing the plate. When the capture no longer matches the accepted screenshot, restore what the user accepted; until then the readings apply. Complete the rest of the page, responsive behavior, finish checks and documentation with the accepted first viewport as the visual direction. This is first-viewport calibration, not a claim that the user reviewed the rest of the page. Shared stylesheet edits do not reopen approval. Preserve the accepted direction; a later explicit user change is a new task.

Assembled-page capture executes inline and declared local scripts from the pinned inputs. Network APIs, frames and workers are unavailable; the initial viewport must settle before capture. Keep the real page and declare its scripts rather than removing behavior to pass review.
