---
name: brainstorming
description: Use when scoping new features, exploring architectural requirements, planning refactors, stress-testing design decisions, or designing greenfield components before writing implementation plans or code.
---

# Brainstorming ideas into designs

Turn ideas into validated designs before writing code or plans.

Check the project context first. For architecture and refactoring work, research external standards, run a codebase gap analysis, and compare trade-offs. For new features, ask clarifying questions one at a time and present the design in stages. Once the user approves the approach, write the design specification and hand off to implementation planning.

<HARD-GATE>
Present the design and secure explicit user approval before writing code, scaffolding projects, or invoking implementation skills. Do not take implementation actions before user approval. This rule applies to every task, regardless of scope.
</HARD-GATE>

## Workflow selection

Identify whether the task involves existing architecture or greenfield capability, then follow the matching branch:

- Architecture or refactor. Follow Branch 1.
- New feature or greenfield. Follow Branch 2.

Both branches terminate by invoking writing-plans. Never invoke implementation skills directly from brainstorming.

## Branch 1. Architecture evaluation and refactoring

Use this branch when modernizing legacy code, redesigning module boundaries, evaluating framework compliance, or restructuring existing components.

### Step 1. External standards research

Survey authoritative standards before proposing changes to existing architecture.

- Delegate deep research to a subagent when exploring multi-source topics. This keeps the orchestrator context window clean.
- Require 5 to 10 credible sources. Acceptable sources include official framework documentation, core contributor publications, official RFCs, and recognized industry engineering guides.
- Direct the subagent to return:
  1. Complete citations with source titles and exact URLs.
  2. Concrete architectural rules organized by layer or subsystem.
  3. Anti-patterns and hazards identified by the sources.
  4. Dense output without filler phrases or conversational padding.

Completion criterion. A structured synthesis containing at least 5 verified source citations and an actionable list of technical rules for each affected layer.

### Step 2. Codebase gap analysis

Audit the active codebase against the researched standards using a structured gap analysis.

Inspect existing files, models, controllers, configurations, and test suites. Classify findings into three categories:

1. Sound patterns. Components that follow standards. Note why they remain untouched to prevent regressions.
2. Flaws to remove. Bugs, anti-patterns, leaky abstractions, query builder state pollution, and tight coupling.
3. Additions to build. Missing abstractions, typed entities, endpoints, route handlers, or service layers needed to bridge the gap.

Provide concrete file paths, class names, and line references for every finding.

Completion criterion. A three-part inventory mapping specific codebase locations to each category, with zero unverified assumptions about the current code.

### Step 3. Tradeoff analysis and approach proposal

Formulate 2 to 3 distinct implementation approaches based on the gap analysis.

- Define contrasting strategies, such as an in-place pragmatic refactor versus a clean-slate modular rewrite.
- Evaluate each option across five criteria:
  1. Scope and disruption to active systems.
  2. Backward compatibility with views, frontend scripts, and external callers.
  3. Testability and verification effort.
  4. Implementation complexity and delivery risk.
  5. Long-term maintainability.
- Evaluate data scaling and state lifecycle. Consult `references/architecture-scalability.md` when designing list endpoints, table pagination, or interactive state persistence.
- Include the status quo as a baseline comparison.
- Lead with your recommended option and state the technical reasons for the choice.
- Ask the user to choose an approach before drafting detailed component designs.

Completion criterion. The user selects one approach or provides adjustments.

## Branch 2. Feature and greenfield design

Use this branch when building new capabilities, interfaces, utilities, or workflows from scratch.

### Step 1. Scope assessment and project context

Inspect existing files, docs, and recent commits to understand conventions and dependencies.

- Assess overall scope immediately. If the request spans multiple independent subsystems, flag it and decompose into sub-projects before discussing details.
- Brainstorm the first sub-project through the standard design flow. Each sub-project receives its own design, plan, and implementation cycle.

Completion criterion. A bounded scope confirmed as suitable for a single implementation plan.

### Step 2. Clarifying questions and grilling

Clarify requirements through focused dialogue and verify assumptions before designing.

- Find facts autonomously. Never ask the user for information discoverable via files, configs, git logs, or documentation.
- For simple features, ask questions one at a time with concrete options and a recommended answer.
- Surface multiple interpretations. If a user request allows two or more distinct architectural interpretations, present them explicitly with concrete tradeoffs instead of picking one silently. If requirements contain contradictory constraints or unclear logic, stop immediately and name what is confusing before designing.
- For complex requirements, ambiguous scopes, or explicit stress-testing requests, follow `references/grilling.md`. Map choices to a design tree, ask frontier questions in structured rounds, and resolve every dependency until the frontier is empty.
- Focus on concrete constraints, including inputs, outputs, error handling, storage, and user roles.

Completion criterion. All ambiguities and decision branches resolved through explicit user confirmation, leaving zero unverified assumptions.

### Step 3. Approach exploration

Propose 2 to 3 approaches with tradeoffs, lead with a recommendation, and obtain user confirmation before writing detailed specifications. Evaluate data scaling and reload persistence against `references/architecture-scalability.md`.
- Protect Single Responsibility Principle and modular boundaries: If a user proposal merges unrelated domains or causes lifecycle regressions, run a targeted web search via `search_web` to verify industry conventions, present a grounded counter-argument citing the reference, and propose a clean decoupled alternative.

Completion criterion. The user selects a preferred approach.

## Design presentation and documentation

### Step 1. Present the design

Present the design in sections scaled to complexity. Cover:
- System boundaries and responsibilities.
- Data structures, entities, and database schemas.
- Interfaces, endpoints, and HTTP verbs.
- Error handling and edge cases.
- Automated testing strategy.

Ask the user after each major section whether the technical direction matches expectations.

Completion criterion. The user explicitly confirms that the design direction matches expectations.

### Step 2. Write the design document

Save the design specification to `docs/superpowers/specs/YYYY-MM-DD-<topic>-design.md` or the user-specified path.

Follow the Architecture Decision Record structure:
- Title. Short descriptive title.
- Status. Proposed, Accepted, or Superseded.
- Context. Problem statement, constraints, and findings from research and gap analysis.
- Decision. Selected architecture, component boundaries, and concrete file changes.
- Alternatives considered. Rejected options and reasons for rejecting them.
- Consequences. Direct outcomes and accepted tradeoffs.
- Verification plan. Automated tests and manual checks.

Completion criterion. The spec file is written to disk matching the ADR structure.

### Step 3. Spec self-review

Inspect the written document before presenting it to the user. For automated checking, dispatch a subagent using the template in `references/spec-document-reviewer-prompt.md`, or run these checks manually:

1. Placeholder scan. Search for and remove any TODO, TBD, or vague guidelines.
2. Internal consistency. Confirm that components, route definitions, and data types match across all sections.
3. Scope check. Confirm the design remains focused enough for one implementation plan.
4. Ambiguity check. Remove any requirement that permits multiple contradictory interpretations.

Fix all findings directly in the file.

Completion criterion. The spec passes all four checks with zero placeholders or ambiguities remaining.

### Step 4. User review gate

Prompt the user to review the written specification:

> "The design specification is written to `<path>`. Please review it and confirm if you want any adjustments before we generate the implementation plan."

Wait for explicit user approval. If the user requests adjustments, update the document and repeat the check.

Completion criterion. The user explicitly approves the written specification.

### Step 5. Transition to implementation planning

Invoke the `writing-plans` skill to generate the detailed, phased implementation plan. Do not invoke coding or execution skills until the plan is written and approved.

Completion criterion. The writing-plans skill is invoked.

## Visual companion

A browser-based companion for showing mockups, diagrams, and visual options during brainstorming. Available as a tool, not a mode. Accepting the companion means it is available for questions that benefit from visual treatment. It does not mean every question goes through the browser.

### Offering the companion

When upcoming questions involve visual layouts, mockups, or diagrams, offer the companion once:

> "Some of what we are working on might be easier to explain if I can show it to you in a web browser. I can put together mockups, diagrams, comparisons, and other visuals as we go. This feature is still new and can be token-intensive. Want to try it? Requires opening a local URL."

This offer must be its own message without any other content. Wait for the user response. If declined, proceed with text-only brainstorming.

### Per-question decision

Even after the user accepts, decide for each question whether to use the browser or the terminal:
- Use the browser for visual artifacts such as mockups, wireframes, layout comparisons, and visual architecture diagrams.
- Use the terminal for text artifacts such as requirements questions, conceptual choices, tradeoff lists, and scope decisions.

When the user accepts the browser companion, read `references/visual-companion.md` for server management and screen templates.

## Quick audit checklist

Run this check before transitioning to implementation planning:

| Check | Passing condition |
|---|---|
| Hard gate | Design approved by user before invoking writing-plans or writing code |
| Gap analysis | Codebase mapped to sound patterns, flaws to remove, and additions to build |
| Clarifying questions | Questions asked with concrete options, facts researched autonomously, zero unverified assumptions |
| Spec document | ADR spec written to `docs/superpowers/specs/` with zero placeholders |
| User sign-off | Explicit user confirmation received on chosen approach and final spec |
