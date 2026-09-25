# Heuristics and interaction principles

Audit interactive surfaces against foundational usability heuristics, interaction design mechanics, and international ergonomic standards.

## Authoritative sources

| Source | Author or organization | Domain | Official URL |
| --- | --- | --- | --- |
| 10 Usability Heuristics for User Interface Design (1994, rev 2020) | Jakob Nielsen, Nielsen Norman Group | Evaluation heuristics for digital systems | https://www.nngroup.com/articles/ten-usability-heuristics/ |
| The Design of Everyday Things and Signifiers Concept (2013) | Don Norman, Basic Books | Cognitive models and signifiers | https://jnd.org/signifiers_not_affordances/ |
| Eight Golden Rules of Interface Design (1986, rev 2016) | Ben Shneiderman, University of Maryland | Interface engineering rules | https://www.cs.umd.edu/users/ben/goldenrules.html |
| First Principles of Interaction Design, Revised (2014) | Bruce Tognazzini, AskTog | Interaction mechanics and latency | https://asktog.com/atc/principles-of-interaction-design/ |
| ISO 9241-11:2018 Usability Definitions and Concepts | International Organization for Standardization | Effectiveness, efficiency, satisfaction | https://www.iso.org/obp/ui/#iso:std:iso:9241:-11:ed-2:v1:en |
| ISO 9241-210:2019 Human-Centred Design for Interactive Systems | International Organization for Standardization | Human-centred design lifecycle | https://www.iso.org/obp/ui/#iso:std:iso:9241:-210:ed-2:v1:en |
| ISO 9241-110:2020 Interaction Principles | International Organization for Standardization | Dialogue principles | https://www.iso.org/obp/ui/#iso:std:iso:9241:-110:ed-2:v1:en |
| Ten Principles for Good Design | Dieter Rams, Vitsœ | Functional digital design | https://www.vitsoe.com/us/about/good-design |
| Web Content Accessibility Guidelines 2.2 (2023) | W3C Web Accessibility Initiative | POUR accessibility standard | https://www.w3.org/TR/WCAG22/ |
| Cognitive Engineering Principles for Enhancing HCI Performance (1996) | Jill Gerhardt-Powals | Mental workload reduction | https://doi.org/10.1080/10447319609526145 |

## 1. Nielsen Norman Group 10 usability heuristics

### 01. Visibility of system status
- Any network request taking 100ms to 1000ms must show immediate active feedback on the trigger element.
- Processes exceeding 1000ms require determinate progress indicators or informative indeterminate states.
- Offline status must display a persistent, non-blocking banner informing the user that data is saved locally.
- Anti-pattern. Static submit buttons on slow connections that invite multiple clicks and duplicate payments.

### 02. Match between system and the real world
- Interface text must be free from database column names, raw backend exceptions, and protocol error codes.
- Date, time, currency, and numerical separators must match the user operating system locale via the standard Intl API.
- Information ordering must mirror the user mental workflow, not database foreign key relationships.
- Anti-pattern. Modal dialogs displaying `Unhandled Exception: ORA-00942` or forms requesting `MSISDN` instead of Phone Number.

### 03. User control and freedom
- Destructive actions (archiving, deleting, bulk clearing) require an undo mechanism lasting at least 5 seconds.
- Modals and slide-over panels must provide three independent dismissal mechanisms including the Escape key, a visible close button, and clicking the dimmed backdrop.
- Browser back button navigation must never corrupt state, trigger duplicate mutations, or trap users in redirect loops.
- Anti-pattern. Promotional modals that suppress the close button and trap mobile hardware back gestures.

### 04. Consistency and standards
- Primary buttons across all routes must share identical design tokens (background color, typography, padding, corner radius).
- The relative ordering of primary and secondary actions must remain identical across all views.
- Standard platform icons must preserve their canonical meanings. Never reuse a magnifying glass icon for a data filter.
- Anti-pattern. Placing primary actions on the bottom right on one screen and swapping them to the top left on the next.

### 05. Error prevention
- Form inputs with strict format requirements must use masking or constrained selectors that reject invalid characters.
- High-consequence destructive actions require deliberate confirmation, such as typing the exact resource identifier.
- Critical toggles must display explicit impact warnings before taking effect.
- Anti-pattern. Free-form text fields for numerical currency amounts that throw server errors upon submission.

### 06. Recognition rather than recall
- Complex input rules (such as password requirements) must stay visible on screen, not buried in temporary placeholders.
- Active filters on data grids must render as removable chips visible above the table.
- Multi-step wizards must carry forward and summarize previous inputs on the confirmation step.
- Anti-pattern. Blank forms that rely entirely on placeholder text that vanishes the moment typing begins.

### 07. Flexibility and efficiency of use
- All primary user tasks must be completable using the keyboard alone.
- High-volume data tables must provide multi-select checkboxes and batch action triggers.
- Repetitive workflows must provide documented keyboard shortcuts indicated in tooltips.
- Anti-pattern. Administrative consoles requiring manual per-row clicks without batch approval capabilities.

### 08. Aesthetic and minimalist design
- Every UI element must serve the primary task of the active view. Decorative visual clutter must be removed.
- Secondary data and technical metadata must use progressive disclosure mechanisms.
- Visual hierarchy must limit headings to a maximum of three distinct scale levels per viewport.
- Anti-pattern. Dashboards presenting dozens of brightly colored cards that obscure core operational metrics.

### 09. Help users recognize, diagnose, and recover from errors
- Error messages must describe the exact issue, explain the underlying cause, and offer immediate actionable remedies.
- Invalid input fields must render with accessible color contrast and display inline error text directly below the field.
- Network failure states must provide a single-click retry trigger that preserves entered form data.
- Anti-pattern. Vague dialogs showing `Error 422: Unprocessable Entity` without identifying invalid fields.

### 10. Help and documentation
- Help content must address user tasks rather than internal technical architecture.
- Ambiguous inputs must provide contextual popovers triggered on demand without navigating away.
- Empty states must explain the zero-data condition and provide a primary action button to populate content.
- Anti-pattern. Help links that trigger multi-megabyte PDF downloads or redirect to external community forums.

## 2. Don Norman interaction principles

### Affordances
- Touch screen targets must maintain a minimum physical touch area of 48 by 48 CSS pixels.
- Content lists that exceed the viewport height must preserve native scrolling affordances without CSS clipping.
- Anti-pattern. Text containers configured with `overflow: hidden` that truncate paragraphs without indicating hidden content.

### Signifiers
- Clickable controls must present explicit visual signifiers separating them from static labels.
- Non-interactive elements must never mimic interactive buttons or links.
- Form inputs must display distinct boundaries with a contrast ratio of at least 3:1 against the canvas background.
- Anti-pattern. Flat interfaces that render buttons as unstyled plain text without backgrounds or borders.

### Constraints
- **Physical constraints.** Place destructive controls away from common thumb rest areas on mobile devices.
- **Semantic constraints.** Restrict phone number fields to numerical input modes.
- **Logical constraints.** Automatically disable past dates in departure selectors when the arrival date is established.
- Anti-pattern. Allowing selection of an invalid checkout date, then rejecting the form after payment details are entered.

### Mappings
- Slider controls representing volume or price increases must advance from left to right or bottom to top.
- Pagination navigation must place earlier items on the left and later items on the right.
- Multi-camera or multi-zone controls must map to the physical spatial arrangement of the controlled equipment.
- Anti-pattern. Brightness sliders that darken the display when dragged toward the right.

### Feedback
- Interactive components must expose distinct visual states for `:hover`, `:active`, `:focus-visible`, and `:disabled`.
- The latency between user input and the initial visual acknowledgment must stay under 100 milliseconds.
- Haptic and audio feedback must be reserved for critical confirmations or error conditions.
- Anti-pattern. Message dispatch buttons that remain visually unchanged for seconds after receiving a click.

### Conceptual models
- Information architecture must mirror the user mental workflow rather than database normalization schemes.
- Interface metaphors (such as folders or carts) must behave consistently with their real-world counterparts.
- Anti-pattern. Banking apps requiring knowledge of internal ledger debit-credit terminology to view checking balances.

## 3. Ben Shneiderman eight golden rules

1. **Strive for consistency.** Use identical action verbs across all interfaces. Do not alternate between Edit, Modify, and Update for the same action.
2. **Seek universal usability.** Ensure content scales cleanly up to 200 percent zoom without horizontal scrolling or broken layouts.
3. **Offer informative feedback.** Scale feedback to action significance. Small actions receive subtle visual cues. Large transactions receive explicit status summaries.
4. **Design dialogs to yield closure.** Group interactions into clear beginning, middle, and completion stages with explicit confirmation summaries.
5. **Prevent errors.** Disable invalid options proactively, constrain inputs, and provide inline guidance before form submission.
6. **Permit easy reversal of actions.** Support undo operations to reduce anxiety and encourage feature exploration.
7. **Support internal locus of control.** Keep the user in command of system pace. Avoid unexpected layout shifts, auto-playing media, or unprompted redirects.
8. **Reduce short-term memory load.** Break long identifiers into 3 to 4 character chunks and never require memorizing values across screens.

## 4. Bruce Tognazzini first principles

- **Anticipation.** Surface tools, data, and next-step actions proactively before the user must search for them.
- **Autonomy.** Allow users to navigate and pace their work freely while maintaining non-destructive guardrails.
- **Color blindness.** Never convey meaning through color alone. Pair color tokens with text labels, icons, or patterns.
- **Defaults.** Set default options to the safest, lowest-risk, and most common selection. Never select paid add-ons by default.
- **Efficiency of the user.** Prioritize human time over machine efficiency. Minimize keystrokes and navigation steps.
- **Explorable interfaces.** Provide clear wayfinding and safe reversal mechanisms so users can discover features without fear.
- **Fitts's Law.** Scale targets appropriately and place frequent actions near screen edges or within natural thumb zones.
- **Latency reduction.** Mask unavoidable delays using optimistic rendering and intelligent background prefetching.
- **Protect the user's work.** Preserve entered form data and document drafts locally to survive network losses and session timeouts.
- **Track state.** Retain scroll positions, active tabs, and filter criteria when the user returns from a detail view.

## 5. International ergonomic standards (ISO 9241)

### ISO 9241-11:2018 Usability definitions
Usability represents the outcome of human interaction within a specific context:
- **Effectiveness.** Accuracy and completeness with which users achieve specified goals. Measure using Task Completion Rate (minimum 85 percent target).
- **Efficiency.** Resources expended in relation to the accuracy and completeness of goals. Measure using Time on Task compared to standard baselines.
- **Satisfaction.** Freedom from discomfort and positive attitudes toward product use. Measure using System Usability Scale (SUS > 68) or Single Ease Question (SEQ >= 5.5).

### ISO 9241-210:2019 Human-centred design
- Design relies on explicit understanding of users, tasks, and operating environments.
- Users participate actively throughout design and development.
- Iterative cycles drive development based on continuous empirical evaluations.
- Product decisions must rely on observed user behavior rather than internal organizational hierarchy.

### ISO 9241-110:2020 Interaction principles
1. **Suitability for the task.** Present only information and controls required to complete the immediate objective.
2. **Self-descriptiveness.** Ensure each step is immediately comprehensible without consulting separate manuals.
3. **Conformity with user expectations.** Align behaviors with established domain conventions and platform norms.
4. **Learnability.** Support initial mastery and straightforward re-learning for intermittent users.
5. **Controllability.** Allow the user to determine the pace, sequence, and direction of the interaction.
6. **Use error robustness.** Ensure invalid input does not cause catastrophic failures or discard valid data.
7. **User engagement.** Deliver an interface that supports focused, productive user involvement.

## 6. Dieter Rams ten principles in software

1. **Innovative.** Integrate modern capabilities (biometrics, predictive input) to remove friction rather than as cosmetic novelties.
2. **Useful.** Prune features whose sustained adoption remains below 2 percent to protect core interface utility.
3. **Aesthetic.** Enforce consistent spatial rhythm, modular grids, and clear typographic contrast to build trust.
4. **Understandable.** Ensure primary onboarding flows can be completed in under 3 minutes without external assistance.
5. **Unobtrusive.** Avoid marketing popups or rating prompts while users are in the middle of active workflows.
6. **Honest.** Disclose full costs upfront and make account deletion as straightforward as initial registration.
7. **Long-lasting.** Build on semantic web standards and design tokens rather than short-lived visual trends.
8. **Thorough.** Test all components across five core states including ideal, loading, empty, error, and partial data.
9. **Environmentally friendly.** Minimize digital carbon footprint by compressing assets and trimming bundle sizes under 200KB.
10. **As little design as possible.** Eliminate decorative borders, extraneous shadows, and unnecessary visual markers.

## 7. Jill Gerhardt-Powals cognitive engineering principles

1. **Automate unwanted workload.** Compute currency conversions, tax totals, and date deltas automatically.
2. **Reduce uncertainty.** Present data unambiguously to eliminate hesitation.
3. **Fuse data.** Combine low-level operational variables into clear composite indicators.
4. **Present new information with meaningful aids.** Use familiar real-world analogies to introduce complex systems.
5. **Use names conceptually related to function.** Align labels directly with user goals.
6. **Group data consistently.** Place related inputs in coherent fieldsets with a maximum of 5 to 7 items.
7. **Limit data-driven tasks.** Provide visual graphs and trend indicators rather than raw tabular streams.
8. **Include only needed information.** Display only the data relevant to the active operational stage.
9. **Provide multiple coding of data.** Pair numerical indicators with colors and visual icons.
10. **Practice judicious redundancy.** Reinforce critical system states without producing visual clutter.
