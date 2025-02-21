from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    profiles_following = models.ManyToManyField("self", blank=True, symmetrical=False, related_name="followers")
    # related_name is used for relation from related object back to this one
    
    def __str__(self):
        return self.username

class Post(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    content = models.TextField()
    datetime = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)
