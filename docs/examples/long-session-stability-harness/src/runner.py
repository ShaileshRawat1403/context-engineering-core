from __future__ import annotations

import json
from importlib.machinery import SourceFileLoader
from pathlib import Path
from typing import Tuple


def load_bundle(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def run(path: Path, budget: int = 400) -> Tuple[int, bool, bool, bool]:
    truncator = SourceFileLoader("truncator", str(Path(__file__).parent / "truncator.py")).load_module()
    validator = SourceFileLoader("validator", str(Path(__file__).parent / "validator.py")).load_module()

    bundle = load_bundle(path)
    stabilized, used = truncator.truncate_session(bundle, budget_tokens=budget)
    return (
        used,
        validator.validate_no_pii(stabilized),
        validator.validate_budget(stabilized, budget),
        validator.validate_authority_order(stabilized),
    )


if __name__ == "__main__":
    used, pii_ok, budget_ok, order_ok = run(Path(__file__).parent.parent / "fixtures" / "session.json")
    print(f"Tokens used: {used}")
    print(f"PII removed: {pii_ok}")
    print(f"Within budget: {budget_ok}")
    print(f"Authority order: {order_ok}")
