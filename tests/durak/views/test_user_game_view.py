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
        {"slug": game1.slug, "players": ["anna", "vasyl"]},
        {"slug": game2.slug, "players": ["anna", "vasyl", "igor"]},
    ]
