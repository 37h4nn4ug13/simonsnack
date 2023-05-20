from django.db import models
from menu.models import Product
from django.contrib.auth.models import User


# Create your models here.
class CartItem(models.Model):
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def get_total_price(self):
        return self.quantity * self.item.price

    def __str__(self):
        return f'{self.item.name} x {self.quantity}'

class Cart(models.Model):
    items = models.ManyToManyField(CartItem, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def get_total_cart_price(self):
        total = 0.0
        for cartItem in self.items.all():
            total += cartItem.get_total_price()
        return total

    def delete_cart_items(self):
        for item in CartItem.objects.all():
            item.delete()

    def __str__(self):
        return f'{self.user.username}\'s Cart'
