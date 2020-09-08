from factory import DjangoModelFactory

from durak.models import Card


class CardFactory(DjangoModelFactory):
    class Meta:
        model = Card
        django_get_or_create = (
            "rank",
            "suit",
        )

    rank = "jack"
    suit = "hearts"
