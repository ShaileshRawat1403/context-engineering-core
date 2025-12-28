from __future__ import annotations

import json
from pathlib import Path
from typing import Tuple

from .gates import Artifact, gate_bundle
from .context_assembler import assemble_context


def load_bundle(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def run(path: Path, budget: int = 120) -> Tuple[str, int, int]:
    bundle = load_bundle(path)
    admitted, excluded = gate_bundle(bundle, budget_tokens=budget)
    context = assemble_context(admitted)
    return context, len(admitted), len(excluded)


if __name__ == "__main__":
    ctx, admitted, excluded = run(Path(__file__).parent.parent / "fixtures" / "bundle.json")
    print(ctx)
    print(f"\nAdmitted: {admitted}  Excluded: {excluded}")
