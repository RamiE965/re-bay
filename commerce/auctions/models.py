from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    def __str__(self):
        return f"{self.username}"

CATEGORY_CHOICES = [
    ("Fashion", "Fashion"),
    ("Toys", "Toys"),
    ("Electronics", "Electronics"),
    ("Outdoor", "Outdoor"),
    ("Home", "Home"),
    ("Beauty", "Beauty"),
]

class Listing(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    title = models.CharField(max_length=128, unique=True)
    description = models.TextField(max_length=500)
    startingBid = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.URLField(blank=True)
    category = models.CharField(
        max_length=64,
        choices=CATEGORY_CHOICES,
        default="Fashion")
    watchers = models.ManyToManyField(User, blank=True, related_name="watchlist")
    ended = models.BooleanField(default=False)

    def __str__(self):
        return f"Listing #{self.id}: {self.title} by {self.username.username}"

class Bid(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    biddingPrice = models.DecimalField(max_digits=9, decimal_places=2)
    time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-biddingPrice',)

    def __str__(self):
        return f"Bid #{self.id} at {self.time} by {self.username.username} on {self.listing.title}: {self.biddingPrice}"

class Comment(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    message = models.TextField(max_length=500)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment {self.id} at {self.time} by {self.username.username} on {self.listing.title}: {self.message}"
