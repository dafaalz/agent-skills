# Operate mode depth (and Read notes)

When design SERVES the product: app UIs, admin dashboards, settings panels, data tables, tools, authenticated surfaces, anything where the user is in a task. The essentials live in SKILL.md's modes and the craft floor rules; this file is extended depth, written for Operate surfaces. Read surfaces (docs, guides, long-form) take SKILL.md's Read mode plus this file's typography and consistency rules; their prose measure and navigation matter more than component density.

## The product slop test

Familiarity is often a feature here. The test is whether a category-fluent user can trust the interface immediately or must pause at every subtly-off component.

Product UI's failure mode isn't flatness, it's strangeness without purpose: over-decorated buttons, mismatched form controls, gratuitous motion, display fonts where labels should be, invented affordances for standard tasks. The bar is earned familiarity. The tool should disappear into the task.

## Typography

- **One family is often right.** Product UIs don't need display/body pairing. A well-tuned sans carries headings, buttons, labels, body, data.
- **Fixed rem scale, not fluid.** Clamp-sized headings don't serve product UI. Users view at consistent DPI, and a fluid h1 that shrinks in a sidebar looks worse, not better.
- **Tighter scale ratio.** 1.125–1.2 between steps is typical. More type elements here than on brand surfaces; exaggerated contrast creates noise.
- **Line length still applies for prose** (65–75ch). Data and compact UI can run denser; tables at 120ch+ are fine.

## Color

Product defaults to Restrained. A single surface can earn Committed (a dashboard where one category color carries a report, an onboarding flow with a drenched welcome screen), but Restrained is the floor.

- State-rich semantic vocabulary: hover, focus, active, disabled, selected, loading, error, warning, success, info. Standardize these.
- Accent color used for primary actions, current selection, and state indicators only, not decoration.
- A second neutral layer for sidebars, toolbars, and panels (slightly cooler or warmer than the content surface).

## Layout

- Responsive behavior is structural (collapse sidebar, responsive table, breakpoint-driven columns), not fluid typography.

## Components

Every interactive component has: default, hover, focus, active, disabled, loading, error. Don't ship with half of these.

- Skeleton states for loading, not spinners in the middle of content.
- Empty states that teach the interface, not "nothing here."
- Consistent affordances across the surface. Same button shape. Same form-control vocabulary. Same icon style.
- Overlays escape their container. An absolutely positioned dropdown inside an `overflow: hidden` or `overflow: auto` ancestor gets clipped; reach for `<dialog>`, the popover API, `position: fixed`, or a portal.

## Motion

- 150–250 ms on most transitions. Users are in flow; don't make them wait for choreography.
- Motion conveys state, not decoration. State change, feedback, loading, reveal: nothing else.
- No orchestrated page-load sequences. Product loads into a task; users don't want to watch it load.

## Product constraints

- Decorative motion that doesn't convey state.
- Inconsistent component vocabulary across screens. If the "save" button looks different in two places, one is wrong.
- Display fonts in UI labels, buttons, data.
- Reinventing standard affordances for flavor (custom scrollbars, weird form controls, non-standard modals).
- Heavy color or full-saturation accents on inactive states.
- Modal as first thought. Modals are usually laziness. Exhaust inline / progressive alternatives first.

## Product permissions

Product can afford things brand surfaces can't.

- System fonts and familiar sans defaults.
- Standard navigation patterns: top bar + side nav, breadcrumbs, tabs, command palettes.
- Density. Tables with many rows, panels with many labels, dense information when users need it.
- Consistency over surprise. The same visual vocabulary screen to screen is a virtue; delight is saved for moments, not pages.
# Operate

`impeccable concept-seed --mode operate` prints the two sections below as its MODE RULES block. On an Operate surface the visitor came to get a job done, so the page is first a working product of its category and the world serves it.

## Directions

Someone who uses tools like this one should know where everything is before they notice the world. The world lends four things and only these: type, palette, density, and one signature move. It never supplies the layout, the navigation model, or the controls. Colour is part of the world's contribution, and it does real jobs: a committed palette for the shell (a coloured rail or header, a tinted ground), state colours, data series, selection, and the signature move. A grey screen with one accent colour is the category default without the category's polish, not restraint.

Read every candidate, the assigned direction, and every challenger through that limit before you fuse or judge it. A world taken from a tool or instrument the audience operates (a terminal, a scope, a control panel, a cockpit) or from a fictional interface comes back as a costume of that tool on a working screen: take from it only what transfers as type, palette, density, and a signature move, or replace it from your list. When a catalog world's source is itself an interface language, the same limit holds: it lends type, density, palette, and one signature move, while navigation and controls stay the standard ones for the platform, web components on the web and native controls in an app.

Write each direction's first viewport as the product's shell first: the navigation, the work areas and what each is for, the data the visitor reads first and its states, and then where the signature move lives. Expression may never obscure the task, state, or familiar affordance. Name the signature move concretely, so the comp and the build can find it: service health drawn as a transit map, a schedule set in a timetable's column rhythm. A direction whose world shows up only as a colour scheme has not found its move yet. When you weigh fused challengers, product clarity includes reading as a working product of this category.

## Comps

The comp is the product screen, in the direction's committed palette: its shell and navigation with a distinct area for each job and, where there is data, filters over what they scope and charts and tables with clear states. The world enters only through type, palette, density, and the one signature move; it never supplies the page's organisation, so a working screen never reads as a newspaper, a poster, or any other artifact of the world. Every control is a standard one the visitor already knows how to use, a web component on the web and the platform's native control in an app: buttons, tabs, inputs, selects, filters, tables with sortable headers, navigation that reads as navigation. Never a costume of the world's own interface: a terminal's function-key bar or command prompt, an instrument's bezel, ruled ledger paper standing in for a table. A comp an engineer could not build from the platform's standard components is a picture of the tool, not the tool. The finish bar is the best product in the category: an aligned grid, consistent spacing, a real type scale, and clear hierarchy. The signature move adds to a screen that is already that clean; it never stands in for it.

Prompt with the screen's real content: the product name, realistic data with plausible values and units, real labels, and one state worth seeing (an alert, a degraded service, an empty filter result), never placeholder tiles. State colours (red for critical, amber for degraded) sit on top of the world's palette only where they carry meaning, and a headline number that moves over time shows its recent history, with the onset marked when something changed.

Comps two and three vary the product's organisation, never its world coverage: the navigation model (side rail, top bar, command-first), how the work areas divide the screen, which data leads, the density, and where the signature move sits. Each must be recognisably different from the first at thumbnail size; a variant only its prompt can tell apart adds no choice. A variant that adds world material, texture, or ornament goes further in the wrong direction; on a working screen, more world is a costume.

Self-check every render: with the name covered, does it read as a product of its category, could the visitor do the task from it, and is it at least as clean as the category standard and more distinctive than it? If it reads as an artifact of the world first, regenerate with the shell and the work areas named region by region and the world held to its four contributions.
# Persuade and Experience

`impeccable concept-seed --mode persuade` (or `experience`) prints the two sections below as its MODE RULES block. On these surfaces the design is what the visitor judges, so the world may own and structure the page.

## Directions

When a catalog world's source is itself an interface language, the surface may carry its native grammar across navigation, content, controls, and states, within the platform conventions a native app keeps.

For **Persuade**, the opening must make the offer intelligible and desirable, expose a clear action, and demonstrate something only this product can prove. The action is the one the category's visitors came to take, in its working form: an airline's route-and-dates search, a clinic's open appointment slots, a store's add to cart. A decorative link pointing at it elsewhere does not count. Conversion lives inside the form's own vocabulary: a hook that lands in one line, a visible primary action, a legible reading order. A committed form that hides the offer or the action has not finished translating. For **Experience**, the work itself leads from the first viewport.

## Comps

The world may be the carrier of the page, never a picture of it: a facade, a shutter or a book can be what the page is built on, while a viewport painted whole as a facade, a book cover or a travel poster, with no working parts in it, is a picture of the world, not its website. Material coverage is wanted: the world's material is the ground and the major surfaces, its type sets the headlines, and a world reduced to an accent on a neutral template is the category default with a sticker on it. Coverage is not performance: how many regions act out the concept is limited by the depth rule in visualize.md, and the rest stay in the world's material without performing it. Both ends erase the direction: the painted poster, and the generic product page (a headline over subcopy and a button, a row of equal cards below). The dealt composition sets the skeleton, and the compositions you write for comps two and three answer to the same test: a split hero (copy on one side, the product on the other, a badge row under it) or a centred headline over a row of cards is the template whatever world paints it.

The world carries the page's parts and never absorbs them, so wherever it puts one, the page still works as a page: navigation set into a facade reads as links, copy on a shutter as set text a visitor reads, an action on a door plaque as plainly clickable, text reads against whatever sits behind it, the sections keep a steady vertical rhythm, the primary action is unmistakable, and the section below starts as a section rather than more painting. Fix a poster by making its parts work where the world put them, never by moving them into a standard layout on the world's colour: a cover that becomes copy beside a device on marigold has lost the cover.

When the world is an object, the page is that one object seen once, at one scale and from one point of view, and the object keeps its real form: a book opens to two pages on one gutter, never a third panel, and a spine that carries the navigation belongs to the book on the page, never a second book beside it. More content goes on the object's own surfaces or on the next spread below, never on extra copies or impossible folds.

Comps two and three each go further than the first, never cleaner: a bolder use of the same world, where the world's material carries more of the page's structure (still one dominant move, per the depth rule), a larger or stranger focal move, or a composition the category would not attempt.
# Read

`impeccable concept-seed --mode read` prints the two sections below as its MODE RULES block. On a Read surface the visitor came to understand something, so the page is first a document of its kind, framed by the world.

## Directions

The reader's question leads, and comprehension and wayfinding stay intact at every step. Documentation reads as documentation, a guide as a guide, an article as an article, a changelog as a changelog. The world owns the frame and serves the column. The frame is the masthead, the navigation rail, the ground, the title and section openers, and the way code, tables, and callouts are set: there the world's palette, type, and signature move commit fully, so the page could belong to no other product. The reading column inside it stays calm: a reading face, real contrast, a real measure, nothing performing behind the text. The world never supplies the reading order or replaces the navigation with something a reader has to learn. Documentation still reads as documentation, a guide as a guide, an article as an article.

Candidates from the world's own publishing traditions transfer best: reference books, type specimens, timetables, field guides, technical manuals, scholarly apparatus, a newspaper's wayfinding. A tool, instrument, or fictional interface from the audience's world comes back as a costume on a page meant for reading: take from it only what transfers as type, palette, density, and a signature move, or replace it from your list. When a catalog world's source is itself an interface language, the same limit holds: it lends type, density, palette, and one signature move, while navigation and controls stay the standard ones for the platform.

Write each direction's first viewport as the document's shell first: the navigation and where the reader stands in it, the title and the opening that answers or frames the reader's question, the reading column, and the way forward (contents, section headings, next and previous). Then name where the world owns the frame and where the signature move lives: a masthead, a coloured rail, a running head, a margin system, a numbering scheme, a way of setting code or tables. When you weigh fused challengers, product clarity includes how fast a reader finds and understands the answer.

## Comps

The comp is the document as the reader meets it: a frame the world owns, in the direction's committed palette and type, around a calm reading column at a real measure (on the web about 60 to 75 characters with body text near 16px; in a native app, the platform's body text style and its readable width), with headings in a clear hierarchy and the wayfinding that carries the reader through. Body text is set in a reading face with real contrast against its ground; a monospace face is for code, parameters, and small labels, never the running text or the headings by default. Code, tables, notes, and figures sit in the standard forms readers already know, set in the world's type and palette. The signature move is one system used where it earns its place, never a frame repeated around every element. The world never supplies the page's reading order, so a document never reads as a poster, a magazine cover, or a book photographed open.

Prompt with the real material: the actual title, a real opening paragraph, real section names, and one example of the hardest content the surface holds (a code sample, a reference table, a diagram), never filler text.

Comps two and three vary the reading structure and how the frame carries the world, never the column: the navigation model (sidebar tree, top tabs, inline contents), the column and margin system, how densely the reference material sits, and where the signature move appears. Each must be recognisably different from the first at thumbnail size; a variant only its prompt can tell apart adds no choice. A variant that pushes world material into the reading column makes reading harder and goes the wrong way.

Self-check every render: can a reader tell where they are and where to go next, and read the body comfortably? Then cover the name: could this be any other product's documentation? If so, the frame has not taken the world; push the masthead, rail, ground, and openers further into it. If the render reads as an artifact of the world before it reads as a document, the world has reached the column; pull it back to the frame.
# Region map

A region map names what is actually visible in the approved comp before asset production. It is not a page build or an asset approval.

1. Run `.agents/skills/impeccable/scripts/impeccable comp-spec --comp <comp.png> --grid` and open the original and gridded images.
2. Run `.agents/skills/impeccable/scripts/impeccable comp-spec --schema` for the JSON fields. Write `regions.json` with a `regions` array. Each region needs a stable `id`, `kind`, `note`, and exactly one of `pixelBox`, normalized `box`, or `grid`. Use the original comp’s dimensions.
3. Run `.agents/skills/impeccable/scripts/impeccable comp-spec --comp <comp.png> --regions regions.json --inspect-map`. The output points to a report, overlay, exact crops and `COMPARE` sheets of masked references. The default prints findings; `--json` prints the entire report, with sheet paths in `comparisonSheets`.
4. Open the comparison sheets first to inspect affected crops together, then open individual crops where more detail is needed. Compare their bounds with the original. Inspect excluded foreground pixels as well as geometry errors. Every overlapping non-container code box is masked in full, including empty space inside it. Bound separate text elements separately so artwork in the gaps stays visible; a container describes their layout extent and never replaces its children. Correct the map and inspect again; use a new output directory each time. Zero errors does not certify crop accuracy. Coverage warnings are hints, not proof of completeness.

If the request ends at mapping, stop with the map, inspection report and unresolved findings. To continue a build, measure the inspected map with `comp-spec --comp <comp.png> --regions regions.json` and follow the new-surface workflow.

`--auto` produces horizontal band scaffolding, not element identification. It is optional and does not replace authoring a map.

## Containment

`parentId` identifies an enclosing `container: true` region. Parent and children keep separate IDs and crops. Containment never transfers approval.

## What varies independently

Split regions by what varies independently: content the site swaps (room photos, products, people), moving parts (anything a hover or the signature interaction moves), and structure (frames, surrounds, ornament). A window with open shutters onto a room is three kinds of region: the surround as a plate with a transparent opening, the room as an image region beneath it, and each shutter as its own plate. Overlapping regions are composited in the page. `comp-spec` flags a raster region whose note names a frame and the view it opens onto (`baked-composite`), and the plan and asset review shows it to the user first.

## Painted material

When measuring, `comp-spec` flags a `text`, `control` or `chrome` region, containers included, whose crop looks painted (`painted-pixels`: many colours, soft gradients) and lists it in its summary. The plan and asset review shows flagged regions, and those marked `codeDrawn` (painted material you chose to draw in code), to the user first. Do not leave the catch to them: if a region is painted material (a figure, a photograph, a metal or paper surface), classify it `plate`, `image` or `texture` now.

Comp crops are reference evidence only, never production assets. The map inspector marks its PNGs as comp-derived.
