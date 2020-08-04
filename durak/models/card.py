from django.db import models


class Suit(models.TextChoices):
    HEARTS = "hearts", "Hearts"
    CLUBS = "clubs", "Clubs"
    DIAMONDS = "diamonds", "Diamonds"
    SPADES = "spades", "Spades"


class Rank(models.TextChoices):
    TWO = "2", "Two"
    THREE = "3", "Three"
    FOUR = "4", "Four"
    FIVE = "5", "Five"
    SIX = "6", "Six"
    SEVEN = "7", "Seven"
    EIGHT = "8", "Eight"
    NINE = "9", "Nine"
    TEN = "10", "Ten"
    JACK = "jack", "Jack"
    QUEEN = "queen", "Queen"
    KING = "king", "King"
    ACE = "ace", "Ace"


class Card(models.Model):
    class Meta:
        unique_together = [("rank", "suit")]

    rank = models.CharField(max_length=10, choices=Rank.choices, editable=False)
    suit = models.CharField(max_length=10, choices=Suit.choices, editable=False)

    def natural_key(self):
        return (self.rank, self.suit)

    def __str__(self):
        return f"{self.rank} of {self.suit}"


class DrawCard(models.Model):
    class Meta:
        ordering = ["sort_key"]

    card = models.ForeignKey(Card, related_name="+", on_delete=models.CASCADE)
    sort_key = models.PositiveIntegerField(unique=True)
    game = models.ForeignKey("game", related_name="draw_pile", on_delete=models.CASCADE)
