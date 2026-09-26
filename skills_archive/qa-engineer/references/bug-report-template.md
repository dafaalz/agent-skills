# Standardized bug reporting schema and release sign-off verdicts

Deterministic defect reproduction protocols, technical evidence capture, severity triage definitions, and formal release governance criteria.

## 1. Severity triage taxonomy

Every reported defect is classified into one of five deterministic severity tiers:

* Blocker (Sev-1). Complete failure of core business operations, catastrophic data loss, irreversible data corruption, critical security compromise, or total halt of Tier 1 user journeys with zero workarounds. Requires immediate engineer escalation and emergency hotfix deployment.
* Critical (Sev-2). Primary functionality broken for a significant segment of users with no reasonable workaround, or major compliance violation. Halts mainline release candidate progression unless an explicit executive waiver is granted.
* Major (Sev-3). Significant defect affecting non-critical functionality, or primary functionality failure where an intuitive, acceptable workaround exists. Addressed in the immediate planned sprint.
* Minor (Sev-4). Cosmetic defects, layout misalignments, minor UI rendering quirks, non-blocking copy errors, or slight performance deviations that do not impede functional workflows.
* Trivial (Sev-5). Negligible defects such as typographical errors in internal technical comments, microscopic padding discrepancies, or minor ergonomic suggestions.

## 2. Standardized bug report specification

Defect reports must contain structured, actionable data that enables any engineer to reproduce, diagnose, and resolve the defect without back-and-forth clarification:

* Title. Formatted as `[Component] Concise description of failure condition`.
* Severity. Deterministic tier from Blocker to Trivial.
* Environment. Operating system, client browser or runtime version, application version, deployment target, and git commit SHA.
* Prerequisites and Account State. Required user roles, seeded database fixtures, feature flag states, and initial account balances.
* Steps to Reproduce. Sequential numbered instructions starting from initial unauthenticated state or clean session.
* Expected Behavior. Observable system state according to acceptance criteria.
* Actual Behavior. Concrete failure observed during execution.
* Technical Evidence. Reproducible curl commands, HTTP request and response payloads, browser console logs, and backend application stack traces.
* Root Cause Hypothesis and Suggested Fix. Technical diagnosis pointing to suspect source files or database constraints with recommended engineering solutions.

## 3. Canonical bug report example

The following report demonstrates a production-grade defect submission:

````markdown
# [Checkout] Concurrent multi-tab submission causes duplicate charge and double order creation

## Triage
* Severity: Blocker (Sev-1)
* Component: Checkout and Payment Gateway Integration
* Reporter: Quality Assurance Engineer
* Date: 2026-09-20

## Environment
* Operating System: macOS Sonoma 14.5
* Client: Google Chrome 125.0.6422.142 (Official Build, arm64)
* Application Target: Staging Environment (https://staging.app.example.com)
* Application Version: v2.4.1
* Build Commit SHA: 8f2a1b9c3e4d5f6a7b8c9d0e1f2a3b4c5d6e7f8a

## Prerequisites and Account State
* User Account: customer-tier2@example.com (User ID: `usr_98124`)
* Account State: Valid credit card on file, shopping cart seeded with 1 unit of Item SKU `PRD-100` ($150.00)
* Feature Flags: `checkout_v2_redesign` set to `true`, `express_checkout` set to `false`

## Steps to Reproduce
1. Log in to the application using the prerequisite account.
2. Navigate to `/cart` and proceed to `/checkout`.
3. Fill in standard billing and shipping information.
4. Open the identical checkout URL in a second browser tab within the same authenticated browser session.
5. In Tab 1, click the Pay Now button.
6. Within 100 milliseconds, switch to Tab 2 and click the Pay Now button.

## Expected Behavior
The first request processes payment and completes the order. The second request detects that checkout has already begun, rejects the duplicate submission with HTTP 409 Conflict, and displays an informative notification that the order is already completing. The customer credit card is charged exactly once for $150.00, and exactly one order record is created in the database.

## Actual Behavior
Both browser tabs submit payment requests successfully. The customer credit card is charged twice for $150.00 ($300.00 total). Two distinct orders (`ORD-9901` and `ORD-9902`) are created in the database referencing the same inventory item.

## Technical Evidence

### Curl Reproduction Command
curl -X POST "https://staging.app.example.com/api/v1/orders/checkout" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsIn..." \
  -H "Content-Type: application/json" \
  -H "X-Idempotency-Key: c9d8e7f6-1234-4567-89ab-cdef01234567" \
  -d '{
    "cartId": "cart_88312",
    "paymentMethodId": "pm_card_visa",
    "amount": 15000
  }'

### HTTP Request and Response Payloads
Request Headers:
POST /api/v1/orders/checkout HTTP/1.1
Host: staging.app.example.com
Content-Type: application/json
X-Idempotency-Key: c9d8e7f6-1234-4567-89ab-cdef01234567

Response Headers (Tab 1):
HTTP/1.1 201 Created
Content-Type: application/json
Date: Sat, 20 Sep 2026 11:15:22 GMT

Response Body (Tab 1):
{
  "orderId": "ORD-9901",
  "status": "PAID",
  "transactionId": "ch_3MtwL2LkdIwHu7ix0Example1",
  "amountCharged": 15000
}

Response Headers (Tab 2):
HTTP/1.1 201 Created
Content-Type: application/json
Date: Sat, 20 Sep 2026 11:15:22 GMT

Response Body (Tab 2):
{
  "orderId": "ORD-9902",
  "status": "PAID",
  "transactionId": "ch_3MtwL2LkdIwHu7ix0Example2",
  "amountCharged": 15000
}

### Browser Console Logs
[Warning] Duplicate submission event detected on DOM form element #payment-form
[Error] Uncaught (in promise) Error: Dual active payment handlers resolved simultaneously

### Backend Application Server Logs
2026-09-20T11:15:22.104Z [INFO] [OrderService] Received checkout request for cart cart_88312. TraceID: 4bf92f3577b34da6a3ce929d0e0e4736
2026-09-20T11:15:22.109Z [INFO] [OrderService] Received checkout request for cart cart_88312. TraceID: 7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d
2026-09-20T11:15:22.140Z [INFO] [StripeClient] PaymentIntent pi_1001 created successfully. TraceID: 4bf92f3577b34da6a3ce929d0e0e4736
2026-09-20T11:15:22.142Z [INFO] [StripeClient] PaymentIntent pi_1002 created successfully. TraceID: 7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d
2026-09-20T11:15:22.180Z [INFO] [OrderRepository] Order ORD-9901 persisted to database.
2026-09-20T11:15:22.182Z [INFO] [OrderRepository] Order ORD-9902 persisted to database.

## Root Cause Hypothesis and Suggested Fix

### Technical Hypothesis
The checkout controller in `src/modules/orders/orders.controller.ts` generates client idempotency keys lazily inside individual browser page instances rather than hashing cart state. Also, `OrderService.processCheckout()` does not acquire an exclusive row-level lock (`SELECT FOR UPDATE`) on the shopping cart row before dispatching external payment API calls. Because both requests execute concurrently, both evaluate `cart.status == ACTIVE` before either transaction commits.

### Suggested Fix
1. Enforce distributed idempotency using Redis or database unique constraints keyed on `cartId` with a mandatory lease lock:
   ```sql
   ALTER TABLE orders ADD CONSTRAINT uq_orders_cart_id UNIQUE (cart_id);
   ```
2. Wrap checkout execution in a serializable database transaction:
   ```typescript
   await prisma.$transaction(async (tx) => {
     const cart = await tx.cart.findUniqueOrThrow({
       where: { id: cartId },
       select: { id: true, status: true, version: true }
     });
     if (cart.status !== 'ACTIVE') {
       throw new ConflictException('Cart checkout is already in progress or completed');
     }
     await tx.cart.update({
       where: { id: cartId },
       data: { status: 'CHECKING_OUT', version: { increment: 1 } }
     });
   }, { isolationLevel: Prisma.TransactionIsolationLevel.Serializable });
   ```
````

## 4. Release sign-off verdict schema

Before deploying a release candidate to production, the QA engineer assesses all quality indicators and records a binding verdict.

### Release decision criteria

The decision framework enforces three possible release outcomes:

1. Go Verdict. All release criteria are met without exception:
   * Zero open Blocker (Sev-1) or Critical (Sev-2) defects.
   * All Tier 1 automated user journeys pass with one hundred percent reliability in CI pipelines.
   * Zero unquarantined flaky tests in the test suite.
   * Backend API latency meets performance budgets (p95 under 200 milliseconds, p99 under 500 milliseconds).
   * Frontend Core Web Vitals meet target budgets (LCP under 2.5 seconds, INP under 200 milliseconds, CLS under 0.1).
   * Differential mutation testing score on the release git diff exceeds eighty percent.
   * Security gates pass with zero Critical or High vulnerabilities across static code, container dependencies, and dynamic application scans.

2. No-Go Verdict. Immediate release halt triggered by any of the following conditions:
   * Any open, unresolved Blocker or Critical defect.
   * Any regression in core Tier 1 user flows (authentication, payment, core transactions).
   * Failure of automated security scanning gates or secret exposure.
   * Tail latency regression exceeding twenty percent above established p99 budgets.
   * Evidence of potential data corruption, data leakage, or tenant isolation violations.

3. Conditional Go Verdict. Release permitted under strictly documented mitigations:
   * Discovered defects are strictly confined to Major (Sev-3) or lower severity with validated, documented workarounds.
   * The defective code path is fully encapsulated behind a feature flag configured to disabled by default.
   * Written authorization is obtained from both the Engineering Lead and the Product Manager.
   * A scheduled hotfix pull request addressing the defect is committed to merge within twenty-four hours of release.

### Formal sign-off record template

Every production release candidate requires an archival record documenting the evaluation:

| Release Attribute | Record Entry |
| --- | --- |
| Target Release Version | Release Candidate v2.4.1 |
| Target Deployment Date | 2026-09-20 |
| Git Commit SHA | 8f2a1b9c3e4d5f6a7b8c9d0e1f2a3b4c5d6e7f8a |
| Evaluated Components | Order Service, Checkout UI, Stripe Gateway Integration |
| Tier 1 Automated Journey Status | Passed (48 of 48 journeys green) |
| Active Flaky Tests In Quarantine | 0 unquarantined tests |
| Differential Mutation Score | 84.6 percent (Passed, exceeds 80 percent gate) |
| API p99 Latency Measurement | 342 milliseconds (Passed, budget 500 milliseconds) |
| Core Web Vitals Status | LCP 1.8s, INP 95ms, CLS 0.04 (All Passed) |
| Security Scan Vulnerabilities | 0 Critical, 0 High, 2 Low (Informational only) |
| Final Release Verdict | Go |
| Quality Assurance Sign-off | Signed by Quality Assurance Engineer |
| Engineering Lead Authorization | Signed by Staff Software Engineer |
| Product Manager Authorization | Signed by Principal Product Manager |
