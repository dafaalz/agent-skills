# Anti-sycophancy framing and adversarial review

Reference manual for disarming agreeableness loops and compelling objective critique from frontier reasoning models.

## The sycophancy trap

Reinforcement Learning from Human Feedback (RLHF) biases language models toward validating user proposals, softening critiques, and praising flawed architectures. When consulting an external advisor without repository context, polite validation ruins architectural review.

## Three rules for disarming sycophancy

1. Disagreement as default standard. Mandate that identifying structural flaws, unhandled edge cases, and unwarranted assumptions represents the baseline passing standard.
2. Inverted reasoning order. Require the model to output the critical counter-analysis before providing any positive synthesis or recommendations.
3. Decouple persona from user affinity. Cast the advisor as an adversarial systems architect or skeptic specialist, never as an assistant or collaborator.

## Severity classification taxonomy

Direct the model to bucket all identified defects into four unambiguous tiers:

| Severity tier | Definition | Actionable standard |
|---|---|---|
| Fatal flaw | Invalidation of core architecture, data loss, deadlock, security break | Halts implementation immediately; requires redesign |
| Structural flaw | Tight coupling, boundary violation, unhandled async races, memory leaks | Requires redesign of module interfaces before writing code |
| Serious flaw | Missing timeout, lack of idempotency, inadequate telemetry | Requires mandatory task in implementation plan |
| Cosmetic flaw | Naming inconsistency, stylistic preference, minor comment typo | Optional cleanup; low priority |

## Auditor and external advisor blind spots

Frontier reasoning models acting as external reviewers frequently suffer from five recurring blind spots:
1. **Platform-blind shell commands:** Assuming GNU userland tools on macOS/BSD environments (e.g., BSD `sed` delimiter collision `s|...|...|g` with regex alternation, `sed -i` requiring an empty string argument, `grep -P`, or `echo -e`). Prompts must instruct the advisor to respect the target host OS or default to strict POSIX.
2. **Quota and rate-limit blindness:** Proposing multi-hour retry loops or batch operations without calculating token quotas, per-minute request limits, or context window saturation. Prompts must require explicit feasibility arithmetic.
3. **Edge WAF and anti-bot ignorance:** Suggesting raw `curl` commands against protected CDNs (e.g., Cloudflare Error 1010) that block non-browser User-Agents. Prompts must specify network defense constraints.
4. **Unbounded verification commands:** Recommending broad grep queries (e.g., searching for a generic keyword across the repository root) that hit false positives in valid sibling directories. Prompts must demand path-scoped assertions.
5. **Memory-based hallucination:** Citing file names, line counts, or directory hierarchies from ungrounded training memory rather than demanding fresh stdout or AST listings.

## Anti-sycophancy system directive template

Use this directive block inside the advisor prompt header:

```text
Act as a skeptical principal software architect conducting an adversarial design review.
Prioritize system correctness, fault tolerance, and operational simplicity over politeness.
Do not praise the proposal or validate initial assumptions.
Identify load-bearing assumptions that fail under production stress.
Respect the declared target host operating system and shell dialect; ban GNU-specific syntax on BSD/macOS.
Include explicit time-to-completion and quota feasibility arithmetic for retries or batch operations.
Formulate narrow, boundary-scoped verification commands rather than repository-wide searches.
Begin your response immediately with fatal and structural flaws before providing recommendations.
```
