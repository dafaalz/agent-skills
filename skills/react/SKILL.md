---
name: react
description: Use when designing, building, testing, or optimizing React and Next.js applications, Server Components, client state, or data fetching. Don't use for non-React frameworks or static HTML.
---

# React

Performance optimization and architectural patterns for React and Next.js applications. Contains 70 prioritized rules across 8 impact categories.

## Workflow

### Step 1. Bottleneck identification and seam isolation

Profile component rendering or network waterfalls to isolate the exact performance bottleneck or architectural requirement.

Completion criterion. An identified target file, component, or network trace mapped to an observed performance metric or defect.

### Step 2. Rule selection and priority triage

Consult the priority catalog below to match the isolated symptom, evaluating highest-impact categories first.

Completion criterion. A selected rule name from `rules/<rule-name>.md` corresponding to the primary performance defect.

### Step 3. Reference consultation

Read the specific rule file in `rules/<rule-name>.md` for concrete code implementations, anti-patterns, and mechanical fixes.

Completion criterion. The rule file is inspected and the canonical fix pattern is established before mutating source files.

### Step 4. Surgical implementation

Apply the minimal code changes required to eliminate the bottleneck without modifying adjacent business logic or state hooks.

Completion criterion. Targeted components implement the rule pattern with zero orphan imports or unused state.

### Step 5. Verification pass

Run build commands, test suites, and bundle or render profiling to verify that the bottleneck is eliminated.

Completion criterion. Clean build exit code, passing test assertions, and verified elimination of the target performance defect.

## Rule categories by priority

| Priority | Category | Impact | Prefix | Focus |
| --- | --- | --- | --- | --- |
| 1 | Eliminating Waterfalls | CRITICAL | `async-` | Parallelize requests, defer await, use streaming |
| 2 | Bundle Size Optimization | CRITICAL | `bundle-` | Tree-shaking, dynamic imports, avoid barrel files |
| 3 | Server-Side Performance | HIGH | `server-` | Server Actions auth, RSC caching, minimize client serialization |
| 4 | Client-Side Data Fetching | MEDIUM-HIGH | `client-` | SWR deduplication, passive listeners, compact client storage |
| 5 | Re-render Optimization | MEDIUM | `rerender-` | Primitive dependencies, state colocation, deferred values |
| 6 | Rendering Performance | MEDIUM | `rendering-` | Content visibility, ternary conditionals, SVG animation wrappers |
| 7 | JavaScript Performance | LOW-MEDIUM | `js-` | Map and Set lookups, early exits, loop hoisting |
| 8 | Advanced Patterns | LOW | `advanced-` | Stable callback refs, single initialization, event handler refs |

## Rule catalog

### 1. Eliminating waterfalls (CRITICAL)

- `async-cheap-condition-before-await`. Check cheap sync conditions before awaiting flags or remote values.
- `async-defer-await`. Move await into branches where values are actually used.
- `async-parallel`. Use Promise.all() for independent operations.
- `async-dependencies`. Use partial dependency helpers for mixed async dependencies.
- `async-api-routes`. Start promises early and await late in API route handlers.
- `async-suspense-boundaries`. Wrap async components in Suspense to stream content.

### 2. Bundle size optimization (CRITICAL)

- `bundle-barrel-imports`. Import modules directly from concrete paths instead of index barrel files.
- `bundle-analyzable-paths`. Prefer statically analyzable import and file system paths.
- `bundle-dynamic-imports`. Use dynamic imports for heavy client components below the fold.
- `bundle-defer-third-party`. Load analytics, logging, and heavy third-party scripts after hydration.
- `bundle-conditional`. Load optional modules only when their feature flag is activated.
- `bundle-preload`. Preload heavy modules on user hover or focus interactions.

### 3. Server-side performance (HIGH)

- `server-auth-actions`. Authenticate and authorize inside every Server Action like an API endpoint.
- `server-cache-react`. Use React.cache() for per-request deduplication across the component tree.
- `server-cache-lru`. Use LRU caching for expensive cross-request compute.
- `server-dedup-props`. Avoid duplicate serialization across React Server Component boundaries.
- `server-hoist-static-io`. Hoist static asset reads and fonts to module level.
- `server-no-shared-module-state`. Avoid module-level mutable request state in RSC and SSR environments.
- `server-serialization`. Minimize data payload size passed from server to client components.
- `server-parallel-fetching`. Restructure parent-child components to parallelize data fetches.
- `server-parallel-nested-fetching`. Chain nested fetches per item concurrently in Promise.all().
- `server-after-nonblocking`. Use Next.js after() for non-blocking secondary tasks.

### 4. Client-side data fetching (MEDIUM-HIGH)

- `client-swr-dedup`. Use SWR or React Query for automatic client-side request deduplication.
- `client-event-listeners`. Deduplicate global window or document event listeners.
- `client-passive-event-listeners`. Use passive event listeners for scroll and touch listeners.
- `client-localstorage-schema`. Version and minimize localStorage and sessionStorage payloads.

### 5. Re-render optimization (MEDIUM)

- `rerender-defer-reads`. Do not subscribe to state that is only used inside action callbacks.
- `rerender-memo`. Extract expensive pure subtrees into memoized components.
- `rerender-memo-with-default-value`. Hoist default non-primitive props to prevent broken memoization.
- `rerender-dependencies`. Use primitive dependencies in effects instead of object references.
- `rerender-derived-state`. Subscribe to derived booleans rather than raw updating values.
- `rerender-derived-state-no-effect`. Derive state during render calculations rather than via effects.
- `rerender-functional-setstate`. Use functional setState callbacks for stable handler references.
- `rerender-lazy-state-init`. Pass initializer functions to useState for expensive initial values.
- `rerender-simple-expression-in-memo`. Avoid useMemo for simple primitive arithmetic or short string operations.
- `rerender-split-combined-hooks`. Split hooks that track independent concerns and update cycles.
- `rerender-move-effect-to-event`. Relocate user interaction logic into event handlers instead of effects.
- `rerender-transitions`. Wrap non-urgent updates in startTransition to keep UI responsive.
- `rerender-use-deferred-value`. Defer expensive renders to keep keyboard and mouse input fluid.
- `rerender-use-ref-transient-values`. Use refs for high-frequency transient values that do not impact layout.
- `rerender-no-inline-components`. Never define component functions inside parent component render bodies.

### 6. Rendering performance (MEDIUM)

- `rendering-animate-svg-wrapper`. Animate a wrapper div with hardware acceleration instead of the SVG element directly.
- `rendering-content-visibility`. Apply CSS content-visibility to long offscreen lists.
- `rendering-hoist-jsx`. Hoist static JSX trees outside components to avoid recreation.
- `rendering-svg-precision`. Reduce SVG coordinate decimal precision to cut DOM weight.
- `rendering-hydration-no-flicker`. Use inline layout scripts for client-only theme or layout data.
- `rendering-hydration-suppress-warning`. Suppress expected client-server hydration mismatches explicitly.
- `rendering-activity`. Use the React Activity component for preserving background state across tabs.
- `rendering-conditional-render`. Use ternary expressions rather than logical AND to avoid 0 rendering bugs.
- `rendering-usetransition-loading`. Prefer useTransition for pending states instead of custom boolean flags.
- `rendering-resource-hints`. Preconnect and preload assets using React DOM resource hints.
- `rendering-script-defer-async`. Apply defer or async attributes to external script tags.

### 7. JavaScript performance (LOW-MEDIUM)

- `js-batch-dom-css`. Group multiple DOM style changes via class names or cssText.
- `js-index-maps`. Build Map instances for repeated record lookups by ID.
- `js-cache-property-access`. Cache repeated object property lookups inside hot loops.
- `js-cache-function-results`. Cache pure compute results in module-level Map caches.
- `js-cache-storage`. Cache localStorage and sessionStorage reads in memory.
- `js-combine-iterations`. Combine multiple chained filter and map calls into a single loop.
- `js-length-check-first`. Compare array lengths before performing deep array comparisons.
- `js-early-exit`. Return early from functions to minimize nested conditional execution.
- `js-hoist-regexp`. Hoist RegExp instantiation outside functions and loops.
- `js-min-max-loop`. Use a single comparison loop for min and max instead of sorting.
- `js-set-map-lookups`. Use Set and Map for O(1) membership checks.
- `js-tosorted-immutable`. Use toSorted() for immutable array sorting.
- `js-flatmap-filter`. Use flatMap to filter and map in a single pass.
- `js-request-idle-callback`. Defer non-critical compute to browser idle periods.

### 8. Advanced patterns (LOW)

- `advanced-effect-event-deps`. Do not include useEffectEvent return functions in effect dependencies.
- `advanced-event-handler-refs`. Store unstable event handler callbacks in refs for stable consumption.
- `advanced-init-once`. Execute one-time application bootstrap logic once per application lifecycle.
- `advanced-use-latest`. Use useLatest ref helpers to access latest state inside stable callbacks.

## Applying rules

Read individual rule files in `rules/` for concrete problem descriptions, incorrect code snippets, and correct implementations:

```text
rules/async-parallel.md
rules/bundle-barrel-imports.md
rules/server-auth-actions.md
```
