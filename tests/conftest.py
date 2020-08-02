import json

from rest_framework.test import APIClient

import pytest
from pytest_factoryboy import register
from tests.factories.event_factory import EventFactory
from tests.factories.game_factory import GameFactory
from tests.factories.user_factory import UserFactory

register(EventFactory)
register(UserFactory)
register(GameFactory, slug="fakegame123")

# Utilities


@pytest.fixture
def api_client(player):
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
