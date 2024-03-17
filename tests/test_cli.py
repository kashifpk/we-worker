from typer.testing import CliRunner

runner = CliRunner()


def test_cli_run_we_worker():
    from we_worker.cli import app

    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "number of worker processes" in result.stdout
