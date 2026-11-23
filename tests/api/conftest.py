import pytest


@pytest.fixture
def api_context(playwright, base_url):
    """Docstring: an API client for one test, created fresh and closed afterwards."""
    context = playwright.request.new_context(base_url=base_url)
    yield context
    context.dispose()
