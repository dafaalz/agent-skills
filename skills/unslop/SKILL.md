---
name: unslop
description: Strip AI slop patterns, eliminate filler, and restore authentic human cadence. Use when drafting prose, reviewing text for AI patterns, editing documentation, rewriting generic AI output, or cutting LLM writing habits. Don't use for functional code refactoring, schema migrations, or terminal command optimization.
---

# Unslop

Audit prose and documentation to strip AI patterns, eliminate filler, and restore human cadence.

## Workflow

Follow these four steps in sequence:

### Step 1. Mode selection and pattern scan

Determine the operation mode based on user intent:
- Detect mode. If the user asks whether text is AI slop, or requests an audit or scan without rewriting, catalog every matched pattern, quote the offending line, and state a concise fix. Never guess AI authorship percentages or score drafts. Present findings and stop.
- Edit mode (default). Catalog patterns across four categories to prepare for rewriting:
  1. Banned vocabulary, empty adverbs, and marketing fluff in English and Indonesian.
  2. Structural puffery, faux-insight setups, colon reveals, and fake-profound kickers.
  3. Syntactic tells, calque structures (such as relative "di mana" or "yang mana"), passive voice, and weak adverbs.
  4. Punctuation defects, including em dashes, mid-sentence colons, and decorative styling.

Consult `references/slop-patterns.md` for English structural patterns and `references/indonesian-patterns.md` for Indonesian patterns.

Completion criterion. A written catalog listing matched patterns, line locations, and target categories, or a completed detect mode report.

### Step 2. Concrete rewrite

Rewrite flagged sections using plain vocabulary, active voice, and verifiable facts.
- Apply the minimum effective edit. Preserve the writer's authentic voice, cadence, bluntness, humor, and level of polish. Leave strong human sentences alone.
- Apply the portability test. Cut generic claims that could move unchanged to another company or product, or anchor them with specific facts.
- Show, don't tell the reader what to think. Let facts, mechanisms, and metrics carry weight without authorial commentary declaring them important or surprising.
- Replace vague feelings with concrete measurements, numbers, or system mechanisms.
- Drop empty filler clauses instead of rewording them.
- Pair every removed prohibition with a direct positive action.
- Preserve all underlying technical facts and intent.

Completion criterion. Rewritten text containing zero cataloged patterns while retaining writer voice and all factual points.

### Step 3. Cadence and tone calibration

Adjust sentence rhythm and voice according to document scope:
- Untangle complex sentences without flattening spoken cadence.
- For narrative prose, vary sentence lengths across paragraphs, state clear stances, and avoid robotic symmetry or stacked punchy fragments.
- For technical documentation and agent runbooks, state exact paths, commands, and preconditions without decorative prose.

Completion criterion. No three consecutive sentences share the same length or clause pattern.

### Step 4. Final verification pass

Audit the draft against the quick audit checklist at the bottom of this document. For edit requests, output the full rewritten draft and a concise list of what changed.

Completion criterion. Text passes every check in the quick audit checklist with zero exceptions.

## Boundary isolation

Apply these rules strictly to human-facing prose, documentation, walkthroughs, and chat explanations.

Keep code syntax, database schemas, API parameters, variable names, terminal commands, and git commits neutral and idiomatic. Never inject voice quirks, slang, or arbitrary renames into functional code.

## Core rules

### Content and framing

- **Cut puffery.** Replace promotional fluff with verifiable events, measurements, or actions. Write "built in 2024" instead of "a testament to modern innovation".
- **Name specific sources.** Attribute facts to an exact person, repository, document, or dataset. Avoid weasel attributions like "experts agree" or "studies show". If no verifiable source exists, delete the claim.
- **Apply the portability test.** If a sentence could appear unchanged in documentation for another project or company, it provides no concrete value. Cut the claim or anchor it to specific system invariants, endpoints, or numbers.
- **Describe mechanism instead of feel.** Avoid subjective statements like "types that follow your schema" or "the database stays close at hand". State the mechanical contract or measured delta directly, such as code generation validating against schema definitions or query execution timing under 2ms. If a statement cannot be rewritten as a verifiable instruction, mechanism, or metric, delete it.
- **Show, don't tell.** Remove commentary that tells the reader what to think or notice, such as "this distinction matters" or "the key point is".
- **Cut faux-insight setups.** Delete posturing like "what most people get wrong" or "here is what nobody tells you". State the claim directly.
- **Eliminate colon reveals.** Rewrite dramatic reveals like "the best part: it works offline" into standard declarative sentences.
- **Delete fake-profound kickers.** Strip final mic-drop aphorisms and cute metaphors. End on the last concrete fact, finding, or immediate next action.
- **Strip superficial participial clauses.** Remove trailing "-ing" clauses like "highlighting the importance" or "ensuring seamless integration". Write them as distinct sentences or omit them entirely.
- **Replace formulaic contrasts.** Delete phrases like "not just X, but Y" or "despite challenges, X continues to thrive". State the actual technical state directly.
- **Strip formulaic openings and closings.** Delete throat-clearing intros like "In today's fast-paced world" or "Whether you are a beginner or an expert". Delete sycophantic sign-offs like "The future looks bright". Open with the core fact and close with the immediate next step.
- **Break rule-of-three cliches and stop synonym cycling.** Eliminate triad groupings like "fast, scalable, and robust". Pick the single primary technical property that matters. When a technical term is correct, repeat it consistently instead of cycling through synonyms.

### Plain vocabulary and substitutions

Use plain words and direct verbs. Consult these reference guides for comprehensive substitution tables, structural patterns, and metaphor conversions:

- English substitution tables, metaphor translations, empty adverbs, and filler phrases. Read `references/slop-patterns.md`.
- Indonesian calque replacements, pleonasm eliminations, and conversational filler patterns. Read `references/indonesian-patterns.md`.

### Style and typography

- **Ban em dashes and en dashes.** Replace em dashes, en dashes, and hyphens acting as dashes with periods or commas. Split complex thoughts into two separate sentences.
- **Restrict colons.** Use colons only to introduce an explicit list, a table, or a code block. Never use colons as connectors in the middle of sentences, as pseudo-labels like Note or Summary, or for dramatic colon reveals.
- **Limit bold styling.** Use bold styling only for lead-ins and critical warnings. Keep standard text, acronyms, and proper nouns in normal weight.
- **Convert redundant inline-header lists.** Catch bold labels that merely restate the following sentence clause, such as bolding Performance followed by Performance improved. Convert them to fluid prose. Keep bold lead-ins only when they end in a period, name the topic, and are followed by genuinely distinct detail.
- **Prevent over-compression.** Write complete sentences with necessary articles and active verbs. Avoid telegram-style fragments, symbol-speak, and shorthand arrows that require decoding, such as parser fails bad date, exit 2, no write. Expand into clear prose, such as the parser rejects invalid dates, returns exit code 2, and writes no data to disk.
- **Use sentence case headings.** Capitalize only the first word and proper nouns in headings.
- **Remove decorative elements.** Strip emojis from headings and bullet lists. Convert curly quotes to straight quotes.

### Communication artifacts and filler

- **Strip chatbot filler.** Delete "Certainly!", "Of course!", "I hope this helps!", "Great question!", "Tentu saja!", "Tentu!", "Dengan senang hati!", and "Semoga membantu!". Open directly with the answer, code block, or file path.
- **Cut filler transitions.** Replace "in order to" with "to". Replace "due to the fact that" with "because". In Indonesian, replace "guna untuk" or "demi untuk" with "untuk", and replace "disebabkan oleh karena" with "karena". Delete "it is important to remember that", "di era digital saat ini", and "tidak dapat dipungkiri bahwa". State the fact directly.
- **Cut empty adverbs.** Delete adverbs like "literally", "actually", "honestly", "simply", "truly", or "fundamentally" when they add no factual information.
- **Eliminate hedging chains.** Replace "could potentially possibly be" with "may". In Indonesian, replace "berpotensi untuk dapat" with "dapat" or "bisa".
- **Use active voice.** Place the actor before the action. Change "the file is loaded by the runner" to "the runner loads the file". In Indonesian, change "file dimuat oleh runner" to "runner memuat file".
- **Cut bolstering adverbs.** Delete adverbs that prop up weak verbs. Replace "runs very quickly" with "completes in under 5ms". Replace "significantly improves" with the measured metric. In Indonesian, replace "sangat krusial" with "wajib" or state the exact failure condition.
- **Avoid negative listing and fake-strong verbs.** Replace "Not X. Not Y. Z" by stating Z directly. Replace "serves as a hub for" with direct active verbs like "tracks" or "routes".
- **Eliminate mannered prose.** Replace literary flourishes, philosophical aphorisms, rhetorical fragments, and personified code with literal descriptions. Instead of writing "the plan holds the truth" or "wire it or delete it", state the functional execution rule directly. Replace figurative verbs like "rides along" or "stands on" with direct technical relationships like "invokes" or "depends on".

## Quick audit checklist

Run this check before finishing any writing task:

| Check | Passing condition |
|---|---|
| AI vocabulary | Zero occurrences of banned words from English and Indonesian substitution tables |
| Calque syntax | Zero occurrences of relative "di mana" or "yang mana" connecting clauses |
| Pleonasms | Zero redundant pairs such as "guna untuk", "demi untuk", "disebabkan karena", or "adalah merupakan" |
| Dash punctuation | Zero em dashes, en dashes, or hyphen substitutes |
| Colon usage | Colons appear only before lists, tables, or code blocks with zero colon reveals |
| Pseudo-labels | Zero connector labels like Note, Summary, Catatan, or Ringkasan |
| Voice preservation | Authentic tone, bluntness, and cadence preserved without forced corporate flattening |
| Portability and mechanism | Every statement names a mechanical contract, metric, or invariant rather than an emotional impression |
| Inline headers | Zero bold labels that redundantly repeat the subsequent sentence clause |
| Compression | Zero telegram-style shorthand fragments or symbol-speak chains |
| Mannered prose | Zero personified code, philosophical aphorisms, or literary fragments |
| Structure | Zero faux-insight setups, zero fake-profound kickers, and zero trailing -ing clauses |
| Active voice | Every action sentence names the active subject |
| Adverbs | Zero bolstering or empty adverbs |
| Headings | Sentence case without decorative emojis |
| Evidence | Claims cite a specific metric, command, or source |
| Boundaries | Functional code, schemas, and commands remain idiomatic and untouched |
