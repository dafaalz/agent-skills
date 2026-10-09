# UI and UX review report format

Consolidate interface mechanics and usability findings into a structured, evidence-backed evaluation with Before, After, and Why tables.

## 1. Severity classification

Assign every finding to one of three severity tiers:

- **Blocker.** Prevents interaction, strips keyboard focus rings (`outline: none`), violates WCAG 2.2 AA contrast standards, causes severe Cumulative Layout Shift, breaks responsive layouts at 320px, creates unrecoverable data loss, traps navigation, displays silent failure states, or causes task abandonment.
- **Warning.** Inconsistent spacing scales, unlinked form labels, missing empty states, non-concentric border radii, hover states triggering on touchscreens, premature error validation, thumb zone reachability issues, or unnecessary cognitive load.
- **Nit.** Minor typographic adjustments, slight spacing imbalances, non-critical microcopy polish, or terminology inconsistencies.

## 2. Evidence structure

Every finding must provide:
1. Exact file path, component name, route, and line numbers.
2. The specific standard, WCAG success criterion, cognitive law, or usability heuristic violated.
3. Relevant empirical research or specification citation when applicable.
4. A comparative Before, After, and Why table.
5. A concrete code diff or copy modification in the project's native syntax.
6. Projected impact on accessibility or usability metrics (TCR, Lostness, Drop-off rate).

## 3. Finding limit and final verdicts

- Cap findings at a maximum of 12 items per audit to focus on high-impact defects and avoid cognitive overload.
- Prioritize Blocker and Warning items over cosmetic nits.
- Assign one of two final verdicts:
  - Approve. Zero blockers and fewer than three non-critical warnings.
  - Changes Requested. One or more blockers, or widespread interface or usability regressions.

## 4. Markdown report template

Use this standard markdown structure:

````markdown
# UI and UX review for <Target Scope, Component, or Flow Name>

## Summary
- Target scope: `<file path, component, route, or PR identifier>`
- Styling engine: `<Tailwind / CSS Modules / Vanilla CSS / styled-components>`
- Primary user goal: `<primary user intent and optimal step count>`
- Inspected surfaces: `<count of screens, components, or routes audited>`
- Findings count: `<total> (<blocker count> Blockers, <warning count> Warnings, <nit count> Nits)`
- Final verdict: `Approve` | `Changes Requested`

## Usability and technical projection
- Accessibility compliance: `<WCAG 2.2 AA passing / failing with specifics>`
- Task Completion Rate (TCR) risk: `<Low, Medium, or High with explanation>`
- Cognitive load profile: `<Cowan chunks, Hick-Hyman choices>`
- Error recovery rating: `<Resilient / Vulnerable / Fatal>`

## Findings

### 1. [<Severity>] <Descriptive Finding Title>
- Location: `<file path>:<line> or <route>`
- Standard violated: `<Standard, WCAG SC, Heuristic, or Cognitive Law>`
- Research citation: `<Specification or author citation if applicable>`

#### Before, after, and why

| Before | After | Why |
| --- | --- | --- |
| `<problematic styling, markup, or copy>` | `<compliant modern implementation>` | `<empirical reason, browser engine standard, or cognitive mechanism>` |

#### Concrete resolution

```<language>
// Code diff or markup showing the exact fix in project idiom
```
````
