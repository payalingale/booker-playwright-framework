import logging

import pytest
from playwright.sync_api import Error as playwrightError

from config.settings import ENVIRONMENTS

logger = logging.getLogger(__name__)


def pytest_addoption(parser):
    parser.addoption(
        "--env",
        action="store",
        default="demo",
        choices=list(ENVIRONMENTS),
        help="Environment to test",
    )


@pytest.fixture(scope="session")
def base_url(request):
    """Get the base url from Environments"""
    env_name = request.config.getoption("--env")
    return ENVIRONMENTS[env_name]


@pytest.fixture(scope="session", autouse=True)
def app_is_up(playwright, base_url):
    """Health Check of application before starting the execution"""
    context = playwright.request.new_context(base_url=base_url)
    try:
        response = context.get("/api/room", timeout=10000)
        status = response.status
    except playwrightError as error:
        logger.error(f"Health check failed: cannot reach {base_url}/api/room")
        pytest.exit(
            f"Health check failed: cannot reach {base_url}/api/room , ({error})",
            returncode=3,
        )
    finally:
        context.dispose()
    logger.info(f"Health check: GET {base_url}/api/room returned {status}")
    if status != 200:
        pytest.exit(
            f"Health check failed: GET {base_url}/api/room returned status {status}",
            returncode=3,
        )
