"""Tests for command modules."""

from typer.testing import CliRunner
from nuaa_cli import app

runner = CliRunner()


class TestCommandErrors:
    """Test command error handling."""

    def test_design_missing_args(self):
        """Test design command requires arguments."""
        result = runner.invoke(app, ["design"])
        assert result.exit_code != 0

    def test_propose_missing_args(self):
        """Test propose command requires arguments."""
        result = runner.invoke(app, ["propose"])
        assert result.exit_code != 0

    def test_measure_missing_args(self):
        """Test measure command requires arguments."""
        result = runner.invoke(app, ["measure"])
        assert result.exit_code != 0

    def test_document_missing_args(self):
        """Test document command requires arguments."""
        result = runner.invoke(app, ["document"])
        assert result.exit_code != 0

    def test_refine_missing_args(self):
        """Test refine command requires arguments."""
        result = runner.invoke(app, ["refine"])
        assert result.exit_code != 0

    def test_report_missing_args(self):
        """Test report command requires arguments."""
        result = runner.invoke(app, ["report"])
        assert result.exit_code != 0

    def test_engage_missing_args(self):
        """Test engage command requires arguments."""
        result = runner.invoke(app, ["engage"])
        assert result.exit_code != 0

    def test_partner_missing_args(self):
        """Test partner command requires arguments."""
        result = runner.invoke(app, ["partner"])
        assert result.exit_code != 0

    def test_train_missing_args(self):
        """Test train command requires arguments."""
        result = runner.invoke(app, ["train"])
        assert result.exit_code != 0

    def test_event_missing_args(self):
        """Test event command requires arguments."""
        result = runner.invoke(app, ["event"])
        assert result.exit_code != 0

    def test_risk_missing_args(self):
        """Test risk command requires arguments."""
        result = runner.invoke(app, ["risk"])
        assert result.exit_code != 0
