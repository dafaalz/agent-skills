# Exploratory testing charters, boundary heuristics, and error guessing

Structured charters, formal boundary value analysis, equivalence partitioning matrices, state machine traversal, and empirical error guessing heuristics for deep quality verification.

## 1. Session-based test management charters

Session-Based Test Management organizes exploratory testing into uninterrupted, time-boxed investigation sessions guided by explicit charters. Rather than executing rigid scripted steps, testers pursue specific missions while documenting execution paths, anomalies, and coverage metrics.

### Charter anatomy

Every exploratory test session adheres to a standardized charter structure:

* Charter Title. Clear descriptive identifier following the bracketed component naming convention.
* Target Area. Specific feature, user workflow, service endpoint, or integration boundary under investigation.
* Duration. Fixed time box. Short sessions run 45 to 60 minutes for focused edge checks. Normal sessions run 60 to 90 minutes for in-depth feature sweeps. Long sessions run 90 to 120 minutes for cross-subsystem user journeys.
* Mission. Concrete objective defining what system behaviors to explore, what risks to evaluate, and what information to uncover.
* Environment. Application version, build commit hash, target environment URL, client browser or operating system, and backend database state.
* Test Execution Notes. Chronological record of areas explored, configurations exercised, and test hypotheses evaluated.
* Defect Findings. Summary of bugs discovered with cross references to formal defect tracking records.
* Opportunities and Uncharted Areas. High-risk areas, unexpected side paths, or edge behaviors discovered during testing that require future dedicated sessions.
* TBS Breakdown. Metrics recording the percentage of session duration spent on Test execution and design, Bug investigation and reporting, and Setup or administrative overhead.

### Concrete session charter example

The following charter demonstrates a completed session auditing the payment processing workflow:

```markdown
# Charter [Checkout-04] Idempotency and Payment Recovery Verification

## Metadata
* Target Area: Checkout checkout flow and Stripe webhook processing
* Duration: 75 minutes (Normal session)
* Tester: Quality Assurance Engineer
* Environment: Staging v2.4.1 (commit 8f2a1b9), macOS 14.5, Chrome 125, isolated tenant store-42
* TBS Metric: 65% Test, 25% Bug, 10% Setup

## Mission
Explore the multi-item checkout submission process under unstable network connectivity and rapid repeated submissions to uncover payment duplication, inventory race conditions, and hung order states.

## Execution Notes
1. Seeded tenant store-42 with five inventory items having stock quantity equal to one.
2. Configured browser network throttling to Slow 3G with 2000ms latency.
3. Added single stock item to shopping cart and advanced to payment step.
4. Clicked Pay Now button and immediately clicked button four additional times within 500ms.
5. Observed client UI disables button on initial click, but underlying form submit listener fired twice before DOM re-render completed.
6. Verified backend order service logs. Found two concurrent order creation requests carrying identical client idempotency keys.
7. First request acquired row lock and charged mock credit card successfully.
8. Second request encountered duplicate key constraint violation on order_transactions table and returned unhandled HTTP 500 to client instead of HTTP 409 or cached success response.

## Discovered Defects
* [Checkout] Concurrent checkout submission returns HTTP 500 when idempotency key collision occurs (Defect BUG-1042).

## Uncharted Areas
* Evaluate webhook retry behavior when Stripe webhook delivers charge.succeeded before local database transaction commits.
* Test payment processing behavior when customer closes browser tab during 3D Secure redirect.
```

## 2. Boundary value analysis heuristics

Boundary Value Analysis tests inputs at the edges of equivalence partitions. Software defects cluster disproportionately at boundaries due to off-by-one comparisons, loop termination errors, array indexing mistakes, and numeric overflow conditions.

### Two-value versus three-value boundary design

Black box test design uses two primary boundary testing techniques:

1. Two-Value Boundary Testing. For each boundary edge, test two points consisting of the boundary value itself and the closest adjacent value outside the boundary. For a numeric input valid on the range from MIN to MAX, two-value testing evaluates:
   * MIN (valid on-boundary)
   * MIN minus 1 (invalid off-boundary)
   * MAX (valid on-boundary)
   * MAX plus 1 (invalid off-boundary)
   Two-value boundary testing provides high defect detection efficiency with minimal test case count. It is the industry standard for robust commercial software.

2. Three-Value Boundary Testing. For each boundary edge, test three points consisting of the boundary value itself, the closest adjacent value inside the boundary, and the closest adjacent value outside the boundary. For a numeric input valid on the range from MIN to MAX, three-value testing evaluates:
   * MIN minus 1 (invalid off-boundary)
   * MIN (valid on-boundary)
   * MIN plus 1 (valid interior point)
   * MAX minus 1 (valid interior point)
   * MAX (valid on-boundary)
   * MAX plus 1 (invalid off-boundary)
   Three-value boundary testing is mandatory for safety critical systems, financial calculation engines, healthcare applications, and complex relational inequality conditions.

### Concrete boundary value matrices

The tables below provide boundary test designs across common data types.

#### Numeric integer boundaries for transfer amount (Valid range 1 to 10000 dollars)

| Test ID | Boundary Edge | Value Under Test | Boundary Type | Expected Classification | Expected Result |
| --- | --- | --- | --- | --- | --- |
| BVA-NUM-01 | Lower Edge | 0 | 2-Value and 3-Value | Invalid | Validation error, transfer rejected |
| BVA-NUM-02 | Lower Edge | 1 | 2-Value and 3-Value | Valid On-Boundary | Transfer processed successfully |
| BVA-NUM-03 | Lower Edge | 2 | 3-Value Interior | Valid In-Boundary | Transfer processed successfully |
| BVA-NUM-04 | Upper Edge | 9999 | 3-Value Interior | Valid In-Boundary | Transfer processed successfully |
| BVA-NUM-05 | Upper Edge | 10000 | 2-Value and 3-Value | Valid On-Boundary | Transfer processed successfully |
| BVA-NUM-06 | Upper Edge | 10001 | 2-Value and 3-Value | Invalid | Validation error, limit exceeded |

#### String length boundaries for username (Valid range 3 to 30 characters)

| Test ID | Boundary Edge | Value Under Test | Boundary Type | Expected Classification | Expected Result |
| --- | --- | --- | --- | --- | --- |
| BVA-STR-01 | Lower Edge | 2 characters ("ab") | 2-Value and 3-Value | Invalid | Rejected, minimum length error |
| BVA-STR-02 | Lower Edge | 3 characters ("abc") | 2-Value and 3-Value | Valid On-Boundary | Accepted, account created |
| BVA-STR-03 | Lower Edge | 4 characters ("abcd") | 3-Value Interior | Valid In-Boundary | Accepted, account created |
| BVA-STR-04 | Upper Edge | 29 characters (29 "a"s) | 3-Value Interior | Valid In-Boundary | Accepted, account created |
| BVA-STR-05 | Upper Edge | 30 characters (30 "a"s) | 2-Value and 3-Value | Valid On-Boundary | Accepted, account created |
| BVA-STR-06 | Upper Edge | 31 characters (31 "a"s) | 2-Value and 3-Value | Invalid | Rejected, maximum length error |

#### Array collection size for batch order upload (Valid range 1 to 50 items)

| Test ID | Boundary Edge | Collection Size | Boundary Type | Expected Classification | Expected Result |
| --- | --- | --- | --- | --- | --- |
| BVA-ARR-01 | Lower Edge | 0 items (empty array) | 2-Value and 3-Value | Invalid | Rejected, empty batch error |
| BVA-ARR-02 | Lower Edge | 1 item | 2-Value and 3-Value | Valid On-Boundary | Accepted, batch processed |
| BVA-ARR-03 | Lower Edge | 2 items | 3-Value Interior | Valid In-Boundary | Accepted, batch processed |
| BVA-ARR-04 | Upper Edge | 49 items | 3-Value Interior | Valid In-Boundary | Accepted, batch processed |
| BVA-ARR-05 | Upper Edge | 50 items | 2-Value and 3-Value | Valid On-Boundary | Accepted, batch processed |
| BVA-ARR-06 | Upper Edge | 51 items | 2-Value and 3-Value | Invalid | Rejected, batch limit exceeded |

## 3. Equivalence partitioning tables

Equivalence Partitioning divides input data domains into distinct classes where the system treats all values within a class identically. Selecting one representative value from each partition covers the functional range while eliminating redundant test execution.

### User age verification for insurance policy (Valid range 18 to 65 inclusive)

| Partition ID | Partition Description | Partition Type | Test Input | Expected Behavior |
| --- | --- | --- | --- | --- |
| EP-AGE-01 | Negative integer values | Invalid | -1 | HTTP 422, age cannot be negative |
| EP-AGE-02 | Minors under statutory legal age | Invalid | 17 | Validation error, minimum age is 18 |
| EP-AGE-03 | Eligible working age bracket | Valid | 35 | Policy application approved |
| EP-AGE-04 | Senior citizens above policy ceiling | Invalid | 66 | Validation error, maximum age is 65 |
| EP-AGE-05 | Non-numeric string data | Invalid | "twenty" | HTTP 400, numeric format required |
| EP-AGE-06 | Null or missing payload value | Invalid | null | HTTP 422, age is required |

### Customer email address field (RFC 5322 standard format)

| Partition ID | Partition Description | Partition Type | Test Input | Expected Behavior |
| --- | --- | --- | --- | --- |
| EP-EML-01 | Standard alphanumeric email | Valid | "user@example.com" | Email accepted, registration proceeds |
| EP-EML-02 | Email with plus addressing tag | Valid | "user+qa@sub.domain.org" | Email accepted, tag preserved |
| EP-EML-03 | Email with numeric domain | Valid | "customer@123.co" | Email accepted, registration proceeds |
| EP-EML-04 | Missing at-sign character | Invalid | "userexample.com" | Validation error, invalid email format |
| EP-EML-05 | Missing top-level domain | Invalid | "user@domain" | Validation error, invalid email format |
| EP-EML-06 | Multiple at-sign characters | Invalid | "user@@example.com" | Validation error, invalid email format |
| EP-EML-07 | Leading or trailing whitespace | Invalid | " user@example.com " | Sanitized or validation error |
| EP-EML-08 | Exceeding 254 total characters | Invalid | 255 character string | Validation error, email too long |

### Discount promo code (6 to 10 uppercase letters or numbers)

| Partition ID | Partition Description | Partition Type | Test Input | Expected Behavior |
| --- | --- | --- | --- | --- |
| EP-PRM-01 | Active valid promo code | Valid | "SUMMER2026" | 20 percent discount applied |
| EP-PRM-02 | Valid format but expired code | Invalid | "SPRING2024" | Error, promo code expired |
| EP-PRM-03 | Valid format but exhausted limit | Invalid | "ONEUSEONLY" | Error, redemption limit reached |
| EP-PRM-04 | Lowercase letters required upper | Valid | "summer2026" | Auto-capitalized and applied |
| EP-PRM-05 | Code containing punctuation | Invalid | "DISCOUNT!" | Error, alphanumeric characters only |
| EP-PRM-06 | Empty string promo code | Invalid | "" | Error, promo code cannot be empty |

## 4. State transition testing matrices

State Transition Testing evaluates systems whose behavior depends not only on immediate inputs, but also on current entity state and historical events.

### E-commerce order lifecycle finite state machine

Consider an order entity traversing the following states:
* Created (initial state after cart checkout)
* Pending Payment (awaiting gateway confirmation)
* Paid (payment successfully authorized and captured)
* Processing (warehouse allocation and packaging)
* Shipped (order handed over to logistics carrier)
* Delivered (customer received shipment)
* Cancelled (order terminated before fulfillment)
* Refunded (funds returned to customer after payment)

### Complete state transition matrix

The table below defines all state transitions. Cells indicate resulting next states for valid transitions, or explicit rejection for invalid transitions:

| Current State | Event Initiate Payment | Event Payment Success | Event Payment Failed | Event Start Packing | Event Dispatch Carrier | Event Confirm Delivery | Event Cancel Order | Event Refund Order |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Created | Pending Payment | Invalid (HTTP 409) | Invalid (HTTP 409) | Invalid (HTTP 409) | Invalid (HTTP 409) | Invalid (HTTP 409) | Cancelled | Invalid (HTTP 409) |
| Pending Payment | Invalid (HTTP 409) | Paid | Created | Invalid (HTTP 409) | Invalid (HTTP 409) | Invalid (HTTP 409) | Cancelled | Invalid (HTTP 409) |
| Paid | Invalid (HTTP 409) | Invalid (HTTP 409) | Invalid (HTTP 409) | Processing | Invalid (HTTP 409) | Invalid (HTTP 409) | Cancelled (Trigger Refund) | Refunded |
| Processing | Invalid (HTTP 409) | Invalid (HTTP 409) | Invalid (HTTP 409) | Invalid (HTTP 409) | Shipped | Invalid (HTTP 409) | Invalid (HTTP 409) | Refunded (Recall Stock) |
| Shipped | Invalid (HTTP 409) | Invalid (HTTP 409) | Invalid (HTTP 409) | Invalid (HTTP 409) | Invalid (HTTP 409) | Delivered | Invalid (HTTP 409) | Invalid (HTTP 409) |
| Delivered | Invalid (HTTP 409) | Invalid (HTTP 409) | Invalid (HTTP 409) | Invalid (HTTP 409) | Invalid (HTTP 409) | Invalid (HTTP 409) | Invalid (HTTP 409) | Refunded (Return Flow) |
| Cancelled | Invalid (HTTP 409) | Invalid (HTTP 409) | Invalid (HTTP 409) | Invalid (HTTP 409) | Invalid (HTTP 409) | Invalid (HTTP 409) | Invalid (HTTP 409) | Invalid (HTTP 409) |
| Refunded | Invalid (HTTP 409) | Invalid (HTTP 409) | Invalid (HTTP 409) | Invalid (HTTP 409) | Invalid (HTTP 409) | Invalid (HTTP 409) | Invalid (HTTP 409) | Invalid (HTTP 409) |

### Transition traversal levels

State machine validation requires systematic path execution:

1. 0-Switch Coverage. Every single valid state transition is traversed at least once. This verifies basic lifecycle mechanics and database persistence across all nominal paths.
2. 1-Switch Coverage. Every valid sequence of two consecutive transitions is traversed. For example, `Created -> Pending Payment -> Paid` followed by `Pending Payment -> Paid -> Processing`. This verifies that prior states do not leave residual flags that corrupt downstream transitions.
3. Invalid Transition Testing. Every illegal cell in the transition matrix is explicitly executed. Testers assert that the application rejects the action with appropriate error codes, emits warning telemetry, and leaves entity state completely unaltered.

## 5. Error guessing heuristics and cheat sheet

Error Guessing relies on engineering intuition and historical post-mortem analyses to inject scenarios that formal specifications regularly overlook.

### Concurrency and race conditions

* Rapid Double Clicking. Submit transactional buttons twice within 100 milliseconds to test client disabling, idempotency key enforcement, and database unique constraints.
* Parallel Browser Sessions. Open two tabs on the same account and edit shared resources simultaneously. Verify optimistic locking mechanisms and conflict detection.
* Inventory Exhaustion Race. Simulate five concurrent purchasers competing for the last available physical item. Assert that exactly one order completes and four receive out of stock notifications.
* Check-Then-Act Gaps. Exploit latency between balance verification and account debit by firing simultaneous withdrawal requests.
* Re-authentication Overlap. Initiate sensitive operations in one tab while revoking session permissions in a second tab.

### Special characters and unicode edge cases

* Emoji Surrogate Pairs. Input multi-byte emojis such as family sequences or flags containing zero-width joiners (`\u200D`) into text fields to test database `utf8mb4` encoding support.
* Bidirectional Text and RTL Overrides. Inject right-to-left override markers (`\u202E`) to verify that user interface layout does not invert or obscure text content.
* Null Byte Injections. Append `\0` within form strings to test whether downstream C-based binaries or file handlers terminate input prematurely.
* Special Whitespace Sequences. Submit non-breaking spaces (`\u00A0`), zero-width spaces (`\u200B`), and leading carriage returns to verify string sanitization.
* SQL Injection Strings. Submit `' OR 1=1 --`, `admin'--`, and `'; DROP TABLE users;--` to verify parameterized query enforcement.
* Cross-Site Scripting Vectors. Submit `<script>alert(1)</script>`, `<img src=x onerror=alert(1)>`, and `javascript:alert(1)` into rich text and comment inputs.

### Network timeouts and transport interruptions

* Mid-Flight Client Aborts. Terminate client TCP connections while uploading large multipart attachments or streaming large downloads. Verify server cleans temporary files.
* Packet Latency Throttling. Throttle upstream bandwidth to Slow 3G with 2500ms latency to expose premature client timeouts or missing loading indicators.
* HTTP 429 Rate Limit Handling. Flood API endpoints until rate limits trigger. Confirm client presents retry countdown banners rather than generic crashes.
* Sudden Disconnects. Disconnect network interfaces immediately after payment dispatch. Confirm system resolves final order status upon network restoration without double charging.
* Server Restart During Job Execution. Restart application nodes while asynchronous background jobs process. Verify queue workers acknowledge jobs only after atomic completion.

### Zero and negative quantities

* Zero Item Quantities. Submit order lines with quantity zero. Confirm cart rejection and calculate total price without division by zero errors.
* Negative Monetary Values. Submit coupon codes or balance transfers containing negative numbers (`-50.00`) to uncover inverted balance calculations.
* Floating Point Precision Curiosities. Submit operations involving `0.1 + 0.2` to confirm monetary calculations use arbitrary-precision decimal representations rather than raw floating point types.
* Integer Boundary Overflows. Submit values at 32-bit signed integer maximum (`2147483647`) and 64-bit integer maximum (`9223372036854775807`) to verify overflow handling.
* Empty Collections. Submit payloads with empty JSON arrays `[]` or empty JSON objects `{}` where nested structures are expected.

### Boundary timestamps and temporal anomalies

* Leap Year Boundary. Test date operations on February 29 in leap years and February 28 to March 1 transitions in non-leap years.
* Daylight Saving Time Clock Adjustments. Test cron jobs, booking slots, and billing cycles during spring forward and fall back transitions where hours repeat or skip.
* Timezone Rollover. Create transactions near `23:59:59 UTC` from client locations in negative timezones (such as UTC-8) to expose calendar date discrepancies.
* Month End Expiration Dates. Test recurring billing subscriptions created on January 31 when processed in February.
* Year 2038 Unix Timestamp Rollout. Test long-term financial projections, certificate expirations, and mortgage schedules that reference dates past January 19, 2038.
