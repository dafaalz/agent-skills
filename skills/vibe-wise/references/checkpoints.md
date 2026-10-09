# Checkpoint formats and presentation rules

Use these checkpoint templates to maintain learner ownership and verify scope before writing code.

## Checkpoint types and exact syntax

Prefix each checkpoint with a bold heading containing the exact checkpoint type.

### 1. Build checkpoint

Use to probe how the learner wants to model the system or handle a specific technical problem.

Syntax:

```markdown
Build checkpoint: <topic>

<Socratic question focused on one specific architectural decision, data relationship, or failure case.>
```

Execution rules:
- Ask one question per turn.
- Wait for the user to state their approach.
- Do not propose code or database schema inside a Build checkpoint.

### 2. Design checkpoint

Use to summarize the agreed architecture before finalizing scope.

Syntax:

```markdown
Design checkpoint: <topic>

Proposed approach:
<Factual summary of the user's architectural decision in 2 to 3 sentences.>

Trade-offs:
<Direct statements of accepted trade-offs, such as extra query overhead or storage costs.>

Proposed additions:
| Detail | Proposal | Why it matters |
|---|---|---|
| Indexing | Add index on `folder_id` | Speeds up lookup from O(N) to O(log N) |

Next actions:
1. Confirm and continue. This approach makes sense, proceed to implementation scope.
2. Discuss. Ask questions or adjust the design before deciding.
```

Execution rules:
- Keep the proposed additions table minimal. Include only details necessary for stability, data integrity, or performance.
- Wait for user confirmation before moving to implementation.

### 3. Implementation checkpoint

Use to authorize code changes for a single, scoped component.

Syntax:

```markdown
Implementation checkpoint: <topic>

Target changes:
- Create `src/models/membership.py` with foreign key definitions.
- Add migration file in `migrations/` for the join table.
- Add unit test in `tests/test_membership.py` covering deletion isolation.

Next actions:
1. Implement this step. Write the code and run the tests for this scoped step.
2. Discuss. Adjust the scope or clarify details before writing code.
```

Execution rules:
- Limit scope to one testable piece. Never bundle entire multi-tier architectures into a single implementation step.
- Wait for user confirmation before writing or modifying files.

### 4. Implementation report

Output immediately after writing code and running verification checks.

Syntax:

```markdown
Implementation report: <topic>

Summary of changes:
- Created `src/models/membership.py`: defined `Membership` model linking `user_id` and `workspace_id`.
- Added migration `migrations/003_create_memberships.sql`: created table with unique composite constraint.
- Added test in `tests/test_membership.py`: verified that deleting a workspace removes linked memberships.

Verification:
- Command run: `pytest tests/test_membership.py`
- Result: 2 passed in 0.14s.

Architecture alignment:
<One sentence explaining how the code reflects the user's design choice.>
```

Execution rules:
- Name the exact files modified and commands executed.
- State test results factually without self-congratulatory adjectives.
