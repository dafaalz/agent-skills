# Interface review report format

Format interface review findings into a structured, evidence-backed evaluation with Before, After, and Why tables.

## 1. Severity classification

Assign every finding to one of three severity tiers:

- **Blocker.** Prevents interaction, strips keyboard focus rings (`outline: none`), violates WCAG 2.2 AA contrast standards, causes severe Cumulative Layout Shift, breaks responsive layouts at 320px, or deletes user inputs without recovery.
- **Warning.** Inconsistent spacing scales, unlinked form labels, missing empty states, non-concentric border radii, or hover states triggering on touchscreens.
- **Nit.** Minor typographic adjustments, microcopy polish, or non-critical styling inconsistencies.

## 2. Evidence structure

Every finding must provide:
1. Exact file path and line numbers.
2. The specific rule, standard, or specification violated.
3. A comparative Before, After, and Why table.
4. A concrete code diff in the project's native styling syntax or framework idiom.

## 3. Finding limit and final verdicts

- Cap findings at a maximum of 12 items per audit to focus on high-impact defects.
- Prioritize Blocker and Warning items over cosmetic nits.
- Assign one of two final verdicts:
  - Approve. Zero blockers and fewer than three non-critical warnings.
  - Changes Requested. One or more blockers, or widespread interface regressions.

## 4. Markdown report template

Use this standard markdown structure:

````markdown
# Interface review for <Target Scope or Component Name>

## Summary
- Target scope: `<file path, component, or PR identifier>`
- Styling engine: `<Tailwind / CSS Modules / Vanilla CSS / styled-components>`
- Inspected surfaces: `<count of screens or components audited>`
- Findings count: `<total> (<blocker count> Blockers, <warning count> Warnings, <nit count> Nits)`
- Final verdict: `Approve` | `Changes Requested`

## Findings

### 1. [<Severity>] <Descriptive Finding Title>
- Location: `<file path>:<line>`
- Standard violated: `<Standard Name, e.g., WCAG 2.2 SC 2.4.11 / W3C Corner Shaping>`

#### Before, after, and why

| Before | After | Why |
| --- | --- | --- |
| `<problematic styling or markup>` | `<compliant modern implementation>` | `<empirical reason, browser engine standard, or accessibility rule>` |

#### Concrete resolution

```<language>
// Code diff showing the exact fix in project idiom
```
````
