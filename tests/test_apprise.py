import os
import unittest
from unittest.mock import patch

from apprise.config.file import ConfigFile
from click.testing import CliRunner

from overdueist import cli

class TestAppriseConfigLoading(unittest.TestCase):
    def test_load_default_configs(self):
        """Test that default apprise config paths are used if no option given."""
        config = cli.load_apprise_config(None)
        paths = [c.path for c in config if isinstance(c, ConfigFile)]
        assert os.path.expanduser("~/.apprise") in paths
        assert os.path.expanduser("~/.config/apprise.conf") in paths

    def test_load_config_by_flag(self):
        """Test that config passed in via --apprise-config is used."""
        runner = CliRunner()
        with patch("overdueist.cli.App") as f:
            result = runner.invoke(cli.main, "--apprise-config=foobar.conf")
        assert result.exit_code == 0
        kwargs = f.call_args.kwargs
        config = kwargs.get("apprise_config")
        assert config
        paths = [c.path for c in config if isinstance(c, ConfigFile)]
        assert os.path.expandvars("$PWD/foobar.conf") in paths

    def test_load_config_by_env(self):
        """Test that config passed in via APPRISE_CONFIG_PATH is used."""
        runner = CliRunner()
        with patch("overdueist.cli.App") as f:
            result = runner.invoke(cli.main, env={"APPRISE_CONFIG_PATH": "barbaz.conf"})
        assert result.exit_code == 0
        kwargs = f.call_args.kwargs
        config = kwargs.get("apprise_config")
        assert config
        paths = [c.path for c in config if isinstance(c, ConfigFile)]
        assert os.path.expandvars("$PWD/barbaz.conf") in paths
