---
name: react
description: "Use when auditing and optimizing React/Next.js application performance, component waterfalls, bundle sizes, Server Actions, or re-render dependencies. Don't use for CSS design (use frontend-design), UX usability critiques (use ui-ux-review), UI prototyping (use prototype), CSS/spring animations (use ui-motion), or multi-task execution plans (use agent-planning)."
---

# React

Performance optimization and architectural patterns for React and Next.js applications. Profile and optimize React and Next.js applications by eliminating network waterfalls, managing bundle size, and reducing unnecessary re-renders.

## Modes

Select an execution mode before Step 1:
- Audit mode (default). Profile bundles, waterfalls, and re-renders, and report findings without editing source code.
- Optimize mode. Restructure Server and Client boundaries, stream Suspense trees, split chunks, upgrade action hooks, and apply compiler-safe optimizations.

## Reference quick routing

| Optimization domain | Reference module | Scope |
|---|---|---|
| Render & network optimization | [references/render-optimization.md](references/render-optimization.md) | React 19 mutations, Core Web Vitals, & waterfalls |

## Workflow

Follow these five steps in sequence.

### Step 1. Toolchain probe and bottleneck identification

Probe the project runtime, compiler configuration, and performance symptoms before modifying code:

1. Check React version, Next.js version, and compiler configuration across `package.json` and Next.js config:
   ```bash
   node -e "const fs=require('fs'),p=JSON.parse(fs.readFileSync('package.json','utf8')),d={...p.dependencies,...p.devDependencies},c=['next.config.ts','next.config.mjs','next.config.js'].find(f=>fs.existsSync(f));console.log({react:d.react,next:d.next,compiler:Boolean(d['babel-plugin-react-compiler']||(c&&/reactCompiler\s*:\s*true/.test(fs.readFileSync(c,'utf8'))))})"
   ```
2. Run TypeScript compiler diagnostics with Next.js route typegen:
   ```bash
   npx next typegen && npx tsc --noEmit
   ```
3. Profile component rendering or network waterfalls to isolate the exact bottleneck.

Completion criterion: Command output confirms React version, compiler status, zero baseline TypeScript errors, and an isolated performance metric defect.

### Step 2. Rule selection and priority triage

Consult the priority catalog below to match the isolated symptom, evaluating highest-impact categories first. Enforce joint security and serialization invariants: every RSC or Server Action change must verify server authorization and Client boundary DTO safety.

Completion criterion: A selected rule set from references/rules/ addressing the performance defect alongside server security constraints.

### Step 3. Reference consultation

Read the specific rule file in references/rules/<prefix>-<name>.md for concrete code implementations, anti-patterns, and mechanical fixes.

Completion criterion: The rule file is inspected and the canonical fix pattern is established before mutating source files.

### Step 4. Surgical implementation

Apply minimal code changes to eliminate the bottleneck:
- Upgrade legacy `useState`/`useEffect` mutation flows to React 19 `useActionState`, `useOptimistic`, and uncontrolled `FormData` with automatic rollback.
- Place Server Actions in dedicated files with `'use server'` at the top (never inside `'use client'` files). Validate session credentials and tenant access inside the action. Return serializable discriminated unions (`ActionState { ok: boolean, error: string | null }`) instead of throwing raw errors that Next.js censors in production.
- When `compiler: true`, do not add manual `useMemo`, `useCallback`, or `React.memo`. Use immutable derivations (`.toSorted()`) and accept `ref` as a standard React 19 prop.
- For high-frequency interactive controls like range sliders, separate local thumb position state from transitioned data filtering to preserve responsive input tracking.
- Use `.reduce()` instead of `Math.max(...array)` for numeric aggregations over dynamic datasets to prevent call stack size limits.

Completion criterion: Targeted components implement the rule pattern with zero orphan imports, verified security boundaries, and clean compiler derivation paths.

### Step 5. Verification pass

Run build commands, test suites, and type checks to verify that the bottleneck is eliminated:
```bash
npx next typegen && npx tsc --noEmit && npm test
```

Completion criterion: Clean build exit code, passing test assertions, and verified elimination of the target performance defect.

## Boundary isolation

Confine optimization strictly to component rendering patterns, bundle splitting, and data fetching:
- Preserve backend API route contracts, database schemas, and business validation logic.
- Never modify component visual aesthetics, design tokens, or typography in the name of performance.
- Preserve existing accessibility attributes and semantic markup; never remove aria attributes or keyboard handlers to simplify rendering.
- Preserve public exported signatures, but narrow internal `'use client'` props to minimal serializable DTOs. Block raw database model leakage across the Client boundary using `experimental_taintObjectReference`.
- Ensure `'use client'` is explicitly declared at the top of client component files.
- Type Next.js 15 `params` and `searchParams` as Promises (`Promise<{ slug: string }>`) and await them concurrently with `cookies()`.
- Guard concurrent RSC reads with `Promise.allSettled` and an `AbortController` timeout signal to prevent whole-page crashes and detached orphaned queries.

## Rule categories by priority

| Priority | Category | Impact | Prefix | Focus |
| --- | --- | --- | --- | --- |
| 1 | Eliminating Waterfalls | CRITICAL | `async-` | Parallelize requests, defer await, use streaming |
| 2 | Server Actions and Security | CRITICAL | `server-` | Server Actions auth, RSC caching, minimize client serialization |
| 3 | Bundle Size Optimization | HIGH | `bundle-` | Tree-shaking, dynamic imports, avoid barrel files |
| 4 | Client-Side Data Fetching | MEDIUM-HIGH | `client-` | SWR deduplication, passive listeners, compact client storage |
| 5 | Re-render Optimization | MEDIUM | `rerender-` | Primitive dependencies, state colocation, deferred values |
| 6 | Rendering Performance | MEDIUM | `rendering-` | Content visibility, ternary conditionals, SVG animation wrappers |
| 7 | JavaScript Performance | LOW-MEDIUM | `js-` | Map and Set lookups, early exits, loop hoisting |
| 8 | Advanced Patterns | LOW | `advanced-` | Stable callback refs, single initialization, event handler refs |

Detailed rule specifications, code examples, and bad versus good patterns are stored individually in references/rules/<prefix>-<name>.md.

## Quick audit checklist

Review this table before completing React optimization tasks:

| Check | Passing condition |
|---|---|
| Next.js 15 dynamic APIs | `params`, `searchParams`, and `cookies()` awaited properly as Promises |
| Waterfalls | Data dependencies run concurrently via `Promise.allSettled` with `AbortController` timeout |
| Suspense streaming | Heavy or slow queries deferred and streamed via `<Suspense>` boundaries |
| Boundary serialization | Internal `'use client'` props narrowed to safe DTOs; raw ORM records tainted |
| Server Actions | Actions declared in `'use server'` files, verify session auth, and return serializable union results |
| Modern actions | Forms use `useActionState`, `useOptimistic`, and uncontrolled inputs with rollback |
| Compiler compatibility | Zero redundant `useMemo`/`useCallback` when compiler active; immutable derivations used |
| Native props | Components accept `ref` as standard prop without legacy `forwardRef` |
| Input responsiveness | High-frequency sliders decouple immediate thumb state from heavy transitioned filtering |
| Array aggregation | Aggregations use `.reduce()` instead of spreading unbounded arrays |
| Bundle size | Heavy client modules split dynamically with tree-shaking preserved |
| Accessibility | Semantic elements, ARIA attributes, and focus order preserved intact |
| Verification | Automated tests pass and TypeScript emits zero diagnostic errors |
