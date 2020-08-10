from django.core.management.base import BaseCommand

from durak.models import Game
from durak.models import Card, DrawCard
from django.utils.functional import cached_property
from random import shuffle


class Command(BaseCommand):
    help = "Restart game"

    def add_arguments(self, parser):
        parser.add_argument("--slug", type=str, help="Game slug", required=True)

    def handle(self, slug=None, *args, **kwargs):
        self.slug = slug

        try:
            self.restart_game()
            self.write_success(f"Reset Game {self.game}")
        except Game.DoesNotExist as e:
            self.stdout.write(e, self.style.ERROR)
            return

    def restart_game(self):
        self.delete_events()
        self.shuffle_cards()

    def shuffle_cards(self):
        self.game.draw_pile.all().delete()
        card_ids = list(Card.objects.values_list('pk', flat=True))
        shuffle(card_ids)
        for sort_key, card_id in enumerate(card_ids):
            DrawCard.objects.create(game=self.game, card_id=card_id, sort_key=sort_key)

    def delete_events(self):
        self.game.event_set.all().delete()

    @cached_property
    def game(self):
        return Game.objects.get(slug=self.slug)

    def write_success(self, message):
        self.stdout.write(self.style.SUCCESS(message))

    def write_error(self, message):
        self.stdout.write(self.style.ERROR(message))
