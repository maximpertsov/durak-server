from random import shuffle

from django.core.management.base import BaseCommand
from django.utils.functional import cached_property

from durak.models import Card, DrawCard, Game


class Command(BaseCommand):
    help = "Restart game"

    def add_arguments(self, parser):
        parser.add_argument("--slug", type=str, help="Game slug", required=True)
        parser.add_argument(
            "--low-six", action="store_true", help="Lowest rank is a six",
        )

    def handle(self, slug=None, low_six=None, *args, **kwargs):
        self.slug = slug
        self.low_six = low_six

        try:
            self.restart_game()
            self.remove_ranks_below_six()
            self.write_success(f"Reset Game {self.game}")
        except Game.DoesNotExist as e:
            self.stdout.write(e, self.style.ERROR)
            return

    def remove_ranks_below_six(self):
        if not self.low_six:
            return

        DrawCard.objects.filter(game__slug=self.slug, card__rank__in="2345").delete()
        self.write_success(f"Removed all ranks below six in {self.game}")

    def restart_game(self):
        self.delete_events()
        self.shuffle_cards()

    def shuffle_cards(self):
        self.game.draw_pile.all().delete()
        card_ids = list(Card.objects.values_list("pk", flat=True))
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
