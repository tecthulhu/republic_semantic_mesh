#!/usr/bin/env python3
"""CTRL-0013 fixtures (SPEC-0136): each class fires, and the false-positive set does not.

The second half is the harder and more important one. This repository is full of paths
that look like leaks: container addresses, repo-relative paths, dot-directory tool
layout, and words containing "key" or "token". A control that fired on those would be
switched off within a day — and a control that is off is worse than none, because it
carries the appearance of coverage.

Run from anywhere: python3 tools/test_topology_lint.py
"""
import pathlib
import sys
import tempfile

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

import topology_lint as tl  # noqa: E402

failures = []


def check(name, ok, detail=""):
    print(f"  {'PASS' if ok else 'FAIL'}  {name}{'' if ok else '  — ' + str(detail)[:240]}")
    if not ok:
        failures.append(name)


def scan_line(line, denylist=None):
    with tempfile.TemporaryDirectory() as td:
        root = pathlib.Path(td)
        (root / "platform").mkdir()
        (root / "docs").mkdir()
        (root / "docs" / "LOCAL_CONFIGURATION.md").write_text("no bindings here\n")
        (root / "f.md").write_text(line + "\n")
        found, exempt = tl.scan(root, denylist)
        return found, exempt


def fires(line, cls, denylist=None):
    found, _ = scan_line(line, denylist)
    return [f for f in found if f[2].startswith(cls)]


print("CTRL-0013 fixtures — five classes fire; the look-alikes do not\n")

# --- the classes fire -------------------------------------------------------
check("C1 a private key block is caught",
      fires("-----BEGIN OPENSSH PRIVATE KEY-----", "C1"), "")  # topology-ok: fixture input, a synthetic key header proving C1 fires
check("C1 a provider secret format is caught",
      fires("token = sk-abcdefghijklmnopqrstuvwxyz012345", "C1"), "")  # topology-ok: fixture input, a synthetic secret format proving C1 fires
check("C2 a credential-file location is caught",
      fires('key_file = "~/somewhere/.republic_anthropic_api_key"', "C2"), "")  # topology-ok: fixture input, a synthetic credential path proving C2 fires
check("C2 an ssh private key path is caught",
      fires("copy /etc/keys/id_ed25519 somewhere", "C2"), "")  # topology-ok: fixture input, the case that caught the over-broad container exemption
check("C3 an absolute home path is caught",
      fires("root = /home/someone/tecthulhu/atomic_ingest", "C3"), "")  # topology-ok: fixture input, a synthetic path proving C3 fires
check("C3 a home-anchored user directory is caught",
      fires("scan ~/tecthulhu/atomic_ingest for manifests", "C3"), "")  # topology-ok: fixture input, a synthetic path proving C3 fires
check("C4 a denylisted host is caught",
      fires("shipped from workstation.local", "C4", denylist=["workstation.local"]), "")

# --- the false-positive set does NOT fire -----------------------------------
# Every line below is real content from this repository or the floor's no-action ruling.
NEGATIVES = [
    ("container socket",        "connect to /run/l0/agent.sock"),
    ("container key path",      "reads /run/l0/adapter/provider.key inside the image"),  # topology-ok: negative fixture, a container address that must not fire
    ("container leaf token",    "the leaf token at /run/l0/leaf.token"),
    ("repo-relative acta",      "rows live under platform/acta/EVID-x.json"),
    ("repo-relative tools",     "run platform/tools/atom_lint.py --tree"),
    ("dot-dir tool layout",     "spool at ~/.ferry/spool/<sha256>"),
    ("dot-dir config",          "credentials in ~/.ferry/config.yaml, gitignored"),  # topology-ok: negative fixture, generic tool layout per the floor ruling
    ("dot-dir downloads",       "scan ~/Downloads for a manifest"),
    ("container HOME config",   "personal OAuth credential in `~/.claude/.credentials.json`"),  # topology-ok: negative fixture, the container's own HOME
    ("word pair with slash",    "envelopes/tokens (must verify) and a rogue set"),
    ("ikey/skey/host words",    "| Availability check | GET /auth/v2/check (validates ikey/skey/host) |"),
    ("FIDO2/passkey word",      "FIDO2/passkey local signatures (truth_level: evidence)"),
    ("placeholder path",        "REPUBLIC_INGEST_ROOT=<ingest-root> python3 tools/ingest_lint.py"),
]
for name, line in NEGATIVES:
    found, _ = scan_line(line)
    check(f"no false positive: {name}", not found, f"{line[:60]!r} -> {found}")

# --- exemptions -------------------------------------------------------------
found, exempt = scan_line("root = /home/someone/thing   # topology-ok: fixture data")
check("an annotated line is exempted, not silently dropped",
      not found and exempt and exempt[0][3] == "fixture data", (found, exempt))

found, _ = scan_line("root = /home/someone/thing   # topology-ok:")
check("an exemption with no reason does not exempt", bool(found), found)

# --- class 5 ----------------------------------------------------------------
with tempfile.TemporaryDirectory() as td:
    root = pathlib.Path(td)
    (root / "platform").mkdir()
    (root / "docs").mkdir()
    (root / "platform" / "t.py").write_text('v = os.environ.get("REPUBLIC_THING")\n')
    (root / "docs" / "LOCAL_CONFIGURATION.md").write_text("nothing documented\n")
    undoc = tl.resolved_bindings(root) - (tl.documented_bindings(root) or set())
    check("C5 a resolved binding with no documented row is caught",
          undoc == {"REPUBLIC_THING"}, undoc)
    (root / "docs" / "LOCAL_CONFIGURATION.md").write_text("| REPUBLIC_THING | the thing |\n")
    undoc = tl.resolved_bindings(root) - (tl.documented_bindings(root) or set())
    check("C5 documenting the binding clears it", not undoc, undoc)

# --- the denylist is not committed -----------------------------------------
committed = pathlib.Path(tl.REPO) / "platform" / "tools" / "hosts.denylist"
check("the real denylist is not committed content",
      not committed.is_file() or committed.stat().st_size == 0,
      "a committed denylist naming real hosts would itself be the leak")

print(f"\n{'PASS' if not failures else 'FAIL'} — CTRL-0013 fixture suite"
      f"{'' if not failures else ': ' + ', '.join(failures)}")
sys.exit(1 if failures else 0)
