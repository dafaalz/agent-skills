---
name: i18n
description: Use when implementing internationalization, localization, locale negotiation, date/number formatting, ICU messages, or RTL/BiDi layouts. Don't use for single-language text editing or translation of prose.
---

# Internationalization (i18n)

Make a codebase correct outside a single locale. This skill audits and implements internationalization across nine domains documented in reference modules under `references/`.

## Scope contract

The user may narrow the work by naming aspects, languages, or both. Parse the request before modifying files:

| Request | Languages in scope | Domains in scope |
|---|---|---|
| Bare `/i18n` | Detect from project, ask if ambiguous | All nine |
| `/i18n languages en, es` | `en`, `es` only | All nine |
| `/i18n dates only` | Current set | `intl-date-and-time-format.md` only |
| `/i18n add Arabic` | Existing plus `ar` | All nine, RTL and BiDi prioritized |
| `/i18n audit only` | Detect from project | All nine, audit report without edits |

Rules for narrowed requests:
1. A narrowed language set narrows configuration, not code correctness. If only `en` and `es` are requested, use logical CSS properties, locale-aware formatting APIs, and ICU messages so future locales require only configuration changes.
2. A narrowed domain set does not excuse breaking sibling domains. Note out-of-scope defects in findings without fixing them unless the user expands the scope.
3. When the target language set is ambiguous, ask the user before implementing.

## Workflow

### Step 1. Stack and inventory reconnaissance

Audit the repository to detect existing i18n tooling before adding dependencies:

```bash
ls -la
head -n 60 package.json pyproject.toml composer.json Gemfile go.mod 2>/dev/null
grep -rIl --exclude-dir={node_modules,.git,dist,build,vendor} -E "i18next|react-intl|vue-i18n|next-intl|formatjs|gettext|babel|lingui|MessageFormat" . | head -n 30
find . -path ./node_modules -prune -o \( -name "*.po" -o -name "*.xliff" -o -name "*.arb" -o -name "*.ftl" -o -name "messages*.json" -o -name "locales" -o -name "i18n" \) -print 2>/dev/null | head -n 30
```

Record runtime capabilities, existing catalog locations, translation formats, and user locale persistence sources. Extend existing libraries instead of introducing competing frameworks.

Completion criterion. A verified inventory listing the runtime, active i18n libraries, catalog paths, and locale storage strategy.

### Step 2. Progressive disclosure and domain module loading

Consult only the reference modules relevant to the scoped domains:

| Domain | Reference module | Load condition |
|---|---|---|
| Language tags and locale negotiation | [references/intl-language.md](references/intl-language.md) | Always loaded. Defines tag vocabulary and negotiation. |
| Dates, times, time zones, calendars | [references/intl-date-and-time-format.md](references/intl-date-and-time-format.md) | Timestamps rendered, parsed, or stored. |
| Numbers, currencies, units | [references/intl-number-and-currency.md](references/intl-number-and-currency.md) | Money, counts, percentages, or measurements displayed. |
| Bidirectional text and RTL layout | [references/intl-bidi.md](references/intl-bidi.md) | RTL language in scope or physical CSS directions found. |
| Pluralization, gender, ICU messages | [references/intl-pluralization.md](references/intl-pluralization.md) | Strings interpolate counts or variables. |
| Collation, sorting, comparison | [references/intl-collation-and-sorting.md](references/intl-collation-and-sorting.md) | Lists sorted, searched, or deduplicated. |
| Unicode text processing | [references/intl-text-processing.md](references/intl-text-processing.md) | Strings truncated, sliced, or case-folded. |
| Content, catalogs, assets | [references/intl-content-and-assets.md](references/intl-content-and-assets.md) | Always loaded. Governs catalog layouts and expansion. |
| Localization testing and QA | [references/intl-testing-and-qa.md](references/intl-testing-and-qa.md) | Always loaded. Verifies pseudolocales and gates. |

Completion criterion. Relevant domain reference files loaded into session context based on user scope.

### Step 3. Audit and severity classification

Scan for locale-hardcoded patterns and catalog findings:

```bash
grep -rn --exclude-dir={node_modules,.git,dist,build,vendor} -E "toLocaleDateString\(\)|toLocaleString\(\)|new Date\(.*\)\.getDate\(\)" . | head -n 30
grep -rn --exclude-dir={node_modules,.git,dist,build,vendor} -E "\.toUpperCase\(\)|\.toLowerCase\(\)" . | head -n 30
grep -rn --exclude-dir={node_modules,.git,dist,build,vendor} -E "=== *1|=== *0|count *[<>=]+ *1|\$\{count\}" . | head -n 30
grep -rn --exclude-dir={node_modules,.git,dist,build,vendor} -E "margin-left|margin-right|padding-left|padding-right|text-align:\s*(left|right)|left:|right:" . | head -n 30
grep -rn --exclude-dir={node_modules,.git,dist,build,vendor} -E "\.sort\(\)|ORDER BY" . | head -n 30
```

Classify each finding by impact:

| Severity | Definition | Examples |
|---|---|---|
| Critical | Corrupts data or alters calculation values | Storing local wall-clock time as UTC instant, parsing localized currency with `parseFloat`, slicing strings across grapheme boundaries |
| High | Visibly broken UI or grammar for target locale | Hardcoded `count === 1` plural checks, code-unit string sorting, unlocalized dates rendered in server timezone |
| Medium | Prevents subsequent locale onboarding | Physical CSS margins and padding, concatenated sentence fragments, fixed date format strings |
| Low | Completeness and polish gaps | Missing inline `lang` tags, absent pseudolocale testing builds in CI |

Completion criterion. A written findings table identifying file locations, line numbers, defect categories, and planned remediation.

### Step 4. Ordered implementation

Execute changes in strict architectural sequence:
1. Locale model. Define how locales are negotiated, stored, and resolved across boundaries.
2. Catalog structure. Establish message files, keying conventions, and interpolation tokens.
3. String extraction. Replace hardcoded copy with catalog keys and named parameters.
4. Formatting. Replace ad-hoc date and number formatters with standard platform APIs or library formatters.
5. Plurals and grammar. Convert count-dependent logic to ICU plural messages with CLDR categories.
6. Layout and BiDi. Switch physical CSS properties to logical equivalents, setting `dir` attributes where required.
7. Collation. Replace code-unit comparisons with locale-aware collator calls.
8. Testing infrastructure. Add pseudolocale pipelines, lint rules, and matrix test fixtures.

Completion criterion. Code modifications applied in sequence matching repository conventions without unused abstractions.

### Step 5. Verification

Verify work against concrete criteria:
- App builds and automated tests pass.
- Audited views render all in-scope locales without falling back to default language keys.
- User-facing paths contain zero raw `toLocaleDateString()` or `new Date().toString()` calls without explicit locale options.
- Numeric conditionals like `count === 1` are replaced with ICU plural syntax.
- String comparisons use `Intl.Collator` or case folding rather than raw `toLowerCase()`.
- Layouts employ CSS logical properties (`margin-inline-start`, `padding-inline-end`).
- Pseudolocale tests show zero unextracted raw strings and zero truncated containers.

Completion criterion. Fresh command output confirming clean test runs and zero unresolved audit items.

## Common pitfalls

| Mistake | Failure mode | Correct pattern |
|---|---|---|
| Adding libraries before checking repo | Colliding i18n architectures and duplicate keys | Audit dependencies first, extend existing tools |
| `count === 1` conditional | Breaks in Polish, Arabic, and Russian plural rules | ICU `plural` with standard CLDR categories |
| `parseFloat(localizedNumber)` | German `1.234,56` parses as `1.234` | Locale-aware numeric parsing or raw numeric storage |
| Unspecified locale in formatters | Falls back to server OS locale in production | Pass explicit resolved locale to formatter |
| Local time stored as instant | Daylight saving shifts shift timestamps by an hour | Store UTC instant with separate IANA timezone identifier |
| Physical CSS properties | Layout fails to mirror in RTL locales | Use `margin-inline-start` and logical properties |
| Code-unit `.sort()` | Sorts `Å`, `é`, and `Z` incorrectly | Use `Intl.Collator(locale).compare` |
| Fragment concatenation | Breaks under differing language word orders | Single message templates with named placeholders |
| `.substring()` slicing | Corrupts surrogate pairs, emoji, and Indic scripts | Use `Intl.Segmenter` with grapheme granularity |
