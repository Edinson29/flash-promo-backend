from django.db import models
from django.db.models import UniqueConstraint
from core.models import TimeStampedModel


class Store(TimeStampedModel):
    name = models.CharField(max_length=100, unique=True)
    address = models.TextField()
    latitude = models.FloatField()
    longitude = models.FloatField()

    class Meta:
        db_table = "store"

    def __str__(self):
        return self.name


class Product(TimeStampedModel):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "product"

    def __str__(self):
        return self.name


class StoreProduct(TimeStampedModel):
    """
    Intermediary model to represent a product being sold in a specific store.
    UseFul to define proce, stock, etc. per store.
    """

    store = models.ForeignKey(
        Store, on_delete=models.CASCADE, related_name="store_products"
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="store_products"
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = "store_product"
        constraints = [
            UniqueConstraint(
                fields=["store", "product"], name="unique_product_per_store"
            )
        ]  # Avoid duplicates

    def __str__(self):
        return f"{self.product.name} in {self.store.name}"
