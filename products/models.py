from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()
    category = models.CharField(max_length=100)
    quantity = models.IntegerField(default=0)  # current stock level
    currency = models.CharField(max_length=100)
    description = models.TextField()
    banner = models.ImageField(upload_to='banner', null=True, blank=True)

    def __str__(self):
        return self.name

class StockTransaction(models.Model):
    TRANSACTION_TYPES = [
        ('IN', 'Stock In'),
        ('OUT', 'Stock Out'),
        ('RETURN', 'Return'),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="transactions")
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    quantity = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
    note = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.transaction_type} - {self.product.name} ({self.quantity})"

    def save(self, *args, **kwargs):
        # Update product quantity BEFORE saving transaction
        if self.transaction_type == 'IN':
            self.product.quantity += self.quantity
        elif self.transaction_type == 'OUT':
            if self.product.quantity - self.quantity < 0:
                raise ValueError("Stock cannot go negative!")
            self.product.quantity -= self.quantity
        elif self.transaction_type == 'RETURN':
            self.product.quantity += self.quantity

        self.product.save()
        super().save(*args, **kwargs)
