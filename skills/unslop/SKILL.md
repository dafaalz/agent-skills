---
name: unslop
description: Use when drafting prose, reviewing text for AI patterns, editing documentation, rewriting generic AI output, or cutting LLM writing habits in English or Indonesian. Don't use for functional code refactoring, schema migrations, or terminal command optimization.
---

# Unslop

Strip AI patterns and filler from prose and documentation, and write plain active sentences.

## Workflow

Run these four steps in order.

### Step 1. Pick a mode and scan for patterns

Pick the mode before you scan. Default to Detect unless the user asks for edits.

- Detect mode. List every match with its line number, the quoted phrase, and the fix. Never guess an AI authorship score. Present the findings and stop.
- Edit mode. Run only on an explicit edit request. Sort patterns into four groups before you rewrite:
  1. Banned words, empty adverbs, and marketing fluff in English and Indonesian.
  2. Structural puffery, faux-insight setups, colon reveals, and fake-profound kickers.
  3. Syntax tells such as relative "di mana" or "yang mana", passive voice, and weak adverbs.
  4. Punctuation defects such as em dashes, mid-sentence colons, and decorative styling.

English task. Read `references/slop-patterns.md` for word swaps and structural patterns.
Indonesian task. Read `references/indonesian-patterns.md` for calque and pleonasm tables.
Mixed task. Read both files.

Completion criterion. A written catalog that lists every matched pattern with its line location and group, or a completed detect mode report.

### Step 2. Rewrite the flagged text

Rewrite flagged sections with plain words, active voice, and verifiable facts.

- Change as little as possible. Keep the writer's wording, jokes, and tone. Leave strong human sentences alone.
- Cut claims that travel. If a sentence could move unchanged to another company or product, it says nothing. Cut it or rewrite it with specific facts.
- State facts, mechanisms, and metrics. Cut lines that tell the reader the point is important or surprising.
- Replace vague claims like "important" or "surprising" with a measurement, a number, or a system mechanism.
- Delete empty filler clauses. Do not reword them.
- Pair every banned word with the plain word that replaces it.
- Keep every technical fact and the writer's goal.

Completion criterion. Rewritten text with zero cataloged patterns that keeps the writer voice and every factual point.

### Step 3. Vary the sentence rhythm

Vary sentence length by document type.

- Split long sentences in two. Keep the writer's wording, jokes, and tone.
- Narrative prose. Vary sentence length across paragraphs and state the claim in plain words.
- Technical docs. State the path, command, precondition, and result.

Completion criterion. No three sentences in a row share the same length or clause pattern.

### Step 4. Run the final check

Check the draft against the quick audit checklist at the end of this document. For an edit request, output the full rewritten draft and a short list of what changed.

Completion criterion. The text passes every row of the quick audit checklist.

## Leave code alone

Use these rules for human-facing prose, documentation, walkthroughs, and chat explanations only.

Keep code syntax, database schemas, API parameters, variable names, terminal commands, and git commits neutral and idiomatic. Never inject voice quirks, slang, or arbitrary renames into functional code.

## Core rules

### Cut puffery and commentary

- **[C1] Cut puffery.** Replace promotional fluff with a verifiable event, measurement, or action. Write "built in 2024" instead of "a testament to modern innovation".
- **[C2] Name specific sources.** Attribute facts to an exact person, repository, document, or dataset. Avoid weasel attributions like "experts agree" or "studies show". If no verifiable source exists, delete the claim.
- **[C3] Cut claims that travel.** If a sentence could appear unchanged in another project or company, it says nothing concrete. Cut it or rewrite it with specific endpoints, invariants, or numbers.
- **[C4] Describe the mechanism, not a feeling.** Replace statements like "types that follow your schema" or "the database stays close at hand" with the mechanical contract or measured delta, such as code that validates against schema definitions or a query that runs under 2ms. Rewrite any statement you cannot express as an instruction, mechanism, or metric, or delete it.
- **[C5] Delete commentary.** Remove text that tells the reader what to think or notice, such as "this distinction matters" or "the key point is".
- **[C6] Delete faux-insight setups.** Drop posturing like "what most people get wrong" or "here is what nobody tells you", and state the claim directly.
- **[C7] Rewrite colon reveals.** Rewrite dramatic reveals like "the best part: it works offline" as declarative sentences.
- **[C8] Delete fake-profound kickers.** Strip final mic-drop aphorisms and cute metaphors. End on the last concrete fact, finding, or immediate next action.
- **[C9] Delete compulsive summary wrap-ups.** Never append a generic summary paragraph or conclusion kicker starting with "Overall", "In conclusion", "Secara keseluruhan", or "Kesimpulannya" once technical steps or findings are complete. End on the final mechanical invariant, output metric, or next action.
- **[C10] Delete trailing participial clauses.** Remove "-ing" clauses like "highlighting the importance" or "ensuring seamless integration". Write them as separate sentences or omit them.
- **[C11] Rewrite formulaic contrasts.** Rewrite "not just X, but Y" or "despite challenges, X continues to thrive" as a direct statement of the technical state.
- **[C12] Delete formulaic openings and closings.** Remove throat-clearing intros like "In today's fast-paced world" and sycophantic sign-offs like "The future looks bright". Open with the core fact and close with the immediate next step.
- **[C13] Break rule-of-three cliches and synonym cycling.** Replace triad groupings like "fast, scalable, and robust" with the single primary technical property and its evidence. When a technical term is correct, repeat it instead of cycling through synonyms.

### Use plain words

Pick plain words and direct verbs. Read the matching reference guide for word swaps, structural patterns, and metaphor conversions.

- English task. Read `references/slop-patterns.md` for English word swaps, metaphor translations, empty adverbs, and filler phrases.
- Indonesian task. Read `references/indonesian-patterns.md` for Indonesian calque swaps, pleonasm cuts, and chatbot filler patterns.
- **[V1] Replace nominalizations with root verbs.** Replace a weak verb plus an abstract noun with the direct root verb. Replace "conduct an analysis of" with "analyze", "perform verification of" with "verify", "conduct the execution of" with "execute", and "make an assessment" with "assess". In Indonesian, replace "melakukan pengujian terhadap" with "menguji", "melakukan investigasi terhadap" with "menyelidiki", "melakukan implementasi" with "mengimplementasikan", and "memberikan penjelasan" with "menjelaskan".

### Fix punctuation and styling

- **[S1] Ban em dashes and en dashes.** Replace em dashes, en dashes, and hyphens acting as dashes with periods or commas, and split long sentences in two.
- **[S2] Restrict colons.** Use colons only to introduce an explicit list, a table, or a code block. Never use colons as mid-sentence connectors, as pseudo-labels like Note or Summary, or for dramatic reveals.
- **[S3] Limit bold styling.** Use bold only for lead-ins and critical warnings. Keep standard text, acronyms, and proper nouns in normal weight.
- **[S4] Convert redundant inline-header lists.** Rewrite bold labels that restate the following clause, such as bolding Performance followed by Performance improved, as fluid prose. Keep a bold lead-in only when it ends in a period, names the topic, and introduces genuinely distinct detail.
- **[S5] Break list symmetry.** Vary clause patterns across bullet lists instead of forcing uniform length or repeating a bold pseudo-label before an identical sentence fragment. Format command output and error codes as tables or fluid prose rather than uniform bold labels.
- **[S6] Prevent over-compression.** Write complete sentences with articles and active verbs. Expand telegram-style fragments and symbol-speak like "parser fails bad date, exit 2, no write" into clear prose, such as "the parser rejects invalid dates, returns exit code 2, and writes no data to disk".
- **[S7] Use sentence case headings.** Capitalize only the first word and proper nouns in headings.
- **[S8] Remove decorative elements.** Strip emojis from headings and bullet lists, and convert curly quotes to straight quotes.

### Cut chatbot filler

- **[F1] Strip chatbot filler.** Delete "Certainly!", "Of course!", "I hope this helps!", "Great question!", "Tentu saja!", "Tentu!", "Dengan senang hati!", and "Semoga membantu!". Open directly with the answer, code block, or file path.
- **[F2] Cut filler transitions.** Replace "in order to" with "to", and "due to the fact that" with "because". In Indonesian, replace "guna untuk" or "demi untuk" with "untuk", and "disebabkan oleh karena" with "karena". Delete "it is important to remember that", "di era digital saat ini", and "tidak dapat dipungkiri bahwa", and state the fact directly.
- **[F3] Cut empty adverbs.** Delete "literally", "actually", "honestly", "simply", "truly", and "fundamentally" when they add no factual information.
- **[F4] Eliminate hedging chains.** Replace "could potentially possibly be" with "may". In Indonesian, replace "berpotensi untuk dapat" with "dapat" or "bisa".
- **[F5] Use active voice.** Place the actor before the action. Change "the file is loaded by the runner" to "the runner loads the file", and "file dimuat oleh runner" to "runner memuat file".
- **[F6] Cut bolstering adverbs.** Delete adverbs that prop up weak verbs. Replace "runs very quickly" with "completes in under 5ms", and "significantly improves" with the measured metric. In Indonesian, replace "sangat krusial" with "wajib" or the exact failure condition.
- **[F7] Avoid negative listing and fake-strong verbs.** Replace "Not X. Not Y. Z" with Z stated directly, and replace "serves as a hub for" with a direct verb like "tracks" or "routes".
- **[F8] Eliminate mannered prose.** Replace literary flourishes, philosophical aphorisms, rhetorical fragments, and personified code with literal descriptions. State a functional execution rule directly instead of writing "the plan holds the truth" or "wire it or delete it", and replace figurative verbs like "rides along" or "stands on" with direct technical relationships like "invokes" or "depends on".

## Quick audit checklist

Run this check before finishing any writing task.

| Check | Passing condition |
|---|---|
| Strip banned words | Zero banned words from the English and Indonesian tables |
| Kill calques | Zero relative "di mana" or "yang mana" clauses |
| Cut pleonasms | Zero redundant pairs such as "guna untuk", "demi untuk", "disebabkan karena", or "adalah merupakan" |
| Ban dashes | Zero em dashes, en dashes, or hyphen substitutes |
| Limit colons | Colons appear only before lists, tables, or code blocks, with zero reveals |
| Drop pseudo-labels | Zero connector labels like Note, Summary, Catatan, or Ringkasan |
| Keep the voice | Authentic tone, bluntness, and cadence preserved without corporate flattening |
| Ground every claim | Every statement names a mechanical contract, metric, or invariant instead of an impression |
| Flatten inline headers | Zero bold labels that repeat the following clause |
| Expand fragments | Zero telegram-style fragments or symbol-speak chains |
| Straighten mannered prose | Zero personified code, philosophical aphorisms, or literary fragments |
| Cut fake structure | Zero faux-insight setups, zero fake-profound kickers, and zero trailing "-ing" clauses |
| Name the actor | Every action sentence names the active subject |
| Cut adverbs | Zero bolstering or empty adverbs |
| Fix headings | Sentence case without decorative emojis |
| Cite evidence | Claims cite a specific metric, command, or source |
| Replace nominalizations | Zero smothered verb and abstract noun chains |
| Delete wrap-ups | Zero conclusion paragraphs or summary kickers |
| Break list symmetry | Natural syntactic variation with zero repeated bold pseudo-labels |
| Protect boundaries | Functional code, schemas, and commands remain idiomatic and untouched |
