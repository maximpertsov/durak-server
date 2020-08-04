from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.generics import RetrieveAPIView

from durak.models import DrawCard, Game


class DrawCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = DrawCard
        fields = ["suit", "rank"]

    suit = serializers.CharField(source="card.suit")
    rank = serializers.CharField(source="card.rank")


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ["slug", "players", "draw_pile"]

    players = serializers.SlugRelatedField(
        "username", queryset=User.objects.all(), many=True
    )
    draw_pile = DrawCardSerializer(many=True)


class GameView(RetrieveAPIView):
    serializer_class = GameSerializer
    queryset = Game.objects.all()
    lookup_field = "slug"
