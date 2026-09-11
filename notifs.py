import logging
import os.path
import sys
from datetime import datetime
from io import StringIO

import apprise
import requests
from todoist_api_python.api_async import TodoistAPIAsync
from todoist_api_python.api import TodoistAPI

hc_url = None


def get_tasks(filter=None):
    with open("token.txt") as f:
        token = f.read().strip()
    api = TodoistAPI(token)
    tasks = api.filter_tasks(query=filter)
    return tasks


def send_notification(title, body):
    # Create an Apprise instance
    apobj = apprise.Apprise()

    # Create an Config instance
    config = apprise.AppriseConfig()

    # Add a configuration source:
    cfg_file = os.path.expanduser("./apprise.yaml")
    config.add(cfg_file)

    # Make sure to add our config into our apprise object
    apobj.add(config)

    # Then notify these services any time you desire. The below would
    # notify all of the services loaded into our Apprise object.
    apobj.notify(
        title=title,
        body=body,
    )

def ping_healthcheck():
    try:
        requests.get(hc_url, timeout=10)
        logging.info("Pinged healthchecks")
    except requests.RequestException as e:
        logging.error("Ping failed: %s", e)

def main():
    overdue = get_tasks(filter="(today | overdue)")
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
            send_notification("Todoist", msg_str)
        except Exception as e:
            logging.error("Failed sending notif: %s", e)
            return sys.exit(1)
        logging.info("Sent message:\n%s", msg_str)
    else:
        logging.info("Nothing to notify")
    ping_healthcheck()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
