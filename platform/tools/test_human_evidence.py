#!/usr/bin/env python3
"""CTRL-0012 fixtures (SPEC-0116, SPEC-0117): the primitive must refuse, and go stale.

Two properties carry this story. The emitter must have no automated path to a human
verdict — otherwise `check: human` becomes a rubber stamp with better provenance. And
a record must stop counting when the corpus moves, or "evidenced" drifts into meaning
"was evidenced once".

Run from anywhere: python3 tools/test_human_evidence.py
"""
import pathlib
import sys
import tempfile

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

import human_evidence as he  # noqa: E402

failures = []


def check(name, ok, detail=""):
    print(f"  {'PASS' if ok else 'FAIL'}  {name}{'' if ok else '  — ' + str(detail)[:260]}")
    if not ok:
        failures.append(name)


def atom(aid, check_kind):
    return {"id": aid, "type": "specification", "scope": "platform", "state": "ratified",
            "version": "1.0.0", "instantiated_at": "2026-01-01T00:00:00Z",
            "author": "fixture", "authorized_by": "DEC-0001", "title": f"{aid} fixture",
            "binding": "checked", "check": check_kind}


ATOMS = {"SPEC-9001": (atom("SPEC-9001", "human"), "src", "body"),
         "SPEC-9002": (atom("SPEC-9002", "machine"), "src", "body")}


def refuses(**kw):
    with tempfile.TemporaryDirectory() as td:
        try:
            he.emit(atoms=ATOMS, digest="aaaa", acta_dir=td, **kw)
            return None
        except he.Refused as e:
            return str(e)


print("CTRL-0012 fixtures — no automated path to a human verdict\n")

# The happy path exists, or the refusals below prove nothing.
with tempfile.TemporaryDirectory() as td:
    rec = he.emit("SPEC-9001", "Kyle Scott", "pass", "read it", ATOMS, "aaaa", td)
    check("a human verdict on a check: human claim is recorded",
          rec["claim_ref"] == "SPEC-9001" and rec["checker"] == "Kyle Scott"
          and rec["check_kind"] == "human" and rec["corpus_digest"] == "aaaa", rec)
    check("the record carries no authority of its own",
          rec.get("authorized_by") is None,
          "a human-evidence record must not authorize; its authority is the commit")

# SPEC-0116's three refusals.
r = refuses(claim="SPEC-9002", checker="Kyle Scott", verdict="pass", note="")
check("a verdict on a check: machine claim is refused",
      r and "not human" in r, r)

r = refuses(claim="SPEC-9001", checker="", verdict="pass", note="")
check("an empty checker is refused — the tool invents no human",
      r and "will not invent one" in r, r)

r = refuses(claim="SPEC-9001", checker=None, verdict="pass", note="")
check("a missing checker is refused", r and "must name the human" in r, r)

r = refuses(claim="SPEC-NOPE", checker="Kyle Scott", verdict="pass", note="")
check("a verdict on a claim that resolves to nothing is refused",
      r and "resolves to no atom" in r, r)

# SPEC-0117: content-addressed staleness.
with tempfile.TemporaryDirectory() as td:
    he.emit("SPEC-9001", "Kyle Scott", "pass", "", ATOMS, "digestA", td)
    cov, stale = he.current_evidence(ATOMS, "digestA", td)
    check("a record covers the digest it names", "SPEC-9001" in cov and not stale,
          f"covered={list(cov)} stale={list(stale)}")

    cov, stale = he.current_evidence(ATOMS, "digestB", td)
    check("the same record goes stale once the corpus moves",
          "SPEC-9001" not in cov and "SPEC-9001" in stale,
          f"covered={list(cov)} stale={list(stale)}")

    # A fresh verdict at the new digest restores coverage — staleness is not death.
    he.emit("SPEC-9001", "Kyle Scott", "pass", "re-read", ATOMS, "digestB", td)
    cov, stale = he.current_evidence(ATOMS, "digestB", td)
    check("a fresh verdict at the new digest restores coverage",
          "SPEC-9001" in cov and "SPEC-9001" not in stale,
          f"covered={list(cov)} stale={list(stale)}")

# A failing verdict is recorded but does not evidence the claim.
with tempfile.TemporaryDirectory() as td:
    he.emit("SPEC-9001", "Kyle Scott", "fail", "does not hold", ATOMS, "digestA", td)
    cov, _stale = he.current_evidence(ATOMS, "digestA", td)
    check("a fail verdict is recorded but does not count as evidence",
          "SPEC-9001" not in cov,
          "a refusal is part of the record; it is not a pass")

print(f"\n{'PASS' if not failures else 'FAIL'} — CTRL-0012 fixture suite"
      f"{'' if not failures else ': ' + ', '.join(failures)}")
sys.exit(1 if failures else 0)
