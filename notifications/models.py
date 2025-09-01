from django.db import models
from core.models import TimeStampedModel


class Notification(TimeStampedModel):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    flash_promo = models.ForeignKey("flash_promos.FlashPromo", on_delete=models.CASCADE)
    sent_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "notification"
