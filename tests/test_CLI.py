from client.cli import app
from typer.testing import CliRunner

def test_cli_has_start_watch():
    runner = CliRunner()
    result = runner.invoke(app, ["--help"])
    assert "start-watch" in result.output
