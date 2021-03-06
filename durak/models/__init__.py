"""
Models must be imported here to be detected by Django migrations

isort:skip_file
"""

from .player import Player
from .event import Event
from .game import Game, GameVariant, GameResult, GameRequest
from .card import Card
