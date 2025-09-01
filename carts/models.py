from django.db import models


class Cart(models.Model):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "cart"


class ReservedItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey("stores.Product", on_delete=models.CASCADE)
    flash_promo = models.ForeignKey(
        "flash_promos.FlashPromo", on_delete=models.CASCADE, null=True, blank=True
    )
    reserved_until = models.DateTimeField(help_text="One minute after being added")
    is_purchased = models.BooleanField(default=False)

    class Meta:
        db_table = "reserved_item"
