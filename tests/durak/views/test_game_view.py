import pytest


@pytest.mark.django_db
def test_get_game(call_api, game_with_players):
    url = "/api/game/{}".format(game_with_players.slug)
    response = call_api("get", url)
    assert response.status_code == 200
    assert response.json() == {
        "players": ["anna", "vasyl", "igor", "grusha"],
        "slug": game_with_players.slug,
    }
