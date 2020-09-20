# from collections import OrderedDict

import pytest


@pytest.fixture
def cards(card_factory):
    return [
        card_factory(suit="spades", rank="ace"),
        card_factory(suit="hearts", rank="2"),
    ]


@pytest.fixture
def call_game_request_api(call_api):
    def wrapped(
        method, pk=None, user=None, payload=None, status_code=None, response_data=None
    ):
        url = "/".join(["/api/game/request", *([str(pk)] if pk else [])])
        response = call_api(method, url, user=user, payload=payload)
        if status_code:
            assert response.status_code == status_code
        if response_data:
            assert response.json() == response_data
        return response

    return wrapped


@pytest.fixture
def variant_data():
    return {"lowest_rank": "6", "attack_limit": 100, "with_passing": True}


@pytest.mark.django_db
def test_create_game_request(call_game_request_api, anna, vasyl, variant_data):
    call_game_request_api("get", user=anna, status_code=200, response_data=[])

    parameters = {"player_count": 3}
    expected_game_request_data = {
        "id": 1,
        "players": [vasyl.username],
        "parameters": parameters,
        "variant": variant_data,
    }
    call_game_request_api(
        "post",
        user=vasyl,
        payload={"parameters": parameters, "variant": variant_data},
        status_code=201,
        response_data=expected_game_request_data,
    )
    call_game_request_api(
        "get", user=anna, status_code=200, response_data=[expected_game_request_data]
    )


@pytest.mark.django_db
def test_join_game_request(call_game_request_api, anna, vasyl, variant_data):
    parameters = {"player_count": 3}
    create_response = call_game_request_api(
        "post", user=vasyl, payload={"parameters": parameters, "variant": variant_data},
    )

    game_request_id = create_response.json()["id"]
    expected_response = {
        "id": game_request_id,
        "players": [anna.username, vasyl.username],
        "parameters": parameters,
        "variant": variant_data,
    }
    call_game_request_api(
        "patch",
        pk=game_request_id,
        user=anna,
        payload={},
        status_code=200,
        response_data=expected_response,
    )


@pytest.mark.django_db
def test_create_game_request_with_invalid_player_specifications(
    call_game_request_api, vasyl, variant_data
):
    def get_kwargs(parameters, error_message):
        return {
            "method": "post",
            "user": vasyl,
            "payload": {"parameters": parameters, "variant": variant_data},
            "status_code": 400,
            "response_data": {"parameters": [error_message]},
        }

    call_game_request_api(
        **get_kwargs({}, "Must specify either players or player count")
    )
    call_game_request_api(**get_kwargs({"player_count": 1}, "Player count must be 2-4"))
    call_game_request_api(**get_kwargs({"player_count": 5}, "Player count must be 2-4"))


@pytest.mark.django_db
def test_join_full_game(call_game_request_api, anna, vasyl, igor, grusha, variant_data):
    create_response = call_game_request_api(
        "post",
        user=anna,
        payload={"parameters": {"player_count": 3}, "variant": variant_data},
    )
    game_request_id = create_response.json()["id"]
    call_game_request_api("patch", pk=game_request_id, user=vasyl, status_code=200)
    # game is created
    assert (
        "game"
        in call_game_request_api(
            "patch", pk=game_request_id, user=igor, status_code=200
        ).json()
    )
    call_game_request_api(
        "patch",
        pk=game_request_id,
        user=grusha,
        status_code=400,
        response_data=["Game is full"],
    )
