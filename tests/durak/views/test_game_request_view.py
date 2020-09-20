# from collections import OrderedDict

import pytest

# from durak.models import Game, GameRequest


@pytest.fixture
def assert_user_game_requests(call_api):
    def wrapped(user, response_json):
        url = "/api/game/request"
        response = call_api("get", url, user=user)
        assert response.status_code == 200
        assert response.json() == response_json

    return wrapped


@pytest.mark.django_db
def test_create_game_request(call_api, assert_user_game_requests, anna, vasyl):
    assert_user_game_requests(anna, [])

    response = call_api(
        "post",
        "/api/game/request",
        payload={
            "parameters": {},
            "variant": {"lowest_rank": "6", "attack_limit": 100, "with_passing": True},
        },
        user=vasyl,
    )
    assert response.status_code == 201

    assert_user_game_requests(
        anna,
        [
            {
                "id": 1,
                "parameters": {},
                "players": [vasyl.username],
                "variant": {
                    "lowest_rank": "6",
                    "attack_limit": 100,
                    "with_passing": True,
                },
            }
        ],
    )


#
#
# @pytest.fixture
# def test_accept_game_request(players, game_request_factory, call_api):
#     def wrapped(player1, player2, parameters):
#         game_request = game_request_factory(player1=player1, parameters=parameters)
#
#         assert game_request.player2 is None
#         assert Game.objects.count() == 0
#
#         response = call_api(
#             "patch",
#             f"/api/game/request/{game_request.pk}",
#             payload={"player2": player2.username},
#             user=player2,
#         )
#         assert response.status_code == 200
#         game_request.refresh_from_db()
#         assert game_request.player2 == player2
#
#         Game.objects.count() == 1
#         game = Game.objects.first()
#         assert response.data == {
#             "id": game_request.pk,
#             "game": game.slug,
#             "parameters": parameters,
#             "player1": player1.username,
#             "player2": player2.username,
#         }
#
#     return wrapped
#
#
# @pytest.mark.django_db
# def test_accept_game_request_p1_red(players, test_accept_game_request):
#     player1, player2 = players
#     test_accept_game_request(player1, player2, {"team": Team.RED.value})
#
#     game = Game.objects.first()
#     assert game.player1 == player1
#     assert game.player2 == player2
#
#
# @pytest.mark.django_db
# def test_accept_game_request_p1_black(players, test_accept_game_request):
#     player1, player2 = players
#     test_accept_game_request(player1, player2, {"team": Team.BLACK.value})
#
#     game = Game.objects.first()
#     assert game.player1 == player2
#     assert game.player2 == player1
#
#
# @pytest.mark.django_db
# def test_accept_game_request_p1_random(players, test_accept_game_request):
#     player1, player2 = players
#     test_accept_game_request(player1, player2, {})
#
#     game = Game.objects.first()
#     assert game.player1 in players
#     assert game.player2 in players and game.player2 != game.player1
#
#
# @pytest.mark.django_db
# def test_reject_game_request(players, game_request_factory, call_api):
#     player1, player2 = players
#     game_request = game_request_factory(player1=player1)
#
#     response = call_api("delete", f"/api/game/request/{game_request.pk}", user=player2)
#     assert response.status_code == 204
#     with pytest.raises(GameRequest.DoesNotExist):
#         game_request.refresh_from_db()
#
#
# @pytest.mark.django_db
# def test_list_game_requests(players, game_request_factory, call_api):
#     player1, player2 = players
#     open_game_request = game_request_factory(player1=player1)
#     game_request_factory(player1=player1, player2=player2)
#
#     response = call_api("get", "/api/game/request", user=player2)
#     assert response.status_code == 200
#
#     assert response.data == [
#         OrderedDict(
#             {
#                 "id": open_game_request.pk,
#                 "player1": player1.username,
#                 "player2": None,  # TODO: remove this?
#                 "parameters": open_game_request.parameters,
#             }
#         )
#     ]
