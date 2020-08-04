from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.generics import RetrieveAPIView

from durak.models import Game


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ["slug", "players"]

    players = serializers.SlugRelatedField(
        "username", queryset=User.objects.all(), many=True
    )


class GameView(RetrieveAPIView):
    serializer_class = GameSerializer
    queryset = Game.objects.all()
    lookup_field = "slug"
