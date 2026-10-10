---
name: codebase-design
description: Use when designing module interfaces, evaluating abstraction depth, identifying code seams, or turning shallow pass-through wrappers into deep modules. Don't use for syntax styling, single-line bug fixes, or minor formatting changes.
---

# Codebase design

Design deep modules with substantial behavior behind small interfaces, placed at clean seams, and testable directly through those interfaces.

## Workflow

Follow these five steps in sequence.

### Step 1. Domain context and schema ingestion

Read the project context and verify actual data schemas before modifying or creating modules.

1. Inspect `AGENTS.md`, `CODEBASE.md`, or `CLAUDE.md` in the project root if present. Use the domain nouns, bounded contexts, and naming conventions defined there.
2. Audit database schemas and migration files:
   - For projects with existing databases, inspect migration directories (such as `database/migrations/`, `prisma/schema.prisma`, or `src/db/`).
   - Ground all entity attributes, foreign keys, and relations in verified schema files on disk. Never invent columns or assume database fields based on general model training.
   - For greenfield repositories without existing migrations, mark the status as greenfield initialization and draft the initial schema explicitly without unverified assumptions.
3. Infer domain boundaries and seams directly from verified migrations, route declarations, and existing data models.

Completion criterion. The agent names modules, methods, and attributes using verified project domain terms and disk-backed database schemas.

### Step 2. Design It Twice offer

Offer the user an exploratory multi-agent design pass before committing to a single interface.

Ask the user:

> "Do you want to run a Design It Twice pass with parallel sub-agents to explore 2 to 3 contrasting interface designs, or proceed directly with a single design?"

- If the user accepts, consult `references/design-it-twice.md` and dispatch sub-agents using `invoke_subagent`.
- If the user declines, proceed directly to Step 3.

Completion criterion. User preference recorded and the matching design branch initiated.

### Step 3. Deep module and seam formulation

Formulate the interface and identify module boundaries using deep module principles.

1. Apply the deletion test. Imagine deleting the module. If complexity vanishes, the module is a shallow pass-through wrapper and should be merged or deleted. If complexity reappears across multiple callers, the module earns its keep. Consult `references/codebase-health-and-hotspots.md` for git churn hotspot detection, deletion test execution, and architecture diagrams.
2. Minimize interface surface and reject line count metrics. Measure depth by leverage gained per unit of interface learned, never by lines of code ratio. Rewarding code volume encourages artificial bloat. Reduce public methods, simplify parameters, and design functions to return pure values rather than producing mutating side effects.
3. Classify dependencies across seams. Consult `references/deepening.md` to classify external touchpoints into in-process, local-substitutable, remote owned, or true external.
4. Enforce seam discipline. Follow the rule that one adapter represents a hypothetical seam, while two adapters represent a real seam. Do not introduce interface ports unless at least two concrete adapters exist.
5. Simplicity first and reuse hierarchy. Take the first option that fully works. Prioritize an existing codebase helper or pattern first, the standard library or platform feature second, an installed dependency third, and minimum new code last. Never add a dependency for a few lines. Never introduce abstractions, generics, or configurability layers for single-use code.
6. Shortcut discipline and essential boundaries. When taking an intentional implementation shortcut, mark it in code using `shortcut: <the limit>, <when to upgrade>`. Never cut trust boundary validation, data loss error handling, security invariants, or accessibility in the name of minimalism.
7. Align interface with test surface. Ensure callers and automated tests cross the same external seam. Do not leak internal test hooks into the public interface.

Completion criterion. A written interface specification defining inputs, outputs, error states, and concrete seam placement.

### Step 4. User review gate

Present the proposed interface design to the user before writing implementation code.

Cover these technical details:
- Module responsibility and what implementation logic sits behind it.
- Public interface signature and parameter types.
- Seam placement and adapter classifications.
- Automated testing strategy through the public interface.

Wait for explicit user approval. If the user requests adjustments, update the interface and repeat the review.

Completion criterion. Explicit user confirmation approving the interface design.

### Step 5. Transition to implementation planning

Invoke the `writing-plans` skill to generate a phased implementation plan.

Completion criterion. The writing-plans skill is invoked with the approved interface design.

## Core vocabulary

Use these architectural terms consistently:

| Term | Definition | Avoid substituting |
|---|---|---|
| Module | A discrete unit with an interface and an implementation | Component, service, unit |
| Interface | Everything a caller must know to use the module correctly, including types, invariants, ordering constraints, error modes, configuration, and performance traits | API, signature |
| Implementation | Internal code body hidden behind the interface | Adapter |
| Depth | Abstraction power at the interface, maximizing behavior while minimizing surface area | Lines of code ratio |
| Seam | The location where behavior can be altered without editing the caller | Boundary |
| Adapter | A concrete implementation that satisfies an interface at a seam | Infrastructure, driver |
| Multiplier | Total capability gained by callers per unit of interface learned | Abstraction power |
| Locality | Concentration of change, knowledge, and bugs in one place | Cohesion |

## Quick audit checklist

Run this check before finishing the skill execution:

| Check | Passing condition |
|---|---|
| Depth check | Module hides internal complexity behind a minimal parameter surface |
| Deletion test | Deleting module causes complexity to reappear across callers |
| Seam discipline | No interface port created for single-adapter dependencies |
| Test surface | Tests exercise the module through the same seam used by callers |
| Progressive disclosure | Deepening and multi-agent rules loaded from `references/` |
| Reuse hierarchy | Prioritizes existing helpers and platform features before new dependencies |
| Pipeline handoff | Transition offered to `writing-plans` upon design approval |
