from django.db import models
from core.models import TimeStampedModel


class User(TimeStampedModel):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)

    class Meta:
        db_table = "user"


class UserSegment(TimeStampedModel):
    SEGMENT_CHOICES = [
        ("user_standard", "Usuario Estándar"),
        ("new_user", "Usuario Nuevo"),
        ("frequent_user", "Usuario Frecuente"),
    ]
    name = models.CharField(
        max_length=50,
        unique=True,
        choices=SEGMENT_CHOICES,
        help_text="The unique identifier for the segment.",
    )
    display_name = models.CharField(
        max_length=100,
        help_text="The display name for the segment in the app or admin.",
        default="",
    )
    description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = "user_segment"

    def __str__(self):
        return self.name


class UserProfile(TimeStampedModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    segments = models.ManyToManyField(UserSegment, related_name="users")
    latitude = models.FloatField()
    longitude = models.FloatField()

    class Meta:
        db_table = "user_profile"


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

    class Meta:
        db_table = "user_device"

    def _str__(self):
        return f"{self.user.email} - {self.device_type} ({self.device_id})"
