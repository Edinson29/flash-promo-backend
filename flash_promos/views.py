from rest_framework import viewsets, status
from rest_framework.response import Response
from django.utils import timezone
from django.core.cache import cache
from geopy.distance import distance
from .models import FlashPromo
from users.models import UserProfile, UserDevice
from stores.models import StoreProduct
from notifications.models import Notification
from .serializers import FlashPromoSerializer
from core.firebase import FirebaseService
from datetime import timedelta


class FlashPromoViewSet(viewsets.ModelViewSet):
    queryset = FlashPromo.objects.all()
    serializer_class = FlashPromoSerializer
    CACHE_KEY_ACTIVE = "flash_promos_active"

    def list(self, request):
        is_active = request.query_params.get("is_active")

        if is_active == "true":
            promos = cache.get(self.CACHE_KEY_ACTIVE)

            if not promos:
                promos = FlashPromo.objects.filter(is_active=True).select_related(
                    "store_product__store", "store_product__product"
                )
                page = self.paginate_queryset(promos)
                if page is not None:
                    serializer = self.get_serializer(page, many=True)
                    promos = serializer.data
                    cache.set(self.CACHE_KEY_ACTIVE, promos, timeout=300)
                    return self.get_paginated_response(promos)

                serializer = self.get_serializer(promos, many=True)
                promos = serializer.data
                cache.set(self.CACHE_KEY_ACTIVE, promos, timeout=300)

            return Response(promos)

        queryset = self.paginate_queryset(self.queryset)
        if queryset is not None:
            serializer = self.get_serializer(queryset, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(self.queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = FlashPromoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        title = serializer.validated_data.get("title")
        store_product = serializer.validated_data.get("store_product")
        special_price = serializer.validated_data.get("special_price")
        user_segment_ids = serializer.validated_data.get("user_segments", [])
        start_time = timezone.now()

        try:
            store_product_db = StoreProduct.objects.select_related(
                "store", "product"
            ).get(id=store_product.id)
        except StoreProduct.DoesNotExist:
            return Response(
                {"detail": "StoreProduct not found."}, status=status.HTTP_404_NOT_FOUND
            )

        # Check whether that product already has another active promotion (in any store).
        if FlashPromo.objects.filter(
            store_product__product=store_product_db.product,
            is_active=True,
        ).exists():
            return Response(
                {
                    "detail": "This product already has an active flash promotion in another store."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # create flash promo
        end_time = start_time + timedelta(hours=2)  # configurable
        flash_promo = FlashPromo.objects.create(
            title=title,
            store_product=store_product,
            special_price=special_price,
            start_time=start_time,
            end_time=end_time,
            is_active=True,
        )

        # Invalidate cache
        cache.delete(self.CACHE_KEY_ACTIVE)

        flash_promo.user_segments.set(user_segment_ids)
        serializer = self.get_serializer(flash_promo)

        store_location = (
            flash_promo.store_product.store.latitude,
            flash_promo.store_product.store.longitude,
        )

        # Search for users within the specified radius
        nearby_users = []
        for user_profile in UserProfile.objects.all():
            user_location = (user_profile.latitude, user_profile.longitude)
            if distance(store_location, user_location).km <= flash_promo.radius:
                # Validate that the user has not received another notification today
                if not Notification.objects.filter(
                    user=user_profile.user,
                    sent_at__date=timezone.now().date(),
                ).exists():
                    nearby_users.append(user_profile.user)

        device_tokens = UserDevice.objects.filter(
            user__in=nearby_users,
            is_active=True,
        ).values_list("device_token", flat=True)

        # create recordes in notification model
        notifications = [
            Notification(user=user, flash_promo=flash_promo) for user in nearby_users
        ]
        Notification.objects.bulk_create(notifications)

        # send notifications
        data = {
            "flash_promo_id": flash_promo.id,
            "title": serializer.data.get("title"),
            "special_price": str(serializer.data.get("special_price")),
            "store_product_id": flash_promo.store_product.id,
            "store_name": flash_promo.store_product.store.name,
            "product_id": flash_promo.store_product.product.id,
            "product_name": flash_promo.store_product.product.name,
            "start_time": serializer.data.get("start_time"),
            "end_time": serializer.data.get("end_time"),
        }
        FirebaseService().send_notifications_in_batches(
            device_tokens=device_tokens,
            title=serializer.data.get("title"),
            body=data,
        )

        return Response(serializer.data, status=status.HTTP_201_CREATED)
