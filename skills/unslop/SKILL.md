---
name: unslop
description: Use when drafting prose, reviewing text for AI patterns, editing documentation, rewriting generic AI output, or cutting LLM writing habits.
---

# Unslop

Audit prose and documentation to strip AI patterns, eliminate filler, and restore human cadence.

## Workflow

Follow these four steps in sequence:

### Step 1. Pattern scan

Inspect text against the reference rules below. Catalog every occurrence across four categories:
1. Banned vocabulary and abstract metaphors.
2. Structural puffery, hollow transitions, and formulaic openings or endings.
3. Syntactic tells, passive voice, and weak adverbs.
4. Punctuation defects, including em dashes, mid-sentence colons, and decorative styling.

Completion criterion. A written catalog listing each matched pattern, line location, and target category.

### Step 2. Concrete rewrite

Rewrite flagged sections using plain vocabulary, active voice, and verifiable facts.
- Replace vague feelings with concrete measurements, numbers, or system mechanisms.
- Drop empty filler clauses instead of rewording them.
- Pair every removed prohibition with a direct positive action.
- Preserve all underlying technical facts and intent.

Completion criterion. Rewritten text containing zero cataloged patterns while retaining all factual points.

### Step 3. Cadence and tone calibration

Adjust sentence rhythm and voice according to document scope:
- For narrative prose, vary sentence lengths across paragraphs, state clear stances, and write from a defined perspective.
- For technical documentation and agent runbooks, state exact paths, commands, and preconditions without decorative prose.

Completion criterion. No three consecutive sentences share the same length or clause pattern.

### Step 4. Final verification pass

Audit the draft against the quick audit checklist at the bottom of this document.

Completion criterion. Text passes every check in the quick audit checklist with zero exceptions.

## Boundary isolation

Apply these rules strictly to human-facing prose, documentation, walkthroughs, and chat explanations.

Keep code syntax, database schemas, API parameters, variable names, terminal commands, and git commits neutral and idiomatic. Never inject voice quirks, slang, or arbitrary renames into functional code.

## Core rules

### Content and framing

- **Cut puffery.** Replace promotional fluff with verifiable events, measurements, or actions. Write "built in 2024" instead of "a testament to modern innovation".
- **Name specific sources.** Attribute facts to an exact person, repository, document, or dataset. If no verifiable source exists, delete the claim.
- **Strip superficial participial clauses.** Remove trailing "-ing" clauses like "highlighting the importance" or "ensuring seamless integration". Write them as distinct sentences or omit them entirely.
- **Replace formulaic contrasts.** Delete phrases like "not just X, but Y" or "despite challenges, X continues to thrive". State the actual technical state directly.
- **Strip formulaic openings and closings.** Delete throat-clearing intros like "In today's fast-paced world" or "Whether you are a beginner or an expert". Delete sycophantic sign-offs like "The future looks bright". Open with the core fact and close with the immediate next step.
- **Break rule-of-three cliches.** Eliminate triad groupings like "fast, scalable, and robust". State the single primary technical property that matters.

### Plain vocabulary and substitutions

Use plain words and direct verbs. Consult this substitution table for banned AI vocabulary:

| Banned term | Concrete replacement |
|---|---|
| additionally / furthermore | also, next, or start a new sentence |
| crucial / vital / paramount | needed, required, or state the exact risk |
| delve / dive deep | explore, inspect, read, analyze |
| enduring / testament to | proves, demonstrates, lasts |
| enhance / foster | improve, speed up, support |
| garner / showcase | get, collect, show, display |
| interplay / intricate | interaction, complex, detailed |
| landscape (abstract) | market, system, codebase, context |
| pivotal / cornerstone | main, key, primary |
| tapestry / substrate (abstract) | base, foundation, mix |
| underscore / highlight | stress, show, prove |
| vibrant / breathtaking | active, dense, or describe exact traits |
| utilize / leverage | use |
| facilitate | help, enable |
| seamless / holistic | direct, unified, integrated |

Translate abstract metaphors into concrete system components:
- "API surface" becomes "endpoints" or "exported functions"
- "vector" becomes "method" or "direction"
- "paradigm" becomes "pattern" or "approach"
- "scaffolding" becomes "template" or "boilerplate"

### Style and typography

- **Ban em dashes and en dashes.** Replace em dashes, en dashes, and hyphens acting as dashes with periods or commas. Split complex thoughts into two separate sentences.
- **Restrict colons.** Use colons only to introduce an explicit list, a table, or a code block. Never use colons as connectors in the middle of sentences or as pseudo-labels like Note or Summary.
- **Limit bold styling.** Use bold styling only for lead-ins and critical warnings. Keep standard text, acronyms, and proper nouns in normal weight.
- **Use sentence case headings.** Capitalize only the first word and proper nouns in headings.
- **Remove decorative elements.** Strip emojis from headings and bullet lists. Convert curly quotes to straight quotes.

### Communication artifacts and filler

- **Strip chatbot filler.** Delete "Certainly!", "Of course!", "I hope this helps!", and "Great question!". Open directly with the answer, code block, or file path.
- **Cut filler transitions.** Replace "in order to" with "to". Replace "due to the fact that" with "because". Delete "it is important to remember that" and state the fact directly.
- **Eliminate hedging chains.** Replace "could potentially possibly be" with "may".
- **Use active voice.** Place the actor before the action. Change "the file is loaded by the runner" to "the runner loads the file".
- **Cut bolstering adverbs.** Delete adverbs that prop up weak verbs. Replace "runs very quickly" with "completes in under 5ms". Replace "significantly improves" with the measured metric.

## Quick audit checklist

Run this check before finishing any writing task:

| Check | Passing condition |
|---|---|
| AI vocabulary | Zero occurrences of banned words from the substitution table |
| Dash punctuation | Zero em dashes, en dashes, or hyphen substitutes |
| Colon usage | Colons appear only before lists, tables, or code blocks |
| Pseudo-labels | Zero connector labels like Note or Summary |
| Voice | Every action sentence names the active subject |
| Adverbs | Zero adverbs bolstering weak verbs |
| Headings | Sentence case without decorative emojis |
| Evidence | Claims cite a specific metric, command, or source |
| Boundaries | Functional code, schemas, and commands remain idiomatic and untouched |
