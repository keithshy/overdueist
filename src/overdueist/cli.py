import logging
import re

import click
from apprise import AppriseConfig
from apprise.cli import DEFAULT_CONFIG_PATHS

from .app import App


def load_apprise_config(config_path: str | None) -> AppriseConfig:
    if config_path:
        paths = re.split(r'[\r\n;]+', config_path)
        config = AppriseConfig(paths=paths)
    else:
        config = AppriseConfig(paths=DEFAULT_CONFIG_PATHS)

    return config


@click.command()
@click.option("-t", "--api-token", type=str, envvar="OVERDUEIST_API_TOKEN")
@click.option("--apprise-config", type=str, envvar="APPRISE_CONFIG_PATH")
@click.option("--apprise-tag", type=str, envvar="OVERDUEIST_APPRISE_TAG", default="all")
@click.option("--hc-url", type=str, envvar="OVERDUEIST_HC_URL")
def main(api_token: str, apprise_tag: str, apprise_config: str | None, hc_url: str | None):
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    )
    apprise_config_obj = load_apprise_config(apprise_config)
    app = App(
        api_token=api_token,
        apprise_tag=apprise_tag,
        apprise_config=apprise_config_obj,
        hc_url=hc_url,
    )
    app.run_once()
