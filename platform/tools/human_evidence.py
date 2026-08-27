#!/usr/bin/env python3
"""CTRL-0012 — the human-evidence primitive (SPEC-0116, SPEC-0117).

A `check: human` claim has been unbindable by construction. A rule needs a control, a
control is a thing that runs, and the whole point of these claims is that what runs is
a person reading. So eleven ratified claims have sat in `unbound_claims` since the
meters were built — not because anyone forgot them, but because the corpus had no
record form for *a human examined this and rendered a verdict*.

This is that record form.

**It is not a second authorization mechanism, and the distinction is load-bearing.**
Floor-touch is authorization — a merge, a Duo approval, "I permit this". Human evidence
is examination — "I looked at this and here is my verdict". The corpus has kept these
as cousins through STORY-0014 and the ferry's machine/principal split, and collapsing
them here would undo both. A human-evidence record carries no authority: its authority
is the signing commit that lands it, exactly as a ceremony's is (SPEC-0116). No new
authority mechanism is invented, and none is needed.

**What the control asserts, and what it cannot.** It asserts the *record exists*, names
a human, covers the claim, and is current against the corpus digest. It does not and
cannot grade the judgment inside — that judgment is the human's, and a control claiming
to verify it would be the overclaim SPEC-0135's own conformance clause forbids.

**Staleness is content-addressed, not scheduled.** A record is true-at-T against the
digest it names (ONT-014). When the corpus moves, the record stops covering the claim
and the claim returns to unevidenced. That is the same mechanism `--since` and the
embedder already use, rather than an expiry date somebody has to remember.

Usage:
    python3 tools/human_evidence.py --claim SPEC-0001 --checker "Kyle Scott" \\
        --verdict pass --note "read against DOC-0000 §4"
    python3 tools/human_evidence.py --report
"""
import argparse
import datetime
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from atom_lint import corpus_digest, lint  # noqa: E402
from paths import ACTA, CORPUS, SCHEMA  # noqa: E402

PREFIX = "EVID-human-"


class Refused(Exception):
    """A refusal is an outcome, not an error path."""


def emit(claim, checker, verdict, note, atoms, digest, acta_dir=None):
    """Assemble a human-evidence record, or refuse.

    Three refusals, and each closes a way this could have become an automated path to
    a human verdict:

    - **The claim must exist.** A record for nothing evidences nothing.
    - **The claim must be `check: human`.** Emitting one for a `check: machine` claim
      would let a person's say-so stand in for a control that could simply be run —
      the exact substitution the corpus spends its machinery preventing.
    - **The checker must be an explicit human identity**, passed in. There is no
      default, no environment fallback, and no derivation from git config: a record
      whose checker the tool supplied is a record no human made.
    """
    entry = atoms.get(claim)
    if entry is None:
        raise Refused(f"{claim} resolves to no atom — a verdict about nothing")
    atom = entry[0]
    if atom.get("check") != "human":
        raise Refused(
            f"{claim} is check: {atom.get('check')!r}, not human — a human verdict may "
            f"not stand in for a control that can be run (SPEC-0116)")
    if not checker or not str(checker).strip():
        raise Refused(
            "no checker identity supplied — a human-evidence record must name the human, "
            "and the tool will not invent one (SPEC-0116)")
    if verdict not in ("pass", "fail"):
        raise Refused(f"verdict {verdict!r} is not pass or fail")

    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    rec = {
        "id": f"{PREFIX}{claim}-{now[:19].replace(':', '')}",
        "type": "evidence", "scope": "platform", "state": "active", "version": "1.0.0",
        "instantiated_at": now, "author": str(checker), "authorized_by": None,
        "title": f"human examination of {claim}: {verdict}",
        "control_ref": "CTRL-0012",
        # Content-addressed: the record covers the corpus as it stood, and stops
        # covering it when the corpus moves (ONT-014, SPEC-0117).
        "subject": f"{claim}@corpus:{digest}",
        "verdict": verdict, "checked_at": now,
        "checker": str(checker),
        "check_kind": "human",
        "claim_ref": claim,
        "corpus_digest": digest,
        "note": note or "",
    }
    out = pathlib.Path(acta_dir or ACTA)
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{rec['id']}.json").write_text(json.dumps(rec, indent=1))
    return rec


def records(acta_dir=None):
    for f in sorted(pathlib.Path(acta_dir or ACTA).glob(f"{PREFIX}*.json")):
        try:
            yield json.loads(f.read_text())
        except ValueError:
            continue


def current_evidence(atoms, digest, acta_dir=None):
    """Which `check: human` claims carry a *current* human verdict.

    Current means the record names today's corpus digest. A record against an earlier
    digest is not wrong — it was true at its T — it simply no longer covers a corpus
    that has moved, which is what makes staleness a property of content rather than a
    timer.
    """
    covered, stale = {}, {}
    for r in records(acta_dir):
        claim = r.get("claim_ref")
        if not claim or r.get("check_kind") != "human" or r.get("verdict") != "pass":
            continue
        (covered if r.get("corpus_digest") == digest else stale).setdefault(claim, []).append(r["id"])
    return covered, {k: v for k, v in stale.items() if k not in covered}


def report(acta_dir=None):
    atoms, errors = lint([str(CORPUS)], str(SCHEMA))
    if errors:
        print(f"refusing to report against a red corpus: {len(errors)} finding(s)")
        return 1
    digest = corpus_digest(atoms)
    human = sorted(i for i, (a, _s, _b) in atoms.items() if a.get("check") == "human")
    covered, stale = current_evidence(atoms, digest, acta_dir)
    print(f"corpus@{digest}")
    print(f"  check: human claims   {len(human)}")
    print(f"  currently evidenced   {len(covered)}")
    print(f"  stale (digest moved)  {len(stale)}")
    for c in human:
        mark = "evidenced" if c in covered else ("stale" if c in stale else "—")
        print(f"    {c:11} {mark}")
    return 0


def main():
    ap = argparse.ArgumentParser(description="human-evidence primitive (CTRL-0012)")
    ap.add_argument("--claim")
    ap.add_argument("--checker", help="the human rendering the verdict; no default")
    ap.add_argument("--verdict", choices=("pass", "fail"), default="pass")
    ap.add_argument("--note", default="")
    ap.add_argument("--evidence-dir", default=None)
    ap.add_argument("--report", action="store_true")
    a = ap.parse_args()

    if a.report or not a.claim:
        return report(a.evidence_dir)

    atoms, errors = lint([str(CORPUS)], str(SCHEMA))
    if errors:
        print(f"refusing to emit against a red corpus: {len(errors)} finding(s)")
        return 1
    try:
        rec = emit(a.claim, a.checker, a.verdict, a.note, atoms,
                   corpus_digest(atoms), a.evidence_dir)
    except Refused as e:
        print(f"REFUSED — {e}")
        return 1
    print(f"wrote {rec['id']}")
    print(f"  {rec['claim_ref']} {rec['verdict']} by {rec['checker']} at corpus@{rec['corpus_digest']}")
    print("  authority is the commit that lands this, exactly as a ceremony's is")
    return 0


if __name__ == "__main__":
    sys.exit(main())
