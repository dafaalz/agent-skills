# Test matrices, boundary value analysis, and exploratory charters

Techniques for designing test matrices, computing boundary partitions, and executing session-based exploratory testing charters.

## 1. Boundary value analysis

Boundary value analysis tests inputs at the edges of equivalence classes. Software defects cluster at boundaries because off-by-one comparisons, loop limits, and numerical overflows occur there.

### Two-value versus three-value boundary design

Use two primary techniques for boundary design.

1. Two-value boundary testing. For each boundary edge, test two points consisting of the boundary value itself and the closest adjacent value outside the boundary.
2. Three-value boundary testing. For each boundary edge, test three points consisting of the boundary value itself, the closest adjacent value inside the boundary, and the closest adjacent value outside the boundary.

Apply two-value testing for standard business applications. Apply three-value testing for financial calculation engines, healthcare software, and relational inequality checks.

### Numeric integer boundary matrix

Valid range 1 to 10000 inclusive.

| Test ID | Boundary edge | Tested value | Boundary type | Classification | Expected result |
|---|---|---|---|---|---|
| BVA-NUM-01 | Lower edge | 0 | 2-Value and 3-Value | Invalid | Validation error, transfer rejected |
| BVA-NUM-02 | Lower edge | 1 | 2-Value and 3-Value | Valid on-boundary | Transfer processed successfully |
| BVA-NUM-03 | Lower edge | 2 | 3-Value interior | Valid in-boundary | Transfer processed successfully |
| BVA-NUM-04 | Upper edge | 9999 | 3-Value interior | Valid in-boundary | Transfer processed successfully |
| BVA-NUM-05 | Upper edge | 10000 | 2-Value and 3-Value | Valid on-boundary | Transfer processed successfully |
| BVA-NUM-06 | Upper edge | 10001 | 2-Value and 3-Value | Invalid | Validation error, limit exceeded |

### String length boundary matrix

Valid username range 3 to 30 characters.

| Test ID | Boundary edge | Tested value | Boundary type | Classification | Expected result |
|---|---|---|---|---|---|
| BVA-STR-01 | Lower edge | 2 characters | 2-Value and 3-Value | Invalid | Rejected, minimum length error |
| BVA-STR-02 | Lower edge | 3 characters | 2-Value and 3-Value | Valid on-boundary | Accepted, account created |
| BVA-STR-03 | Lower edge | 4 characters | 3-Value interior | Valid in-boundary | Accepted, account created |
| BVA-STR-04 | Upper edge | 29 characters | 3-Value interior | Valid in-boundary | Accepted, account created |
| BVA-STR-05 | Upper edge | 30 characters | 2-Value and 3-Value | Valid on-boundary | Accepted, account created |
| BVA-STR-06 | Upper edge | 31 characters | 2-Value and 3-Value | Invalid | Rejected, maximum length error |

## 2. Equivalence partitioning

Equivalence partitioning divides input data domains into distinct classes where the application handles all values in a class identically. Selecting one representative value per partition provides thorough coverage while eliminating redundant tests.

### User age verification table

Valid range 18 to 65 inclusive.

| Partition ID | Partition description | Partition type | Test input | Expected behavior |
|---|---|---|---|---|
| EP-AGE-01 | Negative integer values | Invalid | -1 | HTTP 422, age cannot be negative |
| EP-AGE-02 | Minors under statutory legal age | Invalid | 17 | Validation error, minimum age is 18 |
| EP-AGE-03 | Eligible working age bracket | Valid | 35 | Policy application approved |
| EP-AGE-04 | Senior citizens above policy ceiling | Invalid | 66 | Validation error, maximum age is 65 |
| EP-AGE-05 | Non-numeric string data | Invalid | "twenty" | HTTP 400, numeric format required |
| EP-AGE-06 | Null or missing payload value | Invalid | null | HTTP 422, age is required |

### Customer email address table

RFC 5322 standard format.

| Partition ID | Partition description | Partition type | Test input | Expected behavior |
|---|---|---|---|---|
| EP-EML-01 | Standard alphanumeric email | Valid | "user@example.com" | Email accepted, registration proceeds |
| EP-EML-02 | Email with plus addressing tag | Valid | "user+qa@sub.domain.org" | Email accepted, tag preserved |
| EP-EML-03 | Email with numeric domain | Valid | "customer@123.co" | Email accepted, registration proceeds |
| EP-EML-04 | Missing at-sign character | Invalid | "userexample.com" | Validation error, invalid email format |
| EP-EML-05 | Missing top-level domain | Invalid | "user@domain" | Validation error, invalid email format |
| EP-EML-06 | Multiple at-sign characters | Invalid | "user@@example.com" | Validation error, invalid email format |
| EP-EML-07 | Leading or trailing whitespace | Invalid | " user@example.com " | Sanitized or validation error |
| EP-EML-08 | Exceeding 254 total characters | Invalid | 255 character string | Validation error, email too long |

## 3. Session-based exploratory testing charters

Session-based test management organizes exploratory testing into uninterrupted, time-boxed investigation sessions guided by explicit charters. Testers explore target areas dynamically rather than executing rigid scripted steps.

### Charter anatomy

Every exploratory test session adheres to a standardized charter structure.

- Charter title. Clear identifier following bracketed component conventions.
- Target area. Specific feature, user workflow, or service endpoint under investigation.
- Duration. Fixed time box, usually 45 to 90 minutes.
- Mission. Concrete objective defining system behaviors to explore and risks to evaluate.
- Environment. Application version, commit hash, target environment URL, client browser, and database state.
- Test execution notes. Chronological record of areas explored and hypotheses evaluated.
- Defect findings. Summary of bugs discovered with defect identifiers.
- Opportunities and uncharted areas. High-risk areas discovered during testing requiring follow-up sessions.

### Concrete session charter example

```markdown
# Charter [Checkout-04] Idempotency and Payment Recovery Verification

## Metadata
- Target Area. Checkout checkout flow and Stripe webhook processing
- Duration. 75 minutes
- Tester. Quality Assurance Engineer
- Environment. Staging v2.4.1 (commit 8f2a1b9), macOS 14.5, Chrome 125, isolated tenant store-42

## Mission
Explore the multi-item checkout submission process under unstable network connectivity and rapid repeated submissions to uncover payment duplication, inventory race conditions, and hung order states.

## Execution Notes
1. Seeded tenant store-42 with five inventory items having stock quantity equal to one.
2. Configured browser network throttling to Slow 3G with 2000ms latency.
3. Added single stock item to shopping cart and advanced to payment step.
4. Clicked Pay Now button and immediately clicked button four additional times within 500ms.
5. Observed client UI disables button on initial click, but underlying form submit listener fired twice before DOM re-render completed.
6. Verified backend order service logs and found two concurrent order creation requests carrying identical client idempotency keys.
7. First request acquired row lock and charged mock credit card successfully.
8. Second request encountered duplicate key constraint violation on order_transactions table and returned unhandled HTTP 500 to client instead of HTTP 409 or cached success response.

## Discovered Defects
- [Checkout] Concurrent checkout submission returns HTTP 500 when idempotency key collision occurs (Defect BUG-1042).

## Uncharted Areas
- Evaluate webhook retry behavior when Stripe webhook delivers charge.succeeded before local database transaction commits.
- Test payment processing behavior when customer closes browser tab during 3D Secure redirect.
```
