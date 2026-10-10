---
name: technical-writing
description: Use when writing or reviewing human-facing documentation, RFCs, README files, PR descriptions, or technical guides. Don't use for drafting internal agent instructions, prompt runbooks, or skill documentation.
---

# Technical writing

Write clear technical documentation that an engineer understands on the first read. Apply four layers in sequence, from document structure down to individual words.

Follow three universal rules across every layer:

- Cut every word that does no work. If the sentence survives without a word, remove it.
- Use the short everyday word. Write "use" instead of "utilize", "help" instead of "facilitate", and "do" instead of "perform".
- Preserve sentence quality above rigid rule compliance. If a rule makes a sentence sound artificial, rewrite the sentence or keep the plain phrasing.

Use codebase truth for naming. Always write the exact symbol, file path, flag, or command name instead of synonyms or descriptive approximations. Avoid invented metaphors. Write terms developers say aloud, such as "move" or "delete".

## Workflow

Follow these four steps in sequence:

### Step 1. Mode selection

Classify the document into exactly one Diátaxis mode before writing. Answer two questions regarding whether the document serves action or understanding, and whether it addresses learning or work:

- Action and learning yields a tutorial.
- Action and work yields a how-to guide.
- Understanding and work yields reference.
- Understanding and learning yields an explanation.

Never blend multiple modes in a single document. Link out to related modes instead of nesting them.

Completion criterion. The document maps to one confirmed Diátaxis mode with explicit external links for out-of-scope material.

### Step 2. Outline and cadence calibration

Draft the document structure using Google Developer Style guidelines while planning sentence rhythm.

- Address the reader directly as "you" in the present tense.
- State who performs each action. Prefer active voice. Use passive voice only when the actor is unknown or irrelevant.
- Write procedures as commands. State preconditions before actions, such as "To delete the document, click Delete."
- Vary sentence length intentionally. Pair short punchy statements that land core facts with longer sentences that outline preconditions or technical consequences.
- Put common cases first and edge cases second.
- Make headings informative verb phrases for tasks or noun phrases for concepts. Concept titles must accept an implicit "About" in front.
- Cut pre-announcements that promise future features.
- In tutorials, describe the exact visible result for every action, including prompt changes, expected stdout, or log lines.

Completion criterion. An outline and initial draft written in second-person imperative style with varied sentence cadence.

### Step 3. Precision bounds and syntactic disambiguation

Refine draft sentences using Simplified Technical English (STE) and Global English principles.

- Restrict each sentence to one instruction or one technical thought. Split sentences exceeding 25 words.
- Place modifiers such as "only" and "not" immediately adjacent to the words they modify.
- Unpack dense noun strings. Change "proto import budget check script" to "script that checks the proto import budget".
- Anchor every pronoun. Ensure every instance of "it", "this", and "they" points to one obvious noun. Repeat the noun when any ambiguity exists.
- Retain structural words like "that" when they eliminate misreadings.
- Remove trailing "-ing" clauses. Replace them with independent clauses or distinct sentences.
- Avoid slashes. Replace "and/or" with "a, b, or both".
- Never form plurals using parentheses like "file(s)". Write the singular or plural noun directly.
- Make text inside parentheses a complete grammatical unit or an independent sentence.
- Ensure every directory tree claim or count matches repository state at the landing commit, and provide the command that regenerates it.

Completion criterion. The text parses in exactly one way, with zero dangling modifiers and zero unanchored pronouns.

### Step 4. Final verification pass

Run the completed draft against the review checklist and codebase truth.

- Confirm that every code symbol, file path, and command flag exists in the repository.
- Verify that code formatting matches project conventions.
- Audit the prose against the review checklist below.

Completion criterion. The document passes every check on the review checklist with zero defects.

## Diátaxis modes

Pick one mode for each document:

- **Tutorial**. Teach through practical action. Guide the learner to build a working artifact from start to finish. Produce visible progress at every step. State the exact expected output after each command. Keep background explanations minimal and link out for deep context.
- **How-to guide**. Solve a specific real-world problem for an experienced reader. Focus entirely on steps to the goal. Omit basic concept explanations. Allow forks and decisions based on the user's setup.
- **Reference**. Provide dry, systematic facts for lookup. Describe system capabilities, flags, configuration options, and error codes without opinion or persuasion. Mirror the underlying code architecture.
- **Explanation**. Deliver understanding and architectural context. Explore design decisions, trade-offs, constraints, and alternative approaches. Discuss opinions and technical rationale here.

## Style and syntax standards

### Audience and tone

- Speak directly to the reader as a knowledgeable peer.
- Ban condescending words such as "simply", "easy", "just", or "obviously".
- Strip promotional vocabulary and corporate buzzwords.
- Write links using descriptive destinations or page titles instead of phrases like "click here".

### Syntactic rules

- Keep articles like "the" and "a" before nouns to prevent dual interpretations.
- Write procedures as commands. Use "Run the test" instead of "The test should be run".
- Repeat articles across lists when items represent distinct things, such as "the client and the server".
- Connect paired thoughts with explicit correlatives, such as "both...and" or "either...or".
- Use periods instead of semicolons. Break long coordinate clauses into separate sentences.
- Never form plurals with parentheses like "file(s)". Write the singular or plural noun directly.
- Avoid slashes like "a/b" or "and/or". Write "a, b, or both".
- Make text inside parentheses a complete grammatical unit or an independent sentence.

### Scope specifics

- PR descriptions and commit messages must follow every layer except Diátaxis mode separation. Write concise briefings that reviewers can digest in under one minute. Link out to large terminal outputs or test logs instead of pasting them inline.
- Match repository conventions for code snippets and examples. Do not force arbitrary indentation rules that clash with project formatters.

## Worked example

### Draft before revision

> Configuration of the proto import ratchet budget script parameters is performed via budget.json. Note that it is important to remember that running with --write, which updates the committed budget to reflect the current count, should only be done when lowering it. If exceeded, CI fails.

### Revision after applying standards

> `budget.mjs` reads the committed budget from `budget.json` and counts the files that import protos. If the count exceeds the budget, CI fails. Run `budget.mjs --write` only to lower the budget.

## Quick reference checklist

Run this check before finishing any human-facing technical text:

| Check | Passing condition |
|---|---|
| Mode boundary | File adheres to exactly one Diátaxis mode with links for out-of-scope material |
| Imperative mood | Every procedural step is an active command with preconditions stated first |
| Cognitive load | Sentences contain one thought or one instruction, staying under 25 words |
| Modifier position | Words like "only" and "not" sit immediately adjacent to their target |
| Pronoun anchor | Every pronoun resolves to a single unambiguous referent without guesswork |
| Codebase truth | All file paths, symbols, commands, options, and counts exist and verify against repo state |
| Structural syntax | Zero slashes like "and/or", zero parenthetical plurals like "(s)", and parentheses contain complete units |
| Tone discipline | Zero condescending adverbs such as "simply" or "easy", and zero conversational padding |
| Punctuation | Zero em dashes, zero en dashes, and colons appear only before lists, tables, or code |
