---
name: writing-plans
description: Create phased implementation plans with test-first tasks from a design specification before writing code. Use when creating phased implementation plans with test-first tasks from a design specification before writing code. Don't use for initial design ideation, exploratory research, or direct code execution.
---

# Writing implementation plans

Turn validated design specifications into phased implementation plans before writing code. Every task in the plan must produce working, testable software with clear file targets, behavioral test assertions, interface contracts, and deterministic verification commands.

Assume the implementer has no prior context of the codebase and requires explicit technical direction for every change.

Announce the following message at session start:
`I am using the writing-plans skill to create the implementation plan.`

Save plans to `docs/superpowers/plans/YYYY-MM-DD-<feature-name>.md` as transient scaffolding artifacts unless the user specifies a different path. Implementation plans are transient execution scaffolding. After implementation is complete and verified, the plan file should be purged to keep the repository clean.

## Workflow

Follow these four steps in sequence:

### Step 1. Scope audit and file mapping

Inspect the specification and repository structure before creating tasks:
- Verify subsystem boundaries. If the specification covers multiple independent subsystems, split the work into separate plans for each subsystem.
- Map target files. Identify every file to create, modify, or delete, along with its specific responsibility.
- Enforce single responsibility. Design units with clear boundaries and well-defined interfaces. Keep files focused so an agent can reason about them within context.
- Co-locate related logic. Group files by functional responsibility rather than technical layer. Files that change together belong together.
- Follow repository conventions. Match existing file and directory patterns. If an existing file is already unwieldy, include a planned split into smaller modules.

Completion criterion. A complete inventory of target files mapped to clear responsibilities, confirmed to belong to a single cohesive subsystem.

### Step 2. Task decomposition and plan drafting

Draft the implementation plan using the templates in the reference section below:
- Add the required plan document header at the top of the file.
- Divide the work into bite-sized tasks. Each task must represent a single component or slice that takes 2 to 5 minutes to execute.
- Enforce test-driven development order for every task:
  1. Write the failing test.
  2. Run the test and confirm failure.
  3. Write minimal implementation code to pass the test.
  4. Run the test and confirm success.
  5. Commit changes with a descriptive message.
- Provide exact file paths, exported signatures, and test assertion contracts. Do not guess application implementation details that the compiler and language server validate.
- Specify exact execution commands with expected exit codes or failure messages for every test step.
- Ensure tasks remain self-contained with explicit inputs, outputs, and behavioral boundaries.

Completion criterion. A drafted plan document containing the mandatory header, granular test-driven tasks, interface contracts, and exact verification commands.

### Step 3. Plan self-review and validation

Audit the drafted plan against the source specification:
- Verify specification coverage. Skim each section of the specification and verify that an explicit task implements it. Add tasks for any missing requirements.
- Scan for placeholders. Confirm that the plan contains zero instances of TODO, TBD, vague validation rules, or undefined target interfaces.
- Verify signature consistency. Confirm that function names, argument lists, and types match across all tasks.
- Optional reviewer subagent. For automated validation, dispatch a subagent using the prompt in `plan-document-reviewer-prompt.md`. Fix all identified defects directly in the plan file.

Completion criterion. The plan document contains zero placeholders, covers all specification requirements, and maintains consistent method signatures throughout.

### Step 4. Execution handoff

Save the plan to disk and present execution options to the user:
- State the saved path clearly.
- Offer the two execution workflows:
  1. Subagent-driven execution (recommended). Dispatches a fresh subagent for each task with reviews between tasks. Requires `subagent-driven-development`.
  2. Inline execution. Executes tasks batch-by-batch within the current session with review checkpoints. Requires `executing-plans`.
- Wait for the user to choose an execution option before executing any tasks.

Completion criterion. The plan file is written to disk and the user is prompted with the execution options.

## Reference templates and rules

### Plan document header template

Every plan must start with this header block:

```markdown
# [Feature Name] Implementation Plan

> **For agentic workers.** REQUIRED SUB-SKILL. Use subagent-driven-development (recommended) or executing-plans to implement this plan task by task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal.** [One sentence describing what this builds]

**Architecture.** [2 to 3 sentences about approach]

**Tech stack.** [Key technologies and libraries]

---
```

### Task structure template

Structure each task with explicit file lists, step checkboxes, interface contracts, and test commands:

````markdown
### Task N. [Component name]

**Files**
- Create `exact/path/to/file.py`
- Modify `exact/path/to/existing.py:123-145`
- Test `tests/exact/path/to/test.py`

- [ ] **Step 1. Write the failing test**

```python
def test_specific_behavior():
    result = function(input)
    assert result == expected
```

- [ ] **Step 2. Run test to verify it fails**

Run `pytest tests/path/test.py::test_name -v`
Expected failure with missing implementation or failed assertion.

- [ ] **Step 3. Write minimal implementation**

```python
def function(input):
    return expected
```

- [ ] **Step 4. Run test to verify it passes**

Run `pytest tests/path/test.py::test_name -v`
Expected status: 0 errors, all assertions pass.

- [ ] **Step 5. Commit**

```bash
git add tests/path/test.py src/path/file.py
git commit -m "feat: add specific feature"
```
````

### Task and interface precision standards

Every step must provide precise contract specifications without duplicating full implementation code in markdown:
- Specify exact file paths and function signatures. Do not write placeholders like `// TODO`.
- Define test assertions and expected inputs and outputs rather than speculative application bodies.
- Rely on the compiler, linter, and test runner for syntax validation during execution.
- Define imported symbols, method signatures, and error types within the plan.

### Goal-driven execution standards

Transform abstract requirements into concrete, verifiable test goals:
- Convert open-ended instructions into testable gates. For example, "add input validation" becomes "write tests asserting failure on invalid inputs, then make them pass".
- Pair every multi-step action with an explicit verification check specifying the exact test command and expected outcome. Strong success criteria enable autonomous verification loops without constant clarification.
