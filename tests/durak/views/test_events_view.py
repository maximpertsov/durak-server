import pytest


@pytest.mark.django_db
def test_get_events_for_game(call_api, game, user, event_factory):
    url = "/api/game/{}/events".format(game.slug)
    response = call_api("get", url)
    assert response.status_code == 200
    assert response.json() == {"events": []}

    # create an event
    event_factory(game=game, user=user)
    response = call_api("get", url)
    assert response.status_code == 200
    assert response.json() == {
        "events": [{"type": "performed_fake_event", "payload": {"user": user.username}}]
    }
