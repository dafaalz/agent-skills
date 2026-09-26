# Divergence Taxonomy

Comprehensive taxonomy of architectural and code divergences across codebases.

## Taxonomy by Concern

Audit every concern in this table. Each row represents a specific divergence to investigate with concrete file evidence.

| Concern | Typical Divergence | Detection Probe |
| --- | --- | --- |
| Module/API usage | `moduleA.doThing()` vs `moduleB.doThing()` | Grep library imports and wrapper calls |
| Import style | Default vs named, relative vs absolute paths, barrel imports vs direct paths | Grep import statements across source files |
| Naming | `camelCase` vs `snake_case`, boolean prefixes, verb choices in functions | Check symbol names and file naming conventions |
| Async style | Callbacks vs promises vs `async/await`, mixed then-chains and await | Search for `\.then\(`, `async function`, `await` |
| Error handling | Exceptions vs Result objects, custom errors vs bare Error, silent catch vs propagation | Search for `throw`, `catch`, `raise`, `Result<` |
| Null handling | `=== null` vs `== null`, nullish coalescing `??` vs logical OR `\|\|`, optional chaining | Search for `\?\?`, `=== null`, `\?\.` |
| State management | Local component state vs global store vs context, mutable vs immutable updates | Check store subscriptions and reducer patterns |
| Data access | ORM vs raw SQL queries, repository pattern vs inline query execution | Grep query builders, models, and SQL strings |
| Validation | Schema validation at API boundaries vs inline checks vs unvalidated payloads | Check validator usage (`zod`, `joi`, `pydantic`) |
| Logging | Structured JSON vs unstructured strings, logger instance vs console statements | Search for `console\.log`, `logger\.`, `print\(` |
| Configuration | Environment variables vs config objects vs hardcoded constants | Search for `process\.env`, `os\.environ`, `config\.` |
| Testing | Test framework choices, BDD `describe/it` vs flat test functions, mocking patterns | Inspect test files and mock utilities |
| Formatting | Indentation, quotes, semicolons, line width. Defer entirely to configured formatter | Check `.editorconfig`, `.prettierrc`, `ruff.toml` |
| Type strictness | Compiler strict mode enabled vs disabled, `any` vs `unknown`, type assertions | Check tsconfig, mypy, or phpstan settings |
| File structure | Single export per file vs multiple exports, colocated tests vs parallel test directory | Check directory tree and test placements |
| Date and numbers | Native Date vs date libraries, floating point currency vs minor unit integers | Search for date math and currency calculations |
| HTTP client | `fetch` vs `axios` vs internal wrappers, inconsistent timeout and retry behavior | Grep HTTP client libraries and helper imports |
| Component architecture | Functional components vs class components, custom hooks vs higher-order components | Check component definitions and composition patterns |

## The Divergence Record Format

For each detected divergence, record concrete evidence so stakeholders can decide immediately.

```markdown
### D1. Module accessor for date arithmetic

**Variant A**. `dayjs` (34 files)
src/orders/created.ts:12, src/cart/total.ts:8, src/user/profile.ts:31 (+31 more)
`dayjs(order.createdAt).add(7, 'day')`

**Variant B**. Native `Date` with local helper (6 files)
src/reports/range.ts:44, src/export/csv.ts:19 (+4 more)
`addDays(new Date(order.createdAt), 7)`

**Variant C**. `date-fns` (2 files)
src/billing/invoice.ts:57, src/billing/proration.ts:22
`addDays(new Date(order.createdAt), 7)`

**Conflict**. Three approaches for one concern. `dayjs` and `date-fns` are both direct dependencies. `addDays` in `src/lib/date.ts` duplicates both.
**Recommendation**. Variant A (`dayjs`), because it represents the majority and is an established dependency.
**Counter-signal**. Variant C is confined to `billing/`, which might be a newer subsystem with intentional design. Confirm before normalizing.
```

## Counting Occurrences

Count exact occurrences instead of estimating. Run exact counts across the repository:

```bash
grep -rIl "dayjs" --exclude-dir={node_modules,.git,dist,build,vendor} . | wc -l
grep -rIl "date-fns" --exclude-dir={node_modules,.git,dist,build,vendor} . | wc -l
```

## Checking Counter-Signals

A minority pattern confined to a specific directory or recent commits often represents an ongoing architectural migration. Inspect git history before assuming the majority pattern is canonical:

```bash
git log --oneline -20 -- src/billing/
git log -S "date-fns" --oneline | head -5
```
