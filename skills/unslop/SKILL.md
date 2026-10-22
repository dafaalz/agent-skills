---
name: unslop
description: Use when drafting prose, reviewing text for AI patterns, editing documentation, rewriting generic AI output, or cutting LLM writing habits in English or Indonesian. Don't use for functional code refactoring (use codebase-design), schema migrations (use schema-migration), or terminal command optimization.
---

# Unslop

Strip AI patterns and filler from prose and documentation. Write plain active sentences.

## Workflow

Run the four steps in sequence.

### Step 1. Pick a mode and scan for patterns

Default to Detect unless the user asks for edits:
- Detect mode. List every match with its line number, the quoted phrase, and the fix. Never guess an AI authorship score. Present the findings and stop.
- Edit mode. Run only on an explicit edit request. Sort matches into four groups:
  1. Banned words, empty adverbs, and marketing fluff in English and Indonesian.
  2. Structural puffery, faux-insight setups, colon reveals, and fake-profound kickers.
  3. Chatbot filler, process narration, and inanimate agency.
  4. Punctuation and syntax defects such as decorative em dashes, mid-sentence colons, and relative "di mana".
- Weight indicators before editing. Primary tells (formulaic contrasts, staged run-ups, forced triads, decorative dashes, repetitive closers) justify an edit on first sighting. Secondary tells (stacked qualifiers, hyphenated pairs) need supporting indicators in the same passage.
- Respect writing samples. Match the sample sentence length, word choice, and punctuation. The sample overrides default style restrictions while meaning stays clear.

For English text, read references/slop-patterns.md for word swaps, metaphor translations, empty adverbs, filler phrases, and structural patterns. For Indonesian text, read references/indonesian-patterns.md for calque swaps, pleonasm cuts, and chatbot filler patterns. Read both for mixed tasks.

Completion criterion: A catalog of every matched pattern with its line number and group, or a completed detect mode report.

### Step 2. Rewrite the flagged text

Rewrite flagged sections with plain words, active voice, and verifiable facts:
- Preserve the original tone, jokes, and technical facts.
- Delete promotional claims that apply unchanged to any product. Preserve architectural invariants, protocol rules, and conceptual trade-offs even when no empirical metric is provided. Do not invent metrics.
- Replace vague labels like "important" or "surprising" with verifiable metrics.
- Cut filler clauses instead of rewording them.
- Replace banned words with plain words.

Completion criterion: Rewritten text with zero cataloged patterns, original tone intact, and every technical fact preserved.

### Step 3. Vary the sentence rhythm

Alternate short and long sentences to keep prose brisk:
- Split long sentences with periods instead of comma splices or conjunction chains.
- For narrative prose, mix sentence lengths across paragraphs and state claims directly.
- For technical documentation, keep causal preconditions attached to commands so execution order remains unambiguous.

Completion criterion: Sentence lengths vary naturally without sacrificing syntactic clarity or causal order.

### Step 4. Run the final check

Check the draft against the quick audit checklist at the end of this document. For an edit request, output the full rewritten draft and a short list of what changed.

Completion criterion: Full rewritten draft and itemized change summary delivered, passing every checklist row.

## Boundary isolation

These rules cover human-facing prose, documentation, walkthroughs, and chat explanations only.

Keep code syntax, code blocks, database schemas, API parameters, variable names, terminal commands, and git commits neutral and idiomatic. Never inject voice quirks, slang, or arbitrary renames into functional code.

Never alter backticked text, including symbols (`symbol`), CLI flags (`--flag`), schema keys, and variable names (`variable_name`).

Literal technical domain terms in prose stay as written. "Vector database", "test harness", "silicon substrate", "programming paradigm", and "API surface" name precise technical concepts, not marketing metaphors.

Indonesian prose keeps standard technical loan terms unchanged, including "payload", "token JWT", "endpoint", "middleware", "controller", "pipeline CI", and "cluster Kubernetes".

## Core rules

### Cut puffery and commentary

- **[C1] Cut puffery.** Replace promotional fluff with a verifiable event, measurement, or action. Write "built in 2024" instead of "a testament to modern innovation".
- **[C2] Name specific sources.** Delete weasel attributions like "experts agree". For empirical claims lacking a source in the prompt, strip the unverifiable modifier rather than inventing metrics or deleting core architectural logic.
- **[C3] Delete generic claims.** Delete a sentence that applies unchanged to another project or company, or rewrite it with exact endpoints, schema fields, or performance metrics.
- **[C4] State how systems run, not vague impressions.** Replace "types that follow your schema" or "the database stays close at hand" with the concrete operation, such as validating fields against schema definitions or running queries under 2ms. Rewrite or delete statements with no operational action or measurement.
- **[C5] Delete commentary.** Remove text that tells the reader what to think or notice, such as "this distinction matters" or "the key point is".
- **[C6] Delete faux-insight setups.** Drop posturing like "what most people get wrong" or "here is what nobody tells you", and state the claim directly.
- **[C7] Rewrite colon reveals.** Rewrite dramatic reveals like "the best part: it works offline" as declarative sentences.
- **[C8] Delete fake-profound kickers.** Strip final mic-drop aphorisms and cute metaphors. End on the last concrete fact, finding, or immediate next action.
- **[C9] Delete compulsive summary wrap-ups.** Never append a generic summary paragraph or conclusion kicker starting with "Overall", "In conclusion", "Secara keseluruhan", or "Kesimpulannya" once technical steps or findings are complete. End on the final response status code, latency metric, test result, or next action.
- **[C10] Cut editorial participial tails.** Delete vague "-ing" commentary like "highlighting the importance" or "ensuring seamless integration". Retain participial clauses that specify concurrent system states or synchronous side effects, such as "blocking concurrent writes until commit".
- **[C11] Rewrite formulaic contrasts.** Rewrite "not just X, but Y" or "despite challenges, X continues to thrive" as the direct technical condition, without rhetorical contrast.
- **[C12] Delete formulaic openings and closings.** Remove throat-clearing intros like "In today's fast-paced world" and sycophantic sign-offs like "The future looks bright". Open with the core fact and close with the immediate next step.
- **[C13] Break marketing triads.** Cut empty adjective triads like "fast, scalable, and robust". Preserve domain-specific technical triads such as CIA (confidentiality, integrity, availability), CAP, or ACID properties.
- **[C14] Stop synonym cycling.** Repeat the correct technical term instead of cycling synonyms or inventing artificial variation.
- **[C15] Delete false ranges.** Remove spurious span constructions like "ranging from simple scripts to complex architectures" or "from startups to Fortune 500 companies". State the specific entity or scope directly.
- **[C16] Delete rhetorical setups and self-answers.** Drop presentation gimmicks like "What if I told you...", "Think about it", "Plot twist", or immediate self-answering questions. State the technical claim directly.
- **[C17] Delete negative listing.** Replace "Not X. Not Y. Z" with Z stated directly.
- **[C18] Cut quotables.** Rewrite any sentence that sounds like a pull-quote. State the mechanism directly.
- **[C19] Cut redundant background in replies.** In a thread reply or ongoing conversation, lead with the decision, action, or answer. Never recap the problem, diagnosis, or context the reader already knows.

### Use plain words

Pick plain words and direct verbs, using the swaps in the reference tables:
- **[V1] Replace nominalizations with root verbs.** Replace a weak verb plus an abstract noun with the direct root verb, as in "conduct an analysis of" to "analyze", "perform verification of" to "verify", "conduct the execution of" to "execute", "make an assessment" to "assess", and "make a modification to" to "modify". In Indonesian, replace "melakukan pengujian terhadap" with "menguji", "melakukan investigasi terhadap" with "menyelidiki", "melakukan implementasi" with "mengimplementasikan", "melakukan konfigurasi" with "mengonfigurasi", "memberikan konfirmasi" with "mengonfirmasi", and "memberikan penjelasan" with "menjelaskan".
- **[V2] Prefer active voice when the actor matters.** Place the actor before the action in operational prose. Retain passive voice in security advisories, protocol specs, and Indonesian *di-* procedural verbs when the receiver is the natural topic or the actor is unknown.
- **[V3] Use direct action verbs.** Replace fake-strong verbs and inflated bureaucratic phrases like "serves as a hub for" or "acts as a catalyst to enable" with direct verbs that name the system mechanism, such as "tracks", "routes", or "runs".
- **[V4] Convert figurative metaphors and personified code to literal system terms.** State execution rules directly instead of writing poetic fragments like "the plan holds the truth", and replace figurative verbs like "rides along" or "stands on" with direct technical relationships like "invokes" or "depends on".
- **[V5] Cut hyperbolic absolutes.** Replace vague generalizations like "everyone knows" with concrete scope. Retain universal quantifiers (`every`, `always`, `never`) when stating formal invariants or security constraints.
- **[V6] Use plain linking verbs for attributes.** Write `is`, `are`, or `has` instead of decorative substitutes like `boasts`, `features`, `serves as`, `functions as`, or `stands as`.

### Fix punctuation and styling

- **[S1] Cut decorative em dashes.** Replace parenthetical em dashes with commas or periods. Retain hyphens in numeric ranges (`ports 8000-8080`) and compound modifiers (`client-server`).
- **[S2] Restrict colons.** Use colons only to introduce an explicit list, a table, or a code block. Never use colons as mid-sentence connectors, as pseudo-labels like Note or Summary, or for dramatic reveals.
- **[S3] Limit bold styling.** Use bold only for lead-ins and critical warnings. Keep standard text, acronyms, and proper nouns in normal weight.
- **[S4] Convert redundant inline-header lists.** Rewrite bold labels that restate the following clause, such as bolding "Performance" followed by "Performance improved", as fluid prose. Keep a bold lead-in only when it ends in a period, names the topic, and introduces distinct detail.
- **[S5] Break list symmetry.** Vary clause patterns across bullet lists instead of forcing uniform length or repeating a bold pseudo-label before an identical sentence fragment. Format command output and error codes as tables or fluid prose rather than uniform bold labels.
- **[S6] Prevent over-compression.** Write complete sentences with articles and active verbs. Expand telegram-style fragments and symbol-speak like "parser fails bad date, exit 2, no write" into clear prose, such as "the parser rejects invalid dates, returns exit code 2, and writes no data to disk".
- **[S7] Use sentence case headings.** Capitalize only the first word and proper nouns in headings.
- **[S8] Remove decorative elements.** Strip emojis from headings and bullet lists, and convert curly quotes to straight quotes.
- **[S9] Ban rhetorical Wh- clefts and throat-clearing starts.** Rewrite pseudo-profound openers like "What makes X unique is..." as direct claims. Retain temporal `When`/`Where` conditional clauses, direct troubleshooting questions ("Why does ...?"), and Indonesian locative `di mana`.
- **[S10] Vary paragraph endings.** Never close two consecutive paragraphs with a punchy one-liner. End on a file path, command, metric, or next action.

### Cut chatbot filler

Remove conversational filler, meta-announcements, process narration, and artificial enthusiasm:
- **[F1] Strip conversational filler.** Delete "Certainly!", "Of course!", "I hope this helps!", "Great question!", "Tentu saja!", "Tentu!", "Dengan senang hati!", and "Semoga membantu!". Open directly with the substantive answer, code block, or file path.
- **[F2] Cut process narration.** Delete self-referential narration of analysis steps, such as "After reviewing the codebase", "Upon closer inspection", "Now let us examine", or "Having analyzed the logs". State the finding, command, or action directly.
- **[F3] Ban inanimate agency.** Never attribute cognitive thought, intentions, or desires to inanimate code, tools, or data models. Replace "the script thinks", "the function wants to validate", or "the model understands" with what the component executes, verifies, or computes.
- **[F4] Cut filler transitions.** Replace "in order to" with "to", and "due to the fact that" with "because". In Indonesian, replace "guna untuk" or "demi untuk" with "untuk", and "disebabkan oleh karena" with "karena". Delete "it is important to remember that", "di era digital saat ini", and "tidak dapat dipungkiri bahwa", and state the fact directly.
- **[F5] Cut empty adverbs and hedging chains.** Delete "literally", "actually", "honestly", "simply", "truly", and "fundamentally" when they add no factual information. Replace hedging chains like "could potentially possibly be" with "may", and Indonesian "berpotensi untuk dapat" with "dapat" or "bisa".
- **[F6] Cut bolstering adverbs.** Delete adverbs that prop up weak verbs. Replace "runs very quickly" with "completes in under 5ms", and "significantly improves" with the measured metric. In Indonesian, replace "sangat krusial" with "wajib" or the exact failure condition.

## Research and editorial sources

The evidence base for these rules, with a citation and the finding it supports per source, is in references/slop-patterns.md and references/indonesian-patterns.md.

## Quick audit checklist

Run this check before finishing any writing task:

| Check | Passing condition |
|---|---|
| Strip banned words | Zero matches in the English and Indonesian tables |
| Kill calques | Zero relative "di mana" or "yang mana" clauses (locative questions exempt) |
| Cut pleonasms | Zero pairs like "guna untuk", "demi untuk", "disebabkan karena", "adalah merupakan" |
| Ban dashes | Zero decorative em dashes (numeric ranges and compound modifiers exempt) |
| Limit colons | Colons before lists, tables, or code blocks only, zero reveals |
| Drop pseudo-labels | Zero connector labels like Note, Summary, Catatan, Ringkasan |
| Keep the voice | Original tone, bluntness, and cadence intact, no corporate flattening |
| Ground claims | Empirical claims backed by metrics; architectural invariants and contracts preserved |
| Flatten inline headers | Zero bold labels that repeat the following clause |
| Expand fragments | Zero telegram-style fragments or symbol-speak chains |
| Remove poetic prose | Zero personified code, philosophical aphorisms, or figurative metaphors |
| Cut fake structure | Zero faux-insight setups, fake-profound kickers, negative listings, and editorial "-ing" tails |
| Name the actor | Active subject in operational prose; passive voice retained for topic-focused security/specs |
| Cut process narration | Zero conversational setups like "After reviewing..." and zero inanimate agency |
| Cut reply recaps | Replies lead with the decision or answer, zero recaps of known background |
| Use plain linking verbs | is, are, or has for attributes, not boasts, features, or serves as |
| Cut adverbs | Zero bolstering or empty adverbs |
| Fix headings | Sentence case without decorative emojis |
| Cite evidence | Claims cite a specific metric, command, or source |
| Replace nominalizations | Zero smothered verb and abstract noun chains |
| Delete wrap-ups | Zero conclusion paragraphs or summary kickers |
| Break list symmetry | Varied clause patterns, zero repeated bold pseudo-labels |
| Ban Wh- clefts | Zero rhetorical clefts like "What makes...", temporal When/Where and diagnostic questions preserved |
| Cut quotables | Zero pull-quote sentences without a stated mechanism |
| Vary endings | No two consecutive paragraphs share a punchy one-liner ending |
| Ban extremes | Zero hyperbolic absolutes without scope; deterministic invariants preserved |
| Protect boundaries | Code, backticked symbols, CLI flags, domain terms, and schemas untouched |
