from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.expressions import OrderBy
from accounts.models import User
from shop.models import Product, Market



class Cart(models.Model):
    STATUS = (
        ('A', 'تایید شده'),
        ('N', 'تایید نشده'),
        ('S', 'پرداخت شده'),
        ('P', 'در دست بررسی'),
    )
    owner = models.ForeignKey(User, on_delete=CASCADE, related_name='owner_cart')
    market = models.ForeignKey(Market, on_delete=CASCADE, related_name='market_cart')
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    status = models.CharField(max_length=1, choices=STATUS)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f"{self.created} - {self.owner}"

    def get_total_price(self):
        return sum(item.get_cost() for item in self.cart_item.all())



class cart_item(models.Model):
    cart = models.ForeignKey(Cart, on_delete=CASCADE, related_name='cart_item')
    product = models.ForeignKey(Product, on_delete=CASCADE, related_name='product_item')
    number = models.PositiveSmallIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=0)
    
    # def __str__(self):
    #     return self.price

    def get_cost(self):
        return self.price * self.number