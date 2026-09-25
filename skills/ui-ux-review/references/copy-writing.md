# Interface copy, action labels, and microcopy

Audit textual clarity, action labels, error messages, and microcopy consistency across user interface components.

## 1. Action clarity and button labels

Button labels must communicate the exact technical outcome of an interaction:
- Open with specific action verbs like "Save changes", "Delete repository", "Invite member", or "Export CSV".
- Reject vague affirmative labels like "OK" or "Yes", especially when confirming destructive or irreversible operations.
- Maintain consistent vocabulary across the entire interface. Do not alternate between "Edit", "Modify", and "Update" for identical functions.
- Match button labels with dialog titles. If a dialog asks "Delete project?", the confirmation button must read "Delete project", not "Confirm".

## 2. Error message structure and recovery guidance

Error notifications must guide the user to resolution without exposing internal system mechanics:
- State what occurred and how the user can recover in the same message.
- Exclude raw database errors, network socket exceptions, or protocol status codes from human-facing notifications.
- Use direct, supportive phrasing. Eliminate accusatory language like "You entered an invalid email address". Write "Enter a valid email address, such as name@example.com".
- Position inline error text directly below the affected input, linked via `aria-describedby`.

## 3. Empty states and contextual guidance

- **First-use empty states.** Explain the purpose of the section and provide a single primary Call to Action to create the first record.
- **No-results empty states.** Acknowledge that zero items matched the query, suggest alternative spellings, and offer a one-click reset action for active filters.
- **Placeholders.** Keep placeholder text instructive by demonstrating formatting examples (such as `e.g. +1 555-0100`). Never rely on placeholder text as a substitute for persistent field labels.

## 4. Microcopy checklist

| Element | Requirement | Failing example | Passing example |
| --- | --- | --- | --- |
| Primary action | Verb-first, specific outcome | "Submit" or "Click here" | "Create organization" |
| Destructive action | Explicit consequence | "OK" or "Proceed" | "Delete database permanently" |
| Validation error | Clear recovery guidance | "Invalid format" | "Enter an 8-character alphanumeric code" |
| Password helper | Visible requirement list | Hidden in placeholder | Bulleted criteria checking off in real time |
| Empty table | Instructive populate trigger | Blank white area | "No active projects. Create your first project." |
