# Memory safety, binary, and kernel hunting

Reach for this file when the target processes untrusted bytes in a memory-unsafe or privileged context: C, C++, Objective-C, Rust `unsafe`, FFI, kernel modules and drivers, parsers and decoders, network daemons, firmware, binary loaders, language runtimes, and JITs. Use `protocols-rpc-and-messaging.md` for protocol authorization and state-machine logic, and this file for process integrity, memory safety, ABI boundaries, and loader behavior.

Pick relevant classes from Phase 1 and split large targets by parser, allocator lifetime, FFI, concurrency, loader, runtime, or privileged interface.

## Authoritative standards

Ground memory safety and binary audits in these authoritative guidelines:

| Standard | Publishing body | Reference URL | Focus |
|---|---|---|---|
| Memory Safe Roadmaps | CISA / NSA / FBI | https://www.cisa.gov/resources-tools/resources/case-memory-safe-roadmaps | Phased elimination of memory safety vulnerabilities |
| Software Memory Safety CSI | NSA | https://media.defense.gov/2022/Nov/10/2003112742/-1/-1/0/CSI_SOFTWARE_MEMORY_SAFETY.PDF | Memory-safe language transitions and hardware mitigations |
| CWE-119 Buffer Errors | MITRE Corporation | https://cwe.mitre.org/data/definitions/119.html | Memory buffer bounds and index calculation weaknesses |
| CWE-416 Use After Free | MITRE Corporation | https://cwe.mitre.org/data/definitions/416.html | Pointer referencing deallocated memory space |

## Core discipline

Include these rules in every agent prompt for this domain:

```text
- Re-derive every bound and lifetime from attacker-controlled inputs and all callers. Validate against the worst accepted case, not a typical test vector.
- A panic, sanitizer finding, or crash proves a defect only when a realistic untrusted input reaches it. Do not infer memory corruption, code execution, or shared availability impact from a label alone.
- Validate in a local harness with sanitizers, deterministic concurrency tests, existing fuzz targets, and debugger-assisted fault classification. Stop after proving the violated invariant and observable impact; do not develop post-corruption techniques.
- Assembly, JIT code, custom allocators, intra-object accesses, and foreign libraries can escape sanitizer coverage. Identify which relevant instructions are instrumented.
- Classify as confirmed only after source evidence and bounded local validation establish the defect and effect. Use needs_validation when ABI, allocator, architecture, feature, deployment, or reachability facts remain unknown.
```

## Bounds, integer, and representation attack classes

### Out-of-bounds read or write

A length, offset, index, or terminator reaches a fixed or allocated buffer without a correct bound. Recalculate available headroom after prefixes, alignment, padding, and terminators. Check both source and destination capacity, and whether a short input is read before its declared length is trusted.

### Integer overflow, underflow, truncation, and signedness

Review attacker-controlled arithmetic before allocation, copy, loop, indexing, and pointer operations. High-hit patterns include `a - b` with `b > a`, `count * element_size`, additions near the type maximum, negative values converted to unsigned, 64-bit lengths narrowed to 32-bit fields, and sentinel values such as `-1` becoming a large size. Confirm which checked representation is later used.

### Unit and pointer-depth confusion

Code mixes bytes, elements, code units, pages, words, wire units, or nested pointer element sizes. Compare the unit at parse, validation, allocation, API boundary, and copy. A bounds check using the same wrong unit as the allocation is still wrong.

### Uninitialized or partially initialized data

A buffer, padding, struct field, or vector capacity is returned, compared, hashed, serialized, or passed across a trust boundary before initialization. Require an observable consumer and realistic output length; stack allocation by itself is not disclosure.

## Lifetime, type, and concurrency attack classes

### Use-after-free, stale view, and double free

Owners are released while callbacks, wait queues, timers, iterators, borrowed slices, or cached raw pointers can still use them. Review every error, cancellation, close, and realloc path. For embedded notification anchors, each free path must drain or detach all observers.

### Type confusion and invalid downcast

A tag, vtable, union discriminator, object kind, or foreign handle is checked differently from the representation later read. Look for unchecked dynamic casts, stale tags after reuse, and serialized types whose validated element differs from the element consumed. Confirm a wrong-type read or write locally without extending the test beyond the violated invariant.

### Rust unsafe invariants and borrow violations

In Rust codebases utilizing `unsafe` blocks, verify compliance with core language safety contracts:
- Strict Provenance rules: converting integers to pointers or casting raw pointers without valid provenance is an invariant violation.
- Aliasing and UnsafeCell: creating multiple mutable references (`&mut`) to the same location, or casting shared references (`&T`) to mutable pointers without `UnsafeCell`, violates the Stacked Borrows and Tree Borrows memory models.
- Undefined behavior on unwind: panic across `extern "C"` FFI boundaries without abort or catch unwind handlers.

### Concurrency races, shared-state, and TOCTOU

Concurrent parser streams, global caches, lazy initialization, signal handlers, and resource teardown can invalidate bounds, policy, or pointers established earlier. Verify the race with a repeatable local schedule, barrier, or thread sanitizer; a hypothetical interleaving without a security-relevant state transition remains `needs_validation`.

## FFI, ABI, and compiler mitigation attack classes

### Binary compilation and hardening mitigations

Verify whether build systems enforce baseline compiler exploit mitigations:
- Stack Smashing Protection (`-fstack-protector-strong`).
- Control Flow Integrity (`-fsanitize=cfi` or hardware shadow stacks).
- Position Independent Executables (`-fPIE -pie`).
- Full Relocation Read-Only (`-Wl,-z,relro,-z,now`).
- Non-executable stacks (`-Wl,-z,noexecstack`).

### Pointer-length and ownership contract mismatch

Caller and callee disagree on who allocates, frees, pins, or mutates a buffer, how long a pointer remains valid, or whether a length is bytes or elements. Trace both sides of every `extern`, CGo, JNI, Python native binding, and generated wrapper. Check null, zero length, aliasing, and callback retention.

### Layout, alignment, and enum disagreement

Foreign code receives a struct, bitfield, packed record, callback signature, integer width, enum, or calling convention that differs by architecture or build flag. Verify `repr`, packing, alignment, endianness, and ABI-specific types. An in-repo declaration mismatch can be confirmed locally; an opaque foreign implementation requires `needs_validation`.

## Binary loading and runtime attack classes

### Library, plugin, and executable search-order trust

A privileged process loads a library, plugin, runtime image, or helper from a path writable by a less-trusted principal, or resolves a bare name through an attacker-influenceable working directory or environment. Compare intended installation ownership with each fallback and compatibility search path. A user loading their own plugin into their own process is not a boundary violation.

### Missing artifact identity or signature binding

A loader verifies one file or metadata record but maps a different image because path resolution, file replacement, architecture slices, or embedded resources are not bound to the check. Supply-channel authenticity belongs in `supply-chain-and-release.md`; this class covers the local verification-to-map gap.

### Malformed binary metadata and relocation handling

Offsets, counts, sections, relocations, symbols, bytecode, or debug metadata are trusted before range, overlap, and representation checks. Test parsers with bounded local fixtures and sanitizers. Separate memory corruption from a safely rejected malformed file.

## Kernel and privileged-interface attack classes

### User-copy bounds and repeated reads

A syscall, ioctl, driver, or kernel parser derives a trusted fact from user memory then reads the same mutable address again. Copy the full request once or revalidate the later copy. Also audit size, direction, and access checks at each user-copy primitive.

### Privileged object lifecycle and dispatch consistency

Externally reachable objects have unbalanced retain or release calls, teardown without observer drain, unchecked selector table indices, or duplicated compatibility paths that omit a guard. Diff each dispatch and free path side by side.

## Universal moves

- Audit fixes and duplicated paths for the same source-to-sink shape. A check in one caller, architecture, protocol role, feature flag, or compatibility path does not protect its siblings.
- Build a table for every parser or FFI boundary: accepted length or type, checked representation, allocation owner, consumer, thread, and teardown.
- Use existing corpora and small locally generated boundary fixtures. Save exact sanitizer or runtime output and the input property that triggers it. Avoid large resource consumption and live targets.

## Validation rules

1. Establish a realistic untrusted entry and exact operation that violates a bounds, type, lifetime, ABI, concurrency, loader, or authority invariant.
2. Classify the observable effect: invalid read, invalid write, stale alias, wrong object, uninitialized output, unauthorized image load, deadlock, or safe process termination. Do not claim a stronger effect than observed.
3. Run the narrowest local harness, existing test, sanitizer, or fuzzer needed to reproduce the effect. Verify sanitizer coverage of the faulting operation and record architecture and build conditions.
4. For concurrency, use a deterministic schedule or sanitizer trace. For binary loading, prove the checked identity differs from the mapped identity and name the lower-trust writer.
5. Return `confirmed` findings only with exact input, source trace, and observed result. Return `needs_validation` for a specific unresolved reachability, ABI, build, deployment, or runtime fact and state the bounded check needed.
