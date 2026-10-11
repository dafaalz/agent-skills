# Structural patterns and editing principles

Reference guide for spotting structural AI patterns and auditing prose for synthetic tells.

## Editing principles

- **Preserve the writer's real voice.** Observe vocabulary, cadence, bluntness, humor, uncertainty, and level of polish before editing. Keep traits that belong to the writer. Do not rewrite distinctive human sentences for symmetry or corporate consistency.
- **Make the minimum effective edit.** Fix AI patterns, factual errors, repetition, and tangled syntax. Leave strong human sentences alone. A draft with personality should still sound like the same author after editing.
- **Apply the portability test.** If a sentence could move unchanged to another person, company, country, or product, it is generic filler. Cut it or anchor it with specific facts, metrics, mechanisms, or consequences.
- **Show, don't tell the reader what to think.** Let facts, mechanisms, and outcomes carry weight. Delete commentary that labels a point as important, surprising, subtle, or obvious. Trust the reader to see the point.
- **Protect specific facts.** Never dilute concrete details into generic statements. Replace "improved performance" with the measured metric, such as "reduced p99 latency from 250ms to 45ms".
- **Preserve useful edge and character.** Retain strong stances, developer slang, honest admissions, and self-corrections when they reflect the author's authentic perspective.

## Structural patterns to eliminate

Each entry quotes the detection phrases and states the rewrite.

### 1. Faux-insight setups

Thought-leader posturing that flatters the author as the lone expert uncovering hidden truths. The tell appears in phrases like "What most people get wrong about X", "Here is what nobody tells you", "The part everyone misses", "The uncomfortable truth is", and "This is the part most founders skip". Delete the setup and state the actual claim directly. "What nobody tells you about distributed systems is that state sync is the real bottleneck" becomes "State synchronization is the main bottleneck in distributed systems."

### 2. Colon reveals

A noun phrase followed by a colon and a dramatic lowercase punchline. The tell appears in phrases like "The best part: it works offline", "The secret: distribution is king", and "The kicker: nobody noticed". Rewrite the sentence as a plain declarative and drop the artificial suspense. "The secret: cache invalidation was broken" becomes "Cache invalidation was broken."

### 3. Interpretive metadiscourse

Authorial commentary that steps outside the subject to instruct the reader how to react. The tell appears in phrases like "That last part matters more than it sounds", "The key point is", "This distinction matters", "In other words", and "Let that sink in". Delete the aside, or supply the missing factual support. "The migration completed with zero downtime. Let that sink in." becomes "The migration completed with zero downtime across 12 shards."

### 4. Fake-profound kickers

A closing sentence reaching for a mic-drop aphorism, poetic metaphor, or philosophical flourish. The tell appears in lines like "In the end, code is just poetry written for machines", "The future is already here, waiting to be coded", and "Because sometimes, the best feature is no feature at all". Delete the kicker outright and do not swap in another metaphor. End on the last concrete fact, finding, or immediate next action.

### 5. Rhetorical setups and self-answers

Presentational gimmicks where the author asks and immediately answers a question, or plants a teaser hook. The tell appears in phrases like "What if I told you...", "Think about it", "Plot twist", and "Question? Answer." Drop the gimmick and state the technical statement directly.

### 6. Dramatic fragmentation

Breaking a simple thought into staccato fragments to manufacture tension. The tell appears in fragments like "Fast. Scalable. Reliable.", "X. And Y. And Z.", and "That is it. That is the whole thing." Combine the fragments into one complete sentence that carries the primary technical quality.

### 7. Synonym cycling

Rotating synonyms for the same concept within a paragraph to avoid repeating a word. The tell appears when one entity becomes "the agent", then "the assistant", then "the tool", then "the helper". Pick the single accurate technical term and repeat it.

### 8. Negative listing

Listing what something is not before stating what it is. The tell appears in constructions like "Not a library. Not a framework. A protocol." and "It is not about speed. It is about correctness." State what the entity is directly, as in "A protocol for state sync" or "Correctness takes precedence over throughput."

### 9. Fake-strong verbs

Replacing simple verbs like "is", "has", or "does" with inflated bureaucratic phrases. The tell appears in phrases like "Serves as a centralized hub for", "acts as a catalyst to enable", and "functions as a cornerstone for". Use a direct verb that names the mechanism, as in "The service routes requests" instead of "The service acts as a centralized routing hub for".

### 10. Weasel attribution

Vague authority claims that invent consensus without citing verifiable sources. The tell appears in phrases like "Experts agree that", "studies show", "industry reports suggest", and "widely regarded as the standard". Name the exact person, benchmark, RFC, or dataset. If no verifiable source exists, delete the claim.

### 11. Compulsive summary wrap-ups

A closing paragraph or section that mechanically rehashes earlier points under the guise of an executive summary. The tell appears in paragraphs opening with "Overall", "In conclusion", "To summarize", "In summary", or "All in all". Delete the wrap-up and end on the last concrete fact, finding, or immediate action.

### 12. Nominalizations and smothered verbs

Burying an active verb inside an abstract Latinate noun paired with a weak dummy verb such as "conduct", "perform", "make", or "facilitate". The tell appears in phrases like "conduct an evaluation of", "perform an assessment of", "make a determination", and "facilitate the implementation of". Replace the dummy verb and abstract noun with the direct active root verb. "The team will conduct the implementation of the outbox pattern" becomes "The team will implement the outbox pattern."

## Expanded vocabulary and filler

### Banned words and marketing fluff

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
| tapestry / substrate (abstract) | base, foundation, mix |
| underscore / highlight | stress, show, prove |
| vibrant / breathtaking | active, dense, or describe exact traits |
| utilize / leverage / harness | use |
| facilitate / empower | help, enable |
| seamless / holistic | direct, unified, integrated |
| elevate / supercharge | improve, accelerate |
| embark / journey | begin, build, run |
| paradigm shift / game changer | new pattern, state exact metric |
| realm / sphere | field, area, domain, codebase |
| beacon / lighthouse | guide, reference, standard |
| multifaceted / nuanced | complex, varied, or name the factors |
| meticulous / painstaking | detailed, thorough, checked |
| ever-evolving / dynamic | changing, active, updated |
| this is huge / changes everything | state the exact measurable benefit |
| robust / resilient | stable, fault-tolerant, tested |
| cutting-edge / state of the art | recent, modern, or state the release year |

### Metaphor translations into concrete components

Translate abstract metaphors into concrete system components.
- "API surface" becomes "endpoints" or "exported functions"
- "vector" becomes "method" or "direction"
- "paradigm" becomes "pattern" or "approach"
- "scaffolding" becomes "template" or "boilerplate"
- "substrate" becomes "base" or "foundation"
- "wedge" becomes "entry point" or "addition"
- "bedrock" becomes "core platform" or "runtime"
- "harness" becomes "test suite" or "runner"
- "ratchet" becomes "tightening limit" or state the exact metric rule
- "evacuate" becomes "migrate" or "move"
- "flywheel" or "north star" becomes the specific operational metric or objective
- "gold-plating" becomes "unneeded scope" or "speculative work"

### Often-empty adverbs

Cut these adverbs when they add no factual information:
- just
- literally
- honestly
- simply
- actually
- truly
- fundamentally
- importantly
- crucially
- inherently
- inevitably

Retain them only when they express authentic uncertainty or necessary contrast.

### Often-empty filler phrases

Cut these throat-clearing and delay phrases:
- at the end of the day
- when it comes to
- at its core
- the reality is
- the truth is
- in terms of
- with regard to
- going forward
- in this article
- let us dive in

## Evaluation rubric

Run these checks against every draft:

1. Does the rewrite maintain the author's original tone, vocabulary, bluntness, and cadence?
2. Does every sentence contain specific context that blocks pasting it into an unrelated topic?
3. Are faux-insight setups, colon reveals, and interpretive commentary removed?
4. Does the text end on a concrete fact or next step instead of an aphorism or mic-drop metaphor?
5. Are all banned words, empty adverbs, and filler phrases eliminated?
6. For audit requests, did the agent quote lines and name patterns without rewriting or claiming AI authorship?
