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


class CardManager(models.Manager):
    def get_by_natural_key(self, rank, suit):
        return self.get(rank=rank, suit=suit)


class Card(models.Model):
    class Meta:
        unique_together = [("rank", "suit")]

    objects = CardManager()
    rank = models.CharField(max_length=10, choices=Rank.choices, editable=False)
    suit = models.CharField(max_length=10, choices=Suit.choices, editable=False)

    def natural_key(self):
        return (self.rank, self.suit)

    def __str__(self):
        return f"{self.rank} of {self.suit}"

    def abbreviated(self):
        short_rank = self.rank if self.rank == "10" else self.rank[0]
        short_suit = self.suit[0]

        return f"{short_rank}{short_suit}".upper()
