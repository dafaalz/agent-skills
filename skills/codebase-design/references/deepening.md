# Deepening

Deepen shallow modules into cohesive units with high leverage while managing dependency boundaries across seams.

## Dependency categories

When assessing a module for deepening, classify each external dependency into one of four categories. The category determines the seam strategy and testing approach.

### 1. In-process

Dependencies that run purely in memory without network or disk I/O, such as pure algorithms, data transformations, or state machines.

- Strategy. Merge scattered helper functions into one deep module.
- Testing. Test directly through the public interface. No mocks or adapters needed.

### 2. Local substitutable

Dependencies that provide fast in-memory or embedded test stand-ins, such as SQLite, PGLite, or in-memory file systems.

- Strategy. Keep the seam internal to the module. Do not expose mock ports through the public interface.
- Testing. Run automated tests against the embedded stand-in directly.

### 3. Remote but owned

First-party services across network boundaries, such as internal microservices, cache clusters, or message queues.

- Strategy. Define a clean port interface at the module seam. The deep module owns domain orchestration while transport logic lives in separate adapters.
- Testing. Production uses the network adapter, while test suites run against an in-memory fake adapter satisfying the same port.

### 4. True external

Third-party external platforms outside operational control, such as payment gateways, SMS providers, or external analytics APIs.

- Strategy. Define an explicit port at the seam. Inject the port into the deep module.
- Testing. Production binds the vendor SDK adapter, while test suites supply an explicit fake adapter.

## Seam discipline

Apply these constraints when establishing interfaces:

1. **The two-adapter threshold.** One adapter represents a hypothetical seam. Two adapters represent a real seam. Never introduce a separate port interface unless at least two concrete adapters exist, typically production and an in-memory test fake. A single-adapter seam adds useless indirection without architectural benefit.
2. **Seam privacy.** Keep internal seams hidden behind the module implementation. Test private seams through module unit tests if necessary, but never expose internal hooks on the public caller interface.
3. **The replacement rule.** When refactoring shallow modules, replace them directly rather than adding another abstraction layer on top of legacy wrappers.
4. **The refactor survival test.** Automated tests must assert observable outcomes through the interface rather than internal state. If a test breaks when internal implementation details change while the interface remains unchanged, the test is testing past the interface. Delete obsolete unit tests on shallow wrappers once interface tests pass.
