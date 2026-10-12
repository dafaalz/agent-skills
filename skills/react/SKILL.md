---
name: react
description: Use when auditing, profiling, and optimizing React and Next.js performance, waterfalls, bundle size, Server Components, or re-renders. Don't use for general HTML styling, non-React frameworks, or initial greenfield scaffolding.
allowed-tools: Read Bash Glob Grep
---

# React

Performance optimization and architectural patterns for React and Next.js applications. Profile and optimize React and Next.js applications by eliminating network waterfalls, managing bundle size, and reducing unnecessary re-renders.

## Modes

Select an execution mode before Step 1:
- Audit mode (default). Profile bundles, waterfalls, and re-renders, and report findings without editing source code.
- Optimize mode. Restructure component hierarchies, split code chunks, and implement memoization.

## Workflow

Follow these five steps in sequence.

### Step 1. Toolchain probe and bottleneck identification

Probe the project runtime, compiler configuration, and performance symptoms before modifying code:

1. Check React version, Next.js version, and compiler configuration in `package.json`:
   ```bash
   node -e "const p=require('./package.json'); console.log({react: p.dependencies?.react, next: p.dependencies?.next, compiler: p.devDependencies?.['babel-plugin-react-compiler']})"
   ```
2. Run TypeScript compiler diagnostics to establish a clean baseline:
   ```bash
   npx tsc --noEmit
   ```
3. Profile component rendering or network waterfalls to isolate the exact bottleneck.

Completion criterion. Command output confirms React version, compiler status, zero baseline TypeScript errors, and an isolated performance metric defect.

### Step 2. Rule selection and priority triage

Consult the priority catalog below to match the isolated symptom, evaluating highest-impact categories first.

Completion criterion. A selected rule name from `references/rules/<rule-name>.md` corresponding to the primary performance defect.

### Step 3. Reference consultation

Read the specific rule file in `references/rules/<rule-name>.md` for concrete code implementations, anti-patterns, and mechanical fixes.

Completion criterion. The rule file is inspected and the canonical fix pattern is established before mutating source files.

### Step 4. Surgical implementation

Apply the minimal code changes required to eliminate the bottleneck without modifying adjacent business logic or state hooks.

Completion criterion. Targeted components implement the rule pattern with zero orphan imports or unused state.

### Step 5. Verification pass

Run build commands, test suites, and type checks to verify that the bottleneck is eliminated:
```bash
npx tsc --noEmit && npm test
```

Completion criterion. Clean build exit code, passing test assertions, and verified elimination of the target performance defect.

## Boundary isolation

Confine optimization strictly to component rendering patterns, bundle splitting, and data fetching:
- Preserve backend API route contracts, database schemas, and business validation logic.
- Never modify component visual aesthetics, design tokens, or typography in the name of performance.
- Preserve existing accessibility attributes and semantic markup; never remove aria attributes or keyboard handlers to simplify rendering.
- Preserve all component prop interfaces, TypeScript contracts, and exported signatures.

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

Detailed rule specifications, code examples, and bad versus good patterns are stored individually in `references/rules/<prefix>-<name>.md`.

## Quick audit checklist

Review this table before completing React optimization tasks:

| Check | Passing condition |
|---|---|
| Waterfalls | Data dependencies run concurrently or stream via Suspense |
| Bundle size | Heavy client modules split dynamically with tree-shaking preserved |
| Server Components | Client boundary placed at leaf nodes without secret leaks |
| Accessibility | Semantic elements, ARIA attributes, and focus order preserved intact |
| Verification | Automated tests pass and TypeScript emits zero diagnostic errors |
