from rest_framework import serializers
from rest_framework.generics import ListAPIView

from durak.models import Event


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ["type", "user", "payload"]

    def to_representation(self, instance):
        result = super().to_representation(instance)
        # TODO: edit?
        return result


class EventView(ListAPIView):
    serializer_class = EventSerializer

    def get_queryset(self):
        return Event.objects.filter(game__slug=self.kwargs["slug"])
