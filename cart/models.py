from django.db import models
from products.models import Product
from users.models import CustomUser
from decimal import Decimal

class Cart(models.Model):
    user = models.ForeignKey(CustomUser, null=True, blank=True, on_delete=models.CASCADE, related_name='carts')
    session_key = models.CharField(max_length=40, null=True, blank=True, unique=True)

    def __str__(self):
        return f"Cart {self.id} (User: {self.user}, Session: {self.session_key})"
    
    def get_total_price(self):
        return sum(item.get_total_price() for item in self.items.all())
    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} × {self.quantity}"
    
    def get_total_price(self):
        return self.product.price * Decimal(self.quantity)