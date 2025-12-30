import json
import sys
from pathlib import Path


FIXTURE = Path(__file__).parent.parent / "fixtures" / "bundle.json"
SRC = Path(__file__).parent.parent / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))
import gates  # type: ignore


def test_out_of_scope_filtered():
    bundle = json.loads(FIXTURE.read_text())
    admitted, excluded = gates.gate_bundle(bundle, budget_tokens=200)
    excluded_ids = {a.artifact_id for a, _ in excluded}
    # doc3 is intentionally low relevance to the user question
    assert "doc3" in excluded_ids
    # core system/task artifacts remain
    admitted_ids = {a.artifact_id for a in admitted}
    assert {"sys", "task"}.issubset(admitted_ids)
