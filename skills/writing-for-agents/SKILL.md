---
name: writing-for-agents
description: Use when drafting or editing agent instructions, AGENTS.md, CLAUDE.md, prompt runbooks, context pointers, or skill documentation.
---

# Writing for agents

Write predictable, high-demand documentation that AI agents consume, including skills, AGENTS.md, CLAUDE.md, and context pointers. Packaging differs across formats, but the governing mechanisms remain identical. Predictable agent execution requires clear information hierarchy, tight leading words, binary completion criteria, and strict anti-slop discipline.

When the document is a skill, read `references/skill-mechanics.md` for frontmatter rules, invocation modes, and router skills.

## Workflow

Follow these four steps in sequence:

### Step 1. Scope audit and budget allocation

Determine document category, context load versus cognitive load budget, and trigger branches.

- Classify the target into an always-loaded file (AGENTS.md, CLAUDE.md, system prompt) or an on-demand pointer (skill description, disclosed reference).
- Identify distinct trigger branches. Each branch represents a separate operational path that changes agent actions.
- Front-load trigger keywords so the model catches them early. Eliminate duplicate synonyms that consume tokens without changing behavior.
- Calculate token impact. Keep always-loaded pointers minimal and push extensive reference material behind pointers.

Completion criterion. A defined document target with explicit trigger branches and confirmed budget mode.

### Step 2. Information hierarchy and tiering

Classify content across three information tiers to protect model attention.

- Primary tier. In-file ordered execution steps in the main document. Keep steps sequential, operational, and focused on the immediate task.
- Secondary tier. In-file reference, constraints, and lookup tables consulted on demand. Group related rules under cohesive headings.
- Tertiary tier. Disclosed reference files in `references/` or standalone markdown documents. Move material exceeding 100 lines into external reference files reached by explicit pointers.
- Apply co-location. Keep concept definitions, associated rules, and edge cases together under one heading.

Completion criterion. An outline separating primary operational steps, secondary on-demand rules, and tertiary disclosed reference files.

### Step 3. Drafting with leading words and positive bounds

Draft the document using established pre-training priors and positive operational constraints.

- Write numbered steps ending in binary, checkable, and exhaustive completion criteria. Every step must allow the agent to verify whether the work is done without guessing.
- Recruit model priors with established leading words such as tracer, probe, baseline, invariant, audit, red, or tight instead of verbose explanations.
- State what the system does, not what it feels like. Replace abstract metaphors with concrete files, endpoints, types, and commands.
- Pair every negative constraint immediately with the required positive action. Avoid dangling prohibitions that pull forbidden patterns into context.

Completion criterion. A complete draft containing operational steps, each ending in a checkable binary completion criterion, with zero dangling negative bans.

### Step 4. Anti-slop audit and pruning

Audit the draft against anti-slop standards and prune redundant text.

- Strip promotional vocabulary, throat-clearing openings, and sycophantic closings.
- Remove em dashes, en dashes, and hyphens acting as dashes. Use periods or commas instead.
- Restrict colons to introducing lists, tables, or code blocks. Remove mid-sentence colons.
- Eliminate passive voice, vague adverbs, and rule-of-three cliches.
- Prune no-ops and duplicate instructions. Rely on environment truth such as directory layouts, package manifests, and CLI help output instead of copying static tables.

Completion criterion. The draft passes every check in the quick audit checklist with zero violations.

## Context pointers

A context pointer names external material and states when to load it. A skill description is a context pointer. A line in AGENTS.md that names a file is also a context pointer. The wording of the pointer determines whether the agent loads the file. If an agent misses a required document because the pointer is vague, sharpen the wording. Inline the material only if sharpening fails.

A pointer performs two jobs. It describes the material, and it lists the trigger branches that require reading it. Every word in an always-loaded pointer costs tokens on every turn. Prune pointers ruthlessly:

- Front-load the leading trigger word so it catches model attention early.
- Keep one trigger per branch. Synonyms that describe the same task waste tokens.
- Remove background details that the body file already explains.

## The two loads

Every document and pointer spends one of two budgets:

- Context load is the cost of always-loaded material on the context window. An AGENTS.md line, a skill description, and text sitting in context on every turn spend tokens whether they fire or not.
- Cognitive load is the cost on the human. The human must remember which documents exist and when to invoke each one. Spend human attention where human judgment matters, and automate or hide the rest.

Material reached only through a pointer avoids context load at the cost of the pointer itself. Material without any pointer relies entirely on cognitive load.

## Information hierarchy and progressive disclosure

A document contains two content types, steps and reference. Steps are ordered actions the agent performs. Reference includes rules, definitions, and facts consulted on demand. Some documents contain only steps. Other documents contain only reference. Many documents combine both. The core decision is where each piece sits on the information hierarchy:

1. In-file steps sit on the primary tier. They state what the agent does, in order.
2. In-file reference sits on the secondary tier, consulted on demand. A flat list of rules works well here.
3. Disclosed reference sits in a separate file, reached by a context pointer, and loaded only when needed. This includes sibling files in `references/` or external shared docs.

Pushing too little material down bloats the primary tier. Pushing too much hides details the agent needs. Balance the two tiers so the primary path stays clear.

Progressive disclosure moves material out of the main file and behind a pointer. This keeps the primary document legible. Use branches as the test. Inline the material that every branch needs, and move material behind a pointer if only certain branches need it. In-file reference that belongs in a separate file buries the main steps and makes execution erratic.

Co-location keeps related concepts together. Keep a concept definition, its rules, and its edge cases under one heading. Grouped instructions read like intentional technical documentation. Scattered rules confuse the model.

Sprawl happens when a document grows too long, even if every line is accurate. Attention thins across long files. When a document sprawls, push reference behind pointers and split tasks by branch or sequence.

## Steps and completion criteria

Every step must end on a clear completion criterion that tells the agent when the step is done. A strong criterion has two properties:

- **Clarity.** The agent must distinguish done from not done. Vague phrasing like "ensure understanding" leads to premature completion, where the agent rushes to finish before doing the actual work. Visible upcoming steps pull the model forward. A sharp bound resists that pull. Sharpen the boundary first. If the step remains fuzzy, move subsequent steps to a later prompt or a subagent.
- **Demand.** Demand sets the standard of work. Writing "account for every modified database model" forces thorough inspection, while "list the changes" does not. Demand drives legwork without needing a dozen micro-steps. High demand applies to flat reference rules just as strongly as it applies to ordered steps.

The strongest completion criteria are checkable, binary, and exhaustive.

## When to split

Splitting a document spends human cognitive load or adds a pointer. Split only when the separation earns its cost:

- Split by sequence when visible future steps tempt the agent to rush the current step. Hiding upcoming steps forces the agent to focus on the work right in front of it.
- Split by invocation when a skill should fire independently. Read `references/skill-mechanics.md` for details.

## Leading words and positive framing

A leading word is a compact concept already present in model pre-training. Words like tracer, probe, baseline, invariant, or audit recruit existing model priors without spending tokens on long explanations. Inventing custom terms forces you to spend tokens defining them, so prefer established terms first.

Leading words anchor behavior in two places. In the document body, the word focuses model attention on a specific standard of execution. In a pointer, a shared keyword links user prompts, documentation, and codebase conventions, triggering the skill reliably.

Look for opportunities to replace verbose explanations with leading words:

- Replace "fast, deterministic, low overhead" with "tight".
- Replace "a test that genuinely catches the issue" with "red".

Prefer positive instructions over negative bans. Steering by prohibition pulls the forbidden concept into context, making the model more likely to fixate on it. Instead of saying "do not write long narrative paragraphs", say "write one-line bullet points". If a prohibition is necessary as a hard guardrail, pair it immediately with the required positive action.

## Anti-slop discipline for agent docs

Agents mirror the tone, formatting, and density of the documents they consume. Writing bloated, vague, or decorative documentation causes agents to produce sloppy code, run-on prose, and unfocused tool calls. Apply strict anti-slop rules to every agent document:

- Cut puffery and promotional phrasing. Strip words like "comprehensive", "pivotal", "vital", "cutting-edge", or "seamless". State the concrete behavior directly.
- Strip conversational filler. Delete phrases like "in order to", "it is important to remember that", and "please note that". Start directly with the action verb.
- Ban em dashes, en dashes, and hyphens used as dashes. Do not trade dashes for parentheses. Use simple periods or commas.
- Avoid colons as mid-sentence connectors. Use a colon only to introduce an explicit list, a table, or a code block. Break run-on sentences into two complete sentences instead.
- Replace abstract jargon with concrete nouns. Change "API surface" to "endpoints", "substrate" to "base", "vector" to "method", and "paradigm" to "pattern". Name the actual file, command, or data structure.
- Say what it does, not how it feels. Replace vague claims like "keeps types close" with exact mechanisms like "generates TypeScript types directly from the database schema".
- Use active voice and short sentences. Name the actor and the action. Keep one operational instruction per sentence so the agent parses it without ambiguity.

## Pruning and maintenance

- Maintain a single source of truth. Keep each rule in one authoritative place so updates require editing only one file. Duplication wastes tokens and makes rules harder to maintain.
- Rely on the environment. Configuration files, directory layouts, package manifests, and command help outputs are sources of truth. Do not copy lookup tables that the agent can inspect dynamically using shell commands. Document only the conventions, gotchas, and architectural reasons that the environment does not state.
- Audit for relevance. Remove sentences that do not change how the agent acts. Stale documentation forms sediment that buries current instructions.
- Delete no-ops. If an instruction tells the model to do something it already does by default, delete the sentence. Test instructions against actual agent behavior rather than guessing.

## Quick audit checklist

Run this check before deploying any agent document:

| Check | Passing condition |
|---|---|
| Frontmatter | Contains kebab-case name and trigger-only description starting with "Use when" |
| Information hierarchy | Primary steps, secondary rules, and tertiary references cleanly separated |
| Completion criteria | Every operational step terminates on a checkable, binary completion criterion |
| Leading words | Recruits established pre-training priors and pairs positive actions to guardrails |
| Anti-slop | Zero banned vocabulary, zero em dashes, and colons appear only before lists, tables, or code |
| Pruning | Zero duplicate rules, zero no-ops, and relies on environment truth |
