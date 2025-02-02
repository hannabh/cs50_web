from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator


CATEGORIES = {
    None: '',
    'Fasion': 'Fashion',
    'Toys': 'Toys',
    'Home': 'Home',
    'Electronics': 'Electronics',
    'Books': 'Books',
}

class User(AbstractUser):
    pass

class Listing(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=255)
    starting_bid = models.DecimalField(decimal_places=2, max_digits=8, validators=[MinValueValidator(0)])
    image_url = models.URLField(blank=True, null=True)
    category = models.CharField(max_length=64, choices=CATEGORIES, blank=True, null=True)
    open = models.BooleanField(default=True)
    listed_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listed_by")
    winner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="winner", blank=True, null=True)
    watchers = models.ManyToManyField(User, blank=True, null=True, related_name='watchlist')

    def get_current_price(self):
        highest_bid = self.bid_set.order_by('-bid').first()  # bid_set is automatically created
        return highest_bid.bid if highest_bid else self.starting_bid

    def get_highest_bidder(self):
        highest_bid = self.bid_set.order_by('-bid').first()
        return highest_bid.bidder if highest_bid else None

    def __str__(self):
        return f"{self.id}: {self.title}"

class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    bidder  = models.ForeignKey(User, on_delete=models.CASCADE)
    bid = models.DecimalField(decimal_places=2, max_digits=8, validators=[MinValueValidator(0)])

class Comment(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    comment = models.CharField(max_length=255)