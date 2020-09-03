from random import shuffle

from durak.models import Card, DrawCard, Player


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
        self.remove_ranks_below_six()

    def shuffle_players(self):
        players = self._game.player_set.all()
        users = [player.user for player in players]
        shuffle(users)
        players.delete()
        for user in users:
            Player.objects.create(game=self._game, user=user)

    def remove_ranks_below_six(self):
        if not self._lowest_rank() == "6":
            return

        DrawCard.objects.filter(game=self._game, card__rank__in="2345").delete()

    def shuffle_cards(self):
        self._game.draw_pile.all().delete()
        card_ids = list(Card.objects.values_list("pk", flat=True))
        shuffle(card_ids)
        for sort_key, card_id in enumerate(card_ids):
            DrawCard.objects.create(game=self._game, card_id=card_id, sort_key=sort_key)

    def delete_events(self):
        self._game.event_set.all().delete()

    def _lowest_rank(self):
        return self._game.variant.lowest_rank
