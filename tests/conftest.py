import json

import pytest
from pytest_factoryboy import register
from rest_framework.test import APIClient

from tests.factories.card_factory import CardFactory
from tests.factories.event_factory import EventFactory
from tests.factories.game_factory import GameFactory, GameVariantFactory
from tests.factories.player_factory import PlayerFactory
from tests.factories.user_factory import UserFactory

register(EventFactory)
register(UserFactory)

register(UserFactory, "anna", username="anna")
register(UserFactory, "vasyl", username="vasyl")
register(UserFactory, "igor", username="igor")
register(UserFactory, "grusha", username="grusha")

register(GameFactory, slug="fakegame123")
register(GameVariantFactory)
register(PlayerFactory)
register(CardFactory)


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
