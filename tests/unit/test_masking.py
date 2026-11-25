import logging

import pytest

from core.masking import mask

logger = logging.getLogger(__name__)


@pytest.mark.parametrize(
    "secret, expected",
    [
        (None, "<empty>"),
        ("", "<empty>"),
        ("abc", "****"),
        ("password", "****word"),
        ("tHzJlWSibFxZYbOz", "****YbOz"),
    ],
    ids=["missing", "empty", "short", "eight-chars", "token"],
)
def test_mask_hides_secret(secret, expected):
    assert mask(secret) == expected


def test_mask_never_returns_the_full_secret():
    secret = "tHzJlWSibFxZYbOz"
    assert secret is not mask(secret)


def test_masked_secret_never_reaches_logs(caplog):
    """check whether the secret reaches logs"""
    secret = "tHzJlWSibFxZYbOz"
    caplog.set_level(level=10)
    logger.info("Logged in with token " + mask(secret))
    print(caplog.text)
    assert secret not in caplog.text
    assert "****YbOz" in caplog.text
