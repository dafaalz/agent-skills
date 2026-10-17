# Rule grafting recipes and templates

Structured templates for grafting failure protections into agent skills.

## Template 1. Named anti-pattern entry

Use this structure when adding failure modes to catalogue skills such as `frontend-design` or `ui-ux-review`.

```markdown
### The [descriptive lowercase kebab or noun title]

[1 to 2 sentences describing the exact code, attribute, or CSS pattern that produces the defect.]

**Why it fails.** [Mechanical explanation describing how the browser engine, screen reader, or runtime misinterprets the syntax, along with the user-visible defect.]

**Fix.** [Exact imperative instruction paired with the required code snippet, CSS utility, or formula.]
```

### Concrete example

```markdown
### The indented whitespace-pre bubble

Placing newlines and indentation spaces inside JavaScript template literals that render inside elements styled with `whitespace-pre-wrap` or `whitespace-pre-line`.

**Why it fails.** The browser renders source-code indentation spaces and leading newlines literally. A one-word string expands into a massive multi-line box with horizontal offset.

**Fix.** Never separate opening and closing HTML tags with source newlines when wrapping dynamic text in `whitespace-pre-*`. Write `>${escapedText}<` flush against tag boundaries, or sanitize output with `.trim()`.
```

---

## Template 2. Execution invariant entry

Use this structure when adding hard prohibitions and guards to procedural skills like `ui-motion`, `executing-plans`, or `systematic-debugging`.

```markdown
N. **[Gerund action naming the guardrail].** Never [prohibited action] on [target scope or condition]. [Direct rationale explaining the failure or crash]. [Required positive action on the same line, naming exact tokens, flags, or parameters].
```

### Concrete example

```markdown
5. **Animating bulk historical data during initial load.** Never bind entrance animations to message histories or bulk collection renders. Render historical logs instantly without motion, and gate animations behind reactive flags (`isNew: boolean`) for live events.
```

---

## Template 3. Seam hunting and defect category entry

Use this structure when updating audit playbooks or inspection tables.

```markdown
- [Specific UI component or event] [failure verb phrase] without [required protective mechanism]. Apply [exact CSS utility or transition parameters] before [state mutation or DOM teardown].
```

### Concrete example

```markdown
- Ephemeral activity indicators (typing indicators, streaming status pills) unmounting abruptly without exit choreography. Apply fade and translateY exit before DOM removal.
```

---

## Template 4. Incident postmortem and triage table

Use this table during Step 1 of the reflection workflow to map session events to skills:

| Incident ID | User symptom or failure trigger | Root cause mechanism | Governing skill | Target file | Action taken |
|---|---|---|---|---|---|
| INC-01 | Distorted bubble width and height | Newline in template literal with `whitespace-pre-wrap` | `frontend-design` | `references/anti-patterns.md` | Grafted named anti-pattern |
| INC-02 | Chat history deleted on submit | Presentation class queried as placeholder guard | `frontend-design` | `references/anti-patterns.md` | Grafted named anti-pattern |
| INC-03 | Screen flash on conversation switch | Static animation class executed on initial 30 items | `ui-motion` | `SKILL.md` | Added invariant #5 |
