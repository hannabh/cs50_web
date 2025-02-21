from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    followers = models.IntegerField(default=0)
    following = models.IntegerField(default=0)

class Post(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    content = models.TextField()
    datetime = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)
