from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Company(models.Model):
    name = models.CharField(max_length=255, unique=True)
    initial_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_shares = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    last_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.name


class Share(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="shares")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="shares")
    quantity = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('owner', 'company')

    def __str__(self):
        return f"{self.owner.username} - {self.company.name} ({self.quantity})"
