# Operate brief

Write this brief before auditing an operate or read route such as tables, forms, dashboards, docs, or settings. Keep it under 150 words.

## Fields

- Scope. Name the route and adjacent states.
- Task. State the job the visitor completes.
- States. List default, loading, empty, error, success, disabled, permission limited.
- Constraints. Name roles, devices, input methods, and time budget.
- Proof. Name real content used. Mark synthetic demo data as synthetic.
- Exit check. State how task success is measured.

## Rules

- Preserve incumbent tokens, components, copy claims, and behavior. Refinement keeps identity. Redesign needs explicit approval.
- Skip eyebrow on operate screens. Keep single column forms. Keep submit enabled with inline errors.
- Record unresolved decisions as questions. Zero placeholders in shipped brief.

Pass condition. Brief lists all six fields with zero placeholders and names the exit check.

## Storage

Keep the brief in the review report header for one-off audits. Promote it to a route sidecar file only when three or more sessions revisit the same route. Delete stale briefs when the route ships a redesign. Never copy token values into the brief. Point to DESIGN.md instead.

## Review use

Read the brief before Step 2 of the audit.
Cite brief fields in findings that break task flow.

## Example

Scope. Route `/users` plus empty, loading, error, and permission limited states. Task. Admin finds a user, edits role, and restores a deleted account. States. Table, skeleton, empty, inline error, undo toast, disabled restore. Constraints. Role admin, desktop and 390px mobile, keyboard and touch. Proof. Real seeded users. Synthetic names marked synthetic. Exit check. Admin completes edit and restore with keyboard alone and zero data loss.
