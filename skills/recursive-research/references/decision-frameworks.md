# Decision frameworks

Score autonomous picks with the weighted decision matrix, then invert the winner. Read this file at Step 2, at Step 4.2, and before you declare fitness at Step 5.

## Weighted decision matrix

1. List at least three candidate options.
2. Set the criteria and a weight per criterion from 1 to 5.
3. Score every option 1 to 5 on every criterion.
4. Multiply the score by the weight, sum the row, and compare the totals.
5. Name the winner and the margin, then hand the winner to the inversion step.

Blocked tie condition. When two options land within 10 percent of each other, add a criterion that separates them instead of picking the first one.

## Thread matrix

Score 5 to 8 candidate threads with these criteria at Step 2.

| Criterion | Weight | Question |
|---|---|---|
| Conceptual coverage | 4 | Does the thread cover a distinct dimension of the topic? |
| Perspective diversity | 3 | Does the thread carry a different school or region? |
| Source access | 3 | Do T1 or T2 sources exist for the thread? |
| User relevance | 4 | Does the thread serve the goal that started the research? |

## Source matrix

Score candidate sources for the current cycle at Step 4.2.

| Criterion | Weight | Scale |
|---|---|---|
| Authority | 5 | T1 scores 5, T2 scores 3, T3 scores 2, Rejected scores 0 |
| Relevance to the current thread | 5 | 1 to 5 by direct match to the thread question |
| Access | 3 | Open full text scores 5, abstract behind a paywall scores 3, blocked scores 1 |
| Field-appropriate recency | 2 | Code rewards the recent, classical philosophy rewards the old |
| Conflict of interest | 3 | Independent scores 5, funded by a party in the dispute scores 1 |

Keep the top 3 to 5 sources.

## Munger inversion

Run the matching question set and write the answers into `gaps.md`.

Thread selection at Step 2.

- Which thread did I drop that carries a dissenting school or a missing region?
- Which perspective absent from the list would make the research partial?

Source selection at Step 4.2.

- Which source did I skip that holds the counter-position?
- Which bias do all the selected sources share, such as one school, one era, or one language?
- Which documented contradicting source can I add now?

Knowledge state at Step 5.4.

- What do I still not know?
- Which sources contradict each other and stayed unresolved?
- Which question would a critical reviewer ask that I cannot answer?

## Fitness measurement

| Criterion | Measure | Source of truth |
|---|---|---|
| Coverage | Findings logged divided by the findings proxy per thread, at 80 percent or higher | `state.md` |
| T1 depth | Count of T1 sources per thread, at 3 or more | `sources-tier-1.md` |
| Saturation | New findings divided by accumulated findings, at 5 percent or lower for 3 cycles | `state.md` |
| Inversion | Answered question set for the current knowledge state | `gaps.md` |
| Cross-thread links | Count of explicit links between different threads, at 3 or more | `findings.md` |
