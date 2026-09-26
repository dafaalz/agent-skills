# Code comment hygiene and anti-slop rules

Rules for auditing code comments. Strip redundant AI conversational narration while preserving critical domain and security context.

## 1. Prohibited AI slop comments

Flag and remove comments matching these categories during code review:

1. **Restating code identifiers.** Comments that translate identifier names into words without adding new information:
   ```typescript
   // BAD:
   // Sets the user name
   setUserName(name);

   // GOOD: (Delete comment entirely)
   setUserName(name);
   ```
2. **Step by step narrative narration.** Conversational AI transcripts tracking obvious chronological flow:
   ```typescript
   // BAD:
   // Step 1: parse the json payload
   // Step 2: validate user permissions
   // Step 3: save to database
   ```
3. **Decorative dividing banners.** Long lines of dashes, slashes, or asterisks intended as visual dividers:
   ```typescript
   // BAD:
   // ==========================================
   // Helper functions
   // ==========================================
   ```
4. **Hollow pseudo-labels.** Comments such as `// Main logic`, `// Handle error`, or `// Return response`.
5. **Context-free TODO markers.** Unanchored `// TODO: fix this later` without an owner, issue tracking number, or verifiable failure condition.
6. **Decorative emojis.** Emojis placed inside code comments, docstrings, or log templates.

## 2. Protected load-bearing comments

Never delete comments that provide load-bearing engineering context:

1. **Non-obvious business invariants.** Domain rules that counter-intuitively explain why standard code patterns cannot be used:
   ```typescript
   // Tax calculation requires truncation rather than rounding per regional legal statute 44.2.
   ```
2. **Workaround references.** Explanations of workarounds for third-party bugs or upstream runtime quirks, including link or issue tracker IDs.
3. **Hardware, timing, and protocol constraints.** Explanations for explicit thread sleeps, debouncing delays, byte endianness, or network framing boundaries.
4. **Mathematical and algorithmic rationale.** Explanations for non-obvious mathematical formulas, bitwise masks, or algorithmic constants.
