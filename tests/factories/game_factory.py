from durak.models import Game
from factory import DjangoModelFactory, Sequence


class GameFactory(DjangoModelFactory):
    class Meta:
        model = Game
        django_get_or_create = ("slug",)

    slug = Sequence(lambda n: "game{}".format(n))
