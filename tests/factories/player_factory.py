from durak.models import Player
from factory import DjangoModelFactory, SubFactory

from .game_factory import GameFactory
from .user_factory import UserFactory


class PlayerFactory(DjangoModelFactory):
    class Meta:
        model = Player

    game = SubFactory(GameFactory)
    user = SubFactory(UserFactory)
