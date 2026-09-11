import logging
import os.path
import sys
from datetime import datetime
from io import StringIO

import requests
from apprise import Apprise, AppriseConfig
from todoist_api_python.api import TodoistAPI


class App:
    def __init__(
        self,
        api_token: str,
        apprise_tag: str="all",
        apprise_config: AppriseConfig | None = None,
        hc_url: str | None = None,
        dry_run=False,
    ):
        self.api_token = api_token
        self.apprise_tag = apprise_tag
        self.apprise_config = apprise_config
        self.hc_url = hc_url
        self.dry_run = dry_run
        self.query = "(today | overdue)"

        self.api = TodoistAPI(self.api_token)

    def send_notification(self, title, body):
        if self.dry_run:
            logging.info("Would send notification: %s - %s", title, body)
            return
        apprise = Apprise()
        apprise.add(self.apprise_config)
        apprise.notify(
            title=title,
            body=body,
            tag=self.apprise_tag,
        )
        logging.info("Sent message:\n%s", body)

    def ping_healthcheck(self):
        assert self.hc_url, "No hc_url configured"
        if self.dry_run:
            logging.info("Would ping healthcheck at %s", self.hc_url)
            return
        try:
            requests.get(self.hc_url, timeout=10)
            logging.info("Pinged healthchecks")
        except requests.RequestException as e:
            logging.error("Ping failed: %s", e)

    def get_tasks(self, query):
        tasks = self.api.filter_tasks(query=query)
        return tasks

    def run_once(self):
        overdue = self.get_tasks(self.query)

        now = datetime.now()
        msg = StringIO()
        for task_list in overdue:
            for task in task_list:
                if task.due and (
                    (task.due.date and datetime.fromisoformat(str(task.due.date)) < now)
                ):
                    msg.write(f"{task.due.string} - {task.content}\n")
        msg_str = msg.getvalue()
        msg.close()

        if msg_str:
            try:
                self.send_notification("Todoist", msg_str)
            except Exception as e:
                logging.error("Failed sending notif: %s", e)
                return sys.exit(1)
        else:
            logging.info("Nothing to notify")

        if self.hc_url:
            self.ping_healthcheck()
