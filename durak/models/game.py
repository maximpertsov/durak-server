from random import random

from django.contrib.auth.models import User
from django.contrib.postgres.fields.jsonb import JSONField
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
        kwargs["seed"] = random()
        return super().create(**kwargs)

    def get_by_natural_key(self, slug):
        return self.get(slug=slug)


class GameVariant(models.Model):
    class Meta:
        unique_together = [("lowest_rank", "attack_limit", "with_passing")]

    lowest_rank = models.CharField(
        max_length=10,
        choices=[(Rank.TWO.value, Rank.TWO.label), (Rank.SIX.value, Rank.SIX.label)],
        default=Rank.SIX.value,
    )
    attack_limit = models.CharField(
        max_length=20,
        choices=[("six", "Six"), ("hand", "Hand"), ("unlimited", "Unlimited")],
        default="six",
    )
    with_passing = models.BooleanField(default=False)


class GameResult(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    durak = models.ForeignKey(User, on_delete=models.PROTECT)


class Game(models.Model):
    objects = GameManager()

    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.CharField(max_length=64, unique=True, editable=False)
    players = models.ManyToManyField(User, through="player")
    variant = models.ForeignKey(GameVariant, on_delete=models.PROTECT)
    seed = models.DecimalField(max_digits=10, decimal_places=10)
    result = models.OneToOneField(GameResult, null=True, on_delete=models.SET_NULL)

    def natural_key(self):
        return self.slug

    def __str__(self):
        return self.slug


class GameRequest(models.Model):
    variant = models.ForeignKey(GameVariant, on_delete=models.CASCADE)
    parameters = JSONField()
    players = models.ManyToManyField(User)
