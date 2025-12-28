import json
import sys
from pathlib import Path

SRC = Path(__file__).parent.parent / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))
import truncator  # type: ignore
import validator  # type: ignore

FIXTURE = Path(__file__).parent.parent / "fixtures" / "session.json"


def test_authority_order_preserved():
    bundle = json.loads(FIXTURE.read_text())
    stabilized, _ = truncator.truncate_session(bundle, budget_tokens=300)
    assert validator.validate_authority_order(stabilized)
    kinds = [a.kind for a in stabilized]
    assert kinds[0] == "system"
