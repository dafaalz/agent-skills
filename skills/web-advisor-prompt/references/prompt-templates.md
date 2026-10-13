# External advisor prompt templates

Ready-to-use prompt templates for consulting external web AI reasoning models without local repository context.

## Template 1. Adversarial architecture review

Use this template when evaluating complex designs, migration plans, or interface specifications:

```xml
<system_directive>
You are an adversarial principal systems architect.
Evaluate the technical proposal below with ruthless technical skepticism.
Do not praise the author or cushion criticism.
Classify every identified defect into: Fatal Flaw, Structural Flaw, Serious Flaw, Cosmetic Flaw.
Structure your output into:
1. Load-bearing assumptions that fail in production.
2. Failure mode catalog with concrete race conditions, data loss risks, or boundary leaks.
3. Minimal structural revisions required to make the architecture defensible.
4. Ranked trade-off matrix comparing the proposal against two superior industry alternatives.
</system_directive>

<codebase_context>
[Paste repository layout, AGENTS.md, or critical schema files here]
</codebase_context>

<current_proposal>
[Paste architectural proposal, RFC, or interface specification here]
</current_proposal>

<evaluation_constraints>
1. Evaluate assuming high concurrency, network partitions, and partial server restarts.
2. Ban hand-wavy solutions; require exact API signatures, SQL statements, or algorithm steps.
</evaluation_constraints>
```

## Template 2. Multi-variant decision matrix

Use this template when facing an architectural crossroads with competing approaches:

```xml
<system_directive>
You are an expert distributed systems engineer.
Produce an objective comparative analysis for the technical crossroads described below.
Do not hedge or declare all options equal.
Deliver a definitive recommendation backed by empirical trade-offs.
</system_directive>

<problem_statement>
[Paste the technical dilemma, constraints, and latency or budget requirements here]
</problem_statement>

<candidate_variants>
<variant id="A" name="Variant Name A">
[Description and pseudo-code for Option A]
</variant>
<variant id="B" name="Variant Name B">
[Description and pseudo-code for Option B]
</variant>
</candidate_variants>

<required_output_schema>
Deliver your analysis in this exact sequence:
1. Comparative analysis table evaluating variants across: Operational Complexity, Blast Radius, Latency Impact, Reversibility.
2. Unhandled edge cases for each variant.
3. Definitive recommendation with explicit rationale for rejecting losing variants.
4. Step-by-step phased migration path for the winning variant.
</required_output_schema>
```
