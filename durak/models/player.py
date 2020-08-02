from django.contrib.auth.models import User
from django.db import models


class Player(models.Model):
    game = models.ForeignKey("game", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
