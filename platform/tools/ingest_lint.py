#!/usr/bin/env python3
"""CTRL-0010 — the ingest structure lint (SPEC-0131).

Republic governs its code layer and did not govern its *instruction* layer. The
channel by which the floor directs the mesh — session pastes, drop-files, hand-moved
folders — produced exactly the failure class the corpus lifecycle makes structurally
impossible: one instruction in two states, an artifact filed as an instruction, work
marked executed while its pull request was open, and a bulk move that nearly swept
live work into `executed/`. Every one of those is an error the atom lifecycle cannot
represent, performed by hand in the one place the lifecycle did not reach.

This is the interim mechanism: the staging tree's structure, checked, until the
folders are promoted to governed atoms and these properties come from the schema
(STRAT-0002).

**Where this runs, stated plainly, because it changes what the check is worth.**
`atomic_ingest/` lives *outside* this repository, so CI cannot see it and no gate can
refuse a merge on it. This is a **control** and not yet **enforcement** — the same
distinction CTRL-0009 exists to keep visible, now applying to the control that polices
instructions. It is invoked by the floor and the agent and it emits evidence like any
standing query; it does not block anything. Making it enforcement means tracking the
ingest tree in a repository CI can read, which is the floor's call and is named as a
gap rather than papered over (SPEC-0131).

Usage:
    REPUBLIC_INGEST_ROOT=<ingest-root> python3 tools/ingest_lint.py
    python3 tools/ingest_lint.py --root <ingest-root>
"""
import argparse
import datetime
import hashlib
import json
import os
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from paths import ACTA  # noqa: E402

# A2: no default. An unset binding is a named error, never a guessed home path — the
# guess is what put machine-truth in this file in the first place, and a tool that
# guesses teaches the next tool to guess.
INGEST_ROOT_ENV = "REPUBLIC_INGEST_ROOT"

# The instruction lifecycle, as folders. This is the atom `state` field wearing a
# directory for a hat, which is why one file may appear in exactly one of them.
# `withdrawn` joins the lifecycle by the floor's ruling of 2026-08-20 (DEC-0008): an
# instruction corrected and replaced *before* enactment is neither deferred (parked)
# nor done (executed), and filing it as either would misreport it. Two inhabitants
# already — ferry charter v0.2 and v0.3, both superseded inside the same correction
# window while their ratifying pull request stayed open.
LIFECYCLE = ("proposed", "active", "executed", "parked", "withdrawn")
# Deliverables. Not instructions, no instruction lifecycle — the atom `type` field,
# similarly disguised.
ARTIFACTS = "artifacts"
KNOWN_FOLDERS = LIFECYCLE + (ARTIFACTS,)

# `manifest` arrives with DEC-0008: the charter's §5 step 1 requires the sweeper to find
# an "ingest-lint-conformant shipment manifest", which is only meaningful if the lint
# has a type for one. A manifest is not an instruction — it is the bill of lading for
# the instructions beside it — but it moves through the same folders and needs the same
# classification, so it joins the vocabulary rather than being exempted from it.
INSTRUCTION_TYPES = {"instruction", "initiator", "decision", "posture", "plan", "manifest"}
ARTIFACT_TYPES = {"artifact"}
ALL_TYPES = INSTRUCTION_TYPES | ARTIFACT_TYPES

# A marker rather than a filename convention, because a filename is a guess and this
# has to be a fact. Read from the head of the file so it is the first thing a human
# sees too.
MARKER = re.compile(r"^<!--\s*ingest:\s*([a-z-]+)\s*-->\s*$", re.M)
MARKER_HEAD_LINES = 10


def marker_of(path):
    """The declared type, or None. Only the head of the file counts: a marker buried
    on line 300 is not front matter, and a reader scanning the top would not see it."""
    try:
        head = "\n".join(path.read_text(encoding="utf-8", errors="replace")
                         .splitlines()[:MARKER_HEAD_LINES])
    except OSError as e:
        return f"<unreadable: {e}>"
    m = MARKER.search(head)
    return m.group(1) if m else None


def scan(root):
    """Every file under the ingest root, with the folder that classifies it."""
    root = pathlib.Path(root)
    entries = []
    for p in sorted(root.rglob("*")):
        # Dot-prefixed path components are infrastructure, not instructions — the same
        # exemption `.git` already has. DEC-0008 sites the ferry's trust registers at
        # `.ferry/`, so the shipment machinery lives inside the tree it serves and must
        # not be graded as cargo.
        if p.is_dir() or any(part.startswith(".") for part in p.relative_to(root).parts):
            continue
        # A detached signature is a shipment control file: bytes over which a marker
        # cannot be added without destroying the thing it signs.
        if p.suffix == ".sig":
            continue
        rel = p.relative_to(root)
        folder = rel.parts[0] if len(rel.parts) > 1 else None
        entries.append({"path": p, "rel": str(rel), "folder": folder,
                        "name": p.name, "marker": marker_of(p)})
    return entries


def findings_for(entries):
    """Every structural rule, each naming the file and the rule it broke.

    A lint that says "invalid" makes someone go looking; a lint that names the file and
    the rule has already done the looking.
    """
    findings = []

    # 1 — cross-state duplicate. One instruction, one state. This is the single
    # authoring-chain law, and it is also what makes a bulk `mv *` recoverable: a move
    # that collapses two states leaves the same name in two folders, and the next run
    # says so. There is no separate wildcard check because this *is* the wildcard check.
    seen = {}
    for e in entries:
        if e["folder"] in LIFECYCLE:
            seen.setdefault(e["name"], []).append(e["folder"])
    for name, folders in sorted(seen.items()):
        if len(folders) > 1:
            findings.append(
                f"{name}: present in {len(folders)} lifecycle states "
                f"({', '.join(sorted(folders))}) — one instruction has one state, and "
                f"two copies mean one of them is lying about where the work is")

    # 3 — unclassified. A file at the ingest root or in a folder outside the known set
    # has no declared state at all. Same rule as the repository tree gate, same reason:
    # the answer to "what is this?" must not be "nobody said".
    for e in entries:
        if e["folder"] is None:
            findings.append(
                f"{e['rel']}: sits at the ingest root, in no lifecycle folder — "
                f"an unclassified instruction is one nobody has to act on and nobody "
                f"can close")
        elif e["folder"] not in KNOWN_FOLDERS:
            findings.append(
                f"{e['rel']}: folder '{e['folder']}' is not a known ingest state "
                f"({', '.join(KNOWN_FOLDERS)})")

    # 2 — the type marker, and its agreement with the folder.
    for e in entries:
        if e["folder"] not in KNOWN_FOLDERS:
            continue                       # already reported as unclassified
        m = e["marker"]
        if m is None:
            if e["folder"] == ARTIFACTS:
                # DEC-0009 / SPEC-0131 v1.4.0: in artifacts/ the folder declares the
                # type, and a marker is optional for digest-pinned deliverables.
                #
                # The rule yields because the alternative is worse. A ferried artifact
                # arrives with its bytes pinned by a receipt and a manifest; adding a
                # marker to satisfy this check would break both in one stroke, so the
                # lint would be demanding that the tree lie to it. The marker's job is
                # catching folder/marker *disagreement*, and an absent marker cannot
                # disagree with anything — the folder has already said what it is.
                continue
            findings.append(
                f"{e['rel']}: no `<!-- ingest: TYPE -->` marker in the first "
                f"{MARKER_HEAD_LINES} lines — type is declared, never inferred from a "
                f"filename (one of: {', '.join(sorted(ALL_TYPES))})")
        elif m not in ALL_TYPES:
            findings.append(
                f"{e['rel']}: unknown ingest type '{m}' "
                f"(one of: {', '.join(sorted(ALL_TYPES))})")
        elif e["folder"] == ARTIFACTS and m not in ARTIFACT_TYPES:
            findings.append(
                f"{e['rel']}: marked '{m}' but filed under {ARTIFACTS}/ — a deliverable "
                f"has no instruction lifecycle, and an instruction filed as one stops "
                f"being acted on")
        elif e["folder"] in LIFECYCLE and m in ARTIFACT_TYPES:
            findings.append(
                f"{e['rel']}: marked 'artifact' but filed under {e['folder']}/ — an "
                f"artifact does not move through the instruction lifecycle")
    return findings


# SPEC-0133: the reference a file makes to the work it directs.
#   <!-- ingest-ref: STORY-0017 PR#33 -->
REF = re.compile(r"^<!--\s*ingest-ref:\s*(.+?)\s*-->\s*$", re.M)
PR_NUM = re.compile(r"PR#(\d+)")
STORY_ID = re.compile(r"\b(STORY-[0-9A-Za-z._-]+)\b")


def ref_of(path):
    try:
        head = "\n".join(path.read_text(encoding="utf-8", errors="replace")
                         .splitlines()[:MARKER_HEAD_LINES])
    except OSError:
        return None
    m = REF.search(head)
    return m.group(1) if m else None


def pr_state(number, repo):
    """open | merged | closed, from the API. Anonymous: the repository is public and
    an unauthenticated answer is one any reader can reproduce."""
    import urllib.error
    import urllib.request
    url = f"https://api.github.com/repos/{repo}/pulls/{number}"
    try:
        req = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json",
                                                   "User-Agent": "republic-ctrl-0010"})
        with urllib.request.urlopen(req, timeout=20) as r:
            d = json.loads(r.read())
    except urllib.error.HTTPError as e:
        return None, f"HTTP {e.code} for PR#{number}"
    except Exception as e:  # noqa: BLE001
        return None, f"{type(e).__name__} resolving PR#{number}: {e}"
    if d.get("merged_at"):
        return "merged", None
    return ("closed" if d.get("state") == "closed" else "open"), None


def coherence_findings(entries, repo, resolve=True):
    """SPEC-0133: a file's folder must agree with the state of the work it references.

    This is the one error class that is about *truth* rather than shape. A file in
    `executed/` whose pull request is still open makes a done-ness claim that is false,
    and a bulk process trusting the folder would drop live work on the floor. It is
    also the error the structural checks cannot see: a clean `mv proposed/* executed/`
    leaves no duplicate and no category error, just a tree that lies.

    **A story's lifecycle state is not a done-signal in this corpus, and that is by
    design.** SPEC-0122 rules that stories stay pre-ratified while the work earning
    their ratification is in flight, and they stay `proposed` after it merges until a
    decision ratifies them. So `STORY-0013` reads `proposed` with its work merged, and
    resolving done-ness from the corpus would mark every finished instruction as
    unfinished. The pull request is the only reliable signal, which is why a file
    claiming `executed/` must name one.
    """
    findings, resolved = [], {}
    for e in entries:
        if e["folder"] not in LIFECYCLE:
            continue
        raw = ref_of(e["path"])
        if not raw:
            continue                       # reference-free: exempt, structure still applies
        e["ref"] = raw
        prs = PR_NUM.findall(raw)
        stories = STORY_ID.findall(raw)

        if not prs:
            # Story-only. Nothing here can distinguish "not started" from "finished",
            # so only a claim of doneness is a problem — the other folders are honest
            # about their uncertainty.
            if e["folder"] == "executed":
                findings.append(
                    f"{e['rel']}: claims executed against {', '.join(stories) or raw!r} "
                    f"with no PR reference — a story's lifecycle state is not a "
                    f"done-signal (SPEC-0122), so this cannot be resolved. Add PR#<n>.")
            continue

        for n in prs:
            if n not in resolved:
                resolved[n] = pr_state(n, repo) if resolve else (None, "resolution skipped")
            state, err = resolved[n]
            if err:
                # Fail closed. An unresolvable check that reports green is theater.
                findings.append(
                    f"{e['rel']}: cannot resolve PR#{n} ({err}) — reporting unverifiable "
                    f"rather than passing it")
                continue
            if e["folder"] == "executed" and state != "merged":
                findings.append(
                    f"{e['rel']}: filed executed/ but PR#{n} is {state} — false-executed. "
                    f"The folder claims done and the work is live.")
            elif e["folder"] == "active" and state == "merged":
                findings.append(
                    f"{e['rel']}: filed active/ but PR#{n} is merged — stale-active; "
                    f"move it to executed/")
            elif e["folder"] == "proposed" and state in ("open", "merged"):
                findings.append(
                    f"{e['rel']}: filed proposed/ but PR#{n} is already {state} — the "
                    f"work is under way or done while the instruction reads unqueued")
    return findings


def counts(entries):
    """5 — reported, not judged. An empty `proposed/` is legal; a crowded `active/`
    is legal and worth seeing, because many-in-flight is a signal about the queue
    rather than an error in it."""
    c = {f: 0 for f in KNOWN_FOLDERS}
    for e in entries:
        if e["folder"] in c:
            c[e["folder"]] += 1
    return c


def digest_of(entries):
    """Content-addressed over the tree's shape and contents, so an unchanged tree
    yields a stable evidence subject (SPEC-0096's discipline, applied here)."""
    h = hashlib.sha256()
    for e in sorted(entries, key=lambda x: x["rel"]):
        h.update(e["rel"].encode())
        h.update(str(e["marker"]).encode())
        try:
            h.update(hashlib.sha256(e["path"].read_bytes()).digest())
        except OSError:
            h.update(b"<unreadable>")
    return h.hexdigest()[:16]


def emit(root, entries, findings, out_dir, extra=None):
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    evid = {"id": f"EVID-ctrl0010-{now[:19].replace(':', '')}", "type": "evidence",
            "scope": "platform", "state": "active", "version": "1.0.0",
            "instantiated_at": now, "author": "ctrl-0010", "authorized_by": None,
            "title": f"ingest structure over {len(entries)} file(s): "
                     f"{'valid' if not findings else f'{len(findings)} violation(s)'}",
            "control_ref": "CTRL-0010",
            "subject": f"ingest@{digest_of(entries)}#files={len(entries)}",
            "verdict": "pass" if not findings else "fail",
            "checked_at": now, "checker": "ctrl-0010-ingest-lint",
            # A5: a role alias, not a path. An evidence row records what was checked,
            # and "which directory on whose laptop" is not part of that claim.
            "ingest_root": "reception:ingest",
            "counts": counts(entries),
            "findings": findings,
            # SPEC-0131's declared gap, carried on every row rather than in a comment
            # nobody reads: this control is invoked, not gated.
            "posture": "the ingest tree lives outside the repository, so no CI gate "
                       "runs this — a control without enforcement until the tree is "
                       "tracked somewhere CI can read (SPEC-0131)"}
    if extra:
        evid.update(extra)
    out = pathlib.Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{evid['id']}.json").write_text(json.dumps(evid, indent=1))
    return evid


def main():
    ap = argparse.ArgumentParser(description="ingest structure lint (CTRL-0010)")
    ap.add_argument("--root", default=os.environ.get(INGEST_ROOT_ENV))
    ap.add_argument("--evidence-dir", default=str(ACTA))
    ap.add_argument("--no-evidence", action="store_true")
    ap.add_argument("--repo", default="tecthulhu/republic",
                    help="repository whose PRs `ingest-ref` markers resolve against")
    ap.add_argument("--no-refs", action="store_true",
                    help="skip SPEC-0133 state coherence (needs network). Recorded in "
                         "the evidence, because a run that skipped a check and a run "
                         "that passed it must not look alike")
    a = ap.parse_args()

    if not a.root:
        print(f"FAIL — no ingest root: set {INGEST_ROOT_ENV} or pass --root <ingest-root>. "
              f"`python3 tools/setup_local.py` writes it for you.")
        return 1
    root = pathlib.Path(a.root).expanduser()
    if not root.is_dir():
        print(f"FAIL — ingest root does not exist: {root}")
        return 1
    entries = scan(root)
    if not entries:
        # SPEC-0092's law, applied here: a check over nothing is not a pass.
        print(f"FAIL — no files under {root}: a check over an empty tree is not a pass")
        return 1

    findings = findings_for(entries)
    coherence = [] if a.no_refs else coherence_findings(entries, a.repo)
    findings += coherence
    referenced = sum(1 for e in entries if e.get("ref"))
    c = counts(entries)
    print(f"CTRL-0010 ingest structure lint over {root}")
    print(f"  {len(entries)} file(s): " + ", ".join(f"{k}={v}" for k, v in c.items()))
    print(f"  state coherence: " + ("skipped (--no-refs)" if a.no_refs else
                                    f"{referenced} file(s) carry an ingest-ref"))
    if not a.no_evidence:
        ev = emit(root, entries, findings, a.evidence_dir,
                  {"state_coherence": "skipped" if a.no_refs else "checked",
                   "referenced_files": referenced})
        print(f"  evidence {ev['id']} (subject {ev['subject']})")
    if findings:
        print(f"\nFAIL — {len(findings)} finding(s):")
        for f in findings:
            print("  •", f)
        return 1
    print("\nPASS — ingest structure valid")
    print("  note: invoked, not gated — the ingest tree is outside the repository, so "
          "no CI\n        check enforces this (SPEC-0131's declared gap)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
