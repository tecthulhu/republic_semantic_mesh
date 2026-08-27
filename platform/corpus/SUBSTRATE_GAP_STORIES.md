# Substrate gap stories — human evidence, revocation runtime, provenance consistency

Three small stories chartered by ARCHITECT_RESPONSE_009 (D38, D39, D41). None
blocks STORY-0002; each closes a gap the C1 gate eventually needs closed. Cut
without `tracker_ref` per D27 — the reference is filled from the issue that
actually exists, in the commit that first needs it.

---

## STORY-0010 — human evidence

The one genuinely missing governance primitive (D39). Every other readiness number
has a mechanism; `check: human` claims have none, so `unbound_claims` cannot reach
zero however much code is written. Eleven claims are waiting on it today.

<!-- atom:begin id=STORY-0010 -->
```yaml
id: STORY-0010
type: story
scope: platform
state: proposed
version: 1.0.0
instantiated_at: "2026-08-12T21:00:00Z"
author: agent-worker-story-0009
authorized_by: null
title: "Human evidence: the signed-determination record for check: human claims"
tags: [governance-primitive, c1-gate]
tracker_ref: "gh:tecthulhu/republic#19"
acceptance: [SPEC-0116, SPEC-0117]
```
A human-evidence record is an `EVID-` atom whose `checker` is a human identity
rather than a tool identity. Evidence is evidence — the atom type does not fork;
what differs is the checker class, that it cannot be auto-emitted, and that its
authority is a signed act. Structurally, a human attesting "RSTR-0002 holds, verified
by inspection at digest X" is the same act as ratifying a decision, so it reuses the
machinery already built rather than adding a parallel one.
<!-- atom:end id=STORY-0010 -->

<!-- atom:begin id=SPEC-0116 -->
```yaml
id: SPEC-0116
type: specification
scope: story:story-0010
state: ratified
version: 1.1.0
instantiated_at: "2026-08-27T17:47:01.653057+00:00"
author: agent-worker-story-0009
authorized_by: DEC-0011
title: "Human-evidence records exist, are signed acts, and cannot be auto-emitted"
tags: [acceptance-criterion]
binding: checked
check: machine
story_ref: STORY-0010
```
A tool assembles a human-evidence record for a named claim at a named corpus digest
with `checker` set to a human identity, and refuses to emit one for a `check:
machine` claim. No automated path can produce a human-checker record: a fixture
demonstrates that the emitter requires an explicit human identity argument and that
the standing report counts such records only for claims whose `check` is `human`.
The record's authority is the signing commit that lands it, exactly as a ceremony's
is — no new authority mechanism is invented.
<!-- atom:end id=SPEC-0116 -->

<!-- atom:begin id=SPEC-0117 -->
```yaml
id: SPEC-0117
type: specification
scope: story:story-0010
state: ratified
version: 1.1.0
instantiated_at: "2026-08-27T17:47:01.653057+00:00"
author: agent-worker-story-0009
authorized_by: DEC-0011
title: "Human evidence goes stale on drift, and the eleven claims are evidenced once"
tags: [acceptance-criterion]
binding: checked
check: machine
story_ref: STORY-0010
```
A human-evidence record is true-at-T against the digest it names (ONT-014), so when
the claim's subject changes the record goes stale and the claim returns to
unevidenced — the same content-addressed staleness `--since` and the embedder
already implement, rather than a new expiry mechanism. A fixture proves a record
covering digest A stops counting once the corpus moves to digest B.

First real use is the acceptance test: the eleven `check: human` claims standing
today — RSTR-0002, RSTR-0004, RSTR-0009, RSTR-0012, SPEC-0001, SPEC-0003, SPEC-0010,
SPEC-0032, SPEC-0042, SPEC-0064, SPEC-0070 — are evidenced by the owner in one
reviewing pass, and `unbound_claims` reaches zero for the first time.
<!-- atom:end id=SPEC-0117 -->

---

## STORY-0011 — revocation runtime

D38 sequences this *after* the hop: the forward path (mint, attenuate, verify) must
prove out before teardown is worth building. What this story ends is P5 attesting a
design rule against a fixture tree instead of shipped behaviour.

<!-- atom:begin id=STORY-0011 -->
```yaml
id: STORY-0011
type: story
scope: platform
state: proposed
version: 1.0.0
instantiated_at: "2026-08-12T21:00:00Z"
author: agent-worker-story-0009
authorized_by: null
title: "Revocation runtime: downward revocation in the verifier, P5 behaviour-attested"
tags: [chain-verifier, post-hop]
tracker_ref: "gh:tecthulhu/republic#20"
acceptance: [SPEC-0118]
```
Revocation is the teardown path and is not on the C1 critical walk — a directive
produces work; it does not require revoking a leaf mid-hop. Until this lands, the
gap is a governed, visible posture (SPEC-0120) rather than a silent overclaim.
<!-- atom:end id=STORY-0011 -->

<!-- atom:begin id=SPEC-0118 -->
```yaml
id: SPEC-0118
type: specification
scope: story:story-0011
state: proposed
version: 1.0.0
instantiated_at: "2026-08-12T21:00:00Z"
author: agent-worker-story-0009
authorized_by: null
title: "chainverify revokes downward; P5 tests the verifier, not a fixture tree"
tags: [acceptance-criterion]
binding: checked
check: machine
story_ref: STORY-0011
```
`base/l0/chainverify.py` implements revocation: a revoked node invalidates its
entire subtree and nothing above it (ENT-051), checked during the chain walk and
failing closed like every other predicate. CTRL-0002's P5 then derives its verdict
from the verifier rather than from a tree the suite built itself, which is what makes
it evidence of behaviour. The revocation credential's shape follows ENT-077
(break-glass, co-signed at renewal). On landing, SPEC-0120's posture is superseded —
not edited — and the one-algebra check (SPEC-0108) still passes, because revocation
lives in the same module as the rest of the algebra.
<!-- atom:end id=SPEC-0118 -->

---

## STORY-0012 — provenance consistency

D41: SPEC-0113 catches content changing without a version bump. This catches the
level beneath — a version bumped while the provenance fields stay behind, which
passes lint today while misattributing the authoring act.

<!-- atom:begin id=STORY-0012 -->
```yaml
id: STORY-0012
type: story
scope: platform
state: proposed
version: 1.1.0
instantiated_at: "2026-08-12T22:00:00Z"
author: agent-worker-story-0009
authorized_by: null
title: "Provenance consistency: a new version must carry a new authoring act"
tags: [gate, follow-on]
tracker_ref: "gh:tecthulhu/republic#21"
acceptance: [SPEC-0119, SPEC-0121]
```
Caught as a near-miss while amending DOC-0000 for DEC-0004: a no-op'd replacement
left the reconciliation's `author` and `instantiated_at` on an amended instance, so
the atom would have claimed authorship by the reconciler at the reconciler's
timestamp. Lint passed. Provenance can currently lie through this gate.

v1.1.0 (D44) adds SPEC-0121: the repository-tree check. Both gates open atom_lint
for the same reason — a governed fact that no control scans — so they land in one
PR rather than two.
<!-- atom:end id=STORY-0012 -->

<!-- atom:begin id=SPEC-0119 -->
```yaml
id: SPEC-0119
type: specification
scope: story:story-0012
state: proposed
version: 1.1.0
instantiated_at: "2026-08-14T06:00:00Z"
author: agent-worker-dec-0005
authorized_by: null
title: "A version increment requires a fresh instantiated_at and a consistent author"
tags: [acceptance-criterion]
binding: checked
check: machine
story_ref: STORY-0012
```
The `--since` mode fails any atom whose `version` increments while
`instantiated_at` is unchanged from the prior instance: a new instance that claims
the previous instance's moment is not a new instance. It further fails an atom whose
`author` is inconsistent with the change class — an amendment carrying content
changes may not be authored by `ont-060-reconciliation`, whose only legitimate
change is a lifecycle transition. Fixtures demonstrate the stale-timestamp case and
the misattributed-author case caught, and a correctly-authored new instance passing.

v1.1.0 — **the prior instance is the previous commit, not the merge base.** The
author check is a claim about one authoring act, so it has to be evaluated against
one hop. DEC-0005's ceremony exposed the difference: the decision ratified
SPEC-0081 (setting `authorized_by`, under the decision's author) and reconciliation
then activated it (setting `state`, under the reconciler's). Both hops lawful; the
endpoint delta showed `authorized_by` moving under the reconciler's name, which the
reconciler never does, and the gate reported a misattribution that had not happened.
A check that cannot see a legitimate sequence will eventually be softened to admit
one, and softening the claim to match the tool is the wrong direction. Fixtures
demonstrate ratify-then-reconcile passing as two hops, and the reconciler amending
content on its own hop still caught.
<!-- atom:end id=SPEC-0119 -->

---

## The revocation posture

<!-- atom:begin id=SPEC-0120 -->
```yaml
id: SPEC-0120
type: specification
scope: platform
state: proposed
version: 1.0.0
instantiated_at: "2026-08-12T21:00:00Z"
author: agent-worker-story-0009
authorized_by: null
title: "Interim posture: revocation is model-attested, not behaviour-attested"
tags: [interim-posture, d38, ent-051]
binding: checked
check: machine
```
`chainverify` implements no revocation, so CTRL-0002's P5 derives its verdict from a
credential tree the suite constructed rather than from the verifier. SPEC-0056
(ENT-051's claim, "revocation walks downward only") is therefore attested against a
model of the rule and not against shipped behaviour, and this atom says so where a
reader of the standing report will see it.

The posture is itself checked, which makes it self-retiring: CTRL-0002 asserts that
the verifier exposes no revocation surface. When STORY-0011 implements one, that
assertion fails and forces this posture's supersession rather than letting it linger
as stale prose. Retirement condition: revocation in the chain verifier
(SPEC-0118), at which point P5 becomes behaviour-attested.
<!-- atom:end id=SPEC-0120 -->

<!-- atom:begin id=RULE-0081 -->
```yaml
id: RULE-0081
type: rule
scope: platform
state: proposed
version: 1.0.0
instantiated_at: "2026-08-12T21:00:00Z"
author: agent-worker-story-0009
authorized_by: null
title: "Bind SPEC-0120 via CTRL-0002"
tags: [binding, interim-posture]
claim: SPEC-0120
control: CTRL-0002
enforcement: ENF-0001
relations:
  - { rel: binds, target: SPEC-0120 }
  - { rel: binds, target: CTRL-0002 }
  - { rel: binds, target: ENF-0001 }
```
<!-- atom:end id=RULE-0081 -->

---

## The posture pattern, generalized

<!-- atom:begin id=PRIN-0005 -->
```yaml
id: PRIN-0005
type: principle
scope: platform
state: proposed
version: 1.0.0
instantiated_at: "2026-08-12T22:00:00Z"
author: agent-worker-story-0012
authorized_by: null
title: "An interim posture names a checkable condition, not a promise to revisit"
tags: [interim-posture, mechanism-over-discipline]
binding: injected
```
Every posture atom SHOULD name a condition that is itself checked, such that the
condition becoming false *fails a control* and forces the posture's supersession
(D42). A posture that promises to be revisited depends on someone remembering; a
posture whose enabling condition is a checked claim cannot outlive its own truth.

SPEC-0120 is the worked example: CTRL-0002 asserts that the chain verifier exposes no
revocation surface, so the first commit that implements revocation turns the suite
red, and the only way to green is to supersede the posture. The story that closes the
gap cannot pretend to be done while the hedge about it still stands.

This is mechanism-over-discipline applied to the corpus's own hedges, which is where
it is easiest to skip: an interim posture is precisely the kind of atom whose author
intends to come back, and intent is not a gate. Postures written before this
principle are not retroactively invalid — SPEC-0074 and SPEC-0115 name retirement
conditions in prose — but the pattern to reach for is the checked one.
<!-- atom:end id=PRIN-0005 -->

<!-- atom:begin id=SPEC-0121 -->
```yaml
id: SPEC-0121
type: specification
scope: story:story-0012
state: proposed
version: 1.2.0
instantiated_at: "2026-08-14T05:10:00Z"
author: agent-worker-dec-0005
authorized_by: null
title: "Every markdown file is governed, allowlisted, or a gate failure"
tags: [acceptance-criterion, d44]
binding: checked
check: machine
story_ref: STORY-0012
```
CTRL-0001 classifies every `*.md` file in the repository as one of: inside
`platform/corpus/**` and therefore governed, parsed and validated; an enumerated
root allowlist (CLAUDE.md, README.md, LICENSE); or a violation.

**At the repository root the allowlist is the whole rule.** Any `*.md` at the root
that is not on it fails the gate, whatever it is called. Below the root the
heuristic still applies — a file carrying atom markers, or named in the `DOC-`/`DEC-`
family or a bridge correspondence family, is a violation wherever it sits — because
under `platform/` and `suite/` an ordinary note is legitimate and a governed document
is not, and something has to tell them apart.

v1.2.0 replaces enumeration at the root with the rule. The naming pattern was widened
three times in four days — `ARCHITECT_RESPONSE_` missed `ARCHITECT_NOTE_`,
`ARCHITECT_` missed `FLOOR_`, both missed `BRIDGE_` — and each widening closed one
instance while leaving the class open. Every one of those files sat at the root with
the gate green. A rule that has to be extended once per new sender is a rule that
protects only against senders someone has already met, and the root does not need the
heuristic: it belongs to the repository's front matter, and governed content has
exactly one home.

This closes SPEC-0091's canonical-tree clause, which has had no enforcing control
since it was written and has been violated twice with every gate green. The reason
it stayed invisible is worth stating: a prose-only document changes no atom digest,
so the corpus looks byte-identical whether the document is admitted or abandoned at
the root. A rule with no binding control is precisely the dangling claim the meters
exist to surface, except this one dangled in the tree-shape dimension no control
scanned.

Fixtures demonstrate an atom-bearing file at the root caught, an
`ARCHITECT_RESPONSE_`-named prose file at the root caught, an allowlisted root file
passing, and the real repository passing.
<!-- atom:end id=SPEC-0121 -->
