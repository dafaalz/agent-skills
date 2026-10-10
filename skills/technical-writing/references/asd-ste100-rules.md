# ASD-STE100 reference for technical writing

This reference operationalizes ASD-STE100 Simplified Technical English (STE) Issue 8 and Issue 9 writing rules for software documentation, system architectures, runbooks, and developer guides.

## Core principles

ASD-STE100 enforces two governing mechanisms:

1. Controlled grammar. 53 structural rules limit sentence length, verb tenses, clause combinations, and punctuation choices.
2. Controlled vocabulary. The specification dictionary assigns each approved word a single meaning and a single part of speech.

In software documentation, domain tokens such as function names, API endpoints, CLI flags, JSON keys, and database entities qualify as Technical Names. Apply STE grammar strictly to the surrounding prose.

## Section 1. Words and vocabulary

### 1. The Power of One

Every word carries exactly one approved meaning and functions as exactly one part of speech.
- Do not use a noun as a verb. Write "Apply oil to the bearing", never "Oil the bearing".
- Do not use a verb as an adjective. Write "The valve that is near the pump", never "The close valve".
- Do not interchange technical terms with everyday synonyms. Pick the single canonical term and repeat it consistently.

### 2. Technical Names versus Technical Verbs

- Technical Names represent specific hardware parts, software components, tools, processes, or configurations. Terms like "mutex", "middleware", "webhook", and "JWT" qualify as Technical Names.
- Technical Verbs describe specific domain actions that have no everyday equivalent. Keep Technical Verbs minimal. Use approved verbs wherever possible.

### 3. American spelling

Use American English spelling based on Merriam-Webster's Collegiate Dictionary.
- Write "color", not "colour".
- Write "synchronize", not "synchronise".
- Write "center", not "centre".
- Write "gage", not "gauge".

### 4. Common unapproved words in software documentation

Replace unapproved synonyms with their approved STE counterparts:

| Unapproved word | Approved replacement | Example fix |
|---|---|---|
| check, verify, confirm | make sure, examine | Make sure that the server responds with status 200. |
| ensure, guarantee | make sure | Make sure that the backup file exists on disk. |
| inspect, audit | examine | Examine the access logs for invalid authentication tokens. |
| perform, execute | do, run | Run the database migration script. |
| terminate, kill, abort | stop | Stop the worker process before you apply the patch. |
| utilize, leverage | use | Use Redis to cache session tokens. |
| facilitate, assist | help | This utility helps the compiler optimize loop bounds. |
| configure, adjust | set up, change | Set up the environment variables in `.env`. |
| display, output | show | The terminal shows the process identifier. |
| prompt (verb) | ask | The CLI asks the user for confirmation. |
| transmit, dispatch | send | Send the payload through the HTTP POST endpoint. |
| initiate, kick off | start | Start the test runner. |
| terminate (connection) | close | Close the socket connection. |

## Section 2. Noun clusters

Limit noun clusters to a maximum of three words.

An unbroken string of four or more nouns obscures the syntactic relationship between modifiers and head nouns. Unpack dense noun clusters using prepositions, articles, or reordered clauses.

| Non-compliant cluster | Compliant rewrite |
|---|---|
| user account verification token generator | generator for user account verification tokens |
| postgres database connection pool timeout | timeout of the PostgreSQL connection pool |
| runtime memory allocation budget check | check that validates the runtime memory budget |

## Section 3. Verbs and tenses

### 1. Approved verb forms

ASD-STE100 permits only six verb forms:
1. Infinitive (to run, to build).
2. Imperative (run the test, open the file).
3. Simple present (the server listens, the service responds).
4. Simple past (the process exited, the migration failed).
5. Simple future with "will" (the system will restart).
6. Past participle functioning strictly as an adjective (the closed connection, the committed transaction).

### 2. Prohibited verb forms

- Prohibit progressive and continuous tenses. Never use forms of "to be" combined with "-ing". Write "The server runs", never "The server is running". Write "The worker processed jobs", never "The worker was processing jobs".
- Prohibit perfect tenses. Never combine "have" or "had" with past participles. Write "The runner finished the build", never "The runner has finished the build".
- Prohibit gerunds. Never use words ending in "-ing" as nouns. Write "To clean the cache, run `flushall`", never "Cleaning the cache requires running `flushall`".

### 3. Modal verbs

Permit only three auxiliary verbs:
- "can" expresses capability or permission.
- "will" expresses future certainty.
- "must" expresses a mandatory requirement.

Prohibit ambiguous modals:
- Ban "should". In standard technical prose, "should" creates doubt about whether an action is mandatory. Use "must" or the imperative mood.
- Ban "may". Replace "may" with "can" for capability or state explicit conditional logic with "if".
- Ban "could", "would", and "might".

## Section 4. Sentence length and structure

- Procedural sentences must not exceed 20 words. Every sentence that gives an instruction must stay within this bound.
- Descriptive sentences must not exceed 25 words. Every sentence that explains a concept or system behavior must stay within this bound.
- Convey only one complete thought or instruction per sentence. Split coordinate clauses connected by "and" into separate sentences.

## Section 5. Procedural writing

- State preconditions before actions. When a command requires a specific operational state, place the condition first, separated by a comma. Write "To compile the binary, run `make build`", never "Run `make build` to compile the binary". Write "If the port is busy, change the configuration", never "Change the configuration if the port is busy".
- Present actions in strict chronological order. Never write "Restart the server after editing the configuration". Write "Edit the configuration. Then restart the server."
- Use exactly one instruction per sentence. Do not chain multiple actions with "and". Split "Pull the latest branch and run the migrations" into two separate sentences, "Pull the latest branch. Run the database migrations."
- Write all procedural steps in the imperative mood. Start directly with the base form of the verb. Never add polite filler words such as "please".

## Section 6. Descriptive writing

- Limit paragraphs to a maximum of six sentences.
- Begin every paragraph with a clear topic sentence that defines the subject. All following sentences must directly support that topic sentence.
- Organize descriptive passages from general architecture down to specific implementation details.

## Section 7. Safety instructions and notices

Reserve safety keywords for genuine technical risks. Place notices immediately before the procedural step to which they apply.

### 1. WARNING

Use WARNING strictly for hazards that can cause irreversible data loss, production outages, or physical injury.
Format:
```text
WARNING: Running this command deletes all records in the production database. Make sure that you have an isolated backup before you continue.
```

### 2. CAUTION

Use CAUTION for conditions that can cause service degradation, invalid system state, build failures, or configuration corruption.
Format:
```text
CAUTION: Changing the default cipher suite disconnects legacy clients. Verify client compatibility before you apply the change.
```

### 3. NOTE

Use NOTE for non-hazardous technical data, prerequisite context, or architectural clarification. Notes must never contain commands or safety warnings.
Format:
```text
NOTE: The memory limit defaults to 512 megabytes when the configuration omits the parameter.
```

## Section 8. Punctuation

- Prohibit semicolons. Semicolons join clauses that belong in separate sentences. Split coordinate clauses into two distinct sentences separated by a period.
- Restrict colons. Use colons strictly to introduce an explicit vertical list, a table, or a code block. Never use colons as connectors in running text, for dramatic reveals, or as pseudo-labels.
- Prohibit slashes. Slashes introduce ambiguous logical relationships. Replace "and/or" with "a, b, or both". Replace "client/server" with "client and server".
- Restrict hyphens. Use hyphens only in approved compound words or compound Technical Names. Never use hyphens as dashes to separate clauses.
- Restrict parentheses. Use parentheses only for acronym expansions, numeric references, or tool cross-references. Never hide operational requirements, operating limits, or warnings inside parentheses.
- Structure vertical lists cleanly. List items must share parallel grammatical structure. Terminate list items with standard punctuation when they form complete sentences.

## Section 9. Writing practices

- Restructure instead of forcing awkward word-for-word substitutions. When replacing an unapproved word produces an unnatural sentence, rewrite the entire clause into a simpler grammatical structure.
- Prohibit phrasal verbs. Do not combine verbs with prepositions to invent idiomatic verbs. Write "examine" instead of "look into". Write "remove" instead of "take out". Write "continue" instead of "go on".
- Eliminate Latin abbreviations. Write "for example" instead of "e.g.". Write "that is" instead of "i.e.". Write "and others" or list items explicitly instead of "etc.".
- Anchor every pronoun. Pronouns such as "it", "this", and "they" must point unmistakably to the noun in the immediate clause. Repeat the noun when any ambiguity exists.
- Prohibit dangling participles. Ensure that the grammatical subject of the sentence performs the action in any introductory participial clause. Rewrite "When compiling the project, errors occurred" as "When you compile the project, the compiler reports errors."
