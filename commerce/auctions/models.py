from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=255)
    starting_bid = models.DecimalField(decimal_places=2, max_digits=6)
    image_url = models.URLField()
    category = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.id}: {self.title}"

class Bid(models.Model):
    pass 

class Comment(models.Model):
    pass