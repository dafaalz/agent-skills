---
name: web-advisor-prompt
description: Use when packaging repository context, architectural dilemmas, or design trade-offs into an adversarial zero-context advisory prompt for an external frontier web AI or reasoning model. Don't use for local subagent dispatch, internal routine code generation, or user-facing chat.
---

# Web advisor prompt

Package repository context, architectural proposals, and complex engineering dilemmas into dense, zero-context prompts for external frontier reasoning models like Google DeepMind Gemini 4 Argon. Prevent sycophancy, structure context using XML delimiters, and elicit adversarial peer reviews.

## Modes

Select the packaging mode before Step 1:
- Adversarial review mode (default). Package a technical design, RFC, or codebase refactor into an adversarial stress-test prompt that forces the external model to identify fatal flaws before offering recommendations.
- Synthesis and options mode. Package an architectural crossroads into an objective trade-off evaluation matrix comparing two or three competing engineering variants.

## Reference modules

Load reference manuals on demand based on prompt scope:

| Concern | Reference file |
|---|---|
| Gemini 4 Argon reasoning mechanics | [references/gemini-argon-mechanics.md](references/gemini-argon-mechanics.md) |
| Anti-sycophancy framing | [references/anti-sycophancy-framing.md](references/anti-sycophancy-framing.md) |
| Ready XML prompt templates | [references/prompt-templates.md](references/prompt-templates.md) |

## Workflow

Follow these four steps in sequence.

### Step 1. Context extraction and artifact assembly

Extract essential codebase facts, schemas, and architectural boundaries while discarding conversational chat noise:
1. Identify the target dilemma or proposal under evaluation.
2. Read project convention files (`AGENTS.md`, `CODEBASE.md`) and database schemas (`schema.prisma`, migrations, or model files) to ground domain terms.
3. Isolate the exact decision boundary, performance constraints, and external dependencies.
4. Filter out chat conversational baggage, personal commentary, and unresolved speculative tangents.

Completion criterion. An isolated text dossier containing the core proposal, concrete schema definitions, performance constraints, and explicit trade-off questions.

### Step 2. Anti-sycophantic frame and role calibration

Calibrate the system directive to disarm model agreeableness and prevent conversational validation loops:
1. Assign a skeptical specialist role, such as Principal Systems Architect or Adversarial Peer Reviewer. Consult `references/anti-sycophancy-framing.md`.
2. Prohibit praise, sycophantic validation, and conversational pleasantries.
3. Enforce an inverted order of reasoning. Require the external model to articulate fatal flaws and unhandled race conditions before providing recommendations.
4. Establish a four-tier severity classification rubric: Fatal Flaw, Structural Flaw, Serious Flaw, Cosmetic Flaw.

Completion criterion. A written system directive block mandating ruthless skepticism, flaw prioritization, and zero conversational flattery.

### Step 3. XML payload packaging and delimiter isolation

Assemble the complete prompt payload following long-context Gemini prompt engineering standards:
1. Structure payload sections using uppercase XML delimiters: `<system_directive>`, `<codebase_context>`, `<current_proposal>`, `<evaluation_criteria>`, and `<required_output_schema>`. Consult `references/prompt-templates.md`.
2. Place massive background context, schema documents, and interface definitions at the beginning of the prompt body. Consult `references/gemini-argon-mechanics.md`.
3. Position actionable instructions, evaluation questions, and output schemas at the absolute end of the prompt to focus attention.
4. Avoid redundant step-by-step reasoning instructions. Rely on native thinking capabilities without cluttering output.

Completion criterion. A unified XML-delimited prompt payload with background context anchored first and actionable instructions positioned last.

### Step 4. Verification and emission

Audit the generated prompt payload against prompt engineering standards before delivering to the user:
1. Context verification. Confirm that all necessary entity names, type signatures, and architectural constraints are self-contained so an external model with zero repository access understands the system completely.
2. Neutral framing check. Confirm that the prompt does not leak the author preferred solution or bias the model toward a pre-selected outcome.
3. Slop and punctuation check. Confirm that the prompt contains zero em dashes, zero en dashes, and zero pseudo-labels outside quoted code.
4. Emit the complete prompt in a single fenced Markdown code block ready for copying into the external web interface.

Completion criterion. The validated prompt is output inside a copyable code fence accompanied by clear paste instructions for the web AI.

## Common prompting traps

| Trap | Consequence | Corrective action |
|---|---|---|
| Leading question | External model flatters user bias | Frame dilemma as neutral trade-off between two concrete variants |
| Missing schema context | Model hallucinates generic abstractions | Paste verified database schemas and route definitions into `<codebase_context>` |
| Instructions at prompt top | Instructions get diluted by long context payloads | Move actionable tasks and output schemas to the bottom of the prompt |
| Unconstrained output format | Model outputs unfocused conversational essays | Enforce numbered Markdown sections and comparison tables |
| Redundant CoT prompts | Clutters Gemini 4 Argon native thinking engine | Specify clear evaluation criteria instead of manual step-by-step guidance |

## Boundary isolation

Draft prompt payloads for external evaluation only. Do not execute remote web requests, send proprietary secrets outside approved environments, or alter local project code files during prompt formulation.

## Quick audit checklist

Run this check before emitting the advisor prompt:

| Check | Passing condition |
|---|---|
| Zero context self-containment | All domain models and constraints fully specified without local repository dependencies |
| Anti-sycophancy directive | Explicitly mandates skepticism and prioritizes fatal flaws before advice |
| Long-context layout | Context documents positioned at top; instructions and output schema at bottom |
| Delimiter integrity | Distinct XML tags isolate system directive, context, proposal, and tasks |
| Neutrality | Dilemmas presented without telegraphing a preferred choice |
| Copyable output | Complete prompt emitted in a single code fence ready for clipboard copy |
