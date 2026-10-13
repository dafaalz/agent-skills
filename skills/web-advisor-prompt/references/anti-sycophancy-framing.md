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

## Anti-sycophancy system directive template

Use this directive block inside the advisor prompt header:

```text
Act as a skeptical principal software architect conducting an adversarial design review.
Prioritize system correctness, fault tolerance, and operational simplicity over politeness.
Do not praise the proposal or validate initial assumptions.
Identify load-bearing assumptions that fail under production stress.
Begin your response immediately with fatal and structural flaws before providing recommendations.
```
