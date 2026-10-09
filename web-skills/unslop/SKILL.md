---
name: unslop
description: Use when drafting prose, reviewing text for AI patterns, editing documentation, rewriting generic AI output, or cutting LLM writing habits in English or Indonesian. Don't use for functional code refactoring, schema migrations, or terminal command optimization.
---

# Unslop for Claude Web

Audit prose and documentation to strip AI patterns, eliminate filler, and restore human cadence on Claude Web.

<initiative_and_scope>
When asked to edit or unslop text, deliver the revised output directly without lectures. Keep working until the full requested text is audited and rewritten. Do not add unrequested commentary, moralizing about AI, or unrelated sections. If you notice structural issues beyond the scope, state them briefly at the end.
</initiative_and_scope>

<claude_web_environment>
Operate within the Claude Web interface. Accept input pasted into chat or uploaded as documents. Output substantial rewritten text, long articles, and complete documentation as standalone Claude Artifacts (`text/markdown` or `text/plain`). Output short conversational revisions and audit catalogs directly in chat.
</claude_web_environment>

## Workflow

Follow these four steps in sequence:

### Step 1. Mode selection and pattern scan

Determine the operation mode based on user prompt:
- **Detect mode.** If the user asks whether text is AI slop, or requests an audit or scan without rewriting: catalog every matched pattern, quote the offending line, and state a concise fix. Never guess AI authorship percentages or score drafts. Present findings in chat and stop.
- **Edit mode (default).** Scan and catalog patterns across four categories to prepare for rewriting:
  1. Banned vocabulary, empty adverbs, and marketing fluff in English and Indonesian.
  2. Structural puffery, faux-insight setups, colon reveals, and fake-profound kickers.
  3. Syntactic tells, calque structures (such as relative "di mana" or "yang mana"), passive voice, and weak adverbs.
  4. Punctuation defects, including em dashes, mid-sentence colons, and decorative styling.

Consult `references/slop-patterns.md` for English structural patterns and `references/indonesian-patterns.md` for Indonesian patterns.

### Step 2. Concrete rewrite

Rewrite flagged sections using plain vocabulary, active voice, and verifiable facts:
- Apply the minimum effective edit. Preserve the writer's authentic voice, cadence, bluntness, humor, and polish. Leave strong human sentences alone.
- Apply the portability test. Cut generic claims that could move unchanged to another company or product, or anchor them with specific facts.
- Show, don't tell. Let facts, mechanisms, and metrics carry weight without authorial commentary declaring them important or surprising.
- Replace vague feelings with concrete measurements, numbers, or system mechanisms.
- Drop empty filler clauses instead of rewording them.
- Preserve all underlying technical facts and intent.

### Step 3. Cadence and tone calibration

Adjust sentence rhythm and voice according to document scope:
- Untangle complex sentences without flattening spoken cadence.
- For narrative prose, vary sentence lengths across paragraphs, state clear stances, and avoid robotic symmetry or stacked punchy fragments.
- For technical documentation and agent runbooks, state exact paths, commands, and preconditions without decorative prose.
- Ensure no three consecutive sentences share the same length or clause pattern.

### Step 4. Final verification and artifact delivery

Audit the draft against the quick audit checklist below. Deliver the output:
- For long documents (>15 lines): render the full rewritten text inside a Claude Artifact. In the chat message, provide only a concise summary table of cataloged changes.
- For short snippets: output the rewritten text directly in chat followed by what changed.

## Core rules

### Content and framing
- **Cut puffery.** Replace promotional fluff with verifiable events, measurements, or actions. Write "built in 2024" instead of "a testament to modern innovation".
- **Name specific sources.** Attribute facts to an exact person, repository, document, or dataset. Avoid weasel attributions like "experts agree" or "studies show".
- **Apply the portability test.** If a sentence fits any company, person, or product unchanged, cut it or replace it with specific technical traits.
- **Show, don't tell.** Remove commentary that tells the reader what to think or notice, such as "this distinction matters" or "the key point is".
- **Cut faux-insight setups.** Delete posturing like "what most people get wrong" or "here is what nobody tells you". State the claim directly.
- **Eliminate colon reveals.** Rewrite dramatic reveals like "the best part: it works offline" into standard declarative sentences.
- **Delete fake-profound kickers.** Strip final mic-drop aphorisms and cute metaphors. End on the last concrete fact, finding, or immediate next action.
- **Strip superficial participial clauses.** Remove trailing "-ing" clauses like "highlighting the importance" or "ensuring seamless integration".
- **Replace formulaic contrasts.** Delete phrases like "not just X, but Y". State the actual state directly.
- **Strip formulaic openings and closings.** Delete throat-clearing intros like "In today's fast-paced world" and sign-offs like "The future looks bright".

### Plain vocabulary substitutions

#### English substitutions
| Banned term | Concrete replacement |
|---|---|
| additionally / furthermore | also, next, or start a new sentence |
| crucial / vital / paramount | needed, required, or state the exact risk |
| delve / dive deep | explore, inspect, read, analyze |
| enduring / testament to | proves, demonstrates, lasts |
| enhance / foster | improve, speed up, support |
| garner / showcase | get, collect, show, display |
| interplay / intricate | interaction, complex, detailed |
| landscape (abstract) / realm | market, system, codebase, context |
| pivotal / cornerstone | main, key, primary |
| utilize / leverage / harness | use |
| facilitate / empower | help, enable |
| seamless / holistic | direct, unified, integrated |
| elevate / supercharge | improve, accelerate |
| embark / journey | begin, build, run |

#### Indonesian substitutions
| Banned Indonesian term | Concrete replacement |
|---|---|
| dalam lanskap / menavigasi lanskap | pada industri, di pasar, dalam sistem, di codebase |
| memainkan peran penting dalam | menentukan, menjadi kunci, mempercepat |
| di mana / yang mana (relatif klausa) | buat kalimat baru atau sambung langsung ke nomina |
| tidak hanya X, tetapi juga Y | sebut aksi X dan aksi Y dalam kalimat mandiri terpisah |
| sebuah bukti nyata dari | membuktikan, menunjukkan, memvalidasi |
| menyelami lebih dalam | memeriksa, menganalisis, menguji |
| merupakan salah satu dari | salah satu, atau pasang predikat langsung |
| krusial / vital / esensial | wajib, dibutuhkan, atau sebut dampak bila gagal |
| membuka potensi penuh / merangkul | meningkatkan kapasitas, menyesuaikan sistem |
| secara keseluruhan / sebagai kesimpulan | hapus, tutup dengan aksi konkret berikutnya |
| di era digital yang serba cepat ini | hapus total, sebut subjek dan waktu riil |
| tidak dapat dipungkiri bahwa | hapus total, nyatakan fakta langsung |
| perlu diingat bahwa / penting untuk dicatat | hapus total, nyatakan aturan langsung |
| melakukan [verba] (eksekusi, validasi) | eksekusi, validasi (gunakan kata kerja aktif) |
| memiliki kemampuan untuk | bisa, dapat, mampu |
| adalah merupakan / merupakan sebuah | adalah, atau jadikan kata benda sebagai predikat |
| alat yang ampuh / senjata ampuh | sebut nama perkakas atau fungsi teknis spesifik |
| guna untuk / demi untuk / disebabkan karena | untuk, karena (hapus pleonasme) |
| berpotensi untuk dapat / diharapkan dapat | dapat, mampu (potong rantai hedging) |

### Style and typography
- **Ban em dashes and en dashes.** Replace dashes with periods or commas. Split complex thoughts into two separate sentences.
- **Restrict colons.** Use colons only to introduce an explicit list, a table, or a code block. Never use colons as connectors in the middle of sentences or for dramatic reveals.
- **Limit bold styling.** Use bold styling only for lead-ins and critical warnings.
- **Use sentence case headings.** Capitalize only the first word and proper nouns.
- **Remove decorative elements.** Strip emojis from headings and bullet lists. Convert curly quotes to straight quotes.

### Communication artifacts and filler
- **Strip chatbot filler.** Delete "Certainly!", "Of course!", "I hope this helps!", "Tentu saja!", and "Semoga membantu!". Open directly with the answer, rewrite, or file diff.
- **Cut empty adverbs.** Delete adverbs like "literally", "actually", "honestly", "simply", or "fundamentally" when they add no factual information.
- **Eliminate hedging chains.** Replace "could potentially possibly be" with "may". Replace "berpotensi untuk dapat" with "dapat".
- **Use active voice.** Place the actor before the action ("the runner loads the file" instead of "the file is loaded by the runner").

## Quick audit checklist

| Check | Passing condition |
|---|---|
| AI vocabulary | Zero occurrences of banned words from English and Indonesian tables |
| Calque syntax | Zero occurrences of relative "di mana" or "yang mana" connecting clauses |
| Pleonasms | Zero redundant pairs such as "guna untuk", "demi untuk", or "adalah merupakan" |
| Dash punctuation | Zero em dashes, en dashes, or hyphen substitutes |
| Colon usage | Colons appear only before lists, tables, or code blocks |
| Voice preservation | Authentic tone, bluntness, and cadence preserved without corporate flattening |
| Structure | Zero faux-insight setups, zero fake-profound kickers, and zero trailing -ing clauses |
| Active voice | Every action sentence names the active subject |
| Output delivery | Substantial rewrites rendered as Claude Artifacts |
