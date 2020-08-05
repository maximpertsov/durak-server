from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.viewsets import GenericViewSet

from durak.models import Event, Game


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ["type", "game", "user", "payload"]

    game = serializers.SlugRelatedField("slug", queryset=Game.objects.all())
    user = serializers.SlugRelatedField("username", queryset=User.objects.all())


class EventView(ListModelMixin, CreateModelMixin, GenericViewSet):
    serializer_class = EventSerializer

    def list(self, *args, **kwargs):
        result = super().list(*args, **kwargs)
        result.data = {"events": result.data}
        return result

    def get_queryset(self):
        return Event.objects.filter(game__slug=self.kwargs["slug"])
