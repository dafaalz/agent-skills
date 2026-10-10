# Evaluation and rule grafting

Protocol for presenting arena artifacts, ingesting human evaluations, isolating differential rules, and applying safe patches.

## 1. Comparison presentation table

Present all completed artifacts in a clean markdown table using clickable `file://` URLs:

```markdown
| Scenario | Candidate A (Baseline) | Candidate B (Candidate) | Selected Winner |
|---|---|---|---|
| S1. Functional Utility | [s1_candidate_a.html](file:///path/to/s1_candidate_a.html) | [s1_candidate_b.html](file:///path/to/s1_candidate_b.html) | [ ] |
| S2. Tactile Physics    | [s2_candidate_a.html](file:///path/to/s2_candidate_a.html) | [s2_candidate_b.html](file:///path/to/s2_candidate_b.html) | [ ] |
| S3. Narrative Craft    | [s3_candidate_a.html](file:///path/to/s3_candidate_a.html) | [s3_candidate_b.html](file:///path/to/s3_candidate_b.html) | [ ] |
```

Instruct the evaluator to open each file pair locally, inspect behavior and performance, and provide a decision line for each scenario.

## 2. Ingesting human feedback and win patterns

Parse evaluator responses to map win conditions and detect rule regressions:

1. **Unanimous Candidate B victory (3-0).**
   All proposed modifications passed without regression. Proceed directly to patch synthesis.
2. **Split decision (e.g. B wins S2 and S3, but A wins S1).**
   Detect the exact cause of regression. If Candidate B degraded S1 because long durations or decorative effects leaked into functional workflows, scope the rule as an explicit contextual exemption rather than a global override.
3. **Unanimous Candidate A victory (3-0).**
   Candidate B failed across all stress axes. Reject the proposed modification entirely, state the mechanical reason, and solicit a new hypothesis before running additional rounds.

## 3. Differential rule extraction and patch synthesis

Never rewrite an entire skill file after a benchmark run. Extract only the differential rules that generated the superior output:

- **External search grounding.** Before drafting patch diffs, execute targeted queries using `search_web` to discover how official documentation or established industry standards solve the specific defects reported by the evaluator. Validate candidate rules against at least three verified external source URLs (such as official framework documentation, W3C/MDN specifications, or recognized industry creators).
- **Context budget defense.** Keep the target `SKILL.md` strictly under 250 lines. Push long code recipes, configuration tables, or framework guides into dedicated reference files under `references/` using progressive disclosure. Never inline bulky reference documentation into the root skill file.
- **Punctuation and style hygiene.** Verify that proposed rule additions contain zero em dashes, zero en dashes, and colons appearing only before explicit lists or code blocks.
- **Isolate operative clauses.** Identify the exact sentences or token values responsible for the behavioral shift (such as allowing `clip-path: inset()` or capping blur at 20px for large display typography).
- **Match existing conventions.** Format extracted rules using the target skill existing tone, indentation, and structure.
- **Generate surgical diffs.** Present proposed modifications as a clear diff block for user confirmation before modifying files on disk:

```diff
--- a/SKILL.md
+++ b/SKILL.md
@@ -95,3 +95,3 @@
-- Animate transform and opacity exclusively.
+- Animate transform and opacity exclusively. Allow clip-path: inset() on creative curtain reveals.
```

## 4. Iteration and termination options

Conclude each evaluation round by presenting two explicit choices:

1. **Option 1. Execute another test round.** Formulate a refined Candidate C hypothesis and generate fresh scenarios.
2. **Option 2. Commit patch and terminate.** Write the verified modifications permanently to the target skill file and close the arena run.
