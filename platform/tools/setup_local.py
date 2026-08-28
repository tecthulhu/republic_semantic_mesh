#!/usr/bin/env python3
"""A6 — the local-binding generator.

Every machine-binding this repository needs, established by one re-runnable command.

The pattern is the ferry's own installer, turned on the repo: **the repo carries
structure and contracts; machines carry bindings.** Before this existed, a binding was
established by editing a source file, which is exactly how machine-truth got committed
— not through carelessness but because editing the file was the only way to say where
something lived.

Re-runnable and non-destructive: existing values are shown, secrets masked to the last
four characters, and pressing enter keeps what is there. It ends with a read-only
verification pass reporting PASS or FAIL per item, because a setup tool that only
writes has no way to tell you it worked.

Every binding it writes is enumerated in `docs/LOCAL_CONFIGURATION.md`, and CTRL-0013's
class 5 fails the gate if the two ever disagree — so the documentation stays true
rather than having been true once.

Usage:
    python3 tools/setup_local.py            # guided, re-runnable
    python3 tools/setup_local.py --verify   # verification pass only
"""
import argparse
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from paths import PLATFORM  # noqa: E402

PROVIDERS_LOCAL = PLATFORM / "tools" / "providers.local.json"
DENYLIST = PLATFORM / "tools" / "hosts.denylist"

# The catalogue. Every binding the sweep found, in one place, so the doc and the tool
# enumerate the same set — the thing class 5 checks.
BINDINGS = [
    {"key": "REPUBLIC_INGEST_ROOT", "kind": "env", "secret": False,
     "prompt": "Path to the ingest tree (the reception plane's atomic_ingest)",
     "why": "CTRL-0010 lints the instruction staging tree; there is no default"},
    {"key": "REPUBLIC_API_KEY_ANTHROPIC", "kind": "env-or-file", "secret": True,
     "provider": "anthropic",
     "prompt": "Anthropic API key (blank to store a key-file path instead)",
     "why": "SPEC-0085's acceptance run; the adapter holds it, the agent never sees it"},
    {"key": "REPUBLIC_API_KEY_DEEPSEEK", "kind": "env-or-file", "secret": True,
     "provider": "deepseek",
     "prompt": "DeepSeek API key (blank to store a key-file path instead)",
     "why": "SPEC-0125's portability re-run on the identical code path"},
]


def mask(v):
    return "—" if not v else ("*" * max(0, len(v) - 4)) + v[-4:] if len(v) > 4 else "****"


def read_providers():
    if PROVIDERS_LOCAL.is_file():
        try:
            return json.loads(PROVIDERS_LOCAL.read_text())
        except ValueError:
            print(f"  ! {PROVIDERS_LOCAL.name} is not valid JSON; starting fresh")
    return {}


def verify(exports, providers):
    """Read-only. Reports per item; changes nothing."""
    print("\nverification")
    ok = True
    for b in BINDINGS:
        key = b["key"]
        if key in exports and exports[key]:
            print(f"  PASS  {key} set")
            continue
        prov = providers.get(b.get("provider") or "", {})
        path = prov.get("key_file")
        if path:
            p = pathlib.Path(path).expanduser()
            if p.is_file():
                print(f"  PASS  {key} via key-file (present, path not echoed)")
            else:
                print(f"  FAIL  {key} key-file recorded but the file does not resolve")
                ok = False
        else:
            print(f"  FAIL  {key} unset and no key-file recorded")
            ok = False
    print(f"  {'PASS' if DENYLIST.is_file() else 'FAIL'}  host denylist "
          f"{'present' if DENYLIST.is_file() else 'absent — CTRL-0013 class 4 stays inactive'}")
    if not DENYLIST.is_file():
        ok = False
    return ok


def main():
    ap = argparse.ArgumentParser(description="establish this machine's bindings")
    ap.add_argument("--verify", action="store_true")
    a = ap.parse_args()

    providers = read_providers()
    exports = {}

    if a.verify:
        return 0 if verify(exports, providers) else 1

    print("Local bindings for this machine.")
    print("The repo carries structure; this machine carries its bindings.")
    print("Enter keeps the existing value. Nothing here is ever committed.\n")

    for b in BINDINGS:
        prov = providers.get(b.get("provider") or "", {})
        current = prov.get("key_file")
        shown = (mask(current) if b["secret"] and current else current) or "—"
        print(f"{b['key']}\n  {b['why']}\n  current: {shown}")
        val = input(f"  {b['prompt']}: ").strip()
        if not val:
            print("  (kept)\n")
            continue
        if b["kind"] == "env":
            exports[b["key"]] = val
        else:
            # A key typed here is exported, not written to disk; a path is recorded.
            # The tool never copies key material into a file it manages.
            if val.startswith(("/", "~", ".")):
                providers.setdefault(b["provider"], {})["key_file"] = val
                print("  (recorded as a key-file path)\n")
            else:
                exports[b["key"]] = val
                print("  (will be exported; not written to disk)\n")

    if providers:
        PROVIDERS_LOCAL.write_text(json.dumps(providers, indent=1) + "\n")
        print(f"wrote {PROVIDERS_LOCAL.name} (gitignored)")

    if not DENYLIST.is_file():
        print(f"\n{DENYLIST.name} is absent — CTRL-0013's class 4 (host bindings) stays")
        print("inactive without it. Add one host name per line; it is gitignored, because")
        print("a committed denylist naming real hosts would itself be the leak.")
        hosts = input("  host names to deny, comma-separated (blank to skip): ").strip()
        if hosts:
            DENYLIST.write_text("\n".join(h.strip() for h in hosts.split(",") if h.strip()) + "\n")
            print(f"  wrote {DENYLIST.name} (gitignored)")

    if exports:
        print("\nadd these to your shell profile:\n")
        for k, v in exports.items():
            shown = v if k == "REPUBLIC_INGEST_ROOT" else mask(v)
            print(f"  export {k}={shown}" + ("" if k == "REPUBLIC_INGEST_ROOT"
                                             else "   # value masked here; paste the real one"))

    return 0 if verify(exports, providers) else 1


if __name__ == "__main__":
    sys.exit(main())
