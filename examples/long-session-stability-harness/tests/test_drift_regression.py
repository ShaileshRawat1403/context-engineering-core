import json
import sys
from pathlib import Path

SRC = Path(__file__).parent.parent / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))
import truncator  # type: ignore

FIXTURE = Path(__file__).parent.parent / "fixtures" / "session.json"


def test_policy_persists_when_drifts_detected():
    bundle = json.loads(FIXTURE.read_text())
    stabilized, _ = truncator.truncate_session(bundle, budget_tokens=250)
    policy = next((a for a in stabilized if a.artifact_id == "policy"), None)
    assert policy is not None
    assert "Do not provide account numbers" in policy.content
