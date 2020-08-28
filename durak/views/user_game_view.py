from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.generics import ListAPIView

from durak.models import Game


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ["slug", "players"]

    players = serializers.SlugRelatedField(
        "username", queryset=User.objects.all(), many=True
    )


class UserGameView(ListAPIView):
    serializer_class = GameSerializer

    def get_queryset(self):
        return Game.objects.filter(players=self.request.user)
