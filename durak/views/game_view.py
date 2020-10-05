from django.contrib.auth.models import User
from django.db import transaction
from rest_framework import serializers
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet

from durak.models import Game, GameVariant, Player


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

    @transaction.atomic
    def create(self, validated_data):
        variant, _ = GameVariant.objects.get_or_create(**validated_data["variant"])
        instance = Game.objects.create(variant=variant)
        for player in validated_data["player_set"]:
            Player.objects.create(
                game=instance, user=User.objects.get(**player["user"])
            )
        return instance

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["players"] = self._flattened_and_ordered_players(representation)
        representation["seed"] = instance.seed
        representation["hands"] = self._hands(representation)
        return representation

    def _flattened_and_ordered_players(self, representation):
        return [player["user"] for player in representation["players"]]

    def _hands(self, representation):
        return {player: [] for player in representation["players"]}


class GameView(CreateModelMixin, RetrieveModelMixin, GenericViewSet):
    permission_classes = [AllowAny]
    serializer_class = GameSerializer
    queryset = Game.objects.all()
    lookup_field = "slug"
