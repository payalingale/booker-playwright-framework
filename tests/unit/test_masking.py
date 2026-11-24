import pytest
from core.masking import mask


@pytest.mark.parametrize("secret, expected", [(None, "<empty>"), ("", "<empty>"), ("abc", "****"), ("password", "****word"), ("tHzJlWSibFxZYbOz", "****YbOz")], ids=['missing', 'empty', 'short', 'eight-chars', 'token'])
def test_mask_hides_secret(secret, expected):
    assert mask(secret) == expected


def test_mask_never_returns_the_full_secret():
    secret = "tHzJlWSibFxZYbOz"
    assert secret is not mask(secret)
