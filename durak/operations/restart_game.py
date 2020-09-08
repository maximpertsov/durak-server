from random import random, shuffle

from durak.models import Player


class RestartGame:
    @classmethod
    def handle(cls, *, game):
        cls(game=game).restart_game()

    def __init__(self, *, game):
        self._game = game

    def restart_game(self):
        self.delete_events()
        self.shuffle_cards()
        self.shuffle_players()

    def shuffle_players(self):
        players = self._game.player_set.all()
        users = [player.user for player in players]
        shuffle(users)
        players.delete()
        for user in users:
            Player.objects.create(game=self._game, user=user)

    def shuffle_cards(self):
        self._game.seed = random()
        self._game.save()

    def delete_events(self):
        self._game.event_set.all().delete()
