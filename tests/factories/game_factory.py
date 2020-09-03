from factory import DjangoModelFactory, Sequence, SubFactory

from durak.models import Game, GameVariant


class GameVariantFactory(DjangoModelFactory):
    class Meta:
        model = GameVariant
        django_get_or_create = ("lowest_rank", "attack_limit", "with_passing")

    lowest_rank = "6"
    attack_limit = 6
    with_passing = True


class GameFactory(DjangoModelFactory):
    class Meta:
        model = Game
        django_get_or_create = ("slug",)

    slug = Sequence(lambda n: "game{}".format(n))
    variant = SubFactory(GameVariantFactory)
