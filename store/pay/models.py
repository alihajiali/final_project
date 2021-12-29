from django.db import models
from django.db.models.deletion import CASCADE
from accounts.models import User
from shop.models import Product

class cart_item(models.Model):
    STATUS = (
        ('A', 'تایید شده'),
        ('N', 'تایید نشده'),
        ('D', 'حذف شده'),
        ('P', 'در دست بررسی'),
    )
    owner = models.ForeignKey(User, on_delete=CASCADE)
    product = models.ForeignKey(Product, on_delete=CASCADE)
    number = models.PositiveIntegerField()
    created = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=1, choices=STATUS)

    def __str__(self):
        return f"{self.created} : {self.owner}"


class Cart(models.Model):
    owner = models.ForeignKey(User, on_delete=CASCADE)
    baskets = models.ForeignKey(cart_item, on_delete=CASCADE)
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.created} : {self.owner}"