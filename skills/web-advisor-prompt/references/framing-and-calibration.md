# Anti-sycophancy framing and model calibration

Reference manual for disarming RLHF agreeableness loops, enforcing one unified severity rubric, and preserving KV prompt caches across frontier reasoning models.

## Anti-sycophancy rules

1. **Disagreement as baseline.** Mandate identifying structural defects and unhandled failure modes as the minimum passing standard.
2. **Inverted critique order.** Require Fatal and Structural defects before any synthesis or positive recommendation.
3. **Neutral proposal staging.** State constraints and failure tolerances in `<current_proposal>` without revealing a preferred option.

## Unified four-tier severity taxonomy

Use these exact definitions across all profiles and templates:

| Severity tier | Strict definition | Action gate |
|---|---|---|
| Fatal flaw | Confirmed data loss, security compromise, or complete system unrecoverability | Halts implementation until redesigned |
| Structural flaw | Boundary violation, tight coupling, race condition, memory leak, or invalid core assumption | Requires interface redesign before coding |
| Serious flaw | Missing timeout, non-idempotent retry, quota blindness, or weak telemetry | Mandatory task before shipping |
| Cosmetic flaw | Naming drift, formatting preference, or minor documentation typo | Optional cleanup |

## Prompt caching and reasoning-model calibration

Keep static prefix blocks (`<system_directive>`, `<target_environment>`, and `<codebase_context>`) byte-identical across follow-up turns on the same repository slice. Avoid injecting timestamps or random IDs into prefix blocks.

| Model family | Minimum cache prefix | Prompt calibration |
|---|---|---|
| Anthropic Claude (3.7 Sonnet and 4.x) | 1,024 tokens | Enforce flaw-first order, cap surgical blocks to under 100 lines per unit, and hold thinking effort constant across turns to avoid cache invalidation. |
| OpenAI (o1, o3-mini, GPT-4o+) | 1,024 tokens (128-token increments) | Omit artificial step-by-step CoT instructions. State POSIX/BSD constraints, complexity bounds, and strict output schemas directly. |
| Google Gemini 2.5 Pro | 2,048 tokens (implicit) | Demand terse register, tabular trade-off matrices, and explicit relative paths across multi-file dependencies. |

## Recurring external advisor blind spots

1. **Platform-blind shell commands.** Advisors default to GNU flags (`grep -P`, `sed -i` without backup suffix, `date -d`, `stat -c`). Declare macOS Darwin BSD userland in `<target_environment>` and audit shell fences via `scripts/audit_response.py`.
2. **Quota and rate-limit blindness.** Advisors propose multi-hour retry loops without computing request quotas. Mandate explicit arithmetic when reviewing batch workers or API clients.
3. **Unbounded verification queries.** Advisors emit repository-wide `grep` commands that match unrelated sibling directories. Require path-scoped checks.
4. **Estimated line numbers.** Advisors miscount offsets on unnumbered dumps. Always slice and number files via `scripts/package_prompt.py`.

