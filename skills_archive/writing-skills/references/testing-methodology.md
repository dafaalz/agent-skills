# Testing Skills with Subagents

Testing process documentation follows test-driven development. Run baseline scenarios without the skill, observe where the agent deviates, write the skill to address those exact failure modes, verify compliance with the skill active, and close remaining loopholes.

## When to test

Test any skill that:
- Enforces strict workflow sequences (such as test-first development or pre-commit verification).
- Involves non-obvious operational choices where agents default to shortcuts.
- Requires multi-step tool interactions where intermediate validation is mandatory.

Pure reference documents that outline simple syntax or static lookup tables do not require baseline failure testing. Focus testing effort on procedural runbooks and discipline-enforcing rules.

## The testing cycle

Follow these four steps:

### 1. Baseline test (RED)

Launch a subagent on a concrete coding or operational task without loading the candidate skill.
- Provide a realistic prompt representing standard project work.
- Record the subagent choices, commands, and written explanations.
- Identify the exact points where the subagent takes shortcuts, skips verification, or violates desired project conventions.

Completion criterion: A written log documenting the unguided agent failure modes and exact explanations.

### 2. Targeted drafting (GREEN)

Write the minimal skill instructions required to prevent the observed baseline failures.
- Address the specific rationalizations recorded during the baseline run.
- Provide positive operational instructions paired directly with any necessary boundaries.
- Keep instructions focused on the observed failures without adding speculation about hypothetical edge cases.

Completion criterion: A drafted skill document addressing every documented failure from the baseline test.

### 3. Compliance verification (VERIFY GREEN)

Dispatch a fresh subagent with the candidate skill loaded into its context.
- Run the identical task scenario used during the baseline phase.
- Verify that the subagent follows the defined steps in sequence.
- Check that the subagent produces required intermediate artifacts and verification outputs.

Completion criterion: The subagent completes the task following every instruction without skipping validation steps.

### 4. Loophole closure (REFACTOR)

Review the subagent transcript for friction points or newly discovered shortcuts:
- If the subagent finds a way to bypass a requirement while technically following the letter of the instruction, add an explicit counter.
- Prune instructions that produced no measurable effect on behavior.
- Retest with a fresh subagent to confirm compliance remains stable.

Completion criterion: Zero observed shortcuts across two consecutive test runs.

## Designing test scenarios

A reliable test scenario requires three elements:

1. Concrete context: Provide realistic code, configuration files, and dependencies. Do not use abstract or contrived riddles.
2. Competing incentives: Present tasks where a shortcut looks tempting (such as having working code that lacks automated tests, or an urgent bug report requiring quick fixes).
3. Objective evaluation: Define a binary condition for success (such as running a test command before editing production code, or writing an implementation plan before touching source files).
