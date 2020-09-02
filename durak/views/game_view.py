from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import AllowAny

from durak.models import DrawCard, Game, GameVariant


class DrawCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = DrawCard
        fields = ["suit", "rank", "card"]

    suit = serializers.CharField(source="card.suit")
    rank = serializers.CharField(source="card.rank")
    card = serializers.CharField(source="card.abbreviated", read_only=True)


class GameVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameVariant
        fields = ["lowest_rank", "attack_limit", "with_passing"]


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ["slug", "players", "draw_pile", "variant"]

    players = serializers.SlugRelatedField(
        "username", queryset=User.objects.all(), many=True
    )
    draw_pile = DrawCardSerializer(many=True)
    variant = GameVariantSerializer(source="gamevariant")

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["trump_suit"] = self._trump_suit(representation)
        representation["hands"] = self._hands(representation)
        return representation

    def _trump_suit(self, representation):
        return representation["draw_pile"][-1].get("suit")

    def _hands(self, representation):
        return {player: [] for player in representation["players"]}


class GameView(RetrieveAPIView):
    permission_classes = [AllowAny]
    serializer_class = GameSerializer
    queryset = Game.objects.all()
    lookup_field = "slug"
