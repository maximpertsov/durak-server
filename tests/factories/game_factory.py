from durak.models import Game, GameVariant
from factory import DjangoModelFactory, Sequence, SubFactory


class GameFactory(DjangoModelFactory):
    class Meta:
        model = Game
        django_get_or_create = ("slug",)

    slug = Sequence(lambda n: "game{}".format(n))


class GameVariantFactory(DjangoModelFactory):
    class Meta:
        model = GameVariant

    game = SubFactory(GameFactory)
    lowest_rank = "6"
    attack_limit = 6
    with_passing = True
