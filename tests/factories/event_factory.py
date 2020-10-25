from durak.models import Event
from factory import DjangoModelFactory, SubFactory

from .game_factory import GameFactory
from .user_factory import UserFactory


class EventFactory(DjangoModelFactory):
    class Meta:
        model = Event

    game = SubFactory(GameFactory)
    user = SubFactory(UserFactory)
    type = "performed_fake_event"
    payload = {}
    to_state = {}
    version = 1
