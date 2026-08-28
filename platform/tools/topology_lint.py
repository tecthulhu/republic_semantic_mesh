#!/usr/bin/env python3
"""CTRL-0013 — the topology-hygiene control (SPEC-0136).

Machine-specific configuration reached the public repository because no rule
distinguished **repo-truth** from **machine-truth**, so machine-truth was committed
wherever it was convenient: key-file locations in a provider table, a home-anchored
default in a tool, a literal reception path in ratified law, and absolute paths quoted
out of the runtime into evidence rows.

The remediation fixes those sites. This makes the class fail at gate time instead of at
floor review, which is the only version that stays fixed.

**Five classes.** The first three are generic patterns and are committed here. The
fourth is instance data — real host names — and lives in gitignored local config,
because *a committed denylist naming real hosts would itself be the leak*. The fifth
keeps the documentation honest: a binding the tooling resolves but the doc does not
enumerate is a binding someone will have to rediscover.

**The false-positive set is the hard part, and it is fixtured.** This repository is
full of paths that look like leaks and are not: `/run/l0/agent.sock` is a container
address identical on every machine and load-bearing in law; `platform/acta/…` is
repo-relative; `~/.ferry/spool` is documented-generic tool layout naming no user;
`ikey/skey/host` and `FIDO2/passkey` are words. A control that fired on those would be
turned off within a day, and a control that is off is worse than none because it also
carries the appearance of coverage.

Exemptions are per-line, explicit, and carry a reason:

    something with ~/a/path   # topology-ok: <why>

Usage:
    python3 tools/topology_lint.py [--root .] [--denylist tools/hosts.denylist]
"""
import argparse
import datetime
import json
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from paths import ACTA, REPO  # noqa: E402

SKIP_DIRS = {".git", ".venv", "node_modules", "__pycache__", "acta"}
SKIP_SUFFIX = {".sig", ".png", ".jpg", ".pdf", ".lock"}
EXEMPT = re.compile(r"#\s*topology-ok:\s*(\S.*)$")

# Class 1 — secret material itself. Conservative on purpose: a high-entropy screen that
# fires on digests would fire on this corpus constantly, so this looks for key *formats*
# whose shape is unambiguous.
SECRET = re.compile(
    r"-----BEGIN (?:RSA |OPENSSH |EC |PGP )?PRIVATE KEY-----"
    r"|\bsk-[A-Za-z0-9]{20,}"
    r"|\bAKIA[0-9A-Z]{16}\b"
    r"|\bghp_[A-Za-z0-9]{30,}")

# Class 2 — credential-file *locations*: a path whose leaf names a secret. The map to
# the treasure, which is what the original finding was.
CRED_PATH = re.compile(
    # `~` joins the lookbehind: without it the `/` branch matched the slash *inside*
    # `~/.claude/…`, defeating the dot-directory exemption one character to its left.
    # Markdown punctuation is excluded from the path body so a fenced path does not
    # drag a backtick into the finding.
    r"(?<![A-Za-z0-9~])(?:/|~/(?!\.))[^\s\"',`)\]]*"  # topology-ok: the screen's own path grammar
    r"(?:api[_-]?key|\.?secret|token|credential|\.pem|id_rsa|id_ed25519)[^\s\"',`)\]]*",  # topology-ok: the screen's own pattern vocabulary
    re.I)

# Class 3 — machine-local paths. Absolute home paths always; `~/` only when it names a
# second component: a dot-directory is tool layout, a named directory is a person.
ABS_HOME = re.compile(r"/(?:home|Users)/[A-Za-z0-9_.\-]+")
HOME_ANCHOR = re.compile(r"(?<![\w.])~/(?!\.)[A-Za-z0-9_.\-]+/")

# Container-internal addresses: identical on every machine, named in law, not topology.
#
# Narrowed to the L0 addresses that actually appear in the contracts. The first cut
# included /etc, /usr, /var and /proc as "system paths", which waved through
# a real host credential path under /etc — a fixture caught it. The
# exemption must name the addresses law relies on, not every path that looks systemic.
CONTAINER = re.compile(r"^/(?:run/l0|l0|cli|work|adapter|tmp)(?:/|$)")


def is_exempt(line):
    m = EXEMPT.search(line)
    return m.group(1).strip() if m else None


def load_denylist(path):
    """Real host names, from gitignored local config. Absent is not an error — classes
    1–3 still run — but it is reported, because a class that silently does not run is
    the shape of a control that is quietly off."""
    p = pathlib.Path(path)
    if not p.is_file():
        return None
    return [h.strip() for h in p.read_text().splitlines()
            if h.strip() and not h.strip().startswith("#")]


def documented_bindings(root):
    """Bindings enumerated in the local-configuration document."""
    doc = pathlib.Path(root) / "docs" / "LOCAL_CONFIGURATION.md"
    if not doc.is_file():
        return None
    return set(re.findall(r"\bREPUBLIC_[A-Z0-9_]*\*?", doc.read_text()))


# A binding is a name the code actually *reads from the environment* — not every
# REPUBLIC_-shaped string. The first cut matched bare occurrences and flagged a
# whitepaper filename and a fixture's throwaway name as undocumented bindings, which
# would have trained the reader to ignore class 5 within a week.
ENV_READ = re.compile(r"""os\.environ(?:\.get)?\(\s*f?["'](REPUBLIC_[A-Z0-9_]*)""")


def resolved_bindings(root):
    """Bindings the tooling actually resolves, read from the code that resolves them.

    A name built by interpolation — `REPUBLIC_API_KEY_{provider}` — is a *family*, and
    is reported as `NAME*` so the document can enumerate the family rather than every
    member. Fixture files are excluded: a test's synthetic binding is not a binding.
    """
    found = set()
    for p in (pathlib.Path(root) / "platform").rglob("*.py"):
        if any(part in SKIP_DIRS for part in p.parts) or p.name.startswith("test_"):
            continue
        text = p.read_text(errors="replace")
        for m in ENV_READ.finditer(text):
            name = m.group(1)
            after = text[m.end():m.end() + 2]
            found.add(name + "*" if after.startswith("{") else name)
    return found


def scan(root, denylist):
    findings, exempted = [], []
    for p in sorted(pathlib.Path(root).rglob("*")):
        if p.is_dir() or p.suffix in SKIP_SUFFIX:
            continue
        rel = p.relative_to(root)
        if any(part in SKIP_DIRS or part.startswith(".git") for part in rel.parts):
            continue
        try:
            text = p.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for n, line in enumerate(text.splitlines(), 1):
            why = is_exempt(line)
            hit = None
            if SECRET.search(line):
                hit = ("C1 secret-material", "a key or token in committed content")
            else:
                m = CRED_PATH.search(line)
                if m and not CONTAINER.match(m.group(0)):
                    hit = ("C2 credential-location",
                           "a path whose leaf names a secret — the map to the treasure")
                elif ABS_HOME.search(line):
                    hit = ("C3 machine-path", "an absolute home path")
                else:
                    m = HOME_ANCHOR.search(line)
                    if m:
                        hit = ("C3 machine-path",
                               "a home-anchored path naming a user directory")
            if hit and denylist:
                pass
            if not hit and denylist:
                for host in denylist:
                    if re.search(rf"\b{re.escape(host)}\b", line, re.I):
                        hit = ("C4 host-binding", f"a host name from the local denylist")
                        break
            if not hit:
                continue
            if why:
                exempted.append((str(rel), n, hit[0], why))
            else:
                findings.append((str(rel), n, hit[0], hit[1]))
    return findings, exempted


def main():
    ap = argparse.ArgumentParser(description="topology-hygiene control (CTRL-0013)")
    ap.add_argument("--root", default=str(REPO))
    ap.add_argument("--denylist", default=None)
    ap.add_argument("--evidence-dir", default=str(ACTA))
    ap.add_argument("--no-evidence", action="store_true")
    a = ap.parse_args()

    root = pathlib.Path(a.root).resolve()
    dl_path = a.denylist or (root / "platform" / "tools" / "hosts.denylist")
    denylist = load_denylist(dl_path)
    findings, exempted = scan(root, denylist)

    print(f"CTRL-0013 topology hygiene over {root.name}/")
    print(f"  classes 1-3 generic; class 4 "
          + (f"active ({len(denylist)} host(s) from local config)" if denylist
             else "INACTIVE — no local denylist; run `python3 tools/setup_local.py`"))

    # Class 5 — a binding the tooling resolves must have a documented row.
    documented, resolved = documented_bindings(root), resolved_bindings(root)
    if documented is None:
        findings.append(("docs/LOCAL_CONFIGURATION.md", 0, "C5 undocumented-binding",
                         "the local-configuration document does not exist"))
    else:
        for b in sorted(resolved - documented):
            findings.append(("docs/LOCAL_CONFIGURATION.md", 0, "C5 undocumented-binding",
                             f"{b} is resolved by tooling and has no documented row"))
    print(f"  class 5: {len(resolved)} binding(s) resolved, "
          f"{len(documented or [])} documented")
    if exempted:
        print(f"  {len(exempted)} exemption(s) on the record:")
        for f, n, c, why in exempted[:6]:
            print(f"    {f}:{n} [{c}] {why}")

    if not a.no_evidence:
        now = datetime.datetime.now(datetime.timezone.utc).isoformat()
        ev = {"id": f"EVID-ctrl0013-{now[:19].replace(':', '')}", "type": "evidence",
              "scope": "platform", "state": "active", "version": "1.0.0",
              "instantiated_at": now, "author": "ctrl-0013", "authorized_by": None,
              "title": f"topology hygiene: {len(findings)} finding(s), "
                       f"{len(exempted)} exemption(s)",
              "control_ref": "CTRL-0013", "subject": "repo:topology-hygiene",
              "verdict": "pass" if not findings else "fail",
              "checked_at": now, "checker": "ctrl-0013-topology-lint",
              "class4_active": bool(denylist),
              "exemptions": [{"file": f, "line": n, "class": c, "reason": w}
                             for f, n, c, w in exempted]}
        out = pathlib.Path(a.evidence_dir)
        out.mkdir(parents=True, exist_ok=True)
        (out / f"{ev['id']}.json").write_text(json.dumps(ev, indent=1))

    if findings:
        print(f"\nFAIL — {len(findings)} finding(s):")
        for f, n, c, why in findings[:40]:
            where = f"{f}:{n}" if n else f
            print(f"  • {where} [{c}] {why}")
        if len(findings) > 40:
            print(f"  … and {len(findings) - 40} more")
        return 1
    print("\nPASS — no machine-truth in committed content")
    return 0


if __name__ == "__main__":
    sys.exit(main())
