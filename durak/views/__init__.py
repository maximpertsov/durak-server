from django.core.management import call_command
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt


@method_decorator(csrf_exempt, name="dispatch")
class RestartGameView(View):
    def post(self, request, slug):
        call_command("restart_game", slug=slug, low_six=True)
        return JsonResponse({"status": "reset in progress"})


from .event_view import EventView
from .game_view import GameView
