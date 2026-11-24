from importlib.metadata import PackageNotFoundError, version

import requests

from agentlens.logging import logger


def get_agentlens_version():
    try:
        pkg_version = version("agentlens")
        return pkg_version
    except Exception as e:
        logger.warning("Error reading package version: %s", e)
        return None


def check_agentlens_update():
    try:
        response = requests.get("https://pypi.org/pypi/agentlens/json", timeout=5)

        if response.status_code == 200:
            json_data = response.json()
            latest_version = json_data["info"]["version"]

            try:
                current_version = version("agentlens")
            except PackageNotFoundError:
                return None

            if not latest_version == current_version:
                logger.warning(
                    " WARNING: agentlens is out of date. Please update with the command: 'pip install --upgrade agentlens'"
                )
    except Exception as e:
        logger.debug(f"Failed to check for updates: {e}")
        return None
