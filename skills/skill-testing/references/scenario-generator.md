# Scenario generator for empirical skill testing

Framework for formulating three contrasting micro-component test scenarios across visual frontend, backend logic, and technical writing domains.

## 1. Core principles of scenario design

Empirical A/B testing succeeds only when test scenarios stress-test opposing operational boundaries of a target skill:

1. **Avoid full-page requests.** Restrict every scenario to a self-contained micro-component (under 120 lines of code). Full-page prompts waste tokens and introduce extraneous variables.
2. **Enforce contrasting requirements.** Formulate scenarios across three distinct stress axes: strict utility, dynamic tactile physics, and expressive narrative depth.
3. **Identical master prompt contract.** Candidate A and Candidate B must receive the exact same master prompt down to the character. Never inject candidate-specific hints into scenario prompts.
4. **Golden benchmark deconstruction.** When the user provides a high-quality production reference artifact or URL (such as an Awwwards showcase, production repo file, or benchmark HTML), deconstruct its specific mechanics first. Identify what makes it superior (rendering pipelines, physics formulas, easing tokens, and visual layers). Formulate the three scenarios to directly test whether candidate skills can reproduce those specific mechanics without regressing on basic functional invariants.

## 2. Visual frontend and UI motion domain archetypes

When benchmarking frontend, CSS, or motion engineering skills, generate these three contrasting component specifications:

### Scenario 1. High-frequency transactional utility
- Component: Command palette modal or keyboard-navigated select dropdown.
- Stress axis: Zero latency, keyboard shortcuts (`Escape`, `ArrowDown`, `Enter`), ARIA dialog attributes, strict sub-250ms duration budgets, zero decorative distraction.
- Evaluation benchmark: Does the candidate preserve immediate utility without sluggish lag?

### Scenario 2. Tactile dynamic interaction
- Component: Interactive spotlight metric card or magnetic sliding pill navigation.
- Stress axis: Continuous pointer coordinate tracking (`--sx`, `--sy`), fluid bounding rect geometry transfer, physics damping or spring curves, hover and active states.
- Evaluation benchmark: Does the component provide responsive tactile feedback without frame stuttering?

### Scenario 3. Expressive editorial or narrative component
- Component: Headline entrance with kinetic typography or showcase card with curtain wipe mask and windowed image parallax.
- Stress axis: Staggered reveal timing (40ms to 70ms), asymmetric curves (`cubic-bezier(0.16, 1, 0.3, 1)` or `cubic-bezier(0.22, 1, 0.36, 1)`), optical depth-of-field blur, or procedural noise grain.
- Evaluation benchmark: Does the component convey craft, visual weight, and cinematic pacing?

## 3. Backend logic and architecture domain archetypes

When benchmarking backend, database, or architectural design skills:

### Scenario 1. High-throughput query and data integrity
- Task: Model relationship query with eager loading, pagination, and strict database index alignment.
- Stress axis: Elimination of N+1 query traps, zero memory leaks on large recordsets, and atomic transaction safety.

### Scenario 2. Domain boundary and value object encapsulation
- Task: Order payment status transition or multi-currency monetary balance calculation.
- Stress axis: Single responsibility principle, invariant protection, custom typed value objects, and zero state mutation leaks.

### Scenario 3. Integration flow and edge-case resilience
- Task: Webhook ingestion endpoint with idempotent signature verification and queue dispatch.
- Stress axis: Replay attack prevention, network retry handling, graceful failure degradation, and structured audit logging.

## 4. Technical writing and prose domain archetypes

When benchmarking writing, agent runbooks, or localization skills:

### Scenario 1. Concise CLI command reference
- Stress axis: Mechanical grounding, zero promotional throat-clearing, copy-pasteable shell commands, and explicit error code exit tables.

### Scenario 2. Complex architectural decision record
- Stress axis: Balanced trade-off exploration, absence of false contrasts, grounded counter-arguments, and active voice sentence cadence.

### Scenario 3. Incident post-mortem walkthrough
- Stress axis: Concrete timeline metrics, elimination of hedging adverbs, direct root cause attribution, and actionable preventative invariants.
