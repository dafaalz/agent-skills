# Architectural lenses and logic defect audit

Analytical frameworks based on foundational software engineering principles and formal logic defect categories.

## 1. Classical engineering lenses

Evaluate changes against established architectural invariants:

1. **Conceptual integrity.** A system must reflect a single coherent design philosophy. Reject changes that solve an existing problem by introducing an incompatible second pattern or framework layer.
2. **Second-system effect.** Guard against over-engineering simple solutions with speculative abstraction layers, generalized factories, or complex plugin interfaces designed for hypothetical future needs.
3. **Deep modules over shallow wrappers.** Interfaces must hide significant complexity behind compact surfaces. Reject pass-through classes whose interface complexity matches or exceeds their internal implementation.
4. **Law of Demeter and tight coupling.** Avoid method chaining that traverses multiple object boundaries. Components should talk only to immediate collaborators.
5. **DRY vs premature coupling.** Distinguish incidental similarity from true domain duplication. Do not unify two distinct business concepts into one shared utility merely because their current field shapes match.

## 2. Nine categories of logic defects

Inspect code changes for non-syntax logic risks:

1. **Null and undefined traversal.** Optional chaining used defensively without handling the downstream `undefined` branch.
2. **Async interleaving and race conditions.** Concurrent requests mutating shared variables or unresolved promises overwriting newer data.
3. **Resource lifecycle leaks.** Unclosed file handles, unreleased database connections, orphan timers, and missing cleanup hooks in component lifecycles.
4. **Boundary and off-by-one errors.** Inclusive versus exclusive ranges, empty slice handling, zero-length collections, and pagination boundary math.
5. **State drift.** Client state deviating from database truth due to unhandled optimistic update rollbacks or missing cache invalidations.
6. **Swallowed errors and hollow fallbacks.** Catch blocks returning fallback defaults silently without logging or rethrowing critical failures.
7. **Input argument mutation.** Mutating parameters in-place rather than returning immutable copies, causing subtle side effects in upstream callers.
8. **Unsafe type escapes.** Type assertions like `as any` or forced casts masking runtime type mismatches.
9. **Non-deterministic dependencies.** Code relying on system timezone, floating point equality, or unordered map iterations where stable ordering is required.

## 3. Fowler code smell baseline

Apply these heuristics when reviewing diffs. Documented repo coding standards always override this baseline.

| Smell | Diagnostic condition | Remediation action |
|---|---|---|
| Mysterious Name | Name fails to communicate purpose or contained data | Rename the identifier, or redesign if a clear name cannot be found |
| Duplicated Code | Identical logic structure appears in multiple diff hunks | Extract the shared logic into a helper and invoke it from all call sites |
| Feature Envy | Function accesses external object data more than its own data | Relocate the function to the module owning the accessed data |
| Data Clumps | Identical parameter groups travel together across signatures | Encapsulate parameters into a dedicated data structure |
| Primitive Obsession | Raw primitives represent structured domain concepts | Introduce a dedicated domain type for the concept |
| Repeated Switches | Identical conditional branches recur across the change | Replace branching with polymorphism or a shared lookup table |
| Shotgun Surgery | Single logical change requires scattered edits across many files | Consolidate related logic into a single cohesive module |
| Divergent Change | Single module changes for multiple unrelated reasons | Split the module along separate responsibility boundaries |
| Speculative Generality | Unused abstractions or hooks added without specification demand | Delete speculative layers and inline logic until a real requirement appears |
| Message Chains | Caller navigates deeply nested object structures | Encapsulate traversal behind a single query method on the root object |
| Middle Man | Class or function only forwards calls without adding value | Remove wrapper and call target directly |
| Refused Bequest | Subclass ignores or overrides majority of inherited behavior | Replace inheritance with composition |
