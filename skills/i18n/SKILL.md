---
name: i18n
description: "Use when implementing internationalization, localization, locale negotiation, date/number formatting, ICU messages, RTL/BiDi layouts, or text expansion resilience. Don't use for CSS styling (use frontend-design), UX copy review (use ui-ux-review), animation choreography (use ui-motion), React component profiling (use react), or multi-task execution plans (use agent-planning)."
---

# Internationalization (i18n)

Make a codebase correct outside a single locale. This skill audits and implements internationalization across nine domains documented in reference modules under `references/`.

<HARD-GATE>
Write-Target Boundary. Apply internationalization changes strictly to user-facing copy, translation catalogs, formatting helpers, and layout styles.
Do not modify database column names, internal event payloads, API route identifiers, system configuration keys, test assertions, or shell scripts.
</HARD-GATE>

## Modes

Declare the active operating mode before executing any steps:
- Implementation mode (default): Ingest scope, load domain references, audit patterns, and implement localization changes. Run Steps 1 through 5 sequentially.
- Audit mode (`/i18n audit only`): Scan codebase for unlocalized copy, date formatters, and physical CSS rules. Run Steps 1 through 3 only, emit `.agents/state/i18n/audit-report.md`, and halt without modifying files.

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
2. A narrowed domain set does not excuse breaking sibling domains. Note out-of-scope defects in findings without fixing them unless user expands scope.
3. When target language set is ambiguous, ask user before implementing.

## Reference quick routing

| Domain | Reference module | Scope |
|---|---|---|
| Text expansion | [references/text-expansion-resilience.md](references/text-expansion-resilience.md) | Dynamic text expansion resilience & overflow handling |
| Language & negotiation | [references/intl-language.md](references/intl-language.md) | Language tags, BCP 47 vocabulary, & negotiation |
| Dates & times | [references/intl-date-and-time-format.md](references/intl-date-and-time-format.md) | Timestamps, calendar systems, & time zone formatting |
| Numbers & currencies | [references/intl-number-and-currency.md](references/intl-number-and-currency.md) | Currencies, units, percentages, & notation scales |
| Bidirectional & RTL | [references/intl-bidi.md](references/intl-bidi.md) | RTL mirroring, BiDi algorithms, & logical properties |
| Pluralization & ICU | [references/intl-pluralization.md](references/intl-pluralization.md) | Plural rules, gender inflection, & ICU syntax |
| Collation & sorting | [references/intl-collation-and-sorting.md](references/intl-collation-and-sorting.md) | Locale-sensitive string comparison & sorting |
| Unicode text processing | [references/intl-text-processing.md](references/intl-text-processing.md) | Segmenter boundaries, grapheme clusters, & case folding |
| Content & catalogs | [references/intl-content-and-assets.md](references/intl-content-and-assets.md) | Translation catalog layout, formats, & asset localization |
| Testing & QA | [references/intl-testing-and-qa.md](references/intl-testing-and-qa.md) | Pseudolocalization, visual verification, & test gates |

## Workflow

### Step 1. Stack and inventory reconnaissance

Audit the repository to detect existing i18n tooling before adding dependencies:

```bash
head -n 60 package.json pyproject.toml composer.json Gemfile go.mod 2>/dev/null
grep -rIl --exclude-dir={node_modules,.git,dist,build,vendor} -E "i18next|react-intl|vue-i18n|next-intl|formatjs|gettext|babel|lingui|MessageFormat" . | head -n 30
find . -path ./node_modules -prune -o \( -name "*.po" -o -name "*.xliff" -o -name "*.arb" -o -name "*.ftl" -o -name "messages*.json" -o -name "locales" -o -name "i18n" \) -print 2>/dev/null | head -n 30
```

Record runtime capabilities, existing catalog locations, translation formats, and user locale persistence sources. Extend existing libraries instead of introducing competing frameworks.

Completion criterion. `.agents/state/i18n/scope.json` exists on disk with `detected_libraries`, `catalog_paths`, `in_scope_languages`, and `mode`.

### Step 2. Progressive disclosure and domain module loading

Consult only reference modules relevant to scoped domains:

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

Completion criterion. Session context contains all relevant domain reference files based on user scope.

### Step 3. Audit and severity classification

Scan for locale-hardcoded patterns and catalog findings:

```bash
grep -rn --exclude-dir={node_modules,.git,dist,build,vendor} -E "toLocaleDateString\(\)|toLocaleString\(\)|new Date\(.*\)\.getDate\(\)" . | head -n 100
grep -rn --exclude-dir={node_modules,.git,dist,build,vendor} -E "\.toUpperCase\(\)|\.toLowerCase\(\)" . | head -n 100
grep -rn --exclude-dir={node_modules,.git,dist,build,vendor} -E "=== *1|=== *0|count *[<>=]+ *1|\$\{count\}" . | head -n 100
grep -rn --exclude-dir={node_modules,.git,dist,build,vendor} -E "margin-left|margin-right|padding-left|padding-right|text-align:\s*(left|right)|left:|right:" . | head -n 100
grep -rn --exclude-dir={node_modules,.git,dist,build,vendor} -E "\.sort\(\)|ORDER BY" . | head -n 100
```

Classify each finding by impact:

| Severity | Definition | Examples |
|---|---|---|
| Critical | Corrupts data or alters calculation values | Storing local wall-clock time as UTC instant, parsing localized currency with `parseFloat`, slicing strings across grapheme boundaries |
| High | Visibly broken UI or grammar for target locale | Hardcoded `count === 1` plural checks, code-unit string sorting, unlocalized dates rendered in server timezone |
| Medium | Prevents subsequent locale onboarding | Physical CSS margins and padding, concatenated sentence fragments, fixed date format strings |
| Low | Completeness and polish gaps | Missing inline `lang` tags, absent pseudolocale testing builds in CI |

Completion criterion. `.agents/state/i18n/audit-report.md` exists on disk with file locations, line numbers, defect categories, and planned remediation.

When operating in Audit mode, output findings table and halt. Do not proceed to Step 4.

### Step 4. Ordered implementation

Execute changes in strict architectural sequence:
1. Locale model. Define how locales are negotiated, stored, and resolved across boundaries.
2. Catalog structure. Establish message files, keying conventions, and interpolation tokens.
3. String extraction. Replace hardcoded copy with catalog keys and named parameters.
4. Formatting. Replace ad-hoc date and number formatters with standard platform APIs or library formatters.
5. Plurals and grammar. Convert count-dependent logic to ICU plural messages with CLDR categories.
6. Layout and BiDi. Switch physical CSS properties to logical equivalents, and set `dir` attributes on root containers.
7. Collation. Replace code-unit comparisons with locale-aware collator calls.
8. Testing infrastructure. Add pseudolocale pipelines, lint rules, and matrix test fixtures.

Completion criterion. Code modifications apply in sequence matching repository conventions without unused abstractions.

### Step 5. Verification

Verify work against concrete criteria:
1. Run project build and automated test commands. Detect package manager and test runner from lockfiles:

| Lockfile | Build command | Test command |
|---|---|---|
| `pnpm-lock.yaml` | `pnpm run build` | `pnpm test` |
| `yarn.lock` | `yarn build` | `yarn test` |
| `bun.lockb` | `bun run build` | `bun test` |
| `package-lock.json` | `npm run build` | `npm test` |
| `poetry.lock` | (n/a) | `poetry run pytest` |
| `uv.lock` | (n/a) | `uv run pytest` |
| `Pipfile.lock` | (n/a) | `pipenv run pytest` |
| `composer.lock` | `composer build` (or project script) | `vendor/bin/phpunit` |

Record the resolved command in `.agents/state/i18n/verification-commands.txt` before running.
2. Audited views render all in-scope locales without falling back to default language keys.
3. User-facing paths contain zero raw `toLocaleDateString()` or `new Date().toString()` calls without explicit locale options.
4. Numeric conditionals like `count === 1` are replaced with ICU plural syntax.
5. String comparisons use `Intl.Collator` or case folding rather than raw `toLowerCase()`.
6. Layouts employ CSS logical properties (`margin-inline-start`, `padding-inline-end`).
7. Pseudolocale tests show zero unextracted raw strings and zero truncated containers.

Completion criterion. Project build and test commands exit with code 0 and raw output is recorded in `.agents/state/i18n/verification.txt` with zero unresolved audit items.

## Anti-patterns

| ID | Title | Pattern description | Why it fails | Concrete fix |
|---|---|---|---|---|
| I18N-1 | Duplicate stack | Adds a new i18n library without checking repo | Colliding i18n architectures and duplicate keys | Audit dependencies first; extend existing tools |
| I18N-2 | Hardcoded plural | Writes `count === 1 ? 'item' : 'items'` | Fails in languages with multiple plural forms | Use ICU `plural` with standard CLDR categories |
| I18N-3 | Naive number parse | Uses `parseFloat(localizedNumber)` | German `1.234,56` parses as `1.234` | Use locale-aware numeric parsing or raw numeric storage |
| I18N-4 | Unspecified locale | Calls formatters without passing resolved locale | Falls back to server OS locale in production | Pass explicit resolved locale to formatter |
| I18N-5 | Floating instant | Stores local wall-clock time as a UTC instant | Daylight saving shifts alter timestamps by an hour | Store UTC instant with separate IANA timezone ID |
| I18N-6 | Physical styles | Uses `margin-left` or `right: 0` for layouts | Layout fails to mirror in RTL locales | Use `margin-inline-start` and logical properties |
| I18N-7 | Code-unit sort | Uses default `.sort()` on user-facing lists | Sorts accented and non-ASCII characters incorrectly | Use `Intl.Collator(locale).compare` |
| I18N-8 | Sentence stitching | Concatenates phrases with `+` into sentences | Breaks under varying grammatical word orders | Use single message templates with named placeholders |
| I18N-9 | Grapheme slicing | Uses `.substring()` across Unicode text | Corrupts surrogate pairs, emoji, and Indic scripts | Use `Intl.Segmenter` with grapheme granularity |

## Boundary isolation

Apply internationalization changes strictly to user-facing strings, formatting calls, and layout directives:
- Keep database column names, internal event payloads, API route identifiers, and configuration keys in their original canonical English or system format.
- Protect code syntax, CLI commands, and test assertion primitives from translation or localized casing alterations.

## Quick audit checklist

Review this table before completing internationalization changes:

| Check | Passing condition |
|---|---|
| String extraction | User-facing copy loaded from catalogs, zero hardcoded UI strings |
| Locale formatting | Date and number formatters pass explicit locale and time zone |
| Plurals | Pluralization logic uses ICU syntax with CLDR categories |
| Bidirectional layout | Layout uses CSS logical properties and root dir attributes |
| Anti-patterns | Anti-pattern table adheres to 5-column schema with stable IDs |
| Boundary isolation | System keys, column names, and APIs remain in canonical format |
