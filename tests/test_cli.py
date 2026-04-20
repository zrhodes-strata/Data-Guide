from pathlib import Path
from typer.testing import CliRunner
from cli import app

runner = CliRunner()
FIXTURES = Path(__file__).parent / "fixtures"


def test_profile_command_produces_report(tmp_path):
    result = runner.invoke(app, [
        "profile", str(FIXTURES / "sample.csv"),
        "--output", str(tmp_path / "report.html"),
    ])
    assert result.exit_code == 0, result.output
    assert (tmp_path / "report.html").exists()


def test_version_command():
    result = runner.invoke(app, ["version"])
    assert result.exit_code == 0
    assert "0.1.0" in result.output


def test_validate_command_long_format():
    result = runner.invoke(app, [
        "validate", str(FIXTURES / "sample.csv"),
        "--metric-col", "metric",
        "--value-col", "value",
    ])
    assert result.exit_code == 0
    assert "valid" in result.output.lower()


def test_validate_command_missing_col():
    result = runner.invoke(app, [
        "validate", str(FIXTURES / "sample.csv"),
        "--metric-col", "nonexistent",
        "--value-col", "value",
    ])
    assert result.exit_code != 0 or "not found" in result.output.lower()
