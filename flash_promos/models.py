from django.db import models
from core.models import TimeStampedModel
from stores.models import StoreProduct
from users.models import UserSegment
from django.utils import timezone


class FlashPromo(TimeStampedModel):
    store_product = models.ForeignKey(
        StoreProduct, on_delete=models.CASCADE, related_name="flash_promos"
    )
    special_price = models.DecimalField(max_digits=10, decimal_places=2)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    user_segments = models.ManyToManyField(UserSegment, related_name="flash_promos")
    radius = models.PositiveIntegerField(default=2, help_text="The distance is in km")
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "flash_promo"
        indexes = [models.Index(fields=["start_time", "end_time"])]

    def __str__(self):
        return f"Flash Promo for {self.store_product.product.name} at {self.store_product.store.name}"

    def is_valid(self):
        return self.end_time > timezone.now()
