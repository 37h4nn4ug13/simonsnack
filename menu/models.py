from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    img = models.ImageField(upload_to='products', blank=True)
    price = models.FloatField()
    snack = models.BooleanField()
    drink = models.BooleanField()
    special = models.BooleanField()

    def __str__(self):
        return self.name


