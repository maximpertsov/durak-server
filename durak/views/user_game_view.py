from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.generics import ListAPIView

from durak.models import Game
from durak.views.game_view import GameVariantSerializer


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ["created_at", "slug", "players", "variant"]

    players = serializers.SlugRelatedField(
        "username", queryset=User.objects.all(), many=True
    )
    variant = GameVariantSerializer()


class UserGameView(ListAPIView):
    serializer_class = GameSerializer

    def get_queryset(self):
        return Game.objects.filter(players=self.request.user, result__isnull=True)
