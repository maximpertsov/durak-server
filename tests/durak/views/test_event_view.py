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
        "events": [
            {
                "game": game.slug,
                "user": user.username,
                "type": "performed_fake_event",
                "payload": {},
            }
        ]
    }


@pytest.mark.django_db
def test_create_event_for_game(call_api, game, user):
    assert game.event_set.count() == 0
    url = "/api/game/{}/events".format(game.slug)
    response = call_api(
        "post",
        url,
        payload={
            "game": game.slug,
            "user": user.username,
            "type": "fake_event",
            "payload": {},
        },
    )
    assert response.status_code == 201
    assert game.event_set.count() == 1
