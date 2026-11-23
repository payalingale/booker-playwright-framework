import pytest


@pytest.mark.smoke
def test_rooms_endpoint_returns_rooms(api_context):
    """GET /api/room returns 200 and a non-empty list of rooms, each with an id and name."""
    response = api_context.get("/api/room")
    body = response.json()
    assert response.status == 200, f"Expected 200, got {response.status}: {response.text()}"

    rooms = body['rooms']
    assert isinstance(
        rooms, list), f"'rooms' should be a list, got {type(rooms).__name__}: {rooms}"
    assert rooms, "API returned an empty 'rooms' list"

    for i, room in enumerate(rooms):
        assert isinstance(room.get("roomid"),
                          int), f"rooms[{i}] has invalid roomid: {room}"
        assert room.get("roomName"), f"rooms[{i}] missing roomName: {room}"
