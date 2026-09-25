# Cognitive psychology and laws of UX

Audit interfaces against cognitive limits, working memory bounds, perception mechanics, and mathematical interaction laws.

## Authoritative sources

| Source | Author and year | Domain | Official URL |
| --- | --- | --- | --- |
| Laws of UX: Using Psychology to Design Better Products | Jon Yablonski (2020) | Psychological UX principles | https://lawsofux.com |
| The Information Capacity of the Human Motor System | Paul M. Fitts (1954) | Motor target acquisition | https://doi.org/10.1037/h0055392 |
| On the Rate of Gain of Information | William Edmund Hick (1952) | Logarithmic choice time | https://doi.org/10.1080/17470215208416600 |
| Stimulus Information as a Determinant of Reaction Time | Ray Hyman (1953) | Decision time entropy | https://doi.org/10.1037/h0056940 |
| The Magical Number Seven, Plus or Minus Two | George A. Miller (1956) | Classical memory span | https://doi.org/10.1037/h0043158 |
| The Magical Number 4 in Short-Term Memory | Nelson Cowan (2001) | Modern 4-chunk memory limit | https://doi.org/10.1017/S0140525X01003922 |
| Cognitive Load During Problem Solving: Effects on Learning | John Sweller (1988) | Cognitive Load Theory | https://doi.org/10.1207/s15516709cog1202_4 |
| The Economic Value of Rapid Response Time | Walter J. Doherty, IBM (1982) | 400ms interactivity threshold | https://www.ibm.com/history/doherty-threshold |
| When Choice is Demotivating: Can One Desire Too Much? | Sheena S. Iyengar & Mark R. Lepper (2000) | Choice overload | https://doi.org/10.1037/0022-3514.79.6.995 |
| When More Pain Is Preferred to Less: Adding a Better End | Daniel Kahneman et al. (1993) | Peak-End Rule | https://doi.org/10.1111/j.1467-9280.1993.tb00589.x |
| Das Behalten erledigter und unerledigter Handlungen | Bluma Zeigarnik (1927) | Memory of incomplete tasks | https://doi.org/10.1007/BF02409755 |
| Über die Wirkung von Bereichsbildungen im Spurenfeld | Hedwig von Restorff (1933) | Visual isolation effect | https://doi.org/10.1007/BF02409636 |
| Untersuchungen zur Lehre von der Gestalt II | Max Wertheimer (1923) | Gestalt visual organization | https://doi.org/10.1007/BF00410640 |
| Jakob's Law of Internet User Experience | Jakob Nielsen (2000) | External mental models | https://www.nngroup.com/articles/jakobs-law-internet-user-experience/ |

## 1. Mathematical models and quantitative limits

### Fitts's Law
The time required to rapidly move to a target area is a function of the ratio between the distance to the target and the width of the target:

`MT = a + b * log2(D / W + 1)`

Variables:
- `MT`: Movement time in milliseconds.
- `a`: Start and stop device reaction time intercept.
- `b`: Empirical processing speed of the human motor system.
- `D`: Distance from the pointer or finger to the center of the target.
- `W`: Width of the target measured along the axis of motion.
- `log2(D / W + 1)`: Index of Difficulty (ID) expressed in bits.

Audit thresholds:
- Touch targets on mobile must measure at least 48 by 48 CSS pixels.
- The minimum spacing between interactive targets must be 8 CSS pixels to eliminate accidental touches.
- Desktop screen edges and corners provide infinite width (`W -> infinity`) because the operating system bounds cursor travel.

### Hick-Hyman Law
Cognitive decision time to select one option from a set of alternatives scales logarithmically with the number of choices:

`RT = b * log2(n + 1)`

When probabilities across options vary, the information entropy formula applies:

`RT = b * sum(p_i * log2(1 / p_i))`

Variables:
- `RT`: Reaction time in milliseconds.
- `b`: Cognitive processing constant, approximately 150ms to 200ms per bit of information.
- `n`: Number of equally probable alternatives.

Audit thresholds:
- Primary top-level navigation must not present more than 5 to 7 direct choices.
- Increasing choices from 4 to 16 doubles cognitive decision time from 2 bits to 4 bits of mental workload.

### Working memory with Miller and Nelson Cowan limits
George Miller observed a capacity of 7 plus-minus 2 chunks when subjects employ active verbal rehearsal. Nelson Cowan demonstrated that pure working memory capacity without rehearsal is strictly 4 plus-minus 1 chunks (3 to 5 discrete units of information).

Audit thresholds:
- Numerical strings (phone numbers, OTPs, bank accounts, credit cards) must be formatted into chunks of 3 to 4 digits.
- Complex forms and input groups must present a maximum of 4 to 5 related fields per fieldset.

### Choice overload (Iyengar and Lepper)
The classic 24-jam vs 6-jam experiment revealed critical conversion metrics:
- Initial foot traffic. The 24-choice display attracted 60 percent of shoppers, while the 6-choice display attracted 40 percent.
- Actual purchasing conversion. Only 3 percent of shoppers exposed to 24 choices completed a purchase. In contrast, 30 percent of shoppers exposed to 6 choices completed a purchase.
- Practical UI threshold. Restrict SaaS pricing tiers to 3 or a maximum of 4 distinct packages.

### Doherty Threshold
Rapid system response under 400 milliseconds keeps human attention within a continuous cognitive flow.

Quantitative latency tiers:
- 0 to 100 milliseconds. Perceived as instantaneous. Mandatory for button press states, hover changes, and direct manipulation gestures.
- 100 to 300 milliseconds. Perceived as smooth. Ideal for animated transitions and client-side page routing.
- Under 400 milliseconds. The Doherty Threshold. The computer and human interact at a pace that maintains cognitive focus without mental interruptions.
- 400 to 1000 milliseconds. Noticeable delay. Skeleton loaders or subtle shimmer animations are required to bridge the gap.
- Over 1000 milliseconds. Cognitive focus breaks. Determinate progress indicators showing actual percentages or step counts are mandatory.
- Modern web metric Interaction to Next Paint (INP) requires input delay below 200 milliseconds.

## 2. Cognitive Load Theory in interface design

John Sweller defines three distinct types of cognitive load:

### Intrinsic cognitive load
The inherent difficulty of the task itself, such as configuring network routing or calculating overseas taxes. It cannot be eliminated without altering core business functionality.

Mitigation strategies:
- Implement progressive disclosure. Hide advanced parameters behind secondary toggles.
- Provide smart defaults based on the user operating context.
- Break long tasks into sequenced multi-step wizards.

### Extraneous cognitive load
Mental effort imposed by poor UI layouts, confusing terminology, visual clutter, and misaligned components. It consumes working memory without providing any task value.

Elimination strategies:
- Remove purely decorative borders, background textures, and uninformative icons.
- Position input labels directly above fields to prevent erratic eye scanning.
- Provide inline error guidance directly below invalid inputs.

### Germane cognitive load
Mental effort dedicated to processing information, recognizing patterns, and constructing lasting mental models.

Optimization strategies:
- Display real-time visual feedback, such as charts updating instantly when loan parameters adjust.
- Use visual metaphors and structures that mirror real-world user expectations.

## 3. Gestalt perception principles in UI

### Proximity
Items positioned close together are perceived as belonging to a single functional group.
- Spacing ratio rule. Vertical distance between label and input (`S_label`) must satisfy `S_label <= 0.33 * S_group`, where `S_group` is the distance between question blocks.
- Violating proximity forces users to pause and determine which label governs which input.

### Similarity
Elements sharing visual characteristics (shape, color, typography) are perceived as having identical functions.
- Primary Call to Action buttons must share identical color, typography, and corner radius tokens across the entire application.
- Hyperlinks must maintain a distinct visual treatment (such as an underline or dedicated accent color) to separate them from static body text.

### Continuity
The human eye naturally tracks continuous lines, curves, and regular alignments.
- Single-column linear form layouts yield higher completion rates than multi-column layouts because eye gaze travels downward without horizontal interruptions.
- Horizontal card carousels must expose a partially visible card edge (peeking card) to signal that content continues horizontally.

### Closure
The brain automatically completes missing visual contours to perceive an organized whole.
- Skeleton screens exploit closure. Displaying light gray rectangles approximating avatars and paragraphs establishes layout structure before API payloads arrive.
- Minimalist line iconography uses closure to convey meaning without detailed rendering.

### Figure and ground
Visual perception separates the focal element of interest (figure) from the surrounding canvas (ground).
- Modal dialogs must use a darkened backdrop overlay (scrim) with subtle background blur to suppress the ground and elevate the modal as the active figure.
- Drop shadows and tonal elevations distinguish active dropdown menus and sticky navigation headers from the scrollable page beneath.

## 4. Behavioral psychological phenomena

### Peak-End Rule
Users judge an experience primarily by its emotional peak and its conclusion, rather than the arithmetic average of every moment.
- Ensure the final step of critical flows (such as order confirmation or account creation) provides an unambiguous sense of closure and positive feedback.
- Eliminate jarring friction or unexpected fees on the final checkout screen.

### Zeigarnik Effect
Uncompleted tasks create persistent cognitive tension that occupies working memory until resolved.
- Multi-step registration or onboarding processes exceeding 60 seconds must display step indicators showing completed stages and remaining steps.
- Provide automatic draft saving so users can pause an incomplete task without fear of losing progress.

### Von Restorff Effect (Isolation Effect)
When multiple similar items are presented, the item that differs visually from the rest is most likely to be remembered.
- Limit primary visual salience to exactly one primary action per viewport.
- Secondary actions must use outline or ghost button treatments with lower visual weight.

### Jakob's Law
Users spend most of their time on other websites, meaning their mental models are formed by external web conventions.
- Use standard conventions for shopping carts, search inputs, profile menus, and navigation back buttons.
- Do not reinvent fundamental interface mechanics.

## 5. Concrete cognitive audit checklist

Validate compliance using these eight rules during review:

1. **Fitts target compliance.** Verify all interactive mobile elements meet the 48 by 48 CSS pixel target with at least 8 CSS pixels of clearance.
2. **Doherty latency enforcement.** Confirm interactions provide visual feedback within 100ms and display skeleton loaders for delays between 400ms and 1000ms.
3. **Nelson Cowan chunking limit.** Ensure primary navigation bars contain at most 5 tabs and long numerical inputs format into chunks of 3 to 4 characters.
4. **Hick-Hyman choice pruning.** Confirm raw dropdown menus exceeding 10 items include search filtering, and pricing matrices display at most 4 primary plans.
5. **Gestalt proximity ratio.** Confirm the label-to-input gap does not exceed one-third of the gap between distinct question groups.
6. **Von Restorff salience.** Confirm exactly one primary Call to Action dominates the active viewport.
7. **Zeigarnik progress visibility.** Verify wizards requiring more than 60 seconds present step progress indicators and automatic draft persistence.
8. **Jakob's Law conventions.** Confirm search, shopping cart, and back navigation components follow established platform norms.
