---
name: brainstorming
description: Use when scoping new features, exploring architectural requirements, planning refactors, stress-testing design decisions, or designing greenfield components before writing implementation plans or code. Don't use for direct implementation or writing code (use executing-plans), or generating commit messages (use conventional-commit).
---

# Brainstorming ideas into designs

Turn ideas into designs you can build before you write code or plans.

Read project files first. If you change existing code, read official standards, check code against those standards, and compare options. If you build something new, ask one question at a time and show the design in parts. After the user picks an approach, write the spec and call implementation planning.

<HARD-GATE>
Write-Target Boundary. Do not modify files in tracked production directories (`src/`, `app/`, `packages/`, `database/`, `tests/`) or call implementation skills before the user approves the design specification. Ephemeral sandbox exploration is permitted exclusively inside `.agents/scratch/prototypes/<variant-id>/` when delegating visual or state spikes to the `prototype` skill.
</HARD-GATE>

## Workflow selection

Decide if the task changes existing code or adds new code, then run the matching branch:

- Change existing code. Run Branch 1.
- Add new code. Run Branch 2.

Both branches feed into Design presentation and documentation before calling writing-plans; never call implementation skills directly from brainstorming.

## Branch 1. Check existing code and plan changes

Run this branch when you update old code, move module boundaries, check if code follows framework rules, or reshape existing components.

### Step 1. Read external standards

Read official docs before you suggest changes to existing code.

- When the topic crosses domains or needs more sources than a repo read can reach, call the `recursive-research` skill in Targeted mode. Pass the topic, the affected layers, and the request for a brief that feeds a design spec. It writes evidence to `.agents/research/<slug>/`, tiers every source, and returns the five handoff fields.
- When the topic spans a few official sources, ask a subagent to read them. This saves context in the main session.
- Ask for 3 to 5 trusted sources, and tier each one against the source tiering table in the `recursive-research` skill. Use official framework docs, core contributor posts, official RFCs, and trusted engineering guides.
- From either path, require:
  1. Full citations with source titles and exact URLs.
  2. Rules you can apply, grouped by layer or subsystem.
  3. Mistakes and risks the sources name.
  4. The open gaps from `recursive-research`, with the risk each one carries.
  5. Short output with no filler or small talk.

Completion criterion. You list at least 3 checked sources or a brief at `.agents/research/<slug>/`, plus the rules you will apply for each affected layer.

### Step 2. Check code against standards

Read files, models, controllers, configs, and tests. Check what the code does against the standards you read.

Read the code, then sort what you find into three lists:

1. Good code. Code that follows the standards. Write why it stays as is so you avoid breaking it.
2. Bad code to fix. Bugs, anti-patterns, leaky abstractions, query builder state pollution, and tight coupling.
3. Missing code to write. Missing abstractions, typed entities, endpoints, route handlers, or service layers you still need to write.

List file path, class name, and line number for every item.

Completion criterion. You list file paths for each of the three groups and you check every claim in code with zero guesses.

### Step 3. Compare options and suggest one

Write 2 to 3 different ways to fix the code.

- Describe opposite options, such as fix code where it sits versus rewrite it in new modules.
- Check each option on five points:
  1. How much running code you touch.
  2. What breaks for views, frontend scripts, and outside callers.
  3. How you test it.
  4. How hard it is to build and what can fail.
  5. How hard it is to change later.
- Check data growth and state lifecycle. Read `references/architecture-scalability.md` when you design list endpoints, table pagination, or interactive state saves.
- Keep doing nothing as one option.
- Put your pick first and say why it wins in technical terms.
- Ask the user to pick one option before you write detailed designs.

Completion criterion. The user explicitly confirms one chosen option.

## Branch 2. Design new features

Run this branch when you build new capabilities, interfaces, utilities, or workflows from scratch.

### Step 1. Bound the scope

Read files, docs, and recent commits to learn conventions and dependencies.

- Check scope first. If the request spans separate subsystems that you can build alone, flag it and split it into sub-projects before you discuss details.
- Run the first sub-project through the full design flow. Each sub-project gets its own design, plan, and build cycle.

Completion criterion. You bound the scope so it fits one implementation plan.

### Step 2. Ask questions and grill

Clear up requirements through direct talk and check assumptions before you design.

- Find facts by yourself. Never ask the user for facts you can read in files, configs, git logs, or docs.
- For simple features, ask one question at a time with fixed options and a recommended answer.
- Name separate readings. If a request allows two or more readings, show them with tradeoffs instead of picking one in silence. If requirements clash or logic stays unclear, stop and name what confuses you before you design.
- For tangled requirements, unclear scope, or explicit stress-test requests, follow `references/grilling.md`. Map picks to a design tree, ask frontier questions in rounds, and close every dependency until the frontier empties.
- Ask about fixed limits, including inputs, outputs, error handling, storage, and user roles.

Completion criterion. The user confirms every open branch in the design tree or requirements checklist with zero open questions remaining.

### Step 3. Explore approaches and prototype spikes

Write 2 to 3 approaches with tradeoffs, put your pick first, and get user confirmation before you write the full spec. Check data growth and reload saves against `references/architecture-scalability.md`.
- Keep domains apart. If a user pitch mixes unrelated domains or breaks lifecycle behavior, call `recursive-research` in Targeted mode to check industry practice, or search the web with `search_web` for a single check, then show a counter-argument with the source and suggest a split alternative.
- Show opposite visual directions for open UI tasks. When a frontend request lacks visual direction, do not ask open taste questions. Show three distinct directions picked from opposite schools, such as Information Architecture, Editorial Minimalist, Modern Tool, Motion Experimental, Brutalist, or Warm Humanist.
- Run spikes via prototype. If visual density or state ergonomics requires live verification before locking architecture, emit `.agents/state/spike-brief.md` and invoke the `prototype` skill. Require the selected variant locked in `.agents/scratch/prototypes/<variant-id>/PROTOTYPE_LOCK.md` before proceeding.

Completion criterion. The user picks one approach or confirms a locked prototype variant.

## Design presentation and documentation

### Step 1. Show the design

Show the design in sections sized to complexity. Cover:
- System boundaries and who owns what.
- Data shapes, entities, and database schemas.
- Interfaces, endpoints, and HTTP verbs.
- Error handling and edge cases.
- How you test it.

Ask the user after each section if the direction matches.

Completion criterion. The user confirms the direction matches for each presented section covering boundaries, data schemas, endpoints, and test checklist with zero open objections.

### Step 2. Write the design spec

Evaluate the change against three Architecture Decision Record filters:
1. Hard to reverse.
2. Surprising without context.
3. Real trade-offs across components.

If all three filters evaluate to false, author a compact Component Spec stating inputs, outputs, UI tokens, and verification commands. If any filter evaluates to true, write an Architecture Decision Record (ADR) to `docs/specs/YYYY-MM-DD-<topic>-adr.md`. Read `references/domain-modeling.md` for entity naming.

Prepend a standardized hand-off header to the spec:
```yaml
---
artifact_type: adr
lifecycle_state: spec-approved
source_skill: brainstorming
next_skill: writing-plans
selected_option: <option-slug>
in_scope_paths: ["<path-1>"]
verification_entrypoints: ["<test-command>"]
---
```

Write the record with these fields:
- **Title.** Short name for the change.
- **Status.** Proposed, Accepted, or Superseded.
- **Context.** Problem, limits, and what you learned from research and code checks.
- **Decision.** Chosen structure, component bounds, and files you will change.
- **Alternatives considered.** Options you dropped and why you dropped them.
- **Consequences.** Direct results and tradeoffs you accept.
- **Verification plan.** Automated tests and manual checks you will run.

Completion criterion. You write the spec file to disk with the hand-off header and required fields filled.

### Step 3. Self-review the spec

Read the file before you show it to the user. To check automatically, call a subagent with the template in `references/spec-document-reviewer-prompt.md`, or run these checks by hand:

1. Placeholder scan. Search for TODO, TBD, or vague filler and delete them.
2. Internal consistency. Check that components, routes, and data types match in all sections.
3. Scope check. Check that the design still fits one implementation plan.
4. Ambiguity check. Delete any requirement that allows opposite readings.

Fix every issue in the file.

Completion criterion. The spec passes all four checks with zero placeholders left.

### Step 4. User review gate

Ask the user to read the written spec:

> "The design specification is written to `<path>`. Please review it and confirm if you want any adjustments before we generate the implementation plan."

Wait for explicit user approval. If the user asks for changes, update the file and run the check again.

Completion criterion. The user approves the written spec file at `docs/specs/` with zero open change requests.

### Step 5. Move to implementation planning

Call the `writing-plans` skill to write the phased implementation plan. Do not call coding skills until the user approves the plan.

Completion criterion. You call the writing-plans skill.

## Visual companion

A browser tool that shows mockups, diagrams, and visual options during brainstorming. It stays a tool, not a mode. When the user accepts it, you can use it for questions that need visuals. You still ask text questions in the terminal.

### Offering the companion

When next questions cover visual layouts, mockups, or diagrams, offer the companion once:

> "Some of what we are working on might be easier to explain if I can show it to you in a web browser. I can put together mockups, diagrams, comparisons, and other visuals as we go. This feature is still new and can be token-intensive. Want to try it? Requires opening a local URL."

Send this offer as its own message with no other text. Wait for the answer. If the user says no, keep brainstorming in text.

### Per-question decision

After the user says yes, pick the channel for each question:
- Use the browser for mockups, wireframes, layout comparisons, and visual architecture diagrams.
- Use the terminal for requirements questions, word-only picks, tradeoff lists, and scope picks.

When the user accepts the browser companion, read `references/visual-companion.md` for server steps and screen templates.

## Boundary isolation

Keep brainstorming rules to requirements talk, design files, and user dialogue. Keep production code syntax, database migration types, API parameters, and shell commands neutral, standard, and untouched by style picks.

## Quick audit checklist

Check this list before you call implementation planning:

| Check | Passing condition |
|---|---|
| Hard gate | Production write boundary enforced and user approves design before writing code |
| Code check | You list good code, bad code to fix, and missing code to write with file paths |
| Questions | You ask with fixed options, you read facts by yourself, zero guesses remain |
| Spec doc | You write spec with hand-off header to `docs/specs/` with zero placeholders |
| User sign-off | User confirms pick and final spec |
