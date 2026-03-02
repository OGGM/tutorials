#!/usr/bin/env python3

from __future__ import annotations

import json
from pathlib import Path


def clean_notebook(payload: dict) -> bool:
    changed = False

    metadata = payload.get("metadata")
    if isinstance(metadata, dict) and "kernelspec" in metadata:
        del metadata["kernelspec"]
        changed = True

    for cell in payload.get("cells", []):
        if not isinstance(cell, dict) or cell.get("cell_type") != "code":
            continue

        if cell.get("execution_count") is not None:
            cell["execution_count"] = None
            changed = True

        outputs = cell.get("outputs")
        if isinstance(outputs, list) and outputs:
            cell["outputs"] = []
            changed = True

    return changed


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    notebooks_root = root / "notebooks"
    updated = 0

    for notebook in sorted(notebooks_root.rglob("*.ipynb")):
        if ".ipynb_checkpoints" in notebook.parts:
            continue

        payload = json.loads(notebook.read_text(encoding="utf-8"))
        if not isinstance(payload, dict):
            continue

        if clean_notebook(payload):
            notebook.write_text(json.dumps(payload, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
            updated += 1

    print(f"Stripped notebook outputs/kernelspec in {updated} file(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())