# Local configuration — every machine-binding this repository needs

**v0.1 · truth-level: intent · 2026-08-28**

This repository carries **structure and contracts**. Your machine carries **bindings** —
where things live here, which is nobody else's business and true on one host only.

Before this document existed there was no rule separating the two, so machine-truth was
committed wherever it was convenient: credential-file locations in a provider table, a
home-anchored default in a tool, a literal reception path in ratified law. That is the
finding this document and `CTRL-0013` close.

## One command

```
python3 platform/tools/setup_local.py
```

Guided, re-runnable, non-destructive. Existing values are shown with secrets masked to
the last four characters; enter keeps them. It ends with a verification pass reporting
PASS/FAIL per binding. `--verify` runs that pass alone.

## Resolution order — identical for every tool

**environment variable → gitignored local file → a clear error naming this document.**

No tool guesses. A guessed default is how machine-truth got committed the first time,
so an unset binding is a named error rather than a plausible path.

## The bindings

| binding | what it does | resolution | template |
|---|---|---|---|
| `REPUBLIC_INGEST_ROOT` | path to the ingest tree CTRL-0010 lints | env only; **no default** | — |
| `REPUBLIC_API_KEY_*` (family) | one per provider, e.g. `REPUBLIC_API_KEY_ANTHROPIC` | env, else `key_file` in `providers.local.json` | `providers.local.json.example` |
| `REPUBLIC_API_KEY_ANTHROPIC` | credential for SPEC-0085's acceptance run | env, else `key_file` in `providers.local.json` | `providers.local.json.example` |
| `REPUBLIC_API_KEY_DEEPSEEK` | credential for SPEC-0125's portability re-run | env, else `key_file` in `providers.local.json` | `providers.local.json.example` |
| host denylist | host names CTRL-0013 class 4 refuses in committed content | `platform/tools/hosts.denylist` | `hosts.denylist.example` |

The denylist is local and not committed **on purpose**: a committed list of real host
names would itself be the leak the control exists to prevent. Generic patterns
(classes 1–3) ship in the control; instance names stay on the machine.

## This table is enforced, not maintained

`CTRL-0013` class 5 fails the gate when a binding the tooling resolves has no row here.
A7 is kept permanently true rather than true once — adding a binding without documenting
it turns the tree red.

## A fresh clone

```
git clone <repo> && cd republic
python3 platform/tools/setup_local.py
# paste the printed exports into your shell profile
cd platform && python tools/atom_lint.py --tree && python tools/topology_lint.py
```

No real host, home directory, or credential location is named anywhere in committed
content.
