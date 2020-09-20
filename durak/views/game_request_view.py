from django.db import transaction
from rest_framework import serializers
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin, ListModelMixin,
                                   UpdateModelMixin)
from rest_framework.viewsets import GenericViewSet

from durak.models import GameRequest, GameVariant
from durak.views.game_view import GameVariantSerializer

MIN_PLAYERS = 2
MAX_PLAYERS = 4


class GameRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameRequest
        fields = ["id", "players", "parameters", "variant"]

    players = serializers.SlugRelatedField("username", many=True, read_only=True)
    variant = GameVariantSerializer()

    def validate_parameters(self, value):
        if "player_count" in value:
            if MIN_PLAYERS <= value['player_count'] <= MAX_PLAYERS:
                return value
            raise serializers.ValidationError(
                f"Player count must be {MIN_PLAYERS}-{MAX_PLAYERS}"
            )

        raise serializers.ValidationError("Must specify either players or player count")

    @transaction.atomic
    def create(self, validated_data):
        variant, _ = GameVariant.objects.get_or_create(**validated_data.pop("variant"))
        instance = GameRequest.objects.create(variant=variant, **validated_data)
        instance.players.set([self.get_request_user()])
        return instance

    @transaction.atomic
    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)

        if instance.players.count() >= instance.parameters['player_count']:
            raise serializers.ValidationError("Game is full")

        instance.players.add(self.get_request_user())

        return instance

    # def _create_game(self, instance):
    #     game = GameSerializer(data=self._game_players(instance))
    #     game.is_valid(raise_exception=True)
    #     game.save()
    #
    #     self.context['game'] = game.data['slug']

    def get_request_user(self):
        return self.context["request"].user

    def to_representation(self, instance):
        result = super().to_representation(instance)
        self._add_game(result)
        return result

    def _add_game(self, result):
        try:
            result["game"] = self.context["game"]
        except KeyError:
            return

    # def _game_players(self, instance):
    #     players = [instance.player1, instance.player2]
    #     team = instance.parameters.get("team")
    #
    #     if team == Team.RED.value:
    #         pass
    #     elif team == Team.BLACK.value:
    #         players.reverse()
    #     else:
    #         shuffle(players)
    #
    #     return dict(zip(["player1", "player2"], players))


class GameRequestView(
    ListModelMixin,
    CreateModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    GenericViewSet,
):
    serializer_class = GameRequestSerializer
    queryset = GameRequest.objects.all()

    def get_serializer_context(self):
        context = super(GameRequestView, self).get_serializer_context()
        context.update({"request": self.request})
        return context
