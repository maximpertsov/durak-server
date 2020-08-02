from django.contrib.auth.models import User

from factory import DjangoModelFactory, Sequence


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ("username",)

    username = Sequence(lambda n: "user{}".format(n))
