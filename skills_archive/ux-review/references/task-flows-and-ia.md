# Information architecture and task flows

Audit navigation hierarchies, user task completion flows, wayfinding systems, and progressive disclosure mechanics.

## Authoritative sources

| Source | Author or organization | Domain | Official URL |
| --- | --- | --- | --- |
| Information Architecture for the Web and Beyond, 4th Ed (2015) | Louis Rosenfeld, Peter Morville, Jorge Arango | Information systems and structures | https://www.oreilly.com/library/view/information-architecture-4th/9781491913529/ |
| User Experience Design: The UX Honeycomb (2004) | Peter Morville | Facets of user experience | https://semanticstudios.com/user_experience_design/ |
| The Elements of User Experience, 2nd Ed (2010) | Jesse James Garrett | Five planes of product design | http://www.jjg.net/ia/elements.pdf |
| Don't Make Me Think, Revisited, 3rd Ed (2014) | Steve Krug | Usability and scannability | https://sensible.com/dont-make-me-think/ |
| Progressive Disclosure (2006) | Jakob Nielsen, Nielsen Norman Group | Cognitive pacing mechanisms | https://www.nngroup.com/articles/progressive-disclosure/ |
| Quantifying the User Experience, 2nd Ed (2016) | Jeff Sauro and James R. Lewis | Empirical usability statistics | https://measuringu.com/quantifying-the-user-experience/ |
| SUS: A Quick and Dirty Usability Scale (1996) | John Brooke | Usability metric scale | https://measuringu.com/sus/ |
| Measuring Usability with the Single Ease Question (2012) | Jeff Sauro, MeasuringU | Post-task perceived difficulty | https://measuringu.com/single-ease-question/ |
| Mega Menus Work Well in Website Navigation (2006) | Jakob Nielsen, Nielsen Norman Group | Two-dimensional menu hierarchies | https://www.nngroup.com/articles/mega-menus-work-well/ |
| Breadcrumbs: 11 Design Guidelines (2019) | Jakob Nielsen and Kate Moran, NN/g | Secondary orientation paths | https://www.nngroup.com/articles/breadcrumbs/ |

## 1. Information architecture systems and models

### Rosenfeld and Morville four IA systems
- **Organization systems.** Group content logically using hierarchical, chronological, topical, or task-based schemes.
- **Labeling systems.** Represent sections and actions using unambiguous, familiar terms. Eliminate internal company jargon.
- **Navigation systems.** Provide global top-level access, local sub-section structures, contextual cross-links, and supplemental sitemaps.
- **Search systems.** Implement intelligent query matching, autocomplete, faceted filtering, and instructive zero-results handling.

### Peter Morville UX Honeycomb
User experience requires seven interrelated qualities including Useful, Usable, Desirable, Findable, Accessible, Credible, and Valuable. Findability is foundational. If users cannot locate a capability, its functional quality is zero.

### Jesse James Garrett five planes
Product architecture advances from abstract strategy to concrete visual presentation:
1. **Strategy plane.** Balances user needs and business objectives.
2. **Scope plane.** Translates strategy into functional specifications and content requirements.
3. **Structure plane.** Defines interaction design (system responses to user actions) and information architecture (node relationships and taxonomies).
4. **Skeleton plane.** Establishes interface design (controls and inputs), navigation design (pathways), and information design (visual data rendering).
5. **Surface plane.** Delivers sensory styling (colors, typography, spatial rhythm). Flaws in the structure plane cannot be repaired by styling in the surface plane.

### Steve Krug scannability principles
- **Satisficing over optimizing.** Users do not read pages completely. They scan rapidly and select the first reasonable choice.
- **Visual hierarchy.** Critical elements must carry the largest visual prominence. Spatial proximity must reflect functional groupings.
- **Mindless choices.** Eliminate ambiguous labels. Users must understand what will happen before activating a link or button.
- **Omit needless words.** Strip uninformative introductory filler to reduce cognitive noise and clarify actionable affordances.

### Progressive disclosure mechanics
- **The 80/20 rule.** Render 80 percent of typical user requirements immediately on the primary view.
- **Secondary containers.** Place the remaining 20 percent of complex, specialized options inside accordions, tabs, or slide-over drawers.
- **Staged disclosure.** Divide long, multi-step procedures into sequential steps (wizards) to prevent decision paralysis.
- **Explicit signifiers.** Ensure expandable triggers feature unambiguous icons and descriptive labels.

## 2. Quantitative usability and navigation metrics

### Task Completion Rate (TCR)
Measures the percentage of users who successfully complete a defined objective:

`TCR = (Completed Sessions / Total Attempted Sessions) * 100%`

Benchmarks:
- Cross-industry average benchmark. 78 percent according to Sauro and Lewis.
- Critical transactional workflows (checkout, onboarding, password recovery). Minimum 95 percent target.

### Single Ease Question (SEQ)
A single 7-point Likert item administered immediately following task completion:
- Question. "Overall, how easy or difficult was this task to complete?" (1 = Very Difficult, 7 = Very Easy).
- Benchmark. The global benchmark mean is 5.5. Scores below 5.0 indicate severe interaction friction.

### System Usability Scale (SUS)
A 10-item standardized questionnaire yielding a score from 0 to 100:
- Calculation. Subtract 1 from odd-numbered item scores. Subtract even-numbered item scores from 5. Sum the values and multiply by 2.5.
- Benchmark. The global median score is 68. Scores above 80 represent superior usability (Grade A). Scores below 68 indicate substantial architectural flaws.

### Lostness Metric (Smith, 1996)
Quantifies disorientation during navigation tasks:

`L = sqrt(((N / S) - 1)^2 + ((R / N) - 1)^2)`

Variables:
- `N`: Number of unique pages visited during the task.
- `S`: Total number of page visits (including revisits).
- `R`: Minimum optimal number of pages required to complete the task.

Score interpretations:
- `L < 0.4`: Optimal navigation. The user navigates directly to the target.
- `0.4 <= L <= 0.5`: Moderate hesitation. The user searches for pathways.
- `L > 0.5`: Severe disorientation. The user loops and backtracks repeatedly.

### Drop-off rate and funnel leakage
Measures user attrition between successive stages:

`Drop-off Step N = ((Users Entering Step N - Users Entering Step N+1) / Users Entering Step N) * 100%`

Sharp drop-off spikes reveal friction epicenters, typically triggered by unexpected permissions, confusing forms, or surprise costs.

### Behavioral friction telemetry
- **Rage clicks.** Rapid bursts of 3 to 5 clicks within one second on a single component, indicating broken controls or absent feedback.
- **Dead clicks.** Clicks on static elements mistakenly perceived as interactive controls because of deceptive visual signifiers.
- **Field abandonment duration.** Protracted idle intervals prior to abandoning a view, exposing cognitive roadblocks on specific inputs.

## 3. Information architecture patterns and anti-patterns

### Verified patterns
- **Strict hierarchical tree with contextual cross-links.** Descends logically from general categories to specific items. Cross-links allow lateral navigation between related items without forcing users back to the root.
- **Faceted navigation with mutual exclusivity.** Multi-attribute filtering across orthogonal dimensions (price, brand, date). Facet counts update dynamically to prevent zero-result states.
- **Mega-menus for broad hierarchies.** Two-dimensional panels displaying up to three levels of categorized links. Incorporate safe cursor triangles to prevent premature menu closure during diagonal pointer travel.
- **Location-based breadcrumbs.** Displays hierarchical depth (`Root > Category > Subcategory > Active Page`). The active page renders as static text without a hyperlink.
- **Hub-and-spoke for sandboxed tasks.** Directs users from a central hub to self-contained sub-tasks, returning them to the hub upon completion to prevent runaway navigation depth.

### Detrimental anti-patterns
- **Mystery meat navigation.** Hiding navigation targets behind abstract icons lacking text labels, forcing speculative hovering or clicking.
- **Pogo-sticking.** Forcing users to bounce back and forth between an index list and detail screens because summary list cards lack key preview data.
- **Deep navigational silos.** Nesting essential daily tasks more than 3 to 4 click levels deep, drastically eroding findability.
- **Polyhierarchy ambiguity.** Placing a single piece of content under conflicting parent categories without clear taxonomic logic, breaking breadcrumb orientation.
- **The cognitive hoarder.** Presenting all features, links, and banners on a single viewport without visual hierarchy or progressive disclosure.
- **Infinite scroll trap on structured repositories.** Eliminating footers and spatial markers on reference pages, preventing users from reaching legal disclosures or bookmarking positions.

## 4. Task flow audit checklist

Audit critical workflows against these criteria:

### A. Intent and goal clarity
- Can the user identify the final goal of the flow within the first 3 seconds?
- Does each view feature exactly one visually dominant primary Call to Action?
- Do secondary actions use lower visual prominence (outline or text buttons) to avoid competing with the primary goal?

### B. Flow efficiency and redundancy
- Does the workflow represent the minimum theoretical step count required to complete the objective?
- Are unnecessary inputs eliminated by leveraging smart defaults or known user data?
- Is complex branching logic hidden until the user activates its trigger?

### C. Cognitive load and mental models
- Does interface terminology reflect user domain language rather than backend database architecture?
- Is progressive disclosure applied to advanced settings without burying critical options deeper than two clicks?
- Does a visual stepper display current step position, completed stages, and remaining steps?

### D. Wayfinding and orientation
- Do breadcrumbs and page headings clearly communicate current hierarchical location?
- Does an accessible escape hatch (Cancel or Save Draft button) exist within modals and multi-step flows?
- Are users informed immediately whenever background computation exceeds 1000 milliseconds?
