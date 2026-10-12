---
name: unslop
description: Use when drafting prose, reviewing text for AI patterns, editing documentation, rewriting generic AI output, or cutting LLM writing habits in English or Indonesian. Don't use for functional code refactoring, schema migrations, or terminal command optimization.
---

# Unslop

Strip AI patterns and filler from prose and documentation, and write plain active sentences.

## Workflow

Run these four steps in sequence to audit and refine prose.

### Step 1. Pick a mode and scan for patterns

Pick the mode before you scan. Default to Detect unless the user asks for edits.

- In detect mode, list every match with its line number, the quoted phrase, and the fix. Never guess an AI authorship score. Present the findings and stop.
- In edit mode, run only on an explicit edit request. Sort patterns into four groups before you rewrite:
  1. Banned words, empty adverbs, and marketing fluff in English and Indonesian.
  2. Structural puffery, faux-insight setups, colon reveals, and fake-profound kickers.
  3. Chatbot filler, process narration, and inanimate agency.
  4. Punctuation and syntax defects such as em dashes, mid-sentence colons, and relative "di mana".

When handling an English task, read `references/slop-patterns.md` for word swaps and structural patterns.
When handling an Indonesian task, read `references/indonesian-patterns.md` for calque and pleonasm tables.
When handling a mixed task, read both files.

Completion criterion. Deliver a written catalog that lists every matched pattern with its line number and group, or deliver a completed detect mode report.

### Step 2. Rewrite the flagged text

Rewrite flagged sections with plain words, active voice, and verifiable facts.

- Preserve human sentences. Keep the writer's original tone, jokes, and technical facts intact.
- Delete generic claims. Drop sentences that apply unchanged to any product, or anchor them to exact schema parameters, response codes, latency numbers, or test results.
- Replace vague labels. Swap qualitative labels like "important" or "surprising" for verifiable metrics.
- Cut filler clauses directly instead of rewording them.
- Replace banned words with plain words.

Completion criterion. Deliver rewritten text containing zero cataloged patterns while preserving the author's original tone and all technical facts.

### Step 3. Vary the sentence rhythm

Alternate short and long sentences to keep prose brisk.

- Split long sentences with periods instead of comma splices or conjunction chains.
- For narrative prose, mix sentence lengths across paragraphs and state claims directly.
- For technical documentation, state the path, command, precondition, and result in separate sentences.

Completion criterion. Verify that no three consecutive sentences share identical length or clause structure.

### Step 4. Run the final check

Check the draft against the quick audit checklist at the end of this document. For an edit request, output the full rewritten draft and a short list of what changed.

Completion criterion. Full rewritten draft and itemized change summary delivered, passing every row of the quick audit checklist.

## Boundary isolation

Use these rules for human-facing prose, documentation, walkthroughs, and chat explanations only.

Keep code syntax, code blocks, database schemas, API parameters, variable names, terminal commands, and git commits neutral and idiomatic. Never inject voice quirks, slang, or arbitrary renames into functional code.

Protect inline backticked text without exception. Never alter backticked symbols (`symbol`), CLI flags (`--flag`), schema keys, or variable names (`variable_name`).

Protect literal technical domain terms in prose. Terms like "vector database", "test harness", "silicon substrate", "programming paradigm", and "API surface" represent precise technical concepts rather than marketing metaphors.

Do not force translation on standard technical loan terms in Indonesian prose. Preserve established technical terms like "payload", "token JWT", "endpoint", "middleware", "controller", "pipeline CI", and "cluster Kubernetes" in their standard technical form.

## Core rules

### Cut puffery and commentary

- **[C1] Cut puffery.** Replace promotional fluff with a verifiable event, measurement, or action. Write "built in 2024" instead of "a testament to modern innovation".
- **[C2] Name specific sources.** Attribute facts to an exact person, repository, document, or dataset. Delete weasel attributions like "experts agree" or "studies show". If no verifiable source exists, delete the claim.
- **[C3] Delete generic claims.** If a sentence applies unchanged to another project or company without losing meaning, delete it or rewrite it with exact endpoints, schema fields, or performance metrics.
- **[C4] State how systems run, not vague impressions.** Replace vague impressions like "types that follow your schema" or "the database stays close at hand" with concrete technical operations, such as validating fields against schema definitions or running queries under 2ms. Rewrite any statement that lacks an operational action or measurement, or delete it.
- **[C5] Delete commentary.** Remove text that tells the reader what to think or notice, such as "this distinction matters" or "the key point is".
- **[C6] Delete faux-insight setups.** Drop posturing like "what most people get wrong" or "here is what nobody tells you", and state the claim directly.
- **[C7] Rewrite colon reveals.** Rewrite dramatic reveals like "the best part: it works offline" as declarative sentences.
- **[C8] Delete fake-profound kickers.** Strip final mic-drop aphorisms and cute metaphors. End on the last concrete fact, finding, or immediate next action.
- **[C9] Delete compulsive summary wrap-ups.** Never append a generic summary paragraph or conclusion kicker starting with "Overall", "In conclusion", "Secara keseluruhan", or "Kesimpulannya" once technical steps or findings are complete. End on the final response status code, latency metric, test result, or next action.
- **[C10] Delete trailing participial clauses.** Remove "-ing" clauses like "highlighting the importance" or "ensuring seamless integration". Write them as separate sentences or omit them.
- **[C11] Rewrite formulaic contrasts.** Rewrite "not just X, but Y" or "despite challenges, X continues to thrive" by stating the technical condition directly without rhetorical contrast.
- **[C12] Delete formulaic openings and closings.** Remove throat-clearing intros like "In today's fast-paced world" and sycophantic sign-offs like "The future looks bright". Open with the core fact and close with the immediate next step.
- **[C13] Break rule-of-three cliches.** Replace triad groupings like "fast, scalable, and robust" with the single primary technical property and its evidence.
- **[C14] Stop synonym cycling.** When a technical term is correct, repeat it instead of cycling through synonyms or inventing artificial variation.
- **[C15] Delete false ranges.** Remove spurious span constructions like "ranging from simple scripts to complex architectures" or "from startups to Fortune 500 companies". State the specific entity or scope directly.
- **[C16] Delete rhetorical setups and self-answers.** Drop presentation gimmicks like "What if I told you...", "Think about it", "Plot twist", or immediate self-answering questions. State the technical claim directly.
- **[C17] Delete negative listing.** Replace "Not X. Not Y. Z" with Z stated directly.

### Use plain words

Pick plain words and direct verbs. Read the matching reference guide for word swaps, structural patterns, and metaphor conversions.

- When handling an English task, read `references/slop-patterns.md` for English word swaps, metaphor translations, empty adverbs, and filler phrases.
- When handling an Indonesian task, read `references/indonesian-patterns.md` for Indonesian calque swaps, pleonasm cuts, and chatbot filler patterns.
- **[V1] Replace nominalizations with root verbs.** Replace a weak verb plus an abstract noun with the direct root verb. Replace "conduct an analysis of" with "analyze", "perform verification of" with "verify", "conduct the execution of" with "execute", "make an assessment" with "assess", and "make a modification to" with "modify". In Indonesian, replace "melakukan pengujian terhadap" with "menguji", "melakukan investigasi terhadap" with "menyelidiki", "melakukan implementasi" with "mengimplementasikan", "melakukan konfigurasi" with "mengonfigurasi", "memberikan konfirmasi" with "mengonfirmasi", and "memberikan penjelasan" with "menjelaskan".
- **[V2] Use active voice.** Place the actor before the action. Change "the file is loaded by the runner" to "the runner loads the file", and "file dimuat oleh runner" to "runner memuat file".
- **[V3] Use direct action verbs.** Replace fake-strong verbs and inflated bureaucratic phrases with direct verbs that name the system mechanism. Replace "serves as a hub for" or "acts as a catalyst to enable" with direct verbs like "tracks", "routes", or "runs".
- **[V4] Convert figurative metaphors and personified code to literal system terms.** Replace literary flourishes, poetic metaphors, and personified code with literal system terms. State execution rules directly instead of writing poetic fragments like "the plan holds the truth", and replace figurative verbs like "rides along" or "stands on" with direct technical relationships like "invokes" or "depends on".

### Fix punctuation and styling

- **[S1] Ban em dashes and en dashes.** Replace em dashes, en dashes, and hyphens acting as dashes with periods or commas, and split long sentences in two.
- **[S2] Restrict colons.** Use colons only to introduce an explicit list, a table, or a code block. Never use colons as mid-sentence connectors, as pseudo-labels like Note or Summary, or for dramatic reveals.
- **[S3] Limit bold styling.** Use bold only for lead-ins and critical warnings. Keep standard text, acronyms, and proper nouns in normal weight.
- **[S4] Convert redundant inline-header lists.** Rewrite bold labels that restate the following clause, such as bolding "Performance" followed by "Performance improved", as fluid prose. Keep a bold lead-in only when it ends in a period, names the topic, and introduces genuinely distinct detail.
- **[S5] Break list symmetry.** Vary clause patterns across bullet lists instead of forcing uniform length or repeating a bold pseudo-label before an identical sentence fragment. Format command output and error codes as tables or fluid prose rather than uniform bold labels.
- **[S6] Prevent over-compression.** Write complete sentences with articles and active verbs. Expand telegram-style fragments and symbol-speak like "parser fails bad date, exit 2, no write" into clear prose, such as "the parser rejects invalid dates, returns exit code 2, and writes no data to disk".
- **[S7] Use sentence case headings.** Capitalize only the first word and proper nouns in headings.
- **[S8] Remove decorative elements.** Strip emojis from headings and bullet lists, and convert curly quotes to straight quotes.

### Cut chatbot filler

Remove conversational filler, meta-announcements, process narration, and artificial enthusiasm.

- **[F1] Strip conversational filler.** Delete "Certainly!", "Of course!", "I hope this helps!", "Great question!", "Tentu saja!", "Tentu!", "Dengan senang hati!", and "Semoga membantu!". Open directly with the substantive answer, code block, or file path.
- **[F2] Cut process narration.** Delete self-referential narration describing your analysis steps, such as "After reviewing the codebase", "Upon closer inspection", "Now let us examine", or "Having analyzed the logs". State the finding, command, or action directly.
- **[F3] Ban inanimate agency.** Never attribute cognitive thought, intentions, or desires to inanimate code, tools, or data models. Replace "the script thinks", "the function wants to validate", or "the model understands" with what the component literally executes, verifies, or computes.
- **[F4] Cut filler transitions.** Replace "in order to" with "to", and "due to the fact that" with "because". In Indonesian, replace "guna untuk" or "demi untuk" with "untuk", and "disebabkan oleh karena" with "karena". Delete "it is important to remember that", "di era digital saat ini", and "tidak dapat dipungkiri bahwa", and state the fact directly.
- **[F5] Cut empty adverbs and hedging chains.** Delete "literally", "actually", "honestly", "simply", "truly", and "fundamentally" when they add no factual information. Replace hedging chains like "could potentially possibly be" with "may", and Indonesian "berpotensi untuk dapat" with "dapat" or "bisa".
- **[F6] Cut bolstering adverbs.** Delete adverbs that prop up weak verbs. Replace "runs very quickly" with "completes in under 5ms", and "significantly improves" with the measured metric. In Indonesian, replace "sangat krusial" with "wajib" or the exact failure condition.

## Research and editorial sources

| Source | Core finding |
|---|---|
| Liang et al. (Stanford 2024, arXiv:2404.01268) | Frequency surges of marker vocabulary across scientific text after LLM adoption |
| Kobak et al. (Science Advances 2025, arXiv:2406.07016) | Excess vocabulary and style markers tracked across biomedical papers |
| Mitchell et al. (DetectGPT, Stanford 2023, arXiv:2301.11305) | Low perplexity and low burstiness produce predictable phrasing and monotonous cadence |
| Pangram Labs and Beutler Ink (2024, 2025) | Negative parallelism, rule-of-three triads, and false ranges as empirical markers |
| Wikipedia WikiProject AI Cleanup (WP:AIC) | Process narration, inanimate agency, and missing human actors in generated articles |
| Paul Graham (2024) | False formality, synthetic earnestness, and formulaic essay structure |
| Dewan Pers (Peraturan No. 1/2025) | Verification rules, human editorial accountability, and ban on unverified AI text |
| Narabahasa (Ivan Lanin dan Yudhistira) | Foreign syntax calques, robotic conjunction chains, and translationese patterns |

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
| Keep the voice | Authentic tone, bluntness, and cadence remain intact without corporate flattening |
| Ground every claim | Every statement names a schema parameter, status code, latency metric, or test result instead of an impression |
| Flatten inline headers | Zero bold labels that repeat the following clause |
| Expand fragments | Zero telegram-style fragments or symbol-speak chains |
| Remove poetic prose | Zero personified code, philosophical aphorisms, or figurative metaphors |
| Cut fake structure | Zero faux-insight setups, zero fake-profound kickers, zero negative listings, and zero trailing "-ing" clauses |
| Name the actor | Every action sentence names the active subject |
| Cut process narration | Zero conversational setups like "After reviewing..." or inanimate agency |
| Cut adverbs | Zero bolstering or empty adverbs |
| Fix headings | Sentence case without decorative emojis |
| Cite evidence | Claims cite a specific metric, command, or source |
| Replace nominalizations | Zero smothered verb and abstract noun chains |
| Delete wrap-ups | Zero conclusion paragraphs or summary kickers |
| Break list symmetry | Natural syntactic variation with zero repeated bold pseudo-labels |
| Protect boundaries | Functional code, backticked symbols, CLI flags, technical domain terms, and schemas remain untouched |
