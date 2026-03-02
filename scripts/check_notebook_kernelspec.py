#!/usr/bin/env python3

from __future__ import annotations

import json
from pathlib import Path
import sys


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    notebooks_root = root / "notebooks"
    kernelspec_offenders: list[str] = []
    output_offenders: list[str] = []

    for notebook in sorted(notebooks_root.rglob("*.ipynb")):
        if ".ipynb_checkpoints" in notebook.parts:
            continue

        try:
            payload = json.loads(notebook.read_text(encoding="utf-8"))
        except Exception as exc:
            print(f"Failed to parse {notebook.relative_to(root)}: {exc}", file=sys.stderr)
            return 2

        metadata = payload.get("metadata", {})
        if isinstance(metadata, dict) and "kernelspec" in metadata:
            kernelspec_offenders.append(str(notebook.relative_to(root)))

        for idx, cell in enumerate(payload.get("cells", []), start=1):
            if not isinstance(cell, dict) or cell.get("cell_type") != "code":
                continue

            execution_count = cell.get("execution_count")
            outputs = cell.get("outputs")

            has_execution_count = execution_count is not None
            has_outputs = isinstance(outputs, list) and len(outputs) > 0

            if has_execution_count or has_outputs:
                output_offenders.append(f"{notebook.relative_to(root)} (cell {idx})")

    if kernelspec_offenders:
        print("Found notebooks with disallowed metadata.kernelspec:", file=sys.stderr)
        for notebook in kernelspec_offenders:
            print(f" - {notebook}", file=sys.stderr)

    if output_offenders:
        print("Found executed notebook cells (outputs and/or execution_count):", file=sys.stderr)
        for notebook in output_offenders:
            print(f" - {notebook}", file=sys.stderr)

    if kernelspec_offenders or output_offenders:
        msg = ("\nNotebooks committed to this repository must be output-free and kernelspec-free. "
               "To do this, run python scripts/strip_notebook_outputs.py from the tutorials root folder.")
        print(msg, file=sys.stderr)
        return 1

    print("OK: notebooks are clean (no metadata.kernelspec, outputs, or execution_count)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
