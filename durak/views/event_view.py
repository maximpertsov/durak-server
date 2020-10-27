from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet

from durak.models import Event, Game, GameResult


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ["type", "game", "user", "payload", "to_state", "version"]

    game = serializers.SlugRelatedField("slug", queryset=Game.objects.all())
    user = serializers.SlugRelatedField("username", queryset=User.objects.all())

    def create(self, validated_data):
        event = super().create(validated_data)
        self._finished_game(event)
        return event

    def _finished_game(self, event):
        for player in event.to_state.get("players", []):
            if "durak" not in player.get("state", []):
                continue

            user = User.objects.get(username=player["id"])
            event.game.result = GameResult.objects.create(durak=user)
            event.game.save()
            return


class EventView(ListModelMixin, CreateModelMixin, GenericViewSet):
    permission_classes = [AllowAny]
    serializer_class = EventSerializer

    def list(self, *args, **kwargs):
        result = super().list(*args, **kwargs)
        result.data = {"events": result.data}
        return result

    def get_queryset(self):
        return Event.objects.filter(game__slug=self.kwargs["slug"]).order_by("pk")
