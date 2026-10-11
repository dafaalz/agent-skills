---
name: brainstorming
description: Use when scoping new features, exploring architectural requirements, planning refactors, stress-testing design decisions, or designing greenfield components before writing implementation plans or code. Don't use for direct implementation, writing code, or generating commit messages.
---

# Brainstorming ideas into designs

Turn ideas into designs you can build before you write code or plans.

Read project files first. If you change existing code, read official standards, check code against those standards, and compare options. If you build something new, ask one question at a time and show the design in parts. After the user picks an approach, write the spec and call implementation planning.

<HARD-GATE>
Show the design and get explicit user approval before you write code, write project templates, or call implementation skills. Do not write code before the user says yes. This rule covers every task, no matter how small.
</HARD-GATE>

## Workflow selection

Decide if the task changes existing code or adds new code, then run the matching branch:

- Change existing code. Run Branch 1.
- Add new code. Run Branch 2.

Both branches end when you call writing-plans. Never call implementation skills directly from brainstorming.

## Branch 1. Check existing code and plan changes

Run this branch when you update old code, move module boundaries, check if code follows framework rules, or reshape existing components.

### Step 1. Read external standards

Read official docs before you suggest changes to existing code.

- When the topic spans many sources, ask a subagent to read them. This saves context in the main session.
- Ask for 3 to 5 trusted sources. Use official framework docs, core contributor posts, official RFCs, and trusted engineering guides.
- Tell the subagent to return:
  1. Full citations with source titles and exact URLs.
  2. Rules you can apply, grouped by layer or subsystem.
  3. Mistakes and risks the sources name.
  4. Short output with no filler or small talk.

Completion criterion. You list at least 3 checked sources and the rules you will apply for each affected layer.

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

Completion criterion. The user picks one option or asks for changes.

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

Completion criterion. The user confirms every open branch and zero guesses remain.

### Step 3. Explore approaches

Write 2 to 3 approaches with tradeoffs, put your pick first, and get user confirmation before you write the full spec. Check data growth and reload saves against `references/architecture-scalability.md`.
- Keep domains apart. If a user pitch mixes unrelated domains or breaks lifecycle behavior, search the web with `search_web` to check industry practice, show a counter-argument with the source, and suggest a split alternative.
- Show opposite visual directions for open UI tasks. When a frontend request lacks visual direction, do not ask open taste questions. Show three distinct directions picked from opposite schools, such as Information Architecture (rational, data-dense, e.g. Pentagram or Vignelli), Editorial Minimalist (whitespace, refined type, e.g. Dieter Rams or MUJI), Modern Tool (hairline details, dark mode, single accent, e.g. Linear or Raycast), Motion Experimental (generative, kinetic, e.g. Active Theory), Brutalist (raw, high contrast, e.g. Are.na), or Warm Humanist (approachable, organic, e.g. Stripe Press). Never show three options from the same school.

Completion criterion. The user picks one approach.

## Design presentation and documentation

### Step 1. Show the design

Show the design in sections sized to complexity. Cover:
- System boundaries and who owns what.
- Data shapes, entities, and database schemas.
- Interfaces, endpoints, and HTTP verbs.
- Error handling and edge cases.
- How you test it.

Ask the user after each section if the direction matches.

Completion criterion. The user confirms the direction matches.

### Step 2. Write the design doc

Write the Architecture Decision Record (ADR) to `docs/YYYY-MM-DD-<topic>-design.md` or the path the user names. Read `references/domain-modeling.md` for entity naming and ADR filters.

Write the record with these fields:
- **Title.** Short name for the change.
- **Status.** Proposed, Accepted, or Superseded.
- **Context.** Problem, limits, and what you learned from research and code checks.
- **Decision.** Chosen structure, component bounds, and files you will change.
- **Alternatives considered.** Options you dropped and why you dropped them.
- **Consequences.** Direct results and tradeoffs you accept.
- **Verification plan.** Automated tests and manual checks you will run.

Completion criterion. You write the ADR file to disk with all fields filled.

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

Completion criterion. The user approves the written spec.

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
| Hard gate | User approves design before you call writing-plans or write code |
| Code check | You list good code, bad code to fix, and missing code to write with file paths |
| Questions | You ask with fixed options, you read facts by yourself, zero guesses remain |
| Spec doc | You write ADR spec to `docs/YYYY-MM-DD-<topic>-design.md` with zero placeholders |
| User sign-off | User confirms pick and final spec |
