from django.db import models
from core.models import TimeStampedModel


class User(TimeStampedModel):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)


class UserSegment(TimeStampedModel):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)


class UserProfile(TimeStampedModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    segments = models.ManyToManyField(UserSegment, related_name="users")
    latitude = models.FloatField()
    longitude = models.FloatField()


class UserDevice(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="devices")
    device_id = models.CharField(
        max_length=255, unique=True, help_text="Unique device identifier"
    )
    device_type = models.CharField(
        max_length=50, choices=[("ios", "iOS"), ("android", "Android")]
    )
    device_token = models.CharField(max_length=512, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def _str__(self):
        return f"{self.user.email} - {self.device_type} ({self.device_id})"
