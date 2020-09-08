from django.core.management.base import BaseCommand
from django.utils.functional import cached_property

from durak.models import Game, GameVariant
from durak.operations.restart_game import RestartGame


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
            self.update_variant()
            self.restart_game()
        except Game.DoesNotExist as e:
            self.write_error(e.message)
            return

    def restart_game(self):
        RestartGame.handle(game=self.game)
        self.write_success(f"Reset Game {self.game}")

    def update_variant(self):
        if not self.low_six:
            return

        variant, _ = GameVariant.objects.get_or_create(
            lowest_rank="6",
            attack_limit=self.game.variant.attack_limit,
            with_passing=self.game.variant.with_passing,
        )
        self.game.variant = variant
        self.game.save()
        self.write_success("Removed all ranks below six")

    @cached_property
    def game(self):
        return Game.objects.get(slug=self.slug)

    def write_success(self, message):
        self.stdout.write(self.style.SUCCESS(message))

    def write_error(self, message):
        self.stdout.write(self.style.ERROR(message))
