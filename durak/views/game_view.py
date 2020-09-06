from rest_framework import serializers
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet

from durak.models import DrawCard, Game, GameVariant, Player
from durak.operations.restart_game import RestartGame


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
        fields = ["slug", "players", "draw_pile", "variant"]

    players = PlayerSerializer(source="player_set", many=True)
    draw_pile = DrawCardSerializer(many=True)
    variant = GameVariantSerializer()

    def validate(self, data):
        print(f"variant before {dict(data['variant'])}")
        result = super().validate(data)
        print(f"variant after {dict(data['variant'])}")
        return result

    def update(self, instance, validated_data):
        print(f"variant data {dict(validated_data['variant'])}")
        variant, _ = GameVariant.objects.get_or_create(**validated_data["variant"])
        print(f"fetch variant {variant.attack_limit}")
        instance.variant = variant
        instance.save()
        print(f"saved variant {instance.variant.attack_limit}")
        RestartGame.handle(game=instance)
        return instance

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["players"] = self._flattened_and_ordered_players(representation)
        representation["trump_suit"] = self._trump_suit(representation)
        representation["hands"] = self._hands(representation)
        return representation

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
