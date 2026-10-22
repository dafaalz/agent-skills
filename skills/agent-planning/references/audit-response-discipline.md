# Audit Response Discipline

This reference governs how agents must structure responses when receiving a `NO-GO` or `CONDITIONAL` audit verdict.

## The 4-Part Response Structure
When an auditor flags an issue or blocker, structure every response block strictly around empirical evidence:

```markdown
### Blocker N: [Description]

**1. Claim Made Previously:**
> "[Exact quote of contested statement from prior round]"

**2. Empirical Ground Truth:**
```bash
$ [verification command]
[verbatim stdout output]
```

**3. Technical Diagnosis:**
[Physical reason for discrepancy: regex delimiter collision, off-by-one index, etc.]

**4. Itemized Proof of Resolution:**
```bash
$ [command verifying all sibling instances resolved]
[verbatim stdout output]
```
```

## Mandatory Behavioral Constraints
- **Never issue promises:** Do not state "I will be more careful" or "I will check thoroughly." Deliver concrete diffs, commands, and stdout.
- **Never fix in isolation:** When an auditor identifies an instance of a defect, grep the entire project for peer instances before replying.
- **State external blockers plainly:** When an action requires external user execution (e.g., key revocation, credential generation), label the item `PENDING USER ACTION` and never mark it complete.
- **Triangulate evidence:** Where possible, provide multiple independent sources of verification (e.g., git stat, file line counts, runtime diffs).
