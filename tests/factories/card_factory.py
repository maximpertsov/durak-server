from durak.models import Card, DrawCard
from factory import DjangoModelFactory, Sequence, SubFactory

from .game_factory import GameFactory


class CardFactory(DjangoModelFactory):
    class Meta:
        model = Card
        django_get_or_create = (
            "rank",
            "suit",
        )

    rank = "jack"
    suit = "hearts"


class DrawCardFactory(DjangoModelFactory):
    class Meta:
        model = DrawCard

    game = SubFactory(GameFactory)
    card = SubFactory(CardFactory)
    sort_key = Sequence(lambda n: n + 1)
