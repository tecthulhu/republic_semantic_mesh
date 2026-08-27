# Controls

<!-- atom:begin id=CTRL-0001 -->
```yaml
id: CTRL-0001
type: control
scope: platform
state: active
version: 1.2.0
instantiated_at: "2026-08-12T18:38:23.725032+00:00"
author: ont-060-reconciliation
authorized_by: DEC-0003
title: "atom-lint"
tags: [enforcement-plane]
target: codebase
implementation: tools/atom_lint.py
```
Parses ONT-070a boundaries and frontmatter, validates schemas, ids, references, fixed fields, model literals, embedding fields, exception placement
<!-- atom:end id=CTRL-0001 -->

<!-- atom:begin id=CTRL-0002 -->
```yaml
id: CTRL-0002
type: control
scope: platform
state: active
version: 1.2.0
instantiated_at: "2026-08-12T18:38:23.725032+00:00"
author: ont-060-reconciliation
authorized_by: DEC-0003
title: "grammar property suite"
tags: [enforcement-plane]
target: artifact
implementation: tools/test_grammar.py
```
Property tests over the caveat algebra: attenuation monotonicity, fail-closed verification, layer separation, downward revocation
<!-- atom:end id=CTRL-0002 -->

<!-- atom:begin id=CTRL-0003 -->
```yaml
id: CTRL-0003
type: control
scope: platform
state: active
version: 1.2.0
instantiated_at: "2026-08-12T18:38:23.725032+00:00"
author: ont-060-reconciliation
authorized_by: DEC-0003
title: "lifecycle transition checker"
tags: [enforcement-plane]
target: codebase
implementation: tools/atom_lint.py#transitions
```
Validates lifecycle transitions in change history against the state machine and decision authorization
<!-- atom:end id=CTRL-0003 -->

<!-- atom:begin id=CTRL-0004 -->
```yaml
id: CTRL-0004
type: control
scope: platform
state: active
version: 1.2.0
instantiated_at: "2026-08-12T18:38:23.725032+00:00"
author: ont-060-reconciliation
authorized_by: DEC-0003
title: "citizenship conformance suite"
tags: [enforcement-plane]
target: runtime
implementation: suite/citizenship
```
Runs against every derived image: hardening, identity init, descriptor, heartbeat, interface conformance, layer sealing
<!-- atom:end id=CTRL-0004 -->

<!-- atom:begin id=CTRL-0005 -->
```yaml
id: CTRL-0005
type: control
scope: platform
state: active
version: 1.2.0
instantiated_at: "2026-08-14T04:35:36.374238+00:00"
author: ont-060-reconciliation
authorized_by: DEC-0003
title: "gate library suite"
tags: [enforcement-plane]
target: runtime
implementation: suite/gates
```
Tests spawn, merge, and runtime gates: story-required spawn, injection order, restriction pre/post, unsigned-input draft rule
<!-- atom:end id=CTRL-0005 -->

<!-- atom:begin id=CTRL-0006 -->
```yaml
id: CTRL-0006
type: control
scope: platform
state: active
version: 1.2.0
instantiated_at: "2026-08-14T04:35:36.374238+00:00"
author: ont-060-reconciliation
authorized_by: DEC-0003
title: "chain verifier suite"
tags: [enforcement-plane]
target: runtime
implementation: suite/chain
```
Tests the identity walk: chain-to-root, lease TTL at every hop, imperium ceilings, two-party minting, break-glass
<!-- atom:end id=CTRL-0006 -->

<!-- atom:begin id=CTRL-0007 -->
```yaml
id: CTRL-0007
type: control
scope: platform
state: active
version: 1.2.0
instantiated_at: "2026-08-12T18:38:23.725032+00:00"
author: ont-060-reconciliation
authorized_by: DEC-0003
title: "embedder pipeline suite"
tags: [enforcement-plane]
target: artifact
implementation: tools/test_embedder.py
```
Tests per-atom chunking, measurement provenance completeness, instrument digest pinning, generated-rendering rule
<!-- atom:end id=CTRL-0007 -->

<!-- atom:begin id=CTRL-0008 -->
```yaml
id: CTRL-0008
type: control
scope: platform
state: ratified
version: 1.1.0
instantiated_at: "2026-08-12T18:38:07.984886+00:00"
author: consul-extraction-pass
authorized_by: DEC-0003
title: "index and query suite"
tags: [enforcement-plane]
target: artifact
implementation: suite/index
```
Tests standing queries: dangling claims, unevidenced claims, coverage, provenance walk, append-only store
<!-- atom:end id=CTRL-0008 -->

<!-- atom:begin id=CTRL-0009 -->
```yaml
id: CTRL-0009
type: control
scope: platform
state: proposed
version: 1.0.0
instantiated_at: "2026-08-14T17:30:00Z"
author: agent-worker-story-0017
authorized_by: null
title: "merge enforcement probe"
tags: [enforcement-plane, meta-control]
target: artifact
implementation: suite/enforcement
```
Captures the live branch-protection state of the default branch and asserts the facts
the "a red suite blocks merge" claim depends on: status checks required, both
conformance contexts required by name, every required context actually published by a
workflow job, direct push and force-push refused, and no bypass actor. Derived from
the GitHub API on every run, never from a constant.

The only control whose subject is the hosting platform rather than this repository's
own content. That is deliberate: every other control checks something the corpus can
see, and enforcement is the one load-bearing fact that lives outside it.
<!-- atom:end id=CTRL-0009 -->

<!-- atom:begin id=CTRL-0010 -->
```yaml
id: CTRL-0010
type: control
scope: platform
state: active
version: 1.2.0
instantiated_at: "2026-08-14T21:43:37.871489+00:00"
author: ont-060-reconciliation
authorized_by: DEC-0006
title: "ingest structure lint"
tags: [enforcement-plane, instruction-layer, interim]
target: artifact
implementation: tools/ingest_lint.py
```
Validates the instruction staging tree: one instruction in one lifecycle state, a
declared type marker agreeing with its folder, no unclassified file, and — where a
file names the work it directs — a folder state agreeing with that work's real state.

The only control whose subject is outside the repository, and therefore the only one
no CI gate can run. It is invoked, and it says so on every evidence row (SPEC-0131).
<!-- atom:end id=CTRL-0010 -->

<!-- atom:begin id=CTRL-0011 -->
```yaml
id: CTRL-0011
type: control
scope: platform
state: active
version: 1.2.0
instantiated_at: "2026-08-21T01:58:20.663072+00:00"
author: ont-060-reconciliation
authorized_by: DEC-0009
title: "CLI pin check"
tags: [enforcement-plane, versioned-measurement]
target: artifact
implementation: tools/cli_pin_check.py
```
SPEC-0086's enforcing control. Compares the CLI pin the agent build declares against
the pin every evidence row records: each row must carry the executed binary's hash, no
row may drift from the declared version, and one declared version must resolve to
exactly one binary.

The last assertion is the load-bearing one. The binary hash is measured at build and
cannot be declared in the Dockerfile, so the check works both ways round —
declaration against measurement for the version, measurement against measurement for
the binary. A wrapper bump that silently swaps the executable underneath a fixed
version string is then a finding rather than a pin that still reads correctly.
<!-- atom:end id=CTRL-0011 -->

<!-- atom:begin id=CTRL-0012 -->
```yaml
id: CTRL-0012
type: control
scope: platform
state: ratified
version: 1.1.0
instantiated_at: "2026-08-27T17:47:01.653057+00:00"
author: agent-worker-story-0010
authorized_by: DEC-0011
title: "human-evidence primitive"
tags: [enforcement-plane, human-evidence]
target: artifact
implementation: tools/human_evidence.py
```
The control that makes a `check: human` claim bindable. It asserts that a
human-evidence record exists for the claim, names a human, and is current against the
corpus digest it covers — and it asserts nothing about the judgment inside, which is
the human's and which no control can grade.

Emission has no automated path: the emitter refuses a `check: machine` claim, refuses
a missing or empty checker with no default and no derivation from git config, and
refuses a claim that resolves to nothing. Staleness is content-addressed rather than
scheduled: a record covers the digest it names, and stops covering a corpus that has
moved.
<!-- atom:end id=CTRL-0012 -->
