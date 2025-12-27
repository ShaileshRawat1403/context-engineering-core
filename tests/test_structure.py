from pathlib import Path


REQUIRED_PATHS = [
    "00-core/00-index.md",
    "10-primitives/attention/00-spec.md",
    "20-failure-mechanics/degradation/00-spec.md",
    "30-control-mechanisms/validation/00-spec.md",
    "30-control-mechanisms/isolation/00-spec.md",
    "40-system-manifestations/00-index.md",
    "50-governance/00-index.md",
    "skills/operator/context-triage/SKILL.md",
    "skills/operator/session-stabilization/SKILL.md",
    "skills/operator/boundary-hardening/SKILL.md",
    "skills/operator/drift-arrest/SKILL.md",
    "skills/operator/retrieval-gating/SKILL.md",
    "skills/agent/context-triage.md",
    "skills/agent/session-stabilization.md",
    "skills/agent/boundary-hardening.md",
    "skills/agent/drift-arrest.md",
    "skills/agent/retrieval-gating.md",
]


def test_required_files_exist():
    missing = [p for p in REQUIRED_PATHS if not Path(p).exists()]
    assert not missing, f"Missing required files: {missing}"
