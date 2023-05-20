from django.db import models
from django.contrib.auth.models import User


class Credit(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    credit = models.FloatField(default=0)

    def __str__(self):
        return f'{self.user.username} - {self.credit}'
