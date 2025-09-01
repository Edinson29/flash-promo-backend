from django.core.management.base import BaseCommand
from faker import Faker
from faker_food import FoodProvider
import random
import uuid

from users.models import User, UserSegment, UserProfile, UserDevice
from stores.models import Store, Product, StoreProduct



fake = Faker("es_CO")

class Command(BaseCommand):
    help = "Generate mock data for users, stores and products"


    def handle(self, *args, **kwargs):
        users = []
        user_ids = []
        user_segments = []
        user_segment_names = {
            "user_standard": "Usuario standard",
            "new_user": "Nuevo Usuario",
            "frequent_user": "Usuario frecuente"
        }
        stores = []
        products = []

        if User.objects.exists() or Store.objects.exists() or Product.objects.exists():
            self.stdout.write(self.style.WARNING("⚠️ The data already exists; nothing new was created."))
            return

        # USERS!!!!!!!!!!!!
        for user_segment_name in user_segment_names:
            segment = UserSegment.objects.create(
                name=user_segment_name,
                display_name=user_segment_names[user_segment_name],
                description=f"Segmento de {user_segment_names[user_segment_name]}"
            )
            user_segments.append(segment)


        for _ in range(10000):
            user = User.objects.create(
                email=fake.unique.email(),
                name=fake.name()
            )

            users.append(user)
            user_ids.append(user.id)
            
            user_profile = UserProfile.objects.create(
                user=user,
                latitude=fake.latitude(),
                longitude=fake.longitude()
            )

            user_profile.segments.add(random.choice(user_segments))

            UserDevice.objects.create(
                user=user,
                device_id=str(uuid.uuid4()),
                device_type=random.choice(["ios", "android"]),
                device_token=str(uuid.uuid4()),
                is_active=True
            )

        
        # STORES !!!!!!!!!!!!
        for _ in range(random.randint(10, 20)):
            store = Store.objects.create(
                name=fake.unique.company(),
                address=fake.address(),
                latitude=fake.latitude(),
                longitude=fake.longitude()
            )
            stores.append(store)

        for _ in range(random.randint(30, 50)):
            fake.add_provider(FoodProvider)

            product = Product.objects.create(
                name=random.choice([fake.unique.fruit(), fake.unique.vegetable()]),
                description=fake.text(max_nb_chars=200)
            )
            products.append(product)


        # Asign products to all stores !!!!!!!!!!!!
        for store in stores:
            for product in products:
                StoreProduct.objects.update_or_create(
                    store=store,
                    product=product,
                    price=random.randint(500, 1000),
                    stock=random.randint(1, 100),
                )
        
        self.stdout.write(self.style.SUCCESS("✅ Mock data created successfully"))