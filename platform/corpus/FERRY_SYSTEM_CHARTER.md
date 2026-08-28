<!-- ingest: initiator -->
<!-- ingest-ref: STRAT-0002, FERRY_CHARTER_REVIEW_DISPOSITIONS_v0.1, DIGEST_ANCHOR_VERIFICATION_v0.1, CHAT_PLANE_OPERATING_CONVENTION_v0.2, SESSION_INDEX_v0.3, DOCUMENT_CONVENTIONS_v1.0 -->
---
title: FERRY_SYSTEM_CHARTER
version: "0.5"  # canonical; pinned instance FERRY_SYSTEM_CHARTER_v0.5.md
type: initiator
state: proposed
floor: kyle-scott
date: 2026-08-20
owner_session: architect (ee6adc89-…)
truth_level: intent
authorizes: nothing until RATIFIED by owner merge (PA-002/ENT-079)
supersedes_practice: the hand-ferry (C-7) as the primary cross-plane channel
successor_of: STRAT-0002 (this charter concretizes the courier)
---

# Ferry System Charter — v0.5

**v0.4 completes the identity model of 2026-08-20 (v0.3 withdrawn unenacted, same correction window): per-MACHINE enrollment (custody) PLUS per-PRINCIPAL human verification (authorization-in-presence, Duo-witnessed). Two identities, two registers, two honest truth-levels — the machine signs (evidence-grade, offline-verifiable); the human approves (attested, independently witnessed, digest-bound). The trust registers live on the RECEPTION plane; Republic carries zero shipping infrastructure. All v0.2 dispositions otherwise stand.**

## 1. The evidence that forces this

Three silent ferry drops in one week, each caught only by downstream discipline, none prevented: (a) CHAT_PLANE_OPERATING_CONVENTION failed delivery four times — the ferry ceremony's first formal HALT converted the fourth to a named failure; (b) the ledger docs' first commit attempt was blocked because sources never crossed; (c) CEREMONY_withdrawn_amend_and_ledger_disposition was drafted, presented, and never reached atomic_ingest — discovered only when the agent reported `withdrawn/` still undeclared. The hand-ferry's failure mode is silence. This charter builds the mechanism that prevents the class — and per the review round's core finding (C-1), it closes BOTH silences: transport-silence and consumption-silence.

## 2. The law this system operates under (non-negotiable boundaries)

- **B-1 — Artifacts, not authority.** The ferry system moves, stores, hashes, indexes, notifies. It never rules, ratifies, consumes-as-law, or enacts. Enactment remains the floor's signed act.
- **B-2 — Every shipment is signed by a floor-ENROLLED machine, binding the floor's authorization to a registered origin.** The floor's authority enters twice: at **enrollment** (the grant that this machine may ship — recorded in the reception-side register) and in the **manifest's per-shipment AUTH statement**, which the machine's detached signature then binds to its registered identity. Authorization and custody: two facts, two mechanisms, composed by attenuation — the floor grants; the machine signs under the grant; authority narrows, never escalates. Verified at sweep and at reception; results appended to the auth log.
- **B-3 — Digest law everywhere.** Hash at write (forge), verify at read (receipt), per DIGEST_ANCHOR_VERIFICATION_v0.1 V-1..V-5. Register beats receipt beats label.
- **B-4 — No credentials on the chat plane** (CHAT_PLANE_OPERATING_CONVENTION_v0.2 R-7). Sessions reach the store through the connector's server-side auth. Each machine's signing key is that machine's local state, never chat-plane content, never copied between machines — key mobility would collapse custody back into mere authorization.
- **B-5 — Append-only logs.** Shipment log, auth log, acknowledgement log, access log: append-only, hashable, exportable. Corrections are new rows.

## 3. The shipment lifecycle (C-1 — the round's core amendment)

Every shipment has a stable ID and an append-only event chain:

**CREATED → AUTHORIZED → TRANSPORTED → RECEIVED → ACKNOWLEDGED**

- **CREATED** — artifact captured to spool (§5), digest computed, shipment row opened.
- **AUTHORIZED** — the floor's detached signature over the manifest verified; auth row appended.
- **TRANSPORTED** — transfer executed; transport receipt (destination, timestamp, digest-as-sent) appended.
- **RECEIVED** — destination-plane arrival check: digest re-verified where the artifact landed.
- **ACKNOWLEDGED** — the CONSUMING plane's digest-bound acknowledgement: "artifact `<digest>` consumed/enrolled/filed as `<disposition>`." Only this event is terminal.

**Absence of acknowledgement is a named nonterminal state, never implied success.** The lifecycle query "shipments not yet ACKNOWLEDGED, by age" is a first-class P0 report — transfer success is not consumption success, and the gap between them is exactly where §1(c) lived. Delivery semantics are **at-least-once with idempotent receivers** (S-1): idempotency key = instance-name + digest + destination; a re-run of a completed shipment is a no-op, never a duplicate.

## 4. The seven specs (dispositions unchanged from v0.1, restated compactly)

1. Session logging → P1, with the capability limit stated (no ambient transcript export; connector-transit logging is ambient).
2. Versioned artifacts, auto-hash + index → P1; ship_ledger.py logic generalized server-side.
3. Bi-directional = ARTIFACT flow both ways; never authority flow (B-1).
4. Floor authorization per artifact → **B-2, signature-strength, P0.**
5. Shared store search replaces paste-ferry reads → P1.
6. Workflows = notify-and-queue only; never delegation; each workflow class floor-ruled → P2.
7. Adversarial-plane wiring; outputs enter by V-1 intake → P2.

## 5. P0 — the signed, spooled, acknowledged local courier (build next; one sitting)

The sweeper, per the ruled amendments:

1. **Discover** — scan `~/Downloads` (discovery-only; C-3) for an ingest-lint-conformant shipment manifest.
2. **Capture to spool** — for each named artifact: hash → copy to the Ferry-owned content-addressed spool (`~/.ferry/spool/<sha256>`) → re-hash the spool copy → mismatch = HALT. All later operations run from the spool, never from Downloads.
3. **Verify signature (B-2)** — the manifest carries the shipping machine's detached signature over the floor-AUTH-bearing body (§6); the sweeper verifies against the machine's own key locally, and reception re-verifies against the enrolled_machines register; failure, absence, or unenrolled/revoked fingerprint = HALT, shipment stays CREATED.
3b. **Principal approval (B-2)** — Duo push with manifest digest + shipment ID in `pushinfo`; on approve, txid + timestamp recorded in the AUTHORIZED event; deny, timeout, or provider failure = HALT (fail-closed), shipment stays CREATED with the refusal logged.
4. **Taxonomy resolution (S-3)** — every destination bucket must resolve unambiguously against the taxonomy yaml; unmapped or ambiguous = HALT. Taxonomy in repo; machine path/host bindings in gitignored local config.
5. **Transport** — scp from spool; per-file transport receipt appended.
6. **Arrival + acknowledgement** — destination plane re-verifies (RECEIVED); the consuming session/agent returns the digest-bound acknowledgement (ACKNOWLEDGED). The sweeper's `status` command lists un-acknowledged shipments by age.
7. **Logs** — shipment/auth/ack logs under `~/.ferry/log/`, append-only, one JSON row per event.

**P0's first governed delivery: the consolidation ceremony** (five acceptance sets + SPEC-0086 control + SPEC-0131 amendments) — the artifact whose hand-ferry failure is §1(c). The mechanism's first run ships the fix for the failure that proved the mechanism necessary.

## 6. Machine identity & enrollment (the floor's 2026-08-20 ruling — custody, not key)

- **One file is the ship-side: `ferry.py`** (stdlib-only, portable). `ferry.py init` on any new machine: creates `~/.ferry/` (keys, spool, logs), generates a device-bound Ed25519 keypair, derives the **machine identifier = public-key fingerprint** (stable, unforgeable; hostname rides as a human label), and emits an **ENROLLMENT_REQUEST** (label, pubkey, fingerprint, date) for the floor to carry to reception. `ferry.py enroll-principal` (run once: registers the Duo-enrolled human, emits the principal ENROLLMENT_REQUEST), and `ferry.py ship` / `ferry.py status` complete P0 (§5). One file remains the entire ship-side.
- **The trust register lives on the RECEPTION plane:** `<destination_base>/.ferry/enrolled_machines`, where `destination_base` is a reception-plane local binding (never repo content) — append-only rows: fingerprint, label, pubkey, enrollment date, floor authorization; `REVOKED` as a new row, never an edit. **The register row IS the certificate** — a floor-attested binding of identity↔key; no X.509 machinery. The verifier owns the trust decision, so the anchor lives with the verifier.
- **Separation of concerns (the ruling's rationale):** Republic's repo carries zero shipping infrastructure. Superseding the ferry method — P1 Ferry Core, or any future transport — changes the reception plane's local acceptance policy and the local shipping tooling, never Republic code.
- **Per shipment:** the shipping machine signs the manifest (`ssh-keygen -Y sign`, detached `.sig`); the manifest body carries the floor's AUTH statement. Verification resolves the signature against the enrolled-machines register → yields *"manifest `<digest>`, floor-authorized, shipped by `<label>` (`<fingerprint>`), enrolled `<date>`"* — the custody chain's origin link, machine-resolved.
- **Revocation & rotation are per-machine:** a lost or compromised machine is one `REVOKED` row; other machines ship uninterrupted. Rotation = new keypair on the machine, new enrollment row, old row revoked.
- **The PRINCIPAL (human) factor — Duo-witnessed approval, digest-bound:** alongside the machine signature, every shipment requires the enrolled principal's approval via Duo push, with the **manifest digest and shipment ID displayed in the push** (Auth API `pushinfo`) — the human approves this-specific-manifest, not "a login." The approval's **txid + timestamp** are recorded in the shipment's AUTHORIZED event and are auditable against Duo's admin log. **Honest truth-level, recorded in the register:** the machine signature is evidence-grade (offline-verifiable); the Duo approval is attested-with-independent-witness (a third party's transaction record, not a verifiable cryptographic artifact). The `enrolled_principals` register row states the factor and its strength plainly (e.g. `kyle-scott — duo-push, digest-in-push, third-party-witnessed`); the register never claims more verification than the factor provides.
- **Provider port:** the human factor sits behind a provider abstraction (`DuoAuthAPI` primary; `login_duo`/duo_unix fallback if the free edition lacks the Auth API application — cruder binding, honestly recorded; a future hardware token is a provider swap, not a rewrite). Duo credentials (ikey/skey/host) are ship-side local config (`~/.ferry/config.yaml`, gitignored), never chat-plane content (B-4).
- **Two registers at reception:** `enrolled_machines` (what may carry — fingerprint, label, pubkey, date, floor grant) and `enrolled_principals` (who may authorize — principal, factor, strength, date, genesis note). The first principal row is a **genesis act, self-attested and recorded as such** (the ungoverned-genesis-actor pattern: every identity system bootstraps from a root no higher authority certifies; the honest move is to say so in the row). The custody line reads both registers: *"manifest `<digest>` — approved by kyle-scott (duo txid `<id>`, digest-in-push) — shipped from `<label>` (`<fingerprint>`, enrolled `<date>`)."* Floor-touch and human-evidence remain cousins, not unified: machine enrollment is the floor's grant; principal approval is human presence; neither substitutes for the other.
- **Composition:** this is the first live link of the cryptographic-provenance chain, now with per-device identity — the same shape as the mesh's device-bound identity law. P1's Ferry Core verifies against the same register (served, not moved); authorization-classes (C-5) become per-machine, per-class grants in the same register. Nothing migrates; everything inherits.

## 7. P1 — Ferry Core with adapters (design unlocks on P0's first ACKNOWLEDGED receipt — C-9)

- **Ferry Core is the substrate** (identity, custody, lifecycle, authorization, register); **MCP/Custom-Connector is the first adapter over its API**, not the architecture (C-6). Content, custody metadata, and search are logically separated from day one.
- **Acceptance criterion, verbatim (C-4):** *no connector tool may emit a row a session can treat as enactment.*
- **Permissions are capability-scoped per tool verb** (S-2): artifact.search / artifact.fetch / artifact.submit / shipment.request / review.submit — least-privilege per session. **Advertiser: read-only** (floor's S-4 ruling) until a concrete write need is shown and separately ruled.
- **External-reviewer outputs are first-class register citizens** (C-7) — Spec 7 activates inside this schema, never as a second transport architecture.
- The repo remains the truth plane for LAW; the store is the truth plane for TRANSIT. What becomes law lands in the repo by the floor's merge.

## 8. Residuals, stated (C-8 — what P0 does NOT close)

P0 closes the silent-drop class **for an operator who writes the manifest, runs the sweeper, and reads the status report.** Still open at P0: a manifest never written is a shipment never tracked; a sweeper never run moves nothing and says nothing unless the operator checks `status`; ambient cross-plane visibility of non-shipment is a P1 deliverable (the session-side "last-receipt age" query is the cheap bridge). Stated so the charter never overclaims its own coverage.

## 9. Sequencing

1. This charter v0.2 → ratification (floor's merge).
2. Enrollment ceremonies (§6): `ferry.py enroll-principal` once (the swearing-in); `ferry.py init` on each shipping machine (laptop, mini, …); floor carries each ENROLLMENT_REQUEST to reception; register rows appended. One admin-panel check: confirm the Duo free edition exposes the Auth API application; else the fallback provider engages, recorded.
3. P0 build (one sitting) → **first run ships the consolidation ceremony** → agent acknowledges → C-9 gate satisfied.
4. P1 design story opens against the P0 receipts.

## Change log
- **2026-08-28 v0.5** — topology remediation (floor finding of 2026-08-27, A4): §6's
  literal reception path becomes `<destination_base>/.ferry/enrolled_machines`, a
  reception-plane local binding. The literal was an Architect drafting error, owned:
  ratified law named one machine's directory layout, which is the machine-truth the
  finding is about, sitting in the document that governs the mechanism. Nothing else
  moves. Predecessor: FERRY_SYSTEM_CHARTER v0.4 (`416226d91e3c0150b9c655752db71122fbbdda30afd278608adf44ac1967a163`), superseded.
- **2026-08-20 v0.4** — completes the identity model within the same correction window (v0.3 → withdrawn unenacted): §6 gains the PRINCIPAL factor — Duo-witnessed, digest-in-push, txid-recorded human approval per shipment, behind a provider port (DuoAuthAPI primary, login_duo fallback, future tokens a swap); dual registers at reception (`enrolled_machines` + `enrolled_principals`) with factor strength recorded honestly (machine signature = evidence-grade; Duo approval = attested-with-independent-witness); first principal row recorded as a self-attested genesis act; §5 gains fail-closed step 3b; B-4 extended to Duo credentials as ship-side local config. Floor-touch and human-evidence kept as cousins, not unified. Rationale: the operating reality is multiple Macs without uniform biometrics and an existing Duo free plan — the phone travels with the person, so the principal enrolls once while machines enroll each. Predecessor: FERRY_SYSTEM_CHARTER v0.3 (`8345d804bfc3cac93ed092234d60a2bb669de607d94377c759a75a58390e405c`), withdrawn unenacted.
- **2026-08-20 v0.3** — floor's identity ruling, applied before ratification (v0.2 → withdrawn, corrected-and-replaced unenacted; second inhabitant of the withdrawn state): §6 rebuilt as per-machine enrollment — device-bound Ed25519 identity per shipping machine, fingerprint-as-identifier, **reception-side append-only enrolled_machines register as the trust anchor (the register row is the certificate)**, single-file ship-side (`ferry.py init|ship|status`), per-machine revocation/rotation; B-2 restated as enrollment-grant + per-shipment AUTH bound by machine signature (attenuation: authorization and custody as two composed facts); B-4 extended (keys never copied between machines). Rationale on the record: chain of custody, not chain of key; multiple shipping machines are the operating reality; the trust register lives with the verifier so superseding the ferry never touches Republic code. Also carried from the v0.2 delivery: the manifest schema mandates one row per file ACTUALLY shipped (pair-properties claimable only when both members ship, or via explicit regenerate directive) — the stamp-format defect the agent's arrival halt caught on 2026-08-20. Predecessor: FERRY_SYSTEM_CHARTER v0.2 (`7090493e908a78db99c38a362987c54e0178066c4e5e20be0d06392e1b64e397`), withdrawn unenacted.
- **2026-08-18 v0.2** — applies the floor's ruling on FERRY_CHARTER_REVIEW_DISPOSITIONS_v0.1 (`40b921df…`): shipment lifecycle with digest-bound acknowledgement (C-1); capture-to-spool, Downloads discovery-only (C-3); **C-2 ruled at strong form — detached signature from P0** (floor's rationale: mechanisms built controlled from the start so automation stacks rather than being chased); authorization-classes named as P1/P2 evolution, each floor-ruled (C-5); Ferry-Core-with-adapters framing + P1 acceptance criterion (C-6/C-4); external reviewers first-class (C-7); residuals section (C-8); P1 gate on first ACKNOWLEDGED receipt (C-9); at-least-once + idempotent (S-1); capability scoping (S-2); taxonomy fail-closed (S-3); **Advertiser read-only (S-4, floor-ruled)**; Copilot review preserved with scope-drift recorded, not consumed (D-K). Predecessor: FERRY_SYSTEM_CHARTER v0.1 (`a9dc8cf575c8642e94d7e1f8cbad03d05f68e75722a6178423b16b22bb394d34`), superseded.
- **2026-08-16 v0.1** — initial charter: evidence base, boundaries B-1..B-5, seven specs dispositioned, three phases.
