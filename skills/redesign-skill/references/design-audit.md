# Design audit reference

Use this reference to inspect existing projects for generic patterns, visual bugs, and missing interface states.

## Typography

Audit text styling and hierarchy against these rules:

- Default fonts. Replace default system fonts or uniform Inter with fonts that have character, such as Geist, Outfit, Cabinet Grotesk, or Satoshi. For editorial or creative products, pair a serif display header with a sans-serif body.
- Weak headlines. Increase font size for display titles, tighten letter-spacing, and reduce line-height to give headings clear weight.
- Wide paragraphs. Limit body text width to approximately 65 characters per line. Increase line-height to at least 1.5 for comfortable reading.
- Missing intermediate weights. Add Medium (500) and SemiBold (600) weights to create nuanced hierarchy instead of relying solely on Regular (400) and Bold (700).
- Proportional tabular numbers. Use monospace fonts or enable tabular figures with `font-variant-numeric: tabular-nums` in tables, dashboards, and metric displays.
- Uncalibrated letter-spacing. Apply negative tracking (`letter-spacing: -0.02em` to `-0.04em`) to large titles. Apply positive tracking (`letter-spacing: 0.05em`) to uppercase labels and small captions.
- All-caps subheaders. Replace repetitive uppercase subheaders with sentence case or small-caps styling.
- Orphaned final words. Add `text-wrap: balance` to headings and `text-wrap: pretty` to body text to prevent single words on trailing lines.

## Color and surfaces

Audit palette selections and surface styling:

- Pure black backgrounds. Replace `#000000` with tinted off-black tones such as `#0a0a0a`, `#121212`, or dark navy to reduce harsh contrast.
- Oversaturated accent colors. Keep accent saturation below 80 percent so highlighted elements blend naturally with neutral backgrounds.
- Competing accents. Select one primary accent color for actions and links. Remove conflicting secondary accents.
- Mixed gray temperatures. Standardize on one gray palette across the entire application. Do not mix cool slate grays with warm stone grays.
- AI gradient fingerprints. Replace standard purple and blue diagonal gradients with neutral surfaces and a single deliberate accent.
- Generic black shadows. Tint shadow values with the underlying surface hue. For instance, use a dark navy shadow on a navy surface instead of a generic black shadow.
- Sterile flat surfaces. Introduce subtle SVG noise, fine grain overlays, or micro-patterns on large flat containers to create tactile depth.
- Uniform gradients. Replace standard linear gradients with soft radial gradients, mesh gradients, or textured ambient fades.
- Inconsistent light source. Verify that all drop shadows and surface highlights share an identical light direction.
- Section luminance jumps. Avoid inserting dark sections inside light mode pages or light sections inside dark mode pages. Maintain consistent background luminance across the entire page flow.
- Flat background sections. Add ambient background blurs, contextual imagery, or geometric patterns behind hero banners and call-to-action blocks.

## Layout

Audit container constraints, alignment, and composition:

- Predictable symmetry. Break rigid centered alignments with asymmetric column widths, offset margins, or left-aligned headers above structured content.
- Repetitive three-card rows. Replace uniform three-column cards with asymmetric grids, zig-zag layouts, or horizontal scrolling rows.
- Hardcoded viewport height. Replace `height: 100vh` with `min-height: 100dvh` to prevent jumping on mobile browsers with dynamic address bars.
- Complex flexbox math. Use CSS Grid for multi-column structures instead of calculating fractional percentage widths in flexbox.
- Unbounded containers. Wrap content in a max-width container (typically 1200px to 1440px) with centered horizontal margins (`margin-inline: auto`).
- Forced equal card heights. Allow cards to size naturally to their content, or use a masonry grid when card text lengths vary significantly.
- Monolithic border radius. Vary border radii across the component tree by using tighter radii on nested items and softer radii on outer wrapper cards.
- Missing layer depth. Use negative margins and z-index offsets to layer related elements over one another.
- Rigid vertical padding. Optically adjust container spacing by setting bottom padding slightly larger than top padding.
- Repetitive sidebar layouts. Consider top navigation, collapsible panels, or floating command palettes when sidebars consume unnecessary horizontal space.
- Crowded components. Double whitespace between major sections to let content breathe.
- Misaligned card buttons. Align action buttons to the bottom edge across adjacent cards using `margin-top: auto` or CSS Grid alignment.
- Uneven list baselines. Ensure feature checklists in pricing tables start at identical vertical coordinates across columns.
- Baseline misalignment in columns. Align titles, paragraphs, and prices horizontally across sibling cards.
- Unadjusted mathematical centering. Optically adjust icons and button labels by 1px or 2px when geometric centering looks unbalanced.

## Interactivity and states

Audit user interactions and feedback indicators:

- Missing hover states. Add background color transitions, border illumination, or subtle scale changes on hover.
- Missing active feedback. Add `transform: scale(0.98)` or `transform: translateY(1px)` on `:active` to give interactive elements a physical feel.
- Instant state transitions. Add CSS transitions between 200ms and 300ms using easing curves on all interactive properties.
- Missing keyboard focus rings. Provide high-contrast focus rings with `outline` or `box-shadow` for keyboard navigation.
- Missing skeleton screens. Replace generic loading spinners with skeleton cards that match the layout shape.
- Empty dashboard views. Design clear empty states containing helpful onboarding text and a direct creation button.
- Missing form error feedback. Display inline validation messages under form fields. Never use browser alert dialogs.
- Inactive anchor links. Replace `#` href attributes with actual paths or visually disabled states.
- Missing navigation markers. Highlight the active link corresponding to the current URL route.
- Abrupt page jumps. Set `html { scroll-behavior: smooth; }` for in-page anchor links.
- Layout-thrashing animations. Animate only `transform` and `opacity` to maintain 60 frames per second performance.

## Content

Audit copy and placeholder realism:

- Predictable placeholder names. Replace generic names like John Doe with diverse, contextual names.
- Artificially round figures. Replace numbers like 100% or $50.00 with realistic figures like 47.2% or $99.00.
- Fictional company tropes. Replace generic names like Acme Corp with industry-relevant brand names.
- Promotional AI vocabulary. Remove words such as elevate, unleash, next-gen, game-changer, delve, tapestry, and vibrant.
- Exclamatory success messages. Write confident, neutral confirmation copy without exclamation points.
- Generic error greetings. Replace phrases like "Oops!" with clear diagnostic text like "Connection failed. Please retry."
- Passive voice. Use active voice, such as "We could not save your document" instead of "Errors occurred during save."
- Uniform timestamps. Vary article and comment dates realistically.
- Reused avatar assets. Assign distinct avatar imagery to distinct user profiles.
- Lorem ipsum text. Write authentic draft copy that matches the actual product domain.
- Title case headers. Format all page headers and component titles in sentence case.

## Component patterns

Audit common component implementations:

- Heavy borders on white cards. Remove borders or use light surface tints instead of combining heavy borders, drop shadows, and pure white fills.
- Rigid button duos. Supplement primary and ghost button combinations with text links or subtle tertiary actions.
- Pill badges. Replace rounded pill badges with square tags, colored indicator dots, or plain text labels.
- Accordion FAQ sections. Present FAQs in two-column lists or searchable blocks instead of hiding every answer behind an accordion click.
- Testimonial carousels with dots. Use masonry quote walls or single prominent quotes instead of small three-card dot carousels.
- Three-column pricing tables. Highlight the recommended plan through color contrast and visual priority rather than physical height alone.
- Excessive modal overlays. Replace modal popups for simple edits with inline editing, slide-over sheets, or expandable drawers.
- Circular avatars. Use squircle shapes or rounded rectangles for avatar containers.
- Sun and moon icons. Use segmented control buttons or automatic system preference detection for theme toggling.
- Cluttered link footers. Consolidate link lists into clear navigation paths and legal requirements.

## Iconography

Audit visual icons:

- Default icon packs. Consider Phosphor, Heroicons, or bespoke SVG symbols instead of standard default sets.
- Predictable visual metaphors. Replace rocket icons for launch with bolts, terminal prompts, or spark symbols.
- Mixed stroke widths. Standardize all icons to a consistent stroke weight (such as 1.5px or 2px).
- Missing favicon. Provide branded SVG and PNG favicon files in the HTML head.
- Stock photo cliches. Replace staged stock imagery with authentic screenshots, product diagrams, or candid photos.

## Code quality

Audit underlying markup and stylesheet practices:

- Semantic markup. Use `header`, `nav`, `main`, `article`, `section`, `aside`, and `footer` instead of nesting plain `div` tags.
- Inline styling. Move inline style attributes into dedicated stylesheet classes or design tokens.
- Hardcoded pixel widths. Use relative units such as percentages, rem units, and max-width clamps.
- Screen reader alt text. Provide meaningful alt text on all informative imagery. Use empty alt attributes only on purely decorative images.
- Uncontrolled z-index values. Define a structured z-index scale (10, 20, 30, 40, 50) within CSS custom properties.
- Inactive debug artifacts. Remove console logs, debug wrappers, and commented code blocks before finishing.
- Social metadata. Provide Open Graph title, description, and image meta tags in the document head.

## Common omissions

Audit essential usability patterns frequently omitted in generated interfaces:

- Legal documentation. Include links to privacy policy and terms of service in the site footer.
- Return navigation. Ensure every secondary page includes a visible back link or breadcrumb trail.
- Custom 404 page. Build a branded not-found view with links back to common starting points.
- Client form validation. Add real-time field format checking for email addresses and required inputs.
- Skip to content link. Add a keyboard-accessible skip link at the top of the body for accessibility.
- Consent banners. Include a compliant cookie banner if the target audience requires one.
