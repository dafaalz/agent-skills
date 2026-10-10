---
name: technical-writing
description: Use when writing or reviewing human-facing documentation, RFCs, README files, PR descriptions, or technical guides. Don't use for drafting internal agent instructions, prompt runbooks, or skill documentation.
---

# Technical writing

Write clear technical documentation that an engineer understands on the first read. Combine the four Diátaxis documentation modes with ASD-STE100 Simplified Technical English (STE) precision standards.

Follow three universal rules across every layer:

- Cut every word that does no work. If the sentence survives without a word, remove it.
- Use the short everyday word. Write "use" instead of "utilize", "help" instead of "facilitate", and "run" instead of "execute".
- Preserve sentence quality above rigid rule compliance. If a rule makes a sentence sound artificial, rewrite the sentence or keep the plain phrasing.

Use codebase truth for naming. Always write the exact symbol, file path, flag, or command name instead of synonyms or descriptive approximations. Code identifiers, endpoints, flags, and types function as Technical Names. Apply STE rules strictly to the surrounding prose. Consult `references/asd-ste100-rules.md` for detailed writing rules and vocabulary tables.

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

### Step 2. Outline and structure calibration

Draft the document structure using Google Developer Style guidelines and ASD-STE100 paragraph bounds.

- Address the reader directly as "you" in the present tense.
- State who performs each action. Prefer active voice. Use passive voice only when the actor is unknown or irrelevant.
- Order procedural steps in strict chronological sequence.
- State preconditions before actions, such as "To delete the document, click Delete."
- Limit descriptive paragraphs to a maximum of six sentences. Begin each paragraph with an explicit topic sentence.
- Put common cases first and edge cases second.
- Make headings informative verb phrases for tasks or noun phrases for concepts. Concept titles must accept an implicit "About" in front.
- Cut pre-announcements that promise future features.
- In tutorials, describe the exact visible result for every action, including prompt changes, expected stdout, or log lines.

Completion criterion. An outline and initial draft written in second-person imperative style with descriptive paragraphs under seven sentences.

### Step 3. Precision bounds and syntactic disambiguation

Refine draft sentences using ASD-STE100 and Global English principles. Consult `references/asd-ste100-rules.md` for complete substitution tables.

- Limit procedural sentences to a maximum of 20 words.
- Limit descriptive sentences to a maximum of 25 words.
- Give exactly one instruction per sentence. Do not chain multiple actions with "and".
- Limit noun clusters to a maximum of three nouns. Unpack clusters containing four or more nouns with prepositions.
- Use only approved verb forms, which are simple present, simple past, simple future with "will", imperative, and past participles as adjectives.
- Prohibit progressive tenses ending in "-ing" and gerunds acting as nouns. Write "The worker processes jobs", never "The worker is processing jobs".
- Restrict modal auxiliary verbs to "can" for capability, "will" for future certainty, and "must" for mandatory requirements. Ban "should", "could", "would", and "may".
- Replace unapproved verbs and synonyms. Replace "check" or "verify" with "make sure" or "examine". Replace "ensure" with "make sure". Replace "terminate" with "stop".
- Place modifiers such as "only" and "not" immediately adjacent to the words they modify.
- Anchor every pronoun. Ensure every instance of "it", "this", and "they" points to one obvious noun. Repeat the noun when any ambiguity exists.
- Remove trailing "-ing" clauses. Replace them with independent clauses or distinct sentences.
- Prohibit slashes. Replace "and/or" with "a, b, or both".
- Never form plurals using parentheses like "file(s)". Write the singular or plural noun directly.
- Make text inside parentheses a complete grammatical unit or an independent sentence.
- Ensure every directory tree claim or count matches repository state at the landing commit, and provide the command that regenerates it.

Completion criterion. Sentences comply with word count bounds, contain zero progressive verbs, zero ambiguous modals, zero noun clusters exceeding three words, and zero unanchored pronouns.

### Step 4. Final verification pass

Run the completed draft against the review checklist and codebase truth.

- Confirm that every code symbol, file path, and command flag exists in the repository.
- Verify that code formatting matches project conventions.
- Audit the prose against the quick reference checklist below.

Completion criterion. The document passes every check on the review checklist with zero defects.

## Diátaxis modes

Pick one mode for each document:

- **Tutorial**. Teach through practical action. Guide the learner to build a working artifact from start to finish. Produce visible progress at every step. State the exact expected output after each command. Keep background explanations minimal and link out for deep context.
- **How-to guide**. Solve a specific real-world problem for an experienced reader. Focus entirely on steps to the goal. Omit basic concept explanations. Allow forks and decisions based on the user setup.
- **Reference**. Provide dry, systematic facts for lookup. Describe system capabilities, flags, configuration options, and error codes without opinion or persuasion. Mirror the underlying code architecture.
- **Explanation**. Deliver understanding and architectural context. Explore design decisions, trade-offs, constraints, and alternative approaches. Discuss opinions and technical rationale here.

## Style and syntax standards

### Audience and tone

- Speak directly to the reader as a knowledgeable peer.
- Ban condescending words such as "simply", "easy", "just", or "obviously".
- Strip promotional vocabulary and corporate buzzwords.
- Write links using descriptive destinations or page titles instead of phrases like "click here".

### Safety instructions and notices

Place safety notices immediately before the procedural step to which they apply:

- **WARNING**. Use strictly for hazards that cause irreversible data loss, production outages, or security breaches. Open with an imperative command or condition stating the hazard, then state consequence and prevention.
- **CAUTION**. Use for risks of service degradation, invalid runtime states, or build failures.
- **NOTE**. Use for non-hazardous technical clarifications and prerequisites. Notes must never contain commands or imperative verbs.

### Punctuation rules

- Prohibit semicolons. Split coordinate clauses into separate sentences.
- Restrict colons. Use colons strictly to introduce an explicit vertical list, a table, or a code block. Never use colons as connectors in running text.
- Restrict hyphens. Use hyphens only in approved compound words or compound Technical Names. Never use hyphens as dashes to connect thoughts.
- Prohibit slashes like "a/b" or "and/or". Write "a, b, or both".
- Keep articles like "the" and "a" before nouns to prevent dual interpretations.

### Scope specifics

- PR descriptions and commit messages must follow every layer except Diátaxis mode separation. Write concise briefings that reviewers can digest in under one minute. Link out to large terminal outputs or test logs instead of pasting them inline.
- Match repository conventions for code snippets and examples. Do not force arbitrary indentation rules that clash with project formatters.

## Worked example

### Draft before revision

> Configuration of the proto import ratchet budget script parameters is performed via budget.json. Note that it is important to remember that running with --write, which updates the committed budget to reflect the current count, should only be done when lowering it. If exceeded, CI fails.

### Revision after applying standards

> `budget.mjs` reads the committed budget from `budget.json` and counts files that import protos. If the count exceeds the budget, the CI test fails. Run `budget.mjs --write` only when you must lower the budget count.

## Quick reference checklist

Run this check before finishing any human-facing technical text:

| Check | Passing condition |
|---|---|
| Mode boundary | File adheres to exactly one Diátaxis mode with links for out-of-scope material |
| Procedural length | Instructional sentences stay under 21 words (maximum 20 words) |
| Descriptive length | Explanatory sentences stay under 26 words (maximum 25 words) |
| Paragraph bound | Descriptive paragraphs contain at most six sentences with topic sentence first |
| Noun clusters | Zero noun clusters containing more than three words |
| Verb tenses | Only simple present, simple past, simple future with will, and imperative, with zero progressive -ing verbs |
| Modal verbs | Modals restricted to can, will, and must, with zero instances of should or may |
| Imperative mood | Every procedural step is an active command with preconditions stated first |
| Single action | Exactly one instruction per procedural sentence without compound and chains |
| Safety tiers | WARNING, CAUTION, and NOTE follow strict severity definitions and precede actions |
| Modifier position | Words like "only" and "not" sit immediately adjacent to their target |
| Pronoun anchor | Every pronoun resolves to a single unambiguous referent without guesswork |
| Codebase truth | All file paths, symbols, commands, options, and counts exist and verify against repo state |
| Punctuation | Zero semicolons, zero slashes, zero dashes, and colons appear only before lists, tables, or code |
| Tone discipline | Zero condescending adverbs such as "simply" or "easy", and zero conversational padding |
