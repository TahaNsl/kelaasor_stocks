from django.db import models
from django.contrib.auth.models import User
from companies.models import Company, Share

class Order(models.Model):
    ORDER_TYPE = (
        ('BUY', 'Buy'),
        ('SELL', 'Sell'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    order_type = models.CharField(max_length=4, choices=ORDER_TYPE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} {self.order_type} {self.quantity} of {self.company.name} @ {self.price}"


class Transaction(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bought_transactions")
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sold_transactions")
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
