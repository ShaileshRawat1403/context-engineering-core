import json
import sys
from pathlib import Path


FIXTURE = Path(__file__).parent.parent / "fixtures" / "bundle.json"
SRC = Path(__file__).parent.parent / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))
import gates  # type: ignore


def test_ordering_invariance():
    bundle = json.loads(FIXTURE.read_text())
    admitted1, _ = gates.gate_bundle(bundle, budget_tokens=200)

    # shuffle artifacts to ensure ordering is driven by weights, not input order
    shuffled = dict(bundle)
    shuffled["artifacts"] = list(reversed(bundle["artifacts"]))
    admitted2, _ = gates.gate_bundle(shuffled, budget_tokens=200)

    ids1 = [a.artifact_id for a in admitted1]
    ids2 = [a.artifact_id for a in admitted2]
    assert ids1 == ids2
    # system must stay first
    assert ids1[0] == "sys"
