# Story bindings and declared postures

Rule bindings and interim-posture atoms for STORY-0001 and STORY-0008. Postures
are written as checked claims rather than comments so a deviation is something the
suites test and the standing queries can see, never silence (PA-021).

## STORY-0001

STORY-0001's acceptance specifications become *enforceable* only when an active
rule binds them (ONT-036: an unbound claim is a proposal). The three rules below
are that binding, mounting CTRL-0004 at the build gate with ENF-0001 —
the governed form of SPEC-0073's sentence "a red suite blocks merge".

SPEC-0074 records the one deviation SPEC-0071 permits: `resolve`/`recall` are
stubbed until the data-access citizen exists. It is written as a checked claim
rather than a comment, so the interim posture is a thing the suite tests and the
standing queries can see — the L0 open item (c) recommendation carried out
(PA-021: every interim posture exists as a governed atom, never as silence).

<!-- atom:begin id=SPEC-0074 -->
```yaml
id: SPEC-0074
type: specification
scope: story:story-0001
state: proposed
version: 1.0.0
instantiated_at: "2026-08-11T05:30:00Z"
author: agent-worker-story-0001
authorized_by: null
title: "Interim posture: resolve/recall answer NOT_AVAILABLE until data-access exists"
tags: [interim-posture, l0-open-item-c]
binding: checked
check: machine
story_ref: STORY-0001
```
`agentd` serves the L0-020 surface in full except `resolve` and `recall`, which
return the error `NOT_AVAILABLE` together with the posture reason. Both are
served by the data-access citizen over the bus (PA-030 step 7), which does not
exist at step 4; a stub that answers honestly is preferable to an op that
appears to work. BASE-AC-14 is therefore satisfied as a declared posture, and
the conformance suite asserts the stub's exact response so the deviation cannot
quietly become permanent. This atom is superseded — not edited — when
`resolve`/`recall` begin answering.
<!-- atom:end id=SPEC-0074 -->

<!-- atom:begin id=RULE-0076 -->
```yaml
id: RULE-0076
type: rule
scope: platform
state: proposed
version: 1.0.0
instantiated_at: "2026-08-11T05:30:00Z"
author: agent-worker-story-0001
authorized_by: null
title: "Bind SPEC-0071 via CTRL-0004"
tags: [binding, step-4]
claim: SPEC-0071
control: CTRL-0004
enforcement: ENF-0001
relations:
  - { rel: binds, target: SPEC-0071 }
  - { rel: binds, target: CTRL-0004 }
  - { rel: binds, target: ENF-0001 }
```
<!-- atom:end id=RULE-0076 -->

<!-- atom:begin id=RULE-0077 -->
```yaml
id: RULE-0077
type: rule
scope: platform
state: proposed
version: 1.0.0
instantiated_at: "2026-08-11T05:30:00Z"
author: agent-worker-story-0001
authorized_by: null
title: "Bind SPEC-0072 via CTRL-0004"
tags: [binding, step-4]
claim: SPEC-0072
control: CTRL-0004
enforcement: ENF-0001
relations:
  - { rel: binds, target: SPEC-0072 }
  - { rel: binds, target: CTRL-0004 }
  - { rel: binds, target: ENF-0001 }
```
The falsifiability half: this rule is satisfied only when the violating fixture
*fails* the suite, which is why the control is invoked twice with opposite
expectations at the build gate.
<!-- atom:end id=RULE-0077 -->

<!-- atom:begin id=RULE-0078 -->
```yaml
id: RULE-0078
type: rule
scope: platform
state: proposed
version: 1.0.0
instantiated_at: "2026-08-11T05:30:00Z"
author: agent-worker-story-0001
authorized_by: null
title: "Bind SPEC-0073 via CTRL-0004"
tags: [binding, step-4]
claim: SPEC-0073
control: CTRL-0004
enforcement: ENF-0001
relations:
  - { rel: binds, target: SPEC-0073 }
  - { rel: binds, target: CTRL-0004 }
  - { rel: binds, target: ENF-0001 }
```
<!-- atom:end id=RULE-0078 -->

<!-- atom:begin id=RULE-0079 -->
```yaml
id: RULE-0079
type: rule
scope: platform
state: proposed
version: 1.0.0
instantiated_at: "2026-08-11T05:30:00Z"
author: agent-worker-story-0001
authorized_by: null
title: "Bind SPEC-0074 via CTRL-0004"
tags: [binding, step-4, interim-posture]
claim: SPEC-0074
control: CTRL-0004
enforcement: ENF-0001
relations:
  - { rel: binds, target: SPEC-0074 }
  - { rel: binds, target: CTRL-0004 }
  - { rel: binds, target: ENF-0001 }
```
<!-- atom:end id=RULE-0079 -->

## STORY-0008

<!-- atom:begin id=SPEC-0115 -->
```yaml
id: SPEC-0115
type: specification
scope: story:story-0008
state: proposed
version: 1.0.0
instantiated_at: "2026-08-12T17:00:00Z"
author: agent-worker-story-0008
authorized_by: null
title: "Interim posture: evidence embeds in batch, with coverage-zero as the gate"
tags: [interim-posture, d25, ont-085]
binding: checked
check: machine
story_ref: STORY-0008
```
ONT-085 requires embedding to be a non-optional side effect of persistence. In
bootstrap there is no streaming persistence pipeline: controls write their own
evidence rows into `acta/` directly, so a synchronous embed-at-persistence is not
available to honor. The posture, stated rather than left implicit: embedding runs
in batch, and **a non-empty coverage gap is a red condition** — the standing-query
report is the meter, satisfied by running the embedder before the report. ONT-085's
non-optionality is carried by the gate instead of by the write path.

The consequence is honest and bounded: between a control run and the next embedder
run, the newest evidence rows have no vector, so coverage is momentarily nonzero by
construction rather than by neglect. This atom is superseded — not edited — when the
data-access citizen's durable consumer (PA-007) makes persistence synchronous, at
which point embed-at-persistence holds literally and the gate becomes redundant.
<!-- atom:end id=SPEC-0115 -->

<!-- atom:begin id=RULE-0080 -->
```yaml
id: RULE-0080
type: rule
scope: platform
state: proposed
version: 1.0.0
instantiated_at: "2026-08-12T17:00:00Z"
author: agent-worker-story-0008
authorized_by: null
title: "Bind SPEC-0115 via CTRL-0007"
tags: [binding, interim-posture]
claim: SPEC-0115
control: CTRL-0007
enforcement: ENF-0001
relations:
  - { rel: binds, target: SPEC-0115 }
  - { rel: binds, target: CTRL-0007 }
  - { rel: binds, target: ENF-0001 }
```
<!-- atom:end id=RULE-0080 -->

---

## The spawn contract bindings (DEC-0005)

STORY-0002's acceptance criteria were checked by CTRL-0005 for a week before
anything bound them to it. The suite ran, the rows landed, the criteria passed —
and no rule said the criteria were the suite's to check, so ONT-031 read them as
unbound and ONT-060 had no trigger to activate them. A control that checks a claim
nobody wired to it is doing the work without the law noticing.

SPEC-0086 is deliberately absent from this set. It rides every evidence row and no
control asserts it, so binding it here would produce a rule with no enforcing check
— the SPEC-0091 shape. It stays a visible meter line until its control exists
(floor Finding 4, STORY-0014 window).

<!-- atom:begin id=RULE-0089 -->
```yaml
id: RULE-0089
type: rule
scope: platform
state: active
version: 1.2.0
instantiated_at: "2026-08-14T05:55:28.534619+00:00"
author: ont-060-reconciliation
authorized_by: DEC-0005
title: "Bind SPEC-0081 via CTRL-0005"
tags: [binding, spawn-contract, first-floor-touch]
claim: SPEC-0081
control: CTRL-0005
enforcement: ENF-0001
relations:
  - { rel: binds, target: SPEC-0081 }
  - { rel: binds, target: CTRL-0005 }
  - { rel: binds, target: ENF-0001 }
```
CTRL-0005 checks the spawn gate's refusals and what it produces when it admits.
<!-- atom:end id=RULE-0089 -->

<!-- atom:begin id=RULE-0090 -->
```yaml
id: RULE-0090
type: rule
scope: platform
state: active
version: 1.2.0
instantiated_at: "2026-08-14T05:55:28.534619+00:00"
author: ont-060-reconciliation
authorized_by: DEC-0005
title: "Bind SPEC-0082 via CTRL-0005"
tags: [binding, spawn-contract, first-floor-touch]
claim: SPEC-0082
control: CTRL-0005
enforcement: ENF-0001
relations:
  - { rel: binds, target: SPEC-0082 }
  - { rel: binds, target: CTRL-0005 }
  - { rel: binds, target: ENF-0001 }
```
CTRL-0005 checks the IO path: session stream to bus, live render, durable persistence.
<!-- atom:end id=RULE-0090 -->

<!-- atom:begin id=RULE-0091 -->
```yaml
id: RULE-0091
type: rule
scope: platform
state: active
version: 1.2.0
instantiated_at: "2026-08-14T05:55:28.534619+00:00"
author: ont-060-reconciliation
authorized_by: DEC-0005
title: "Bind SPEC-0083 via CTRL-0005"
tags: [binding, spawn-contract, first-floor-touch]
claim: SPEC-0083
control: CTRL-0005
enforcement: ENF-0001
relations:
  - { rel: binds, target: SPEC-0083 }
  - { rel: binds, target: CTRL-0005 }
  - { rel: binds, target: ENF-0001 }
```
CTRL-0005 checks isolation: ephemeral workspace and the sanctioned egress paths.
<!-- atom:end id=RULE-0091 -->

<!-- atom:begin id=RULE-0092 -->
```yaml
id: RULE-0092
type: rule
scope: platform
state: active
version: 1.2.0
instantiated_at: "2026-08-14T05:55:28.534619+00:00"
author: ont-060-reconciliation
authorized_by: DEC-0005
title: "Bind SPEC-0084 via CTRL-0005"
tags: [binding, spawn-contract, first-floor-touch]
claim: SPEC-0084
control: CTRL-0005
enforcement: ENF-0001
relations:
  - { rel: binds, target: SPEC-0084 }
  - { rel: binds, target: CTRL-0005 }
  - { rel: binds, target: ENF-0001 }
```
CTRL-0005 checks attribution: every envelope and commit chain-verifiable to the leaf.
<!-- atom:end id=RULE-0092 -->

<!-- atom:begin id=RULE-0093 -->
```yaml
id: RULE-0093
type: rule
scope: platform
state: active
version: 1.2.0
instantiated_at: "2026-08-14T05:55:28.534619+00:00"
author: ont-060-reconciliation
authorized_by: DEC-0005
title: "Bind SPEC-0085 via CTRL-0005"
tags: [binding, spawn-contract, first-floor-touch]
claim: SPEC-0085
control: CTRL-0005
enforcement: ENF-0001
relations:
  - { rel: binds, target: SPEC-0085 }
  - { rel: binds, target: CTRL-0005 }
  - { rel: binds, target: ENF-0001 }
```
CTRL-0005 checks supervision: interrupt, mid-session injection, clean terminate.
<!-- atom:end id=RULE-0093 -->


<!-- atom:begin id=RULE-0100 -->
```yaml
id: RULE-0100
type: rule
scope: platform
state: active
version: 1.2.0
instantiated_at: "2026-08-21T01:58:20.663072+00:00"
author: ont-060-reconciliation
authorized_by: DEC-0009
title: "Bind SPEC-0086 via CTRL-0011"
tags: [binding, versioned-measurement]
claim: SPEC-0086
control: CTRL-0011
enforcement: ENF-0001
relations:
  - { rel: binds, target: SPEC-0086 }
  - { rel: binds, target: CTRL-0011 }
  - { rel: binds, target: ENF-0001 }
```
The last of the twelve unbound claims that was unbound by choice rather than by
oversight. DEC-0005 left it so deliberately — binding a claim to a control that did
not exist would have been the SPEC-0091 shape — and carried it in the open as a meter
line for six days rather than hiding it. This closes it.
<!-- atom:end id=RULE-0100 -->

<!-- atom:begin id=RULE-0101 -->
```yaml
id: RULE-0101
type: rule
scope: platform
state: ratified
version: 1.1.0
instantiated_at: "2026-08-27T17:47:01.653057+00:00"
author: agent-worker-story-0010
authorized_by: DEC-0011
title: "Bind SPEC-0135 via CTRL-0012"
tags: [binding, human-evidence]
claim: SPEC-0135
control: CTRL-0012
enforcement: ENF-0004
relations:
  - { rel: binds, target: SPEC-0135 }
  - { rel: binds, target: CTRL-0012 }
  - { rel: binds, target: ENF-0004 }
```
SPEC-0135 was minted unbindable: `check: human` with no control that could take a
human's verdict as input. DEC-0008 recorded that openly rather than dressing it as
machine-checked, and this closes it — the first claim bound by the human-evidence
primitive.

ENF-0004 (advisory), not ENF-0001. The control asserts a record exists; a merge blocked
because nobody has read a provider's self-description yet would be a gate enforcing a
reading schedule rather than a property of the code.
<!-- atom:end id=RULE-0101 -->

<!-- atom:begin id=RULE-0102 -->
```yaml
id: RULE-0102
type: rule
scope: platform
state: ratified
version: 1.1.0
instantiated_at: "2026-08-27T17:47:01.653057+00:00"
author: agent-worker-story-0010
authorized_by: DEC-0011
title: "Bind SPEC-0116 via CTRL-0012"
tags: [binding, human-evidence]
claim: SPEC-0116
control: CTRL-0012
enforcement: ENF-0001
relations:
  - { rel: binds, target: SPEC-0116 }
  - { rel: binds, target: CTRL-0012 }
  - { rel: binds, target: ENF-0001 }
```
<!-- atom:end id=RULE-0102 -->

<!-- atom:begin id=RULE-0103 -->
```yaml
id: RULE-0103
type: rule
scope: platform
state: ratified
version: 1.1.0
instantiated_at: "2026-08-27T17:47:01.653057+00:00"
author: agent-worker-story-0010
authorized_by: DEC-0011
title: "Bind SPEC-0117 via CTRL-0012"
tags: [binding, human-evidence]
claim: SPEC-0117
control: CTRL-0012
enforcement: ENF-0001
relations:
  - { rel: binds, target: SPEC-0117 }
  - { rel: binds, target: CTRL-0012 }
  - { rel: binds, target: ENF-0001 }
```
CTRL-0012's fixtures are what check both claims: SPEC-0116's refusals — no automated
path to a human verdict — and SPEC-0117's content-addressed staleness. The half of
SPEC-0117 that CTRL-0012 cannot check is the owner's reviewing pass over the eleven,
which is a story-completion fact rather than a control's job.
<!-- atom:end id=RULE-0103 -->
