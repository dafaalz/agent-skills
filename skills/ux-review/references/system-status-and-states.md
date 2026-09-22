# System status and interface states

Audit interface transparency, perceived latency, state transitions, and background synchronization resilience.

## Authoritative sources

| Source | Author or organization | Domain | Official URL |
| --- | --- | --- | --- |
| Response Times: The 3 Important Limits (1993, rev 2014) | Jakob Nielsen, NN/g | Human time perception thresholds | https://www.nngroup.com/articles/response-times-3-important-limits/ |
| The RAIL Model | Google Web Developers, web.dev | User-centric performance standard | https://web.dev/articles/rail |
| Skeleton Screens 101 (2023) | Nielsen Norman Group | Layout previews and perceived speed | https://www.nngroup.com/articles/skeleton-screens/ |
| Designing Empty States in Complex Applications (2020) | Kate Kaplan, NN/g | Zero-data interface guidelines | https://www.nngroup.com/articles/empty-states-complex-apps/ |
| Material Design 3: Progress Indicators | Google Design | Determinate vs indeterminate loaders | https://m3.material.io/components/progress-indicators/overview |
| Material Design 3: Snackbars | Google Design | Contextual confirmation and toasts | https://m3.material.io/components/snackbar/overview |
| Human Interface Guidelines: Feedback | Apple Inc. | Platform feedback and responsiveness | https://developer.apple.com/design/human-interface-guidelines/feedback |
| Human Interface Guidelines: Modality | Apple Inc. | Modal sheets, detents, and context | https://developer.apple.com/design/human-interface-guidelines/modality |
| Government Design Principles and Service Standard | UK Government Digital Service | Error summary and state clarity | https://www.gov.uk/guidance/government-design-principles |
| WCAG 2.2 Status Messages (Guideline 4.1.3) | W3C Web Accessibility Initiative | Live regions and state announcements | https://www.w3.org/WAI/WCAG22/Understanding/status-messages.html |

## 1. Quantitative latency thresholds and perceived speed

System responsiveness must align with human perception limits established by Robert Miller, Jakob Nielsen, and the Google RAIL model:

### 0 to 100 milliseconds (instantaneous feedback)
The system feels instantly responsive. Direct manipulation feels connected to the user pointer.
- Never display spinners, skeletons, or progress bars within this window.
- Deliver immediate visual micro-interaction feedback (such as active state, button depress, or ripple effect) in under 50 milliseconds.

### 100 to 1000 milliseconds (perceived delay)
The user notices a delay, but their cognitive thought process remains uninterrupted.
- Defer displaying loading indicators for 300 milliseconds. Flashing a spinner for 150 milliseconds causes visual flickering that disrupts concentration.
- When an operation takes 300ms to 1000ms, display a subtle inline spinner or trigger state change without blocking the entire viewport.

### Over 1000 milliseconds (explicit progress state)
The user loses the feeling of operating directly on data and their attention begins to wander.
- For processes with unpredictable durations under 10 seconds, use indeterminate progress indicators or skeleton screens.
- For operations exceeding 10 seconds, provide determinate progress bars with percentages, elapsed and remaining time estimates, and a functioning cancellation trigger.

### Google RAIL performance budget
- **Response.** Acknowledge user input in under 50 milliseconds to deliver the visual frame within 100 milliseconds.
- **Animation.** Complete each animation frame in 16 milliseconds to maintain 60 frames per second. JavaScript budget is 10 milliseconds per frame.
- **Idle.** Break heavy background JavaScript tasks into chunks under 50 milliseconds so the main thread remains receptive to user interactions.
- **Load.** Achieve a Largest Contentful Paint (LCP) under 2.5 seconds on mid-tier cellular networks.

## 2. Skeleton screens versus spinners

Select the appropriate loading pattern based on viewport scope:

### Skeleton screens
Mandatory for full page transitions, initial data feeds, dashboard cards, and modular lists:
- Builds a mental model of layout structure prior to payload arrival, substantially lowering perceived duration.
- Structure skeleton blocks to match the exact dimensions and aspect ratios of incoming text, avatars, and media.
- Apply a subtle left-to-right shimmer animation with a 1.5 to 2.0 second cycle time.

### Spinners
Reserved for atomic, localized actions:
- Embedded inside buttons during form dispatch.
- Infinite scroll footer fetching.
- Search input autocomplete queries.
- Pull-to-refresh swipe gestures.
- Never replace the entire viewport with a solitary spinning loader. Full-page spinners elevate perceived waiting time and provoke anxiety about system freezes.

## 3. Optimistic UI updates and rollback strategy

Optimistic updates render the anticipated successful state instantly before the server verifies the mutation.

### Application rules
- Mandatory for idempotent, low-consequence operations with high success probability (toggling favorites, bookmarks, marking notifications as read, updating checkboxes).
- Record a complete local state snapshot before mutating the UI.
- Dispatch network mutations in the background.

### Rollback telemetry on failure
- When a network request fails (timeout or HTTP 4xx/5xx status), revert state smoothly back to the initial snapshot.
- Display a non-blocking toast or snackbar explaining that the update could not be saved to the server.
- Provide a single-click retry action in the toast.
- Never leave optimistic data on screen if server synchronization fails permanently.

## 4. The six-state completeness model

Every dynamic component must define explicit behaviors across all six states:

### 1. Empty state (zero data)
Following Kate Kaplan and Dan Willis, distinguish across four empty state types:
- **First use.** The user has just registered. Present an onboarding orientation explaining feature benefits and an immediate Call to Action to create the first record.
- **User cleared.** The user completed all tasks (zero inbox, empty backlog). Display positive visual affirmation and offer logical follow-up actions.
- **Errors.** Data failed to load because of network drops or permission errors. Provide an empathetic explanation, status icon, and an in-place retry button.
- **No results.** Search queries or filter combinations returned zero matches. State that no matching results were found, suggest alternative queries, and provide a single-click reset button for active filters.

### 2. Partial state
Displayed when partial records arrive or when presenting cached stale data while background updates proceed:
- Render skeleton placeholders across missing slots to prevent Cumulative Layout Shift (CLS).
- Display a subtle synchronization badge if rendering offline cached data, informing the user that fresh updates are loading.

### 3. Loading state
- Defer spinner display by 300 milliseconds to avoid flickering on fast connections.
- Match skeleton layouts to destination cards.
- Display determinate progress meters during large file transfers or bulk batch operations.

### 4. Error state
- Display an Error Summary banner at the top of forms when multiple validation failures occur, ensuring screen readers announce issues immediately.
- Position specific error instructions directly beneath affected inputs.
- Exclude raw backend stack traces or HTTP error codes. Use plain, supportive language.

### 5. Success state
- Provide immediate confirmation upon task completion.
- For routine, non-destructive actions, present a snackbar or toast visible for 4 to 10 seconds with an embedded undo action.
- For high-stakes transactions (money transfers, checkout completions), transition users to a dedicated confirmation screen displaying reference identifiers and receipt summaries.

### 6. Rollback state
- Trigger smooth exit animations when optimistically added items must be removed after server rejection.
- Surface contextual error alerts explaining the synchronization failure.
- Preserve any text entered by the user to avoid data loss.
