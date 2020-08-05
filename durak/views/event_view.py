from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.viewsets import GenericViewSet

from durak.models import Event


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ["type", "user", "payload"]

    user = serializers.SlugRelatedField("username", queryset=User.objects.all())

    def to_representation(self, instance):
        result = super().to_representation(instance)
        result["payload"].update(user=result.pop("user"))
        return result


class EventView(ListModelMixin, CreateModelMixin, GenericViewSet):
    serializer_class = EventSerializer

    def list(self, *args, **kwargs):
        result = super().list(*args, **kwargs)
        result.data = {"events": result.data}
        return result

    def get_queryset(self):
        return Event.objects.filter(game__slug=self.kwargs["slug"])
