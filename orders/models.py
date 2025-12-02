from django.db import models
from django.contrib.auth.models import User
from products.models import Product

class Operator(models.Model):
    """Business operator who records orders."""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=150)
    contact_number = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.full_name


class Customer(models.Model):
    """Customer placing the order."""
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Order(models.Model):
    """Order recorded by operator for a customer."""
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("shipped", "Shipped"),
        ("delivered", "Delivered"),
        ("cancelled", "Cancelled"),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="orders")
    operator = models.ForeignKey(Operator, on_delete=models.SET_NULL, null=True, related_name="orders")
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    shipping_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0)


    def __str__(self):
        return f"Order #{self.id} - {self.customer.first_name}{self.customer.last_name}"


class OrderItem(models.Model):
    """Line items inside an order."""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)  # snapshot of product price at time of order

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
