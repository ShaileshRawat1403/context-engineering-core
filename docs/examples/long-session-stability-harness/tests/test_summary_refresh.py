import json
import sys
from pathlib import Path

SRC = Path(__file__).parent.parent / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))
import truncator  # type: ignore
import validator  # type: ignore

FIXTURE = Path(__file__).parent.parent / "fixtures" / "session.json"


def test_pii_is_masked_and_budget_respected():
    bundle = json.loads(FIXTURE.read_text())
    stabilized, used = truncator.truncate_session(bundle, budget_tokens=200)
    assert validator.validate_no_pii(stabilized)
    assert validator.validate_budget(stabilized, 200)
    # last two messages should remain after truncation
    ids = {a.artifact_id for a in stabilized}
    assert {"hist2", "hist3"}.issubset(ids)
