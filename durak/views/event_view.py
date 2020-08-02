from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.generics import ListAPIView

from durak.models import Event


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ["type", "user", "payload"]

    user = serializers.SlugRelatedField("username", queryset=User.objects.all())

    def to_representation(self, instance):
        result = super().to_representation(instance)
        result.update(server_event=True)
        return result


class EventView(ListAPIView):
    serializer_class = EventSerializer

    def get(self, *args, **kwargs):
        result = super().get(*args, **kwargs)
        result.data = {"events": result.data}
        return result

    def get_queryset(self):
        return Event.objects.filter(game__slug=self.kwargs["slug"])
