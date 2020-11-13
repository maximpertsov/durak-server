from factory import DjangoModelFactory, Sequence, SubFactory

from durak.models import Game, GameResult, GameVariant


class GameVariantFactory(DjangoModelFactory):
    class Meta:
        model = GameVariant
        django_get_or_create = ("lowest_rank", "attack_limit", "with_passing")

    lowest_rank = "6"
    attack_limit = "six"
    with_passing = True


class GameResultFactory(DjangoModelFactory):
    class Meta:
        model = GameResult


class GameFactory(DjangoModelFactory):
    class Meta:
        model = Game
        django_get_or_create = ("slug",)

    slug = Sequence(lambda n: "game{}".format(n))
    variant = SubFactory(GameVariantFactory)
    seed = 0.1
