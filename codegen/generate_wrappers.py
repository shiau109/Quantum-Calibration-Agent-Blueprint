"""Generate QCA wrapper scripts for every SCQO experiment.

Run under any SCQO venv (it imports scqo, not QCA):

    D:\\github\\.venv-view\\Scripts\\python.exe codegen\\generate_wrappers.py

For each experiment in scqo.experiments.catalog() this writes
scripts/scqo_<name>.py containing one public function whose signature is the
experiment's parameter schema translated into QCA's discovery grammar, plus
data/knowledge/documents/03_Experiment_API.md with the full parameter tables
(bounds/enums/descriptions that the signatures cannot carry).

After writing, it re-runs QCA's real core/discovery.py (under the repo's own
.venv) over scripts/ and asserts every wrapper is discovered with the
intended schema — codegen output is pinned to discovery's actual grammar,
not to our reading of it.

Mapping rules (QCA discovery grammar is deliberately small):
  targets (required array)      -> targets: list                   [required]
  int/number, BOTH bounds       -> Annotated[int|float, (lo, hi)]  (int exclusives tightened by 1)
  int/number, one/no bound      -> bare int|float                  (scqo revalidates)
  string enum (Literal)         -> str                             (choices in the API doc)
  boolean / plain string        -> bool / str
  X | None                      -> bare X, default None            (runtime strips None)
  array (any flavour)           -> list, default None              (scqo applies its real default)
  object                        -> dict, default None
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO / "scripts"
API_DOC = REPO / "data" / "knowledge" / "documents" / "03_Experiment_API.md"
QCA_PYTHON = REPO / ".venv" / "Scripts" / "python.exe"

HEADER = '"""GENERATED — do not edit. Regenerate with: python codegen/generate_wrappers.py"""'

MAX_DOCSTRING_CHARS = 500


def _collapse(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "").strip())


def _docstring(text: str) -> str:
    """One-line docstring literal; discovery reads only the first line."""
    line = _collapse(text)
    if len(line) > MAX_DOCSTRING_CHARS:
        line = line[: MAX_DOCSTRING_CHARS - 1].rstrip() + "…"
    line = line.replace("\\", "\\\\").replace('"""', r"\"\"\"")
    if line.endswith('"'):
        line += " "
    return f'"""{line}"""'


def _unwrap_nullable(prop: dict) -> tuple[dict, bool]:
    """X | None schemas arrive as anyOf [X, null]; return (X, nullable)."""
    any_of = prop.get("anyOf")
    if not any_of:
        return prop, False
    branches = [b for b in any_of if b.get("type") != "null"]
    nullable = len(branches) != len(any_of)
    if len(branches) == 1:
        merged = {**prop, **branches[0]}
        merged.pop("anyOf", None)
        return merged, nullable
    return prop, nullable  # multi-type unions degrade to their outer default


def _bounds(prop: dict, py_type: str):
    """Two-sided bounds -> (lo, hi); anything else -> None."""
    lo = prop.get("minimum")
    hi = prop.get("maximum")
    ex_lo = prop.get("exclusiveMinimum")
    ex_hi = prop.get("exclusiveMaximum")
    if lo is None and ex_lo is not None:
        lo = ex_lo + 1 if py_type == "int" else ex_lo
    if hi is None and ex_hi is not None:
        hi = ex_hi - 1 if py_type == "int" else ex_hi
    if lo is None or hi is None:
        return None
    return (lo, hi)


def _param_entry(name: str, prop: dict, required: bool) -> dict:
    """Everything needed to emit one signature parameter + one doc row."""
    prop, nullable = _unwrap_nullable(prop)
    json_type = prop.get("type")
    enum = prop.get("enum")

    if name == "targets":
        py_type, annotated, default = "list", None, None
    elif json_type == "integer":
        py_type = "int"
        annotated = _bounds(prop, "int")
        default = None if nullable else prop.get("default")
    elif json_type == "number":
        py_type = "float"
        annotated = _bounds(prop, "float")
        default = None if nullable else prop.get("default")
    elif json_type == "boolean":
        py_type, annotated = "bool", None
        default = None if nullable else prop.get("default")
    elif json_type == "string":
        py_type, annotated = "str", None
        default = None if nullable else prop.get("default")
    elif json_type == "array":
        py_type, annotated, default = "list", None, None
    elif json_type == "object":
        py_type, annotated, default = "dict", None, None
    else:
        # Unknown shape: degrade to an omitted-unless-set string.
        py_type, annotated, default = "str", None, None

    if nullable and annotated is not None:
        # A None default cannot satisfy a range check; drop the bounds and
        # let scqo enforce them (the doc still shows them).
        annotated = None

    if name == "targets":
        signature = f"{name}: {py_type}"
    elif required:
        # Required, but NOT targets. QCA's discovery grammar allows exactly one
        # required parameter, so these are emitted with a None default and scqo
        # raises the missing-field error instead — the same division of labour
        # every other rule here uses ("scqo revalidates everything"). The API
        # doc still marks the row **required**, which is what the agent reads.
        signature = f"{name}: {py_type} = None"
    elif annotated is not None:
        signature = f"{name}: Annotated[{py_type}, ({annotated[0]!r}, {annotated[1]!r})] = {default!r}"
    else:
        signature = f"{name}: {py_type} = {default!r}"

    return {
        "name": name,
        "signature": signature,
        "py_type": py_type,
        "required": required,
        "default": prop.get("default"),
        "enum": enum,
        "nullable": nullable,
        "doc_bounds": {
            k: prop[k]
            for k in ("minimum", "maximum", "exclusiveMinimum", "exclusiveMaximum")
            if k in prop
        },
        "description": _collapse(prop.get("description", "")),
    }


def _wrapper_source(entry: dict) -> tuple[str, list[dict]]:
    name = entry["name"]
    schema = entry["parameters_schema"]
    required_names = set(schema.get("required", []))
    props = schema.get("properties", {})

    params = [
        _param_entry(p_name, p_prop, p_name in required_names)
        for p_name, p_prop in props.items()
    ]
    # Python demands non-default params first; schema order otherwise.
    params.sort(key=lambda p: not p["required"])

    uses_annotated = any("Annotated[" in p["signature"] for p in params)
    sig_lines = ",\n    ".join(p["signature"] for p in params)
    forward = ",\n            ".join(f'"{p["name"]}": {p["name"]}' for p in params)

    imports = ["from _scqo_runtime import run_scqo"]
    if uses_annotated:
        imports.insert(0, "from typing import Annotated\n")

    source = (
        f"{HEADER}\n\n"
        + "\n".join(imports)
        + "\n\n\n"
        + f"def scqo_{name}(\n    {sig_lines},\n) -> dict:\n"
        + f"    {_docstring(entry['description'])}\n"
        + f'    return run_scqo(\n        "{name}",\n        {{\n            {forward},\n        }},\n    )\n'
    )
    return source, params


def _doc_rows(params: list[dict]) -> str:
    rows = ["| parameter | type | default | constraints | description |",
            "|---|---|---|---|---|"]
    for p in params:
        constraints = []
        if p["required"]:
            constraints.append("**required**")
        if p["enum"]:
            constraints.append("one of: " + ", ".join(f"`{v}`" for v in p["enum"]))
        for key, label in (
            ("minimum", ">="), ("exclusiveMinimum", ">"),
            ("maximum", "<="), ("exclusiveMaximum", "<"),
        ):
            if key in p["doc_bounds"]:
                constraints.append(f"{label} {p['doc_bounds'][key]}")
        if p["nullable"]:
            constraints.append("omit for backend default")
        description = p["description"].replace("|", "\\|")
        rows.append(
            f"| `{p['name']}` | {p['py_type']} | `{p['default']!r}` | "
            f"{'; '.join(constraints) or '—'} | {description} |"
        )
    return "\n".join(rows)


def generate() -> None:
    from scqo.experiments import catalog

    entries = sorted(catalog(), key=lambda e: e["name"])
    doc_sections = [
        "# SCQO Experiment API (generated)",
        "",
        "GENERATED by codegen/generate_wrappers.py — do not edit by hand.",
        "",
        f"Every experiment below is callable as `scqo_<name>` via run_experiment. "
        f"All {len(entries)} take a required `targets` list of component names "
        f"(this device's roster decides valid names). Parameters typed as "
        f"nullable default to the backend's own value when omitted — never pass "
        f"null explicitly. Writebacks are always suggestions; a human applies "
        f"them outside this system.",
        "",
    ]

    written = []
    for entry in entries:
        source, params = _wrapper_source(entry)
        path = SCRIPTS_DIR / f"scqo_{entry['name']}.py"
        path.write_text(source, encoding="utf-8")
        written.append(path)

        doc_sections += [
            f"## scqo_{entry['name']}",
            "",
            _collapse(entry["description"]),
            "",
            f"- target kinds: {', '.join(entry.get('target_kinds') or []) or 'any'}",
            f"- required operations: {', '.join(entry.get('required_operations') or []) or 'none'}",
            f"- capabilities: {', '.join(entry.get('capabilities') or []) or 'none'}",
            "",
            _doc_rows(params),
            "",
        ]

    # An experiment REMOVED from the catalog must lose its wrapper, or the agent
    # keeps offering a tool whose run_scqo raises KeyError("Unknown experiment")
    # at call time — the failure qubit_spectroscopy_overlap's deletion produced.
    # Sweeping here rather than warning: scripts/scqo_*.py is generated output,
    # so anything not in the catalog is by definition stale.
    kept = {p.name for p in written}
    orphans = [p for p in sorted(SCRIPTS_DIR.glob("scqo_*.py")) if p.name not in kept]
    for path in orphans:
        path.unlink()

    API_DOC.parent.mkdir(parents=True, exist_ok=True)
    API_DOC.write_text("\n".join(doc_sections), encoding="utf-8")
    print(f"wrote {len(written)} wrappers + {API_DOC.relative_to(REPO)}")
    if orphans:
        print("removed (no longer in the catalog): "
              + ", ".join(p.name for p in orphans))

    self_check(len(entries))


def self_check(expected: int) -> None:
    """Run QCA's real discovery over scripts/ and assert the wrapper census."""
    if not QCA_PYTHON.exists():
        sys.exit(f"self-check needs the QCA venv at {QCA_PYTHON}")

    probe = (
        "import json, sys; sys.path.insert(0, r'" + str(REPO) + "');\n"
        "from pathlib import Path\n"
        "from core.discovery import discover_experiments\n"
        "exps = [e for e in discover_experiments(Path(r'" + str(SCRIPTS_DIR) + "'))\n"
        "        if e.name.startswith('scqo_')]\n"
        "print(json.dumps([{'name': e.name,\n"
        "                   'required': [p.name for p in e.parameters if p.required],\n"
        "                   'types': {p.name: p.type for p in e.parameters}}\n"
        "                  for e in exps]))\n"
    )
    out = subprocess.run(
        [str(QCA_PYTHON), "-c", probe],
        capture_output=True, text=True, encoding="utf-8", cwd=str(REPO),
    )
    if out.returncode != 0:
        sys.exit(f"self-check discovery failed:\n{out.stderr}")
    census = json.loads(out.stdout)

    problems = []
    if len(census) != expected:
        problems.append(f"discovered {len(census)} scqo_* wrappers, expected {expected}")
    legal_types = {"int", "float", "str", "bool", "list", "dict"}
    for exp in census:
        if exp["required"] != ["targets"]:
            problems.append(f"{exp['name']}: required={exp['required']} (want ['targets'])")
        for p_name, p_type in exp["types"].items():
            if p_type not in legal_types:
                problems.append(f"{exp['name']}.{p_name}: illegal discovered type {p_type!r}")

    import py_compile

    for path in sorted(SCRIPTS_DIR.glob("scqo_*.py")):
        try:
            py_compile.compile(str(path), doraise=True)
        except py_compile.PyCompileError as err:
            problems.append(f"{path.name}: {err}")

    if problems:
        sys.exit("self-check FAILED:\n  " + "\n  ".join(problems))
    print(f"self-check OK: {len(census)} wrappers, targets-only required, legal types")


if __name__ == "__main__":
    generate()
