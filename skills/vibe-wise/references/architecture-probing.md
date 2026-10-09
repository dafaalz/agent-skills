# Architecture probing and Socratic heuristics

This reference guides Socratic questioning during system design. Use these patterns during Step 2 of the workflow to probe boundaries, data relationships, and failure modes without deciding for the user.

## Four pillars of system design probing

Examine systems across four distinct technical areas. Address one area at a time.

### 1. System boundaries and requirements

Probe the functional scope, expected throughput, and latency bounds before discussing storage or frameworks.

Probe questions:
- What are the core inputs and expected outputs of this subsystem?
- What are the expected read and write traffic volumes per second?
- Which external systems does this service interact with, and what happens if an external system becomes unavailable?

### 2. Data modeling and entity relations

Probe the relationship between domain entities and state persistence.

Probe questions:
- How do these two entities relate, one-to-one, one-to-many, or many-to-many?
- When a parent record is deleted, what happens to associated child records?
- How will the system prevent record duplication without copying entire payloads?

### 3. Component interactions and contracts

Probe the interaction style between services or internal modules.

Probe questions:
- Should this operation run synchronously in the request cycle or asynchronously in a background job?
- What payload contract will the client receive upon initial submission?
- How will callers track long-running work if processing takes more than two seconds?

### 4. Failure modes, concurrency, and trade-offs

Probe edge cases, race conditions, and network splits.

Probe questions:
- What prevents two concurrent requests from modifying the same record simultaneously?
- If the database write succeeds but the notification fails, how does the system recover state?
- How does the system handle duplicate webhooks or retried requests without creating duplicate records?

## Teaching rules and explanation callouts

When the user states they do not recognize a pattern or technology, provide concise technical instruction before asking for their decision.

Format explanations using these exact callout blocks:

```markdown
Concept: <name of technology or pattern>
<Direct factual explanation in 2 to 4 sentences without filler phrases.>

Why this matters:
<Concrete operational impact on the current feature or system.>
```

Rules for teaching:
1. Explain the mechanism directly. Do not quiz the user on definitions.
2. After explaining the concept, return the architecture question to the user. Do not pick the approach automatically.
3. If the user asks for alternatives, present two to three options with explicit trade-offs in a table. Ask the user to select one option.
