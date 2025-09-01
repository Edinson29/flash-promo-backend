from django.core.management.base import BaseCommand
from users.models import User, UserSegment, UserProfile, UserDevice
from stores.models import Store, Product, StoreProduct
from flash_promos.models import FlashPromo
from notifications.models import Notification


class Command(BaseCommand):
    help = "Delete all data from the specified models"

    def handle(self, *args, **kwargs):
        # Lista de modelos a limpiar
        models = [
            Notification,
            FlashPromo,
            StoreProduct,
            Product,
            Store,
            UserDevice,
            UserProfile,
            UserSegment,
            User,
        ]

        # Eliminar los registros de cada modelo
        for model in models:
            model_name = model.__name__
            count = model.objects.count()
            model.objects.all().delete()
            self.stdout.write(
                self.style.SUCCESS(f"✅ Deleted {count} records from {model_name}")
            )

        self.stdout.write(
            self.style.SUCCESS("✅ All data has been deleted successfully!")
        )
