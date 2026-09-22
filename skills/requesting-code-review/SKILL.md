---
name: requesting-code-review
description: Use when completing tasks, implementing major features, or before merging to verify work meets requirements.
---

# Requesting code review

Dispatch the code reviewer subagent to catch issues before they cascade. The reviewer gets precisely crafted context for evaluation, never your session history. This keeps the reviewer focused on the work product rather than your thought process, preserving your own context for continued work.

**Core principle.** Review early, review often.

## When to request review

**Mandatory:**
- After each task in subagent-driven development
- After completing major feature
- Before merge to main

**Optional but valuable:**
- When stuck (fresh perspective)
- Before refactoring (baseline check)
- After fixing complex bug

## How to request

**1. Get git SHAs:**
```bash
BASE_SHA=$(git rev-parse HEAD~1)  # or origin/main
HEAD_SHA=$(git rev-parse HEAD)
```

**2. Dispatch code-reviewer subagent:**

Use Task tool with the code reviewer subagent type, filling the template at `code-reviewer.md`.

**Placeholders:**
- `{WHAT_WAS_IMPLEMENTED}`, what was built
- `{PLAN_OR_REQUIREMENTS}`, what it should do
- `{BASE_SHA}`, starting commit
- `{HEAD_SHA}`, ending commit
- `{DESCRIPTION}`, brief summary

**3. Act on feedback:**
- Fix Critical issues immediately
- Fix Important issues before proceeding
- Note Minor issues for later
- Push back if reviewer is wrong with technical reasoning

## Example

```
[Just completed Task 2: Add verification function]

You: Let me request code review before proceeding.

BASE_SHA=$(git log --oneline | grep "Task 1" | head -1 | awk '{print $1}')
HEAD_SHA=$(git rev-parse HEAD)

[Dispatch code-reviewer subagent]
  WHAT_WAS_IMPLEMENTED: Verification and repair functions for conversation index
  PLAN_OR_REQUIREMENTS: Task 2 from docs/superpowers/plans/deployment-plan.md
  BASE_SHA: a7981ec
  HEAD_SHA: 3df7661
  DESCRIPTION: Added verifyIndex() and repairIndex() with 4 issue types

[Subagent returns]:
  Strengths: Clean architecture, real tests
  Issues:
    Important: Missing progress indicators
    Minor: Magic number (100) for reporting interval
  Assessment: Ready to proceed

You: [Fix progress indicators]
[Continue to Task 3]
```

## Integration with workflows

**Subagent-driven development:**
- Review after each task
- Catch issues before they compound
- Fix before moving to next task

**Executing plans:**
- Review after each batch of tasks
- Get feedback, apply, continue

**Ad-hoc development:**
- Review before merge
- Review when stuck

## Red flags

**Never:**
- Skip review because the task seems simple
- Ignore Critical issues
- Proceed with unfixed Important issues
- Argue without valid technical reasoning

**If reviewer wrong:**
- Push back with technical reasoning
- Show code and tests that prove functionality
- Request clarification

See template at `requesting-code-review/code-reviewer.md`.
