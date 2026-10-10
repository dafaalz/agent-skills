---
name: react
description: Audit, profile, and optimize React and Next.js performance, waterfalls, bundle size, and rendering. Use when auditing, profiling, and optimizing React and Next.js performance, waterfalls, bundle size, Server Components, or re-renders. Don't use for general HTML styling, non-React frameworks, or initial greenfield scaffolding.
allowed-tools: Read Bash Glob Grep
---

# React

Performance optimization and architectural patterns for React and Next.js applications. Governs waterfall elimination, bundle size reduction, Server Components, and render tuning.

## Workflow

Follow these five steps in sequence:

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

Apply performance refactors strictly to rendering structures and network boundaries:
- Preserve all component prop interfaces, TypeScript contracts, and exported signatures.
- Never strip accessibility attributes (`aria-*`, `role`, focus management) to improve render metrics.
- Keep business logic and state hooks intact when applying rendering wrappers.

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
