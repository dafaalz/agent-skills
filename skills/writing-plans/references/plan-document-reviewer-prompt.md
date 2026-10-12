# Plan document reviewer prompt template

Use this template when dispatching a plan document reviewer subagent to verify that the plan is complete, matches the spec, and provides proper task decomposition.

Dispatch after the complete plan is written.

```markdown
Task tool (general-purpose):
  description: "Review plan document"
  prompt: |
    You are a plan document reviewer. Verify this plan is complete and ready for implementation.

    Target plan. [PLAN_FILE_PATH]
    Source spec. [SPEC_FILE_PATH]

    ## What to check

    | Category | What to look for |
    |---|---|
    | Completeness | TODOs, placeholders, incomplete tasks, missing steps |
    | Spec alignment | Plan covers spec requirements, no major scope creep |
    | Task decomposition | Tasks have clear boundaries, steps are actionable |
    | Buildability | Could an engineer follow this plan without getting stuck? |

    ## Calibration

    Only flag issues that cause practical problems during implementation.
    An implementer building the wrong component or getting blocked is an issue.
    Minor phrasing, stylistic preferences, and advisory suggestions are not.

    Approve unless there are serious gaps, such as missing requirements from the spec,
    contradictory steps, placeholder content, or tasks too vague to execute.

    ## Output format

    ## Plan review

    Status. Approved | Issues Found

    Issues (if any).
    * [Task X, Step Y]. [specific issue]. [Why it matters for implementation]

    Recommendations (advisory, do not block approval).
    * [suggestions for improvement]
```

Reviewer returns status, issues (if any), and recommendations.
