# The instruction layer, brought under governance

**STORY-0018.** Source: `INITIATOR_ingest_governance_bootstrap.md` and the four
documents it queued, consumed through `atomic_ingest/` in the order it named.

## What was ungoverned

Republic governs its code layer — atoms, lifecycle, provenance, gates. It did not
govern the channel by which the floor directs the mesh. That channel was session
pastes, drop-files at the repository root, and hand-moved folders, and it produced
precisely the failure class this corpus exists to make impossible:

- one instruction in two lifecycle states at once
- an artifact filed as an instruction
- work marked `executed` while its pull request was open
- a bulk move that nearly swept live work into `executed`

Every one of those is a state the atom lifecycle cannot represent. They happened
because the instruction lifecycle lived in human memory instead of in a check — the
diffuse discipline that this program has, repeatedly and on the record, found does not
hold. The floor performed by hand the exact errors the corpus prevents by construction,
which is a better argument for the corpus than any of its documentation.

## What this is, and what it is not

This is the **interim**: a lint (mechanism), a decision (law), a posture (discipline),
and a state-coherence check (the subtle error closed). It makes the errors *caught*.

It does not make them *impossible*. That is atomization (STRAT-0002), where lifecycle
state is an atom field rather than a folder and a category error fails schema
validation rather than a lint pass. The interim is a bridge with a far bank, and
naming the far bank is what keeps a bridge from becoming a building.

## The honest limit, stated first because it changes what the rest is worth

`atomic_ingest/` lives outside this repository, so **no CI gate runs CTRL-0010.** It is
a control, not enforcement — the same distinction CTRL-0009 was built to keep visible,
now applying to the control that polices instructions. It is invoked by the floor and
the agent, and every evidence row it writes says so.

Making it enforcement means tracking the ingest tree somewhere CI can read it. That is
the floor's call and it is a real choice with a cost: an instruction channel inside the
repository is public, and some instructions may not want to be. Recorded as a declared
gap in SPEC-0131 rather than left for a reviewer to notice that a lint nobody must run
is not a gate.

---

<!-- atom:begin id=SPEC-0131 -->
```yaml
id: SPEC-0131
type: specification
scope: platform
state: active
version: 1.4.0
instantiated_at: "2026-08-21T02:00:00Z"
author: agent-worker-dec-0009
authorized_by: DEC-0009
title: "The instruction staging tree has one state per instruction and a declared type"
tags: [acceptance-criterion, instruction-layer, interim, ingest]
binding: checked
check: machine
story_ref: STORY-0018
```
CTRL-0010 validates `atomic_ingest/` and names both the file and the rule for every
violation. A lint that reports "invalid" makes someone go looking; one that names the
file and the rule has already looked.

The rules, each an error the floor hit by hand:

- **One instruction, one state.** A filename appearing in more than one of
  `proposed`/`active`/`executed`/`parked`/`withdrawn` is a violation — the single-authoring-chain
  law with folders standing in for the `state` field.
- **Type is declared, never inferred.** Each file carries
  `<!-- ingest: TYPE -->` in its head, from a closed set. A filename is a guess; this
  has to be a fact. A marker below the head does not count, because front matter that
  a reader scrolls past is not front matter.
- **Type agrees with folder.** An `artifact` in a lifecycle folder, or an instruction
  under `artifacts/`, is a violation: a deliverable has no instruction lifecycle, and
  an instruction filed as a deliverable stops being acted on.
- **Nothing unclassified.** A file at the ingest root or in an undeclared folder fails,
  for the same reason the repository tree gate rejects one: the answer to "what is
  this?" must never be "nobody said".
- **Counts are reported, not judged.** An empty `proposed/` is legal; a crowded
  `active/` is legal and worth seeing.
- **Empty input is a failure**, not a pass (SPEC-0092's law applied here).

v1.3.0 adds `withdrawn` (DEC-0008). An instruction corrected and replaced *before*
enactment is neither deferred nor done: `parked` says the floor chose to defer,
`executed` says the work landed, and both misreport. The ferry charter forced it twice
in one day — v0.2 superseded by v0.3, v0.3 by v0.4, each inside the window
ratification-by-merge leaves open. A lifecycle that cannot say *replaced before it took
effect* pushes that history into a comment, and a comment is where history stops being
queryable.

v1.4.0 (DEC-0009) makes the type marker **optional in `artifacts/`**, where the folder
already declares the type. A ferried deliverable arrives with its bytes pinned by a
receipt and a manifest; adding a marker to satisfy the lint would break both in one
stroke, so the check would be demanding that the tree lie to it. The marker exists to
catch folder/marker *disagreement*, and an absent marker cannot disagree. Nine
digest-pinned artifacts go green with zero bytes changed.

The same amendment declares `manifest` as an ingest type and exempts ferry
infrastructure — dot-prefixed paths such as `.ferry/`, where DEC-0008 sites the trust
registers, and detached `.sig` files, whose bytes cannot carry a marker without
destroying what they sign. The charter requires the sweeper to find an
"ingest-lint-conformant shipment manifest", which is only meaningful if the lint has a
type for one.

**Declared gap: this is a control without enforcement.** The ingest tree is outside the
repository, so no CI check can run this and no merge is refused on it. Every evidence
row carries that qualification. It closes when the tree is tracked somewhere CI can
read, or when atomization (STRAT-0002) makes the properties structural.

**A second limit, found by testing the claim rather than repeating it.** The source
document held that the lint makes a wildcard sweep safe. It does so only when the
sweep *duplicates* — a clean `mv proposed/* executed/` leaves no duplicate, no category
error, and no unclassified file. It leaves a tree that lies, and nothing structural can
tell that from work that genuinely finished. SPEC-0133 is what closes it, and the
fixture asserting this limit is written to fail if anyone later claims otherwise.

Fixtures demonstrate each rule in both directions, including a same-named artifact
correctly *not* counted as a lifecycle duplicate, and the clean-sweep gap held open on
purpose.
<!-- atom:end id=SPEC-0131 -->

<!-- atom:begin id=RULE-0096 -->
```yaml
id: RULE-0096
type: rule
scope: platform
state: active
version: 1.2.0
instantiated_at: "2026-08-14T21:43:37.871489+00:00"
author: ont-060-reconciliation
authorized_by: DEC-0006
title: "Bind SPEC-0131 via CTRL-0010"
tags: [binding, instruction-layer, interim]
claim: SPEC-0131
control: CTRL-0010
enforcement: ENF-0004
relations:
  - { rel: binds, target: SPEC-0131 }
  - { rel: binds, target: CTRL-0010 }
  - { rel: binds, target: ENF-0004 }
```
ENF-0004 (advisory), not ENF-0001 (block merge) — and the difference is the whole
point. A rule cannot claim to block a merge when nothing runs it at merge time. Naming
ENF-0001 here would be a governed atom asserting an enforcement that does not exist,
which is the failure this story was written to prevent, committed in the act of
preventing it. It becomes ENF-0001 when the tree is somewhere CI can read.
<!-- atom:end id=RULE-0096 -->

---

## The single channel

<!-- atom:begin id=SPEC-0132 -->
```yaml
id: SPEC-0132
type: specification
scope: platform
state: active
version: 1.2.0
instantiated_at: "2026-08-14T21:43:37.871489+00:00"
author: ont-060-reconciliation
authorized_by: DEC-0006
title: "Interim posture: no instruction reaches the mesh except through atomic_ingest"
tags: [declared-posture, interim-posture, instruction-layer, d42]
binding: checked
check: machine
story_ref: STORY-0018
relations:
  - { rel: derives, target: DEC-0006 }
```
Instructions enter at `proposed/`, move to `active/` when consumed, and `executed/`
when their work merges. Content delivered outside the channel is conversation, not
direction, until it enters the channel.

Deliberately binary. Not "manage the instruction lifecycle carefully" — that is the
diffuse discipline that already failed, twice, in ways the floor had to catch by hand.
The question this posture asks has one bit in it: *did an instruction reach the agent
outside `atomic_ingest`?* A narrow rule holds where a broad aspiration does not.

**The residue, named rather than hidden.** One step is not mechanized: the floor
placing an instruction in `proposed/`. Everything after placement is checked —
lifecycle by CTRL-0010, state honesty by SPEC-0133 — so the un-mechanized surface is a
single bright-line human act, which is the smallest residue available before the
courier and the one the courier removes.

Self-failing condition (PRIN-0005): CTRL-0010 asserts the ingest tree exists and holds
the instruction lifecycle. The posture's retirement condition is the courier
(STORY-0006) going live, at which point instructions arrive as corpus atoms and the
single channel is enforced by delivery rather than by a commitment. A posture standing
long past a viable courier is the interim outliving its cure, and STRAT-0002 names the
measurement that decides when that is.
<!-- atom:end id=SPEC-0132 -->

<!-- atom:begin id=RULE-0097 -->
```yaml
id: RULE-0097
type: rule
scope: platform
state: active
version: 1.2.0
instantiated_at: "2026-08-14T21:43:37.871489+00:00"
author: ont-060-reconciliation
authorized_by: DEC-0006
title: "Bind SPEC-0132 via CTRL-0010"
tags: [binding, declared-posture, interim]
claim: SPEC-0132
control: CTRL-0010
enforcement: ENF-0004
relations:
  - { rel: binds, target: SPEC-0132 }
  - { rel: binds, target: CTRL-0010 }
  - { rel: binds, target: ENF-0004 }
```
<!-- atom:end id=RULE-0097 -->

---

## State coherence

<!-- atom:begin id=SPEC-0133 -->
```yaml
id: SPEC-0133
type: specification
scope: platform
state: active
version: 1.2.0
instantiated_at: "2026-08-14T21:43:37.871489+00:00"
author: ont-060-reconciliation
authorized_by: DEC-0006
title: "An instruction's folder must agree with the state of the work it references"
tags: [acceptance-criterion, instruction-layer, interim, ingest]
binding: checked
check: machine
story_ref: STORY-0018
relations:
  - { rel: derives, target: SPEC-0131 }
```
A file naming the work it directs — `<!-- ingest-ref: STORY-0017 PR#33 -->` — must sit
in a folder that agrees with that work's real state. `executed/` against an open pull
request is **false-executed**; `active/` against a merged one is stale; `proposed/`
against work already under way is a queue that has lost track of itself. A file naming
nothing is exempt from this check and still subject to SPEC-0131.

This is the one error class about *truth* rather than shape, and the one the structural
checks cannot reach. A clean sweep into `executed/` leaves a structurally perfect tree
that claims work is done which is not; any process trusting the folder would drop live
work. Binding folder-state to referenced-work-state makes done-ness a resolved fact
rather than a human judgement — the same move the corpus makes for atoms, where state
follows a ratifying act rather than a wish.

**A story's lifecycle state is not a done-signal in this corpus, and that is by
design.** SPEC-0122 rules that a story stays pre-ratified while the work earning its
ratification is in flight, and it stays `proposed` after that work merges until a
decision ratifies it. STORY-0013 read `proposed` with its work merged. So resolving
done-ness from the corpus would mark every finished instruction as unfinished, and the
pull request is the only reliable signal. A file claiming `executed/` must therefore
name one; a story-only reference in `proposed/`, `active/` or `parked/` is honest about
not knowing yet and passes.

Unresolvable references **fail closed** — reported as unverifiable, never passed. The
resolution source is the public GitHub API, unauthenticated, so a reader can repeat the
resolution; the mode is recorded on the evidence row, because a run that skipped this
check and a run that passed it must not look alike.

Fixtures demonstrate: `executed/` against an open pull request caught — the exact
situation the floor caught by hand; the same file green once it merges; stale-active
caught; a queued file whose work has started caught; an unresolvable reference failing
closed; reference-free files exempt; and a story-only reference caught in `executed/`
while passing in the earlier states.
<!-- atom:end id=SPEC-0133 -->

<!-- atom:begin id=RULE-0098 -->
```yaml
id: RULE-0098
type: rule
scope: platform
state: active
version: 1.2.0
instantiated_at: "2026-08-14T21:43:37.871489+00:00"
author: ont-060-reconciliation
authorized_by: DEC-0006
title: "Bind SPEC-0133 via CTRL-0010"
tags: [binding, instruction-layer, interim]
claim: SPEC-0133
control: CTRL-0010
enforcement: ENF-0004
relations:
  - { rel: binds, target: SPEC-0133 }
  - { rel: binds, target: CTRL-0010 }
  - { rel: binds, target: ENF-0004 }
```
<!-- atom:end id=RULE-0098 -->

---

## The destination

<!-- atom:begin id=STRAT-0002 -->
```yaml
id: STRAT-0002
type: strategy
scope: platform
state: active
version: 1.2.0
instantiated_at: "2026-08-14T21:43:37.871489+00:00"
author: ont-060-reconciliation
authorized_by: DEC-0006
title: "Ingest atomization and the courier: retiring the instruction interim"
tags: [instruction-layer, destination, gated]
horizon: "after the interim proves the workflow and measured friction justifies the build"
outcomes:
  - "Instruction lifecycle state is an atom field, not a folder — two states become impossible rather than caught"
  - "Instruction type is a schema type — a category error fails validation, not a lint"
  - "State honesty is inherent: an atom's state follows a ratifying act, so executed cannot be claimed over open work"
  - "Instruction provenance is native: one authoring chain, walkable like every other atom"
  - "The courier (STORY-0006) delivers instruction atoms across planes, retiring the placement residue"
constraints: [SPEC-0131, SPEC-0132, SPEC-0133]
```
**This charters nothing.** It names the far bank so the interim is understood as
interim.

At atomization, CTRL-0010 and SPEC-0133 become redundant: their properties are enforced
by the schema and lifecycle they were standing in for. That is the mark of a
well-formed interim — it names the thing that will make it unnecessary.

The courier carries **artifacts, not authority**: a couriered instruction is still
`proposed` until floor-touched. It is a dumb pipe like the bus, never a governance
service, and it preserves the single authoring chain because delivery is not authorship.

**The gate is a measurement, not a hunch.** Before chartering the courier, capture the
friction the interim actually leaves: how often the floor hand-places instructions, how
often placement is the bottleneck, and how often SPEC-0132's one un-mechanized step is
where delay or error enters. Measure before formalize — the same discipline that
produced the two meters, and the reason DEC-0004 exists.
<!-- atom:end id=STRAT-0002 -->

---

<!-- atom:begin id=STORY-0018 -->
```yaml
id: STORY-0018
type: story
scope: platform
state: active
version: 1.2.0
instantiated_at: "2026-08-14T21:43:37.871489+00:00"
author: ont-060-reconciliation
authorized_by: DEC-0006
title: "Ingest governance bootstrap: the instruction layer gets a lifecycle and a check"
tags: [instruction-layer, interim, bootstrap, ingest]
tracker_ref: "gh:tecthulhu/republic#34"
acceptance: [SPEC-0131, SPEC-0132, SPEC-0133]
relations:
  - { rel: advances, target: STRAT-0002 }
```
Consumed from the governed queue in the order the initiator named, and dogfooded from
the first step: each item moved `proposed → active` on consumption and `active →
executed` on merge, under the discipline being installed.

Does not preempt STORY-0014. The bootstrap is small and it makes every subsequent
instruction — STORY-0014's dispositions included — arrive through the governed channel,
so doing it first pays compounding interest.
<!-- atom:end id=STORY-0018 -->

---

## The injection payload contract (DEC-0007)

<!-- atom:begin id=SPEC-0134 -->
```yaml
id: SPEC-0134
type: specification
scope: platform
state: active
version: 1.2.0
instantiated_at: "2026-08-14T21:43:37.871489+00:00"
author: ont-060-reconciliation
authorized_by: DEC-0007
title: "The injected payload carries all law and declares the force of each entry"
tags: [acceptance-criterion, injection, knowledge-plane, enforcement-plane]
binding: checked
check: machine
relations:
  - { rel: derives, target: DEC-0007 }
```
CTRL-0005 asserts the payload contract DEC-0007 rules:

- **Completeness of law.** Every governed document and restriction whose state is
  `ratified` or `active` reaches the citizen. Ratification is the knowledge threshold;
  binding is not.
- **Force declared, never inferred.** Every entry carries `in_force`. Presence in the
  payload is knowledge; enforcement is a separate fact and says so.
- **No unearned force.** No restriction may carry `in_force: true` while nothing
  evaluates restrictions. The flag tracks implementation, not intention, and flips per
  restriction as evaluators land.
- **Draft is not law.** Pending documents appear as ids and titles under `pending_law`,
  marked `draft`, with no draft text anywhere in the payload.
- **The shortfall reports and never gates.** `unarmed_in_payload` sits beside
  `unbound_claims`; neither moves the verdict.

The third assertion is the load-bearing one, and it exists because the obligation that
became it would have done the opposite. Marking the active restrictions enforced was
the intuitive reading of "declare the force of each entry", and it would have put a
false enforcement claim into every citizen's payload — inside the disposition written
to prevent exactly that. The check makes the honest answer the only one that passes.
<!-- atom:end id=SPEC-0134 -->

<!-- atom:begin id=RULE-0099 -->
```yaml
id: RULE-0099
type: rule
scope: platform
state: active
version: 1.2.0
instantiated_at: "2026-08-14T21:43:37.871489+00:00"
author: ont-060-reconciliation
authorized_by: DEC-0007
title: "Bind SPEC-0134 via CTRL-0005"
tags: [binding, injection]
claim: SPEC-0134
control: CTRL-0005
enforcement: ENF-0001
relations:
  - { rel: binds, target: SPEC-0134 }
  - { rel: binds, target: CTRL-0005 }
  - { rel: binds, target: ENF-0001 }
```
ENF-0001 here, unlike the ingest rules: CTRL-0005 runs in CI on every change, so this
claim genuinely blocks a merge.
<!-- atom:end id=RULE-0099 -->

---

## The ferry, chartered (DEC-0008)

<!-- atom:begin id=STRAT-0003 -->
```yaml
id: STRAT-0003
type: strategy
scope: platform
state: active
version: 1.2.0
instantiated_at: "2026-08-20T16:44:10.423195+00:00"
author: ont-060-reconciliation
authorized_by: DEC-0008
title: "The ferry system: a signed, spooled, acknowledged cross-plane channel"
tags: [ferry, courier, transport, cross-plane, charter]
horizon: "P0 in one sitting; P1 unlocks on P0's first acknowledged receipt"
outcomes:
  - "Artifacts cross planes under floor authority, never carrying authority (B-1)"
  - "Two identities per shipment: an enrolled machine signs for custody, an enrolled principal approves in presence for authorization (B-2)"
  - "Digest law at write and at read; register beats receipt beats label (B-3)"
  - "Keys and provider credentials are per-machine local state, never on the chat plane, never copied between machines (B-4)"
  - "Shipment, auth, acknowledgement and access logs are append-only (B-5)"
  - "A shipment terminates only at a digest-bound acknowledgement, so transport success is never read as consumption success"
  - "Both trust registers live on the reception plane with the verifier, so Republic carries no shipping infrastructure and superseding the ferry never touches Republic code"
constraints: [SPEC-0132]
relations:
  - { rel: derives, target: STRAT-0002 }
  - { rel: contains, target: SPEC-0135 }
```
The charter is admitted at `corpus/FERRY_SYSTEM_CHARTER.md`, v0.4, digest
`416226d91e3c0150`. This atom is the governed handle; the document is the argument.

**What forced it.** Three silent drops in one week, each caught by downstream
discipline and none prevented. **The hand-ferry's failure mode is silence**, and
silence is the one failure no care downstream converts into a signal. Two of the three
this session met directly, and a fourth arrived while the charter was being ratified:
the principal-verifier contract landed with perfect digests and could not be consumed,
because the charter version it cites had not shipped.

**Why the lifecycle terminates where it does.** `CREATED → AUTHORIZED → TRANSPORTED →
RECEIVED → ACKNOWLEDGED`, and only the last is terminal. That contract is the proof: a
flawless delivery whose shipment was unusable. A receipt can say the bytes arrived; it
cannot say the shipment was consumable, and treating those as one fact is where the
silent drops lived.

**Two identities, two truth-levels, honestly labelled.** The machine signature is
evidence-grade — an offline-verifiable artifact. The principal's Duo approval is
attested-with-independent-witness — a third party's transaction record, not a
cryptographic artifact. The registers state each factor's strength plainly and **never
claim more verification than the factor provides**. The first principal row is recorded
as a self-attested genesis act, because every identity system bootstraps from a root no
higher authority certifies and the honest move is to write that down rather than let
the row imply otherwise.

Floor-touch and human-evidence stay cousins here too: machine enrollment is the floor's
grant, principal approval is human presence, and neither substitutes for the other —
the same separation STORY-0014 kept.

**Derives from STRAT-0002 rather than superseding it.** STRAT-0002 names atomization
and the courier; this concretizes the courier and leaves atomization where it was. It
does not retire SPEC-0132: that posture ends when the courier is *live*, and a charter
is a design.
<!-- atom:end id=STRAT-0003 -->

<!-- atom:begin id=SPEC-0135 -->
```yaml
id: SPEC-0135
type: specification
scope: platform
state: active
version: 1.2.0
instantiated_at: "2026-08-27T17:47:02.809225+00:00"
author: ont-060-reconciliation
authorized_by: DEC-0008
title: "The principal-verifier port: one contract, swappable providers, declared strength"
tags: [ferry, identity, principal, provider-port, truth-level]
binding: checked
check: human
relations:
  - { rel: derives, target: STRAT-0003 }
```
Admitted at `corpus/FERRY_PRINCIPAL_VERIFIER_CONTRACT.md`, v0.1, digest
`e5b68c93860d6f09` — the substrate beneath the charter, ratified with it.

One port, one method, `verify(principal, challenge, timeout_s) -> Verdict`. Only
`APPROVED` authorizes; `DENIED`, `TIMEOUT`, `PROVIDER_ERROR` and any exception leave
the shipment `CREATED`, and a provider may not retry into an approval after a deny.
Evidence is returned on **every** path including refusals, because the refusal log is
part of the custody record — an authorization system that records only its approvals
has no way to show what it stopped.

**The conformance clause that carries the weight is §1.3.** Every provider declares its
own `truth_level` and `binding` statically, and the register copies those strings
verbatim. `digest-in-challenge` and `session-only` are different facts: approving a
blind prompt and approving a digest on screen both produce an approval, and only the
declaration distinguishes them. **A provider that overstates its truth_level is
non-conformant by definition** — which makes honest self-description a conformance
requirement rather than a courtesy, and is the same move SPEC-0134 made when it refused
to let a restriction claim force no evaluator provides.

`check: human`. The contract's central obligation is that a provider's declaration
survives adversarial reading, and no machine check can grade whether a sentence about a
provider's own strength is honest. Recorded as human-checked rather than dressed as
machine-checked, which is what this corpus does with SPEC-0072's class of claim.

Duo Auth API is mapped end to end as the first conforming provider — an applicability
proof, not a catalog. §3 declines to specify future providers on the grounds that each
is a conformance exercise against §1 rather than a spec change, and the known display
limit (pushinfo truncation on some devices) is recorded rather than smoothed over.
<!-- atom:end id=SPEC-0135 -->
