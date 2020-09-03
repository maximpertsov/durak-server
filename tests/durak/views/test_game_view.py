import pytest


@pytest.fixture
def game_with_players(
    game, player_factory, card_factory, draw_card_factory, anna, vasyl, igor, grusha,
):
    player_factory(game=game, user=anna)
    player_factory(game=game, user=vasyl)
    player_factory(game=game, user=igor)
    player_factory(game=game, user=grusha)

    draw_card_factory(game=game, card=card_factory(suit="spades", rank="ace"))
    draw_card_factory(game=game, card=card_factory(suit="hearts", rank="2"))

    return game


@pytest.mark.django_db
def test_get_game(call_api, game_with_players):
    url = "/api/game/{}".format(game_with_players.slug)
    response = call_api("get", url)
    assert response.status_code == 200
    assert response.json() == {
        "players": ["anna", "vasyl", "igor", "grusha"],
        "hands": {"anna": [], "vasyl": [], "igor": [], "grusha": []},
        "slug": game_with_players.slug,
        "draw_pile": [
            {"rank": "ace", "suit": "spades", "card": "AS"},
            {"rank": "2", "suit": "hearts", "card": "2H"},
        ],
        "trump_suit": "hearts",
        "variant": {"lowest_rank": "6", "attack_limit": 6, "with_passing": True},
    }


@pytest.mark.django_db
def test_restart_game(call_api, game_with_players):
    url = "/api/game/{}".format(game_with_players.slug)
    response = call_api(
        "patch",
        url,
        payload={
            "variant": {"lowest_rank": "6", "attack_limit": 6, "with_passing": True}
        },
    )
    assert response.status_code == 200

    data = response.json()
    assert set(data["players"]) == set(["anna", "vasyl", "igor", "grusha"])
    assert data["hands"] == {"anna": [], "vasyl": [], "igor": [], "grusha": []}
    assert data["slug"] == game_with_players.slug
    assert data["draw_pile"] == [{"rank": "ace", "suit": "spades", "card": "AS"}]
    assert data["trump_suit"] == "spades"
    assert data["variant"] == {
        "lowest_rank": "6",
        "attack_limit": 6,
        "with_passing": True,
    }
