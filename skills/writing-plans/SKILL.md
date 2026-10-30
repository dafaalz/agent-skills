---
name: writing-plans
description: "Use when creating phased implementation plans with test-first tasks from a design specification before writing code. Don't use for initial design ideation (use brainstorming), exploratory research (use recursive-research), direct code execution (use executing-plans), or multi-task plan verification and audit defense (use agent-planning)."
---

# Writing implementation plans

Turn validated design specifications into phased implementation plans before writing code. Every task in the plan must produce working, testable software with clear file targets, behavioral test assertions, interface contracts, and deterministic verification commands.

Assume the implementer has no prior context of the codebase and requires explicit technical direction for every change.

<HARD-GATE>
Write-Target Boundary. Write only to `docs/superpowers/plans/` and `.agents/state/writing-plans/`. Do not modify application source, tests, schemas, or build configuration while drafting or reviewing a plan.
</HARD-GATE>

Save plans to `docs/superpowers/plans/YYYY-MM-DD-<feature-name>.md` as transient scaffolding artifacts unless the user specifies a different path. Implementation plans are transient execution scaffolding. The purge happens in `executing-plans` after final verification. This skill does not purge the plan file.

## Modes

Select a planning mode before Step 1:
- Author mode (default). Draft new implementation plans with test-first tasks from design specifications.
- Review mode. Audit existing implementation plans against design specs and anti-slop rules without modifying plan status.

## Boundary isolation

Writing plans produces transient execution scaffolding only (`docs/superpowers/plans/`). Never write production application code, modify existing tests, or alter repository code files while drafting implementation plans.

Precedence. This skill owns task content and plan structure. `agent-planning` owns the evidence seal and audit response.

## Workflow

Follow these four steps in sequence.

### Step 1. Scope audit and file mapping

Inspect the specification and repository structure before creating tasks:
- Verify subsystem boundaries. If the specification covers multiple independent subsystems, split the work into separate plans for each subsystem.
- Map target files. Identify every file to create, modify, or delete, along with its specific responsibility.
- Enforce single responsibility. Design units with clear boundaries and well-defined interfaces. Keep files focused so an agent can reason about them within context.
- Co-locate related logic. Group files by functional responsibility rather than technical layer. Files that change together belong together.
- Follow repository conventions. Match existing file and directory patterns. If an existing file is already unwieldy, include a planned split into smaller modules.

Completion criterion. `.agents/state/writing-plans/file-map.json` exists with every target file, its responsibility, and its subsystem.

### Step 2. Task decomposition and plan drafting

Draft the implementation plan using the templates in the reference section below:
- Add the required plan document header at the top of the file.
- Divide the work into bite-sized tasks. Each task touches at most 2 production files and 1 test file.
- Tracer-bullet vertical slices. Build an end-to-end thin slice spanning all required layers first to prove integration before broadening feature breadth.
- Declare blocking dependencies. Every task must declare its blocking dependencies (`Depends on: Task X`) to form an explicit Directed Acyclic Graph (DAG) for concurrent subagent execution across the ready frontier.
- Enforce test-driven development order for every task:
  1. Write the failing test.
  2. Run the test and confirm failure.
  3. Write minimal implementation code to pass the test.
  4. Run the test and confirm success.
  5. Commit changes with a descriptive message.
- Provide exact file paths, exported signatures, and test assertion contracts. Do not guess application implementation details that the compiler and language server validate.
- Specify exact execution commands with expected exit codes or failure messages for every test step.
- Ensure tasks remain self-contained with explicit inputs, outputs, and behavioral boundaries.

Completion criterion. The plan exists at `docs/superpowers/plans/YYYY-MM-DD-<feature-name>.md` with the mandatory header, test-first tasks, interface contracts, and exact verification commands.

### Step 3. Plan self-review and validation

Audit the drafted plan against the source specification:
- Verify specification coverage. Skim each section of the specification and verify that an explicit task implements it. Add tasks for any missing requirements.
- Scan for placeholders. Confirm that the plan contains zero instances of TODO, TBD, vague validation rules, or undefined target interfaces.
- Verify signature consistency. Confirm that function names, argument lists, and types match across all tasks.
- Reviewer subagent. Dispatch a subagent with the prompt in `references/plan-document-reviewer-prompt.md` and fix every defect it reports in the plan file.

Completion criterion. `.agents/state/writing-plans/audit.md` exists with zero placeholders, one task per specification section, and consistent signatures.

### Step 4. Execution handoff

Save the plan to disk and present execution options to the user:
- State the saved path clearly.
- Offer the two execution workflows:
  1. Subagent-driven execution (recommended). Dispatch a fresh subagent for each task with a review of its diff between tasks. Run every task through the harness subagent tool.
  2. Inline execution. Executes tasks batch-by-batch within the current session with review checkpoints. Requires `executing-plans`.
- Wait for the user to choose an execution option before executing any tasks.

Completion criterion. Plan file written to disk and execution options presented to the user.

## Reference templates and rules

### Plan document header template

Every plan must start with this header block:

```markdown
# [Feature Name] Implementation Plan

> **For agentic workers.** REQUIRED SUB-SKILL. Use `executing-plans` to implement this plan task by task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal.** [One sentence describing what this builds]

**Architecture.** [2 to 3 sentences about approach]

**Tech stack.** [Key technologies and libraries]

**Source spec.** [<absolute-or-repo-relative-path-to-spec-or-none>]

---
```

### Task structure template

Structure each task with explicit file lists, dependencies, step checkboxes, interface contracts, and test commands:

````markdown
### Task N. [Component name]

**Dependencies.** Depends on Task 1. Blocks Task 3.

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
Expected status is 0 errors, all assertions pass.

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
- Convert open-ended instructions into testable gates. For example, \"add input validation\" becomes \"write tests asserting failure on invalid inputs, then make them pass\".
- Pair every multi-step action with an explicit verification check that defines the exact test command and expected outcome.

## Anti-patterns

| ID | Title | Pattern description | Why it fails | Concrete fix |
|---|---|---|---|---|
| WPA-1 | Phantom execution skill | Names a skill directory that does not exist | Handoff fails at discovery | Name an existing skill and confirm with `test -d skills/<name>` |
| WPA-2 | Unanchored task map | Step 1 ends with no file on disk | The next session cannot resume | Write the file map to `.agents/state/writing-plans/file-map.json` |
| WPA-3 | Clock-based granularity | Bounds task size in minutes no step measures | Agents split work arbitrarily | Bound by production file count and diff size |
| WPA-4 | Optional verification | Marks the plan audited while the reviewer is optional | Unreviewed plans pass the gate | Make the reviewer mandatory or drop the audit claim |
| WPA-5 | Narration preamble | Announces the skill in chat before any artifact exists | Wastes reader attention | Delete the announcement |

## Quick audit checklist

| Check | Passing condition |
|---|---|
| Header structure | Mandatory plan header present with goal, architecture, and stack |
| Task granularity | Bite-sized 2 to 5 minute tasks with test-first sequence |
| Dependency graph | Every task declares explicit blocking dependencies (DAG) with tracer-bullet sequencing |
| Verification commands | Exact test commands and expected exit codes or failure messages provided |
| Zero placeholders | Zero instances of TODO, TBD, or speculative application logic |
| Reference isolation | Scaffolding plans placed under `docs/superpowers/plans/` |
