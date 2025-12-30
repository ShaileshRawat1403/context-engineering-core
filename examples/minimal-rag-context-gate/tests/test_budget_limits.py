import json
import sys
from pathlib import Path


FIXTURE = Path(__file__).parent.parent / "fixtures" / "bundle.json"
SRC = Path(__file__).parent.parent / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))
import gates  # type: ignore


def test_budget_respected():
    bundle = json.loads(FIXTURE.read_text())
    admitted, excluded = gates.gate_bundle(bundle, budget_tokens=120)
    counter = gates.HeuristicTokenCounter()
    used = sum(counter.count(a.content) for a in admitted)
    assert used <= 120
    # low-relevance doc3 should be excluded
    assert any(a.artifact_id == "doc3" for a, reason in excluded)
