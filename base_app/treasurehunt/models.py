from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Score(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    score = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.user.username


class Answer(models.Model):
    answer = models.CharField(max_length=255)
