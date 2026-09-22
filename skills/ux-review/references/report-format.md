# UX review report format

Consolidate findings into a structured, evidence-backed evaluation report with Before, After, and Why tables.

## 1. Severity classification

Assign every finding to one of three severity tiers:

- **Blocker.** Directly causes task abandonment, creates unrecoverable data loss, traps navigation, displays silent failure states, or violates foundational accessibility thresholds.
- **Warning.** Increases cognitive load, introduces premature error friction, lacks empty-state guidance, violates thumb zone reachability, or slows task completion.
- **Nit.** Minor terminology inconsistencies, slight spacing imbalances, or non-critical microcopy adjustments.

## 2. Evidence structure

Every finding must provide:
1. Exact component name, route, or file path with line numbers.
2. The specific cognitive law, usability heuristic, or empirical research citation violated.
3. A comparative Before, After, and Why table.
4. A concrete resolution provided in the project's native framework or styling syntax.
5. Projected impact on quantitative usability metrics such as TCR, Lostness, or Drop-off rate.

## 3. Finding limit and final verdicts

- Cap findings at a maximum of 12 items per audit to prevent cognitive overload for engineering teams.
- Prioritize Blocker and Warning items over cosmetic nits.
- Assign one of two final verdicts:
  - Approve. Zero blockers and fewer than three non-critical warnings.
  - Changes Requested. One or more blockers, or widespread usability regressions that damage user task completion.

## 4. Markdown report template

Use this standard markdown structure:

````markdown
# UX review for <Target Scope or Flow Name>

## Summary
- Target interface: `<component, route, or task flow>`
- Target user goal: `<primary user intent>`
- Optimal step count: `<minimum theoretical steps>`
- Findings count: `<total> (<blocker count> Blockers, <warning count> Warnings, <nit count> Nits)`
- Usability verdict: `Approve` | `Changes Requested`

## Usability metrics projection
- Task Completion Rate (TCR) risk: `<Low, Medium, or High with explanation>`
- Cognitive load profile: `<Cowan chunks, Hick-Hyman choices>`
- Error recovery rating: `<Resilient / Vulnerable / Fatal>`

## Findings

### 1. [<Severity>] <Descriptive Finding Title>
- Location: `<route, screen, or file:line>`
- Standard violated: `<Heuristic or Cognitive Law, e.g., NN/g H5 Error Prevention / Fitts's Law>`
- Research citation: `<Author, Title, URL>`

#### Before, after, and why

| Before | After | Why |
| --- | --- | --- |
| `<current problematic implementation or copy>` | `<recommended human-centered solution>` | `<empirical reason, cognitive mechanism, or ergonomic benefit>` |

#### Concrete resolution

```<language>
// Concrete code or copy modification fixing the usability defect
```
````
