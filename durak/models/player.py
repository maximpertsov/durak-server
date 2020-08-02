from django.contrib.auth.models import User


class Player(User):
    class Meta:
        proxy = True

    def games(self, **filters):
        from durak.models import Game

        return Game.objects.filter(player1=self, **filters).union(
            Game.objects.filter(player2=self, **filters)
        )
