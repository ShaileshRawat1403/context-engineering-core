import subprocess
from pathlib import Path


FIXTURE = Path(__file__).resolve().parents[1] / "fixtures" / "session.json"


def run(cmd: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, text=True, capture_output=True, check=True)


def test_budget_report_runs():
    result = run(
        [
            "python3",
            "skills/operator/context-triage/scripts/context_budget_report.py",
            "--input",
            str(FIXTURE),
            "--budget",
            "400",
        ]
    )
    assert "Context Budget Report" in result.stdout
    assert "Artifacts:" in result.stdout


def test_reorder_runs():
    result = run(
        [
            "python3",
            "skills/operator/context-triage/scripts/reorder_by_priority.py",
            "--input",
            str(FIXTURE),
        ]
    )
    assert "Reorder by Authority + Kind + Priority" in result.stdout
    assert "sys" in result.stdout


def test_duplicate_scan_runs():
    result = run(
        [
            "python3",
            "skills/operator/context-triage/scripts/duplicate_scan_demo.py",
            "--input",
            str(FIXTURE),
            "--near-threshold",
            "0.9",
            "--shingle-k",
            "4",
        ]
    )
    assert "Duplicate Scan Report" in result.stdout
