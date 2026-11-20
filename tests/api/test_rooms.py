import pytest


@pytest.mark.smoke
def test_rooms_endpoint_returns_rooms(playwright, base_url):
    '''Checks the rooms api'''
    context = playwright.request.new_context(base_url=base_url)
    response = context.get('/api/room')
    assert response.status == 200
    assert response.json()
    context.dispose()
