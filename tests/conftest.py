import json

from rest_framework.test import APIClient

import pytest
from pytest_factoryboy import LazyFixture, register
from tests.factories.event_factory import EventFactory
from tests.factories.game_factory import GameFactory
from tests.factories.player_factory import PlayerFactory
from tests.factories.user_factory import UserFactory

register(EventFactory)
register(UserFactory)

register(UserFactory, "anna", username="anna")
register(UserFactory, "vasyl", username="vasyl")
register(UserFactory, "igor", username="igor")
register(UserFactory, "grusha", username="grusha")

register(GameFactory, slug="fakegame123")
register(PlayerFactory)


@pytest.fixture
def game_with_players(game, player_factory, anna, vasyl, igor, grusha):
    player_factory(game=game, user=anna)
    player_factory(game=game, user=vasyl)
    player_factory(game=game, user=igor)
    player_factory(game=game, user=grusha)
    return game


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def call_api(api_client):
    def wrapped(http_method, url, user=None, payload=None):
        if user:
            api_client.force_authenticate(user)

        args = [url]
        kwargs = (
            {"data": json.dumps(payload), "content_type": "application/json"}
            if payload
            else {}
        )

        return getattr(api_client, http_method)(*args, **kwargs)

    return wrapped
