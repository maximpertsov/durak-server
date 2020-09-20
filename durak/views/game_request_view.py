from django.contrib.auth.models import User
from django.db import transaction
from rest_framework import serializers
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin, ListModelMixin,
                                   UpdateModelMixin)
from rest_framework.viewsets import GenericViewSet

from durak.models import GameRequest, GameVariant
from durak.views.game_view import GameVariantSerializer

# from durak.serializers.game_serializer import GameSerializer


class GameRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameRequest
        fields = ["id", "players", "parameters", "variant"]

    players = serializers.SlugRelatedField("username", many=True, read_only=True)
    variant = GameVariantSerializer()

    @transaction.atomic
    def create(self, validated_data):
        variant, _ = GameVariant.objects.get_or_create(**validated_data.pop("variant"))
        instance = GameRequest.objects.create(variant=variant, **validated_data)
        instance.players.set([self.context["request"].user])
        return instance

    def to_representation(self, instance):
        result = super().to_representation(instance)
        self._add_game(result)
        return result

    def _add_game(self, result):
        try:
            result["game"] = self.context["game"]
        except KeyError:
            return

    def update(self, instance, validated_data):
        updated_instance = super().update(instance, validated_data)
        # if updated_instance.player1 and updated_instance.player2:
        #     self._create_game(updated_instance)
        return updated_instance

    # def _create_game(self, instance):
    #     game = GameSerializer(data=self._game_players(instance))
    #     game.is_valid(raise_exception=True)
    #     game.save()
    #
    #     self.context['game'] = game.data['slug']

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
