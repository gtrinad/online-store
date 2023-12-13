from django.db import models

from app_products.models import Product
from app_users.models import UserProfile


class Order(models.Model):
    """Order model"""

    createdAt = models.DateTimeField(auto_now_add=True, verbose_name="Date of creation")
    user = models.ForeignKey(
        UserProfile,
        on_delete=models.PROTECT,
        verbose_name="User",
        related_name="orders",
    )
    deliveryType = models.CharField(
        max_length=128, default="", verbose_name="Delivery type"
    )
    paymentType = models.CharField(
        max_length=128, default="", verbose_name="Payment type"
    )
    totalCost = models.DecimalField(
        max_digits=10, default=0, decimal_places=2, verbose_name="Total cost"
    )
    status = models.CharField(max_length=128, default="", verbose_name="Status")
    city = models.CharField(max_length=256, default="", verbose_name="City")
    address = models.CharField(max_length=256, default="", verbose_name="Address")
    products = models.ManyToManyField(
        Product, related_name="orders", verbose_name="Products"
    )

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"

    def __str__(self):
        return "Order {pk}".format(pk=self.pk)

    def email(self):
        return self.user.email

    def fullName(self):
        return self.user.fullName

    def phone(self):
        return self.user.phone


class ProductsInOrder(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="products_in_order"
    )
    product = models.ForeignKey(
        Product, on_delete=models.PROTECT, related_name="products_in_orders"
    )
    count = models.PositiveIntegerField()
