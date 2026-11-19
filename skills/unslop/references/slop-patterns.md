# Structural patterns and editing principles

Reference guide for spotting structural AI patterns and auditing prose for synthetic tells.

## Editing principles

- **Preserve the writer's real voice.** Observe vocabulary, cadence, bluntness, humor, uncertainty, and level of polish before editing. Keep traits that belong to the writer. Do not rewrite distinctive human sentences for symmetry or corporate consistency.
- **Make the minimum effective edit.** Fix AI patterns, factual errors, repetition, and tangled syntax. Leave strong human sentences alone. A draft with personality should still sound like the same author after editing.
- **Delete generic claims.** If a sentence applies unchanged to another company, project, or product without losing meaning, delete it or anchor it with specific schema fields, response status codes, latency metrics, or test results.
- **Show, don't tell the reader what to think.** Let facts, mechanisms, and outcomes carry weight. Delete commentary that labels a point as important, surprising, subtle, or obvious. Trust the reader to see the point.
- **Protect specific facts.** Never dilute concrete details into generic statements. Replace "improved performance" with the measured metric, such as "reduced p99 latency from 250ms to 45ms".
- **Preserve useful edge and character.** Retain strong stances, developer slang, honest admissions, and self-corrections when they reflect the author's authentic perspective.
- **Weight indicators before editing.** Primary tells (formulaic contrasts, staged run-ups, forced triads, decorative dashes, repetitive closers) justify an edit on first sighting. Secondary tells (stacked qualifiers, hyphenated pairs) require corroborating patterns in the same passage before you act.
- **Respect writing samples.** When the user supplies a writing sample, observe and match its sentence length, word choices, punctuation, and transitions. The sample overrides default style preferences, provided meaning remains clear.

## Structural patterns to eliminate

Each entry quotes the detection phrases and states the rewrite.

### 1. Faux-insight setups

Posturing as a lone insider reveals false profundity instead of substance. Cues cluster around phrases like "What most people get wrong about X", "Here is what nobody tells you", "The part everyone misses", "The uncomfortable truth is", and "This is the part most founders skip". Delete the setup and state the actual claim directly. "What nobody tells you about distributed systems is that state sync is the real bottleneck" becomes "State synchronization is the main bottleneck in distributed systems."

### 2. Colon reveals

Placing a dramatic noun phrase after a colon manufactures artificial suspense. Look for lines like "The best part: it works offline", "The secret: distribution is king", and "The kicker: nobody noticed". Rewrite the sentence as a direct declarative statement and remove the theatrical delay. "The secret: cache invalidation was broken" becomes "Cache invalidation was broken."

### 3. Interpretive metadiscourse

Coaching readers on how to react interrupts technical explanations. Frequent flags include "That last part matters more than it sounds", "The key point is", "This distinction matters", "In other words", and "Let that sink in". Delete the editorial intrusion or provide concrete evidence. "The migration completed with zero downtime. Let that sink in." becomes "The migration completed with zero downtime across all production database shards."

### 4. Fake-profound kickers

Aphorisms, poetic metaphors, and cosmic conclusions dilute technical findings at paragraph ends. Typical lines include "In the end, code is just poetry written for machines", "The future is already here, waiting to be coded", and "Because sometimes, the best feature is no feature at all". Delete the kicker outright and supply no replacement metaphor. End on the last concrete fact, finding, or immediate next action.

### 5. Rhetorical setups and self-answers

Drop theatrical setups that ask artificial questions only to answer them immediately. Familiar formulas include "What if I told you...", "Think about it", "Plot twist", and "Question? Answer." State the technical conclusion directly without the conversational hook.

### 6. Dramatic fragmentation

Chopping simple clauses into staccato sentence fragments creates fake urgency. This pattern surfaces in sequences like "Fast. Scalable. Reliable.", "X. And Y. And Z.", and "That is it. That is the whole thing." Combine the fragments into one complete sentence that names the primary technical quality and its evidence.

### 7. Synonym cycling

Rotating alternative terms for identical entities across a paragraph muddles technical clarity. This habit surfaces when one component shifts across "the agent", "the assistant", "the tool", and "the helper". Pick the single accurate technical term and maintain it across the entire section.

### 8. Negative listing

Listing rejected possibilities before revealing the actual subject delays the core technical fact. Familiar constructions include "Not a library. Not a framework. A protocol." and "It is not about speed. It is about correctness." State what the subject is directly, as in "A protocol for state sync" or "Correctness takes precedence over throughput."

### 9. Fake-strong verbs

Inflated administrative phrases displace direct verbs like "is", "has", or "routes". Routine examples include "Serves as a centralized hub for", "acts as a catalyst to enable", and "functions as a cornerstone for". Use an active root verb that names the physical mechanism, as in "The service routes requests" instead of "The service acts as a centralized routing hub for".

### 10. Weasel attribution

Citing anonymous authority fabricates consensus without verifiable evidence. Frequent indicators include "Experts agree that", "studies show", "industry reports suggest", and "widely regarded as the standard". Name the exact researcher, benchmark, RFC, or dataset. If no verifiable source exists, delete the claim entirely.

### 11. Compulsive summary wrap-ups

Mechanical conclusion sections rehash earlier findings without adding new data. Common cues open with "Overall", "In conclusion", "To summarize", "In summary", or "All in all". Delete the wrap-up section and end on the last concrete status code, latency metric, test result, or next step.

### 12. Nominalizations and smothered verbs

Burying active verbs inside abstract Latinate nouns combined with weak dummy verbs deadens instructions. Routine cases feature "conduct an evaluation of", "perform an assessment of", "make a determination", and "facilitate the implementation of". Replace the dummy verb and abstract noun with the direct active root verb. "The team will conduct the implementation of the outbox pattern" becomes "The team will implement the outbox pattern."

| Nominalization and smothered verb | Active root verb |
|---|---|
| conduct an analysis of | analyze |
| perform verification of | verify |
| conduct the execution of | execute |
| make an assessment of | assess |
| make a modification to | modify |
| perform an evaluation of | evaluate |
| facilitate the implementation of | implement |
| make a determination | determine |
| perform configuration of | configure |
| provide confirmation of | confirm |
| provide an explanation of | explain |
| perform an inspection of | inspect |
| conduct an investigation of | investigate |
| achieve optimization of | optimize |

### 13. Process narration

Narrating analytical steps wastes reader attention on author workflow instead of findings. Common openings include "After reviewing the codebase", "Upon closer inspection", "Having analyzed the schema", and "In this section we will examine". Delete the workflow recap and state the finding, command, or action directly. "After reviewing the authentication logs, we discovered invalid token signatures" becomes "The authentication logs contained invalid token signatures on incoming requests."

### 14. Inanimate agency

Attributing cognitive intentions or desires to inanimate code confuses mechanical causality. Common instances include "the script wants to verify", "the function believes the input is valid", "the database hopes to avoid locking", and "the algorithm understands user intent". State what the component literally executes, validates, or calculates. "The validator function wants to check for missing email fields" becomes "The validator function checks for missing email fields."

### 15. Trailing participial clauses

Tacking loose `-ing` commentary onto finished actions adds vague editorial filler. Familiar examples include `"ensuring seamless integration"`, `"highlighting the importance of testing"`, `"allowing for better performance"`, and `"fostering collaboration"`. Cut cosmetic participial tails outright or convert them into a separate active sentence, while retaining participial clauses that specify causal preconditions, concurrent system states, or failure guards (such as `"preventing split-brain writes during network partitions"`). `"The runner caches dependencies, ensuring faster builds"` becomes `"The runner caches dependencies. Subsequent builds complete in 12 seconds."`

### 16. False ranges

Spurious span prepositions manufacture artificial breadth between arbitrary extremes. Formulations include `"ranging from simple scripts to enterprise platforms"`, `"from beginners to seasoned architects"`, and `"from small startups to Fortune 500 companies"`. State the specific scope or supported targets directly. `"The tool handles tasks ranging from simple scripts to complex pipelines"` becomes `"The tool runs shell scripts and distributed pipelines."`

### 17. Formulaic contrasts

Mechanical contrast templates force artificial antithesis onto simple factual conditions. Routine occurrences feature `"not just X, but Y"`, `"not only X, but also Y"`, and `"despite challenges, X continues to grow"`. Rewrite rhetorical antithesis as a direct factual statement (`"The update is not just a patch, but a major overhaul"` becomes `"The update rewrites the query planner"`), while preserving dual-invariant technical guarantees (`"The mutex prevents both concurrent writes and stale reads during failover"`).

### 18. Formulaic openings and closings

Broad platitudes and synthetic optimism frame technical topics with generic fluff. Typical markers include "In today's fast-paced world", "In an era of rapid technological advancement", "The future looks bright", and "Together we can achieve excellence". Open directly with the core technical subject and close with the immediate next action.

### 19. Re-explaining what the reader knows (wrong reader)

When replying in an active thread or ongoing conversation, language models often recap the problem, walk through the diagnosis, and present evidence before finally giving the decision on the last line. In an ongoing conversation, the reader already knows the background. Rebuilding context buries the actionable decision. Lead with the decision or answer. Keep only the reasoning that would change whether the reader agrees, and move lengthy proof or diagnosis to an issue ticket or follow-up document.

### 20. Avoiding simple linking verbs (is, are, has)

Language models frequently avoid plain verbs like "is", "are", and "has", replacing them with inflated verbs like "serves as", "acts as", "boasts", "features", "functions as", or "stands as". When describing an attribute or condition, use the direct linking verb. "The repository boasts comprehensive test coverage" becomes "The repository has comprehensive test coverage." "The file serves as the configuration entrypoint" becomes "The file is the configuration entrypoint."

### 21. Staged dialectic paragraphs

Language models evade intra-sentence contrast bans by staging a three-sentence dialectic arc across a paragraph. Cues cluster around "On one hand, X... On the other hand, Y... The sustainable path forward lies in balancing both." Collapse the three sentences into one direct statement of the primary mechanism and the exact engineering trade-off.

### 22. Faux-humility hedges and discourse-pivot scaffolds

Concessive concession-pivot frames manufacture false objectivity before stating a generic claim. Watch for "While workload profiles inevitably diverge across teams, one operational reality remains consistent", "Though no silver bullet exists, teams consistently observe", and transition bridges like "That architectural trade-off brings us to...". Delete the concession shell and state the measured constraint directly.

### 23. Lexical-to-structural calque evasion

When single words are blocked, models substitute inflated multi-word calques. Replace "interrogate the state space" with "test state transitions", "empirical witness" with "reproduction trace" or "benchmark log", "operational terrain" with "production environment", and "braided dependency graph" with "cyclic dependencies".

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
| landscape (abstract) | market, system, codebase, context |
| pivotal / cornerstone | main, key, primary |
| tapestry / substrate (abstract) | base, foundation, mix |
| underscore / highlight | stress, show, prove |
| vibrant / breathtaking | active, dense, or describe exact traits |
| utilize / leverage / harness (abstract) | use |
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
| robust / resilient (marketing) | stable, fault-tolerant, tested |
| cutting-edge / state of the art | recent, modern, or state the release year |
| unlock / unleash | open, access, enable |
| revolutionary / next-level / next-generation | modern, updated, or state the exact capability |

### Technical domain and identifier protection

Leave inline backticked symbols (`symbol`, `--flag`, `variable_name`), unbackticked `camelCase`/`snake_case`/`PascalCase`/`SCREAMING_SNAKE_CASE` identifiers, file paths, URLs, inline math (`$...$`), code blocks, API parameters, and database schema keys intact.

Protect literal engineering domain terms across systems, security, cryptography, hardware, and cloud architecture (`UNS-12`). Preserve `vector` (as in `attack vector`, `interrupt vector`, `feature vector`, `vector database`), `evacuate` (as in `evacuate pods`, `evacuate nodes`, `evacuating collector`), `ratchet` (as in `Double Ratchet`, `coverage ratchet`), `bedrock` (as in `Amazon Bedrock`, `Bedrock Edition`), `substrate` (as in `silicon substrate`, `FR-4 substrate`, `Substrate framework`), `scaffolding` (as in `project scaffolding`), `harness` (`test harness`), `paradigm` (`programming paradigm`), and `API surface` whenever they denote technical mechanisms. Replace terms from the table below only when used as figurative marketing slogans in non-technical copy.

### Metaphor translations into concrete components

| Figurative marketing metaphor | Concrete technical replacement |
|---|---|
| `"API surface"` (in sales copy) | endpoints, exported functions |
| `"vector"` (in business strategy copy) | method, direction |
| `"paradigm"` (in buzzword copy) | pattern, approach |
| `"scaffolding"` (in non-code prose) | template, boilerplate |
| `"substrate"` (in abstract business prose) | base, foundation |
| `"wedge"` (in GTM/sales copy) | entry point, initial feature |
| `"bedrock"` (in non-AWS/non-Minecraft prose) | core platform, runtime |
| `"harness"` (in non-testing prose) | runner, execution wrapper |
| `"ratchet"` (in non-crypto/non-gate prose) | tightening threshold, metric rule |
| `"evacuate"` (in non-cluster/non-GC prose) | migrate, drain |
| `"flywheel"` / `"north star"` | operational metric, target objective |
| `"gold-plating"` | unneeded scope, speculative work |

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

Never retain patronizing or empty adverbs such as "actually", "honestly", "literally", or "simply". State the direct technical condition without emotional padding or defensive posture.

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

## Research and editorial references

- **Liang et al. (Stanford 2024, arXiv:2404.01268).** Documented sharp frequency surges of characteristic marker vocabulary (including "delve", "testament", "intricate", "pivotal", and "showcase") in peer-reviewed scientific papers after LLM release.
- **Kobak et al. (Science Advances 2025, arXiv:2406.07016).** Analyzed vocabulary tracking and style markers across biomedical abstracts, proving broad-scale adoption of automated generation without human editing.
- **Mitchell et al. (DetectGPT, Stanford 2023, arXiv:2301.11305) and Sadasivan et al. (2023).** Demonstrated that AI generation exhibits low perplexity (overly predictable token sequences) and low burstiness (flat, uniform sentence rhythm), contrasting with natural human variation.
- **Pangram Labs and Beutler Ink (2024, 2025).** Documented statistical overrepresentation of negative parallelism ("not only X, but also Y"), rhetorical triad lists ("rule of three"), and spurious span ranges ("from X to Y") in LLM outputs.
- **Wikipedia WikiProject AI Cleanup (WP:AIC).** Cataloged structural patterns common in synthetic writing, emphasizing process narration ("Upon closer inspection"), inanimate agency (attributing consciousness to code or abstract concepts), and dropped actors in passive constructions.
- **Paul Graham (2024).** Identified false formality, inflated diction substitutes, and synthetic earnestness as immediate indicators of machine-generated text.
- **blader/humanizer (2025).** Documented wrong-reader reply recaps, indicator weighting thresholds, voice sample matching overrides, and artificial evasion of basic linking verbs.
- **Dewan Pers (Peraturan No. 1/2025).** Mandated human verification, primary source attribution, and journalistic accountability while banning synthetic consensus claims.
- **Narabahasa (Ivan Lanin dan Yudhistira).** Analyzed English syntax interference, translationese calques, and robotic transition chains in modern Indonesian prose.

## Evaluation rubric

Execute these verification checks against every draft before finishing:

1. Maintain the author's original tone, vocabulary, bluntness, and cadence across every edited passage.
2. Delete generic claims or anchor them to specific schema fields, status codes, latency numbers, or test results.
3. Remove faux-insight setups, colon reveals, false ranges, formulaic contrasts, and interpretive commentary.
4. Eliminate process narration and inanimate agency in favor of literal system operations and verified actors.
5. End on the last concrete fact, test result, or immediate next action instead of an aphorism or mic-drop kicker.
6. Delete all banned words, empty adverbs, and filler phrases cataloged in the reference tables.
7. Quote exact line numbers and identify matched patterns for audit requests without rewriting text or asserting AI authorship scores.
