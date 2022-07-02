from django.db import models
from django.contrib.auth.models import User

class Movies_List(models.Model):
  movie = models.IntegerField()
  username = models.ForeignKey(User,on_delete=models.CASCADE)