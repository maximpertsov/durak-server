import pytest

from durak.models import Game


@pytest.fixture
def users(anna, vasyl, igor, grusha):
    return [anna, vasyl, igor, grusha]


@pytest.fixture
def cards(card_factory):
    return [
        card_factory(suit="spades", rank="ace"),
        card_factory(suit="hearts", rank="2"),
    ]


@pytest.fixture
def game_with_players(game_factory, game_variant_factory, player_factory, cards, users):
    variant = game_variant_factory(lowest_rank="2", attack_limit=6, with_passing=True)
    game = game_factory(slug="abc123", seed=0.1, variant=variant,)
    for user in users:
        player_factory(game=game, user=user)
    return game


@pytest.mark.django_db
def test_get_game(call_api, game_with_players):
    url = "/api/game/{}".format(game_with_players.slug)
    response = call_api("get", url)
    assert response.status_code == 200
    assert response.json() == {
        "players": ["anna", "vasyl", "igor", "grusha"],
        "seed": game_with_players.seed,
        "slug": game_with_players.slug,
        "variant": {"lowest_rank": "2", "attack_limit": 6, "with_passing": True},
    }


@pytest.mark.django_db
def test_create_game(call_api, users, cards):
    url = "/api/game"
    response = call_api(
        "post",
        url,
        payload={
            "variant": {"lowest_rank": "6", "attack_limit": 100, "with_passing": True},
            "players": [{"user": user.username} for user in users],
        },
    )
    assert response.status_code == 201

    data = response.json()

    try:
        assert Game.objects.get(slug=data["slug"])
    except Game.DoesNotExist:
        pytest.fail()

    assert set(data["players"]) == set(["anna", "vasyl", "igor", "grusha"])
    assert data["variant"] == {
        "lowest_rank": "6",
        "attack_limit": 100,
        "with_passing": True,
    }
