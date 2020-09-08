from random import Random

from rest_framework import serializers
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet

from durak.models import Card, Game, GameVariant, Player
from durak.operations.restart_game import RestartGame


class GameVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameVariant
        fields = ["lowest_rank", "attack_limit", "with_passing"]

    def get_unique_together_validators(self):
        return []


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ["user"]

    user = serializers.CharField(source="user.username")


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ["slug", "players", "variant"]

    players = PlayerSerializer(source="player_set", many=True)
    variant = GameVariantSerializer()

    def update(self, instance, validated_data):
        variant, _ = GameVariant.objects.get_or_create(**validated_data["variant"])
        instance.variant = variant
        instance.save()
        RestartGame.handle(game=instance)
        return instance

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["draw_pile"] = self._draw_pile(instance)
        representation["players"] = self._flattened_and_ordered_players(representation)
        representation["trump_suit"] = self._trump_suit(representation)
        representation["hands"] = self._hands(representation)
        return representation

    def _draw_pile(self, instance):
        cards = [
            {"card": card.abbreviated(), "suit": card.suit, "rank": card.rank}
            for card in Card.objects.all()
        ]
        Random(instance.seed).shuffle(cards)
        return cards

    def _flattened_and_ordered_players(self, representation):
        return [player["user"] for player in representation["players"]]

    def _trump_suit(self, representation):
        return representation["draw_pile"][-1].get("suit")

    def _hands(self, representation):
        return {player: [] for player in representation["players"]}


class GameView(RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    permission_classes = [AllowAny]
    serializer_class = GameSerializer
    queryset = Game.objects.all()
    lookup_field = "slug"
