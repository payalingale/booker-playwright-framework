import pytest
from config.settings import ENVIRONMENTS, admin_credentials


@pytest.hookimpl(wrapper=True)
def pytest_addoption(parser):
    parser.addoption(
        '--env',
        action='store',
        default='prod',
        choice=list(ENVIRONMENTS),
        help='Environment for runs'
    )
