from django.db import models

class SoybeanMealPrices(models.Model):
    contract_month = models.CharField(max_length=10, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.contract_month} - {self.price}"