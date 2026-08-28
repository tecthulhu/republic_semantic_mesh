# Republic

**A governance plane for AI-driven software development — rule of law for AI agents.**

Republic is a working system in which AI agents plan and build software under machine-enforced law rather than human supervision. Authority, intent, execution, and verification are governed by ratified rules enforced at build time, spawn time, and on the wire — not by an agent's continued cooperation or a human's continued attention.

The thesis in one sentence: **verification, not generation, is now the binding constraint on AI-driven software development** — and the fix is structural, not supervisory.

---

## The problem this exists to solve

If you've used AI coding tools, you've met the output that's *almost right* — close enough to be tempting, wrong enough to cost the afternoon. That's the individual-scale symptom of a sector-scale problem: the systems that make AI *produce* are everywhere; the systems that make sure it produces *what was intended* are not.

The prevailing defenses are supervisory — in-context instructions, human review, self-authored memory — and each fails in a measured way: instruction-following degrades as context grows; human oversight decays toward acceptance; self-authored memory drifts and entrenches its own errors. The common failure underneath all of them is a **closed loop**: a system consuming its own claims about itself, with nothing external grading them.

Republic takes the mechanism position — *good intentions don't work; mechanisms do.* Governance has to live in the execution path, enforced by machine-checked gates, so that non-compliant patterns fail at build time rather than being caught (or missed) by a tired reviewer later.

## What it actually is

Five primitives, each opening one of those closed loops:

- **Governed atoms** — the unit of governance is the atom, not the document: the smallest piece of normative content carrying its own identity, lifecycle state, authorship, and authorization. A requirement is *bound to enforcement* or it's a flagged, counted defect. So **rule-binding coverage becomes a number** rather than an audit — and enforcement *effectiveness* is measured separately, because a rule can be bound to a control that runs perfectly while measuring the wrong property.
- **A temporal truth model** — nothing mutable is stored. Every governed statement is an immutable, timestamped instance; the current state of anything is a *query* over those instances, never the latest edit of a mutable record. Claims can't quietly outrun their history.
- **One identity type, one direction of authority** — humans and AI agents are the same kind of actor on a cryptographic signing chain rooted at a cold key. Authority can only *narrow* with delegation, never escalate. No trust scores — authority is granted, never inferred from behavior.
- **An enforcement plane with no governance service** — six components (atom store, generated index, linter, gate library, evidence emitter, chain verifier) running on git mechanics and embedded gates at the chokepoints that already hold authority: the merge, the spawn, the message bus. **No separate service to fail open** — the gates are embedded, versioned, and digest-pinned against drift.
- **End-to-end provenance** — for every artifact the system produces, it answers by query: *who decided this, under what authority, executed by what, verified how* — from a verbatim human directive through the identity leaf that executed it to the commits that resulted.

## What runs today

Reported honestly, from the repository — including what doesn't run yet.

- **The substrate is enacted and self-governing.** The founding decision (`DEC-0001`) landed by signed merge under its own ratification machinery; subsequent decisions activated the rule set and corrected the coverage meters when operation revealed a defect. The lifecycle isn't a diagram — every edge has run.
- **The build gate is live and emits public evidence.** A conformance workflow runs the control suite on every change; a red suite blocks merge; the evidence rows are uploaded publicly, so you can check the claim rather than trust the badge. *Blocks merge* is itself evidenced rather than asserted — see below.
- **The riskiest hop is walked.** The spawn contract — a supervised, interruptible AI-agent session in a hardened, isolated, credential-less container, running in bidirectional streaming mode under harness control — ran its acceptance suite green: spawn gate refusing unresolvable spawns, container isolation and per-act attribution verified, network egress deny-by-default and enforced, supervision demonstrated as interrupt-in-flight / mid-session injection / clean termination, credential minting confined to the harness. Proven portable across two model providers by changing two arguments.
- **The evidence machinery catches its own defects.** Adversarial "rogue" fixtures caught real verifier defects before they shipped; the supervision proof was built to assert *truncation*, not just survival, because a buffering proxy would otherwise have faked the whole capability. The standing query for unenforced rules moved from 22 to 8 across this work.

**Not yet:** the full end-to-end chain run (C1) joining every step, the semantic retrieval instrument (currently lexical), and the consult-and-render services. These are named, not hidden — see the whitepaper's §7 and §8.

## Setup

This repository carries structure; your machine carries its bindings. One command
establishes them:

```
python3 platform/tools/setup_local.py
```

Every binding — what it does, how it resolves, which template exists — is enumerated in
[`docs/LOCAL_CONFIGURATION.md`](./docs/LOCAL_CONFIGURATION.md), and a gate check fails
if that list ever drifts from what the tooling actually reads.

## Verify rather than trust

The whole point is that you don't have to take this document's word for it:

- The corpus, schemas, and conformance workflow are public in this repository.
- The founding enactment is tagged `dec-0001-enacted`.
- Evidence records live under `platform/acta/`.
- The conformance workflow and its uploaded evidence rows are in the repository's Actions history.
- The standing queries are re-runnable from the tools directory against any commit: `python platform/tools/embedder.py --report`.

**"A red suite blocks merge" is the load-bearing claim here, so it is evidenced separately.** A CI job that detects a violation is a *control*; a repository rule that refuses the merge when that control is red is *enforcement*, and the two are different facts. `CTRL-0009` captures the second from the live branch-protection setting on every run — never from a constant — and writes it to `platform/acta/` as `EVID-ctrl0009-*`. Re-run it yourself with `python platform/suite/enforcement/run.py`, or check the setting directly without any credential at all:

```
curl -s https://api.github.com/repos/tecthulhu/republic/rules/branches/main
```

What that returns today: both conformance contexts required by name, direct push and force-push refused, and no bypass actor — administrators included. Two honest qualifications ride with it: **branches are not required to be up to date with the base before merging**, so a green check describes what the PR tested rather than always what lands; and **no approving review is required**, so the merge is the owner's act alone. Both are recorded in the evidence rather than omitted from the claim.

Under the system's own truth model, this README is a *rendering*. Where it and the resolved record disagree, **the record wins.**

## The whitepaper

The full argument — the market thesis, the attestational-vs-structural distinction, the four falsifiable hypotheses, and the honest current-state report — is in the whitepaper:

**[`docs/WHITEPAPER.md`](./docs/WHITEPAPER.md)** — always the current version (v1.0.1 today).

It's written to be refutable: it states the criteria by which it could be proven wrong, and the system emits evidence of its own performance — including evidence of failure — as a side effect of operating.

`WHITEPAPER.md` always renders the current version; every prior version stays addressable as an immutable instance in the same directory — [`REPUBLIC_WHITEPAPER_v1.0.1.md`](./docs/REPUBLIC_WHITEPAPER_v1.0.1.md) and its successors — so a supersession happens in the open rather than as a silent replacement. That is the paper's own truth model applied to itself, and it means a citation of a version keeps resolving after the next one lands.

**Releasing a new version:** add the versioned file, then overwrite `WHITEPAPER.md` with the same content. Versioned files are never edited after creation. The build gate checks that the canonical file matches the newest versioned instance, so the public link cannot quietly go stale.

## Status & license

Whitepaper **v1.0.1** (2026-08-14) is the current instance. The ratification is v1.0's, taken on 2026-08-13 from rc9 without amendment; v1.0.1 is a citation supersession that resolves the paper's posture references to their landed atom IDs and leaves the ratification untouched. Both statements are in the paper's own header, and the distinction is the point — a patch that re-cited its sources is not a new ruling.

The platform substrate is enacted and enforcing; the containerized agent layer is the current front. The repository's outbound license is decided but not yet enacted: `DEC-0002` names AGPL-3.0-only, granted personally by the owner, and stands at `proposed` with no LICENSE file committed. Until it is, the deliberate holding posture is **all rights reserved** — the repository is public for inspection, not yet licensed for reuse.

## Author

Republic is designed and built by **Kyle Scott** (Eldritch Labs), with Claude (Anthropic) as a collaborator on research synthesis, drafting, and implementation under the author's direction. All rulings are the author's, recorded in the corpus's decision history.

---

*Requirement identifiers follow the corpus conventions (ONT-, ENT-, PA-, DEC-, SPEC-, CTRL-). The provenance chain, evidence records, and conformance workflow referenced throughout are public in this repository.*
