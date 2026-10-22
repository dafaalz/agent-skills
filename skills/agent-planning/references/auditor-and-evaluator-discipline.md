# Auditor and Evaluator Discipline: Bidirectional Standards

This reference governs standards for evaluators, reviewers, and adversarial advisors to ensure audit commands and recommendations remain empirically sound.

## 1. Test Mandated Commands in Target Environments
- Before demanding that an agent run a specific CLI command, verify syntax against the target operating system (e.g., BSD `sed` on macOS vs GNU `sed` on Linux).
- Avoid delimiter collisions in `sed` substitution patterns by using non-colliding separators (e.g., `#` instead of `|` when regex contains alternations).

## 2. Compute Quota and Throughput Feasibility
- When recommending a rate-limit or retry strategy, calculate exact arithmetic:
  $$\text{Total Calls} \div \text{Quota per Window} = \text{Elapsed Time}$$
- Never advise waiting if the required duration exceeds a realistic interactive session.

## 3. Specify Narrow, Exact Verification Commands
- Ensure verification commands (e.g., `grep`, `find`) specify exact paths or filters.
- Avoid broad grep patterns that match valid sibling assets, which create false-positive violation counts.

## 4. Account for Network Edge Layers
- When diagnosing API connectivity issues, check for CDN anti-bot filters (e.g., Cloudflare Error 1010 blocking default `urllib` User-Agent strings) before assuming key or catalog invalidity.

## 5. Recognize Physical Reality vs Guessing
- If an agent's claim matches physical ground truth, do not classify it as an unverified guess without first examining the exact filtered dataset.

---

*These rules emerged from a specific 18-round audit cycle. They are starting heuristics, not exhaustive constraints. When future audit cycles reveal new failure patterns, update this file with the same ceremony used here. Rules that never trigger in N cycles should be reconsidered for removal to prevent stale constraint accumulation.*
