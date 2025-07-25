from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError

class User(AbstractUser):
    pass


class Author(models.Model):

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Actor(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Performance(models.Model):

    date = models.DateTimeField()
    name = models.CharField(max_length=255)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, blank=True, null=True)
    actors = models.ManyToManyField(Actor, related_name="performances")

    def __str__(self):
        return f"{self.name}, ({self.date})"


class Booking(models.Model):

    performance = models.ForeignKey(Performance, on_delete=models.CASCADE, blank=False, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)
    row = models.PositiveIntegerField()
    seat = models.CharField(max_length=1)

    def clean(self):
        if not (1 <= self.row <= 20):
            raise ValidationError("Row must be between 1 and 20.")
        if self.seat not in [chr(i) for i in range(ord("A"), ord("Q")+1)]:
            raise ValidationError("Seat must be a letter from A to Q.")

    class Meta:
        unique_together = ("performance", "row", "seat")

    def __str__(self):
        return f"{self.performance}, {self.user}, ({self.row}-{self.seat})"


class Message(models.Model):
    SENDER_CHOICES = [
        ("user", "User"),
        ("ai", "AI"),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="messages")
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    sender = models.CharField(max_length=10, choices=SENDER_CHOICES)

    def __str__(self):
        return f"{self.user.username} ({self.sender}): {self.text[:30]}..."
