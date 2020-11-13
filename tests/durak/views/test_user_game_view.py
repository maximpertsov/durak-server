import pytest


@pytest.fixture
def create_game_with_players(game_factory, player_factory):
    def wrapped(*users):
        game = game_factory()
        for user in users:
            player_factory(game=game, user=user)
        return game

    return wrapped


@pytest.mark.django_db
def test_get_user_game(call_api, create_game_with_players, anna, vasyl, igor, grusha):
    game1 = create_game_with_players(anna, vasyl)
    game2 = create_game_with_players(anna, vasyl, igor)
    create_game_with_players(vasyl, igor, grusha)

    response = call_api("get", "/api/games/me", user=anna)
    assert response.status_code == 200
    assert response.json() == [
        {
            "created_at": game1.created_at.isoformat().replace("+00:00", "Z"),
            "slug": game1.slug,
            "players": ["anna", "vasyl"],
            "variant": {
                "lowest_rank": "6",
                "attack_limit": "six",
                "with_passing": True,
            },
        },
        {
            "created_at": game2.created_at.isoformat().replace("+00:00", "Z"),
            "slug": game2.slug,
            "players": ["anna", "vasyl", "igor"],
            "variant": {
                "lowest_rank": "6",
                "attack_limit": "six",
                "with_passing": True,
            },
        },
    ]


@pytest.mark.django_db
def test_get_active_user_games(
    call_api, create_game_with_players, anna, vasyl, igor, grusha, game_result_factory
):
    game1 = create_game_with_players(anna, vasyl)
    game2 = create_game_with_players(anna, vasyl, igor)
    create_game_with_players(vasyl, igor, grusha)

    game2.result = game_result_factory(durak=igor)
    game2.save()

    response = call_api("get", "/api/games/me", user=anna)
    assert response.status_code == 200
    assert response.json() == [
        {
            "created_at": game1.created_at.isoformat().replace("+00:00", "Z"),
            "slug": game1.slug,
            "players": ["anna", "vasyl"],
            "variant": {
                "lowest_rank": "6",
                "attack_limit": "six",
                "with_passing": True,
            },
        },
    ]
