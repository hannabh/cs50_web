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

LISTING_STATUS ={
    'OPEN': 'Open',
    'CLOSED': 'Closed',
}

class User(AbstractUser):
    pass

class Listing(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=255)
    starting_bid = models.DecimalField(decimal_places=2, max_digits=6, validators=[MinValueValidator(0)])
    image_url = models.URLField(blank=True, null=True)
    category = models.CharField(max_length=64, choices=CATEGORIES, blank=True, null=True)
    watchlist = models.BooleanField(default=False)
    status = models.CharField(max_length=6, choices=LISTING_STATUS, default='OPEN')
    listed_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listed_by")
    winner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="winner", blank=True, null=True)

    def __str__(self):
        return f"{self.id}: {self.title}"

class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    bidder  = models.ForeignKey(User, on_delete=models.CASCADE)
    bid = models.DecimalField(decimal_places=2, max_digits=6, validators=[MinValueValidator(0)])

class Comment(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    comment = models.CharField(max_length=255)