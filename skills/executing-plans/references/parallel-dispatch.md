# Parallel subagent dispatch and domain partitioning

Guidance for partitioning independent task domains and dispatching concurrent subagents during plan execution.

## 1. Domain partitioning criteria

Investigating multiple unrelated failures or executing disjoint tasks sequentially wastes execution time. Independent problems do not require shared context.

Dispatch one subagent per independent domain when all of these conditions hold.

- Tasks touch disjoint target files with zero overlap.
- Subsystems fail or operate independently.
- An investigator can understand each defect or feature slice without inspecting other subsystems.
- Tasks share no disk state, database records, or shared mock state.

Do not dispatch parallel agents when any of these conditions hold.

- Failures share a root cause where one fix resolves multiple errors.
- Understanding the defect requires inspecting whole system state.
- Tasks require exploratory debugging before identifying the root issue.
- Agents edit the same target files or compete for identical execution resources.

## 2. Partitioning workflow

Follow this sequence to partition and execute parallel tasks.

1. Group tasks by subsystem, component directory, or test file.
2. Confirm zero file overlap between agent targets using git status or file list comparison.
3. Construct isolated task prompts containing full instructions and scope boundaries.
4. Launch subagents concurrently using background dispatch tools without active polling loops.
5. Review completed reports, inspect diffs across workspaces, and run the combined regression suite.

## 3. Subagent prompt template

Use this standardized template when constructing prompts for parallel subagents.

```markdown
Fix the 3 failing tests in src/agents/agent-tool-abort.test.ts.

1. Test "should abort tool with partial output capture", expects 'interrupted at' in message
2. Test "should handle mixed completed and aborted tools", fast tool aborted instead of completed
3. Test "should properly track pendingToolCount", expects 3 results but gets 0

Follow these steps.

1. Read the test file and identify what each test verifies.
2. Identify the root cause, distinguishing timing bugs from functional defects.
3. Resolve the failure cleanly.
   - Replace arbitrary timeouts with event-based waiting.
   - Fix abort logic in the source implementation if broken.
   - Adjust test expectations only if intentional behavior changed.

Do not increase timeout durations. Fix the underlying defect.
Do not edit files outside src/agents/agent-tool-abort.test.ts and its direct implementation.

Return format.
- Root cause diagnosis
- Modified files and diff summary
- Test execution output confirming green status
```

## 4. Anti-patterns and corrective actions

| Anti-pattern | Failure mechanism | Corrective action |
|---|---|---|
| Broad scope assignment | The subagent inspects multiple subsystems and loses focus | Assign exactly one test file or subsystem per agent |
| Missing error context | The subagent wastes cycles searching for failure points | Provide exact error messages, stack traces, and test names |
| Unbounded file permissions | The subagent refactors shared utilities and breaks systems | Prohibit modifications outside assigned target files |
| Vague completion format | The subagent reports completion without evidence | Require root cause diagnosis, file diffs, and test output |
| Shared resource collision | Agents mutate the same database table concurrently | Isolate test databases or sequence dependent tasks |
