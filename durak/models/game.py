from django.contrib.auth.models import User
from django.db import models
from django.utils.crypto import get_random_string

from durak.models.card import Rank


class GameManager(models.Manager):
    def _generate_slug(self):
        size = 8
        while True:
            slug = get_random_string(size).lower()
            if self.filter(slug=slug).exists():
                size += 1
                continue
            return slug

    def create(self, slug=None, **kwargs):
        kwargs["slug"] = self._generate_slug() if slug is None else slug
        return super().create(**kwargs)

    def get_by_natural_key(self, slug):
        return self.get(slug=slug)


class Game(models.Model):
    objects = GameManager()
    slug = models.CharField(max_length=64, unique=True, editable=False)
    players = models.ManyToManyField(User, through="player")

    def natural_key(self):
        return self.slug

    def __str__(self):
        return self.slug


class GameVariant(models.Model):
    game = models.OneToOneField(Game, on_delete=models.SET_NULL, null=True)
    lowest_rank = models.CharField(
        max_length=10,
        choices=[(Rank.TWO.value, Rank.TWO.label), (Rank.SIX.value, Rank.SIX.label)],
        default=Rank.SIX.value,
    )
    attack_limit = models.IntegerField(
        choices=[(6, "Standard"), (100, "Unlimited")], default=6
    )
    with_passing = models.BooleanField(default=False)
