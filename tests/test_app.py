import logging
import unittest
from unittest.mock import MagicMock, Mock, patch

from overdueist.app import App
from todoist_api_python.api import TodoistAPI
from todoist_api_python.models import Task

class TestRunOnce(unittest.TestCase):
    def setUp(self):
        self.app: Mock = App(api_token="ABC")  # type: ignore
        self.app.api = Mock()
        self.app.send_notification = Mock()

    def _make_task(self, due_date: str, content: str) -> Mock:
        task = MagicMock()
        task.due.date = due_date
        task.due.string = due_date
        task.content = content
        return task

    def _set_tasks(self, tasks: list[Mock]):
        self.app.api.filter_tasks.return_value = [tasks]

    def test_basic(self):
        """Verify basic functionality."""
        due_date = "2026-01-01 00:00:00"
        content = "My Task"
        task = self._make_task(due_date, content)
        self._set_tasks([task])
        with self.assertNoLogs(None, logging.WARNING):
            self.app.run_once()
        assert self.app.send_notification.called
        args = self.app.send_notification.call_args.args
        assert args[0] == "Todoist"
        assert args[1] == "%s - %s\n" % (due_date, content)

    def test_hc(self):
        """Verify healthcheck URL is pinged."""
        self.app.hc_url = "http://localhost"
        self._set_tasks([])
        with patch("overdueist.app.requests") as r:
            with self.assertNoLogs(None, logging.WARNING):
                self.app.run_once()
        assert r.get.called
        args = r.get.call_args.args
        assert args[0] == "http://localhost"

    def test_dry_run(self):
        """Verify dry_run mode does not do anything."""
        self.app: Mock = App(api_token="ABC")  # type: ignore
        self.app.api = Mock()
        self.app.dry_run = True
        self.app.hc_url = "http://localhost"
        due_date = "2026-01-01 00:00:00"
        content = "My Task"
        task = self._make_task(due_date, content)
        self._set_tasks([task])
        with patch("overdueist.app.Apprise") as apprs:
            with patch("overdueist.app.requests") as rqsts:
                with self.assertLogs() as logs:
                    self.app.run_once()
        output = "\n".join(logs.output)
        assert "Would send notification" in output
        assert "Would ping healthcheck" in output
        assert not apprs.notify.called
        assert not rqsts.get.called
