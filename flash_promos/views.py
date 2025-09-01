from rest_framework import viewsets, status
from rest_framework.response import Response
from django.utils import timezone
from geopy.distance import distance
from .models import FlashPromo
from users.models import UserProfile
from stores.models import StoreProduct
from .serializers import FlashPromoSerializer
from datetime import timedelta


class FlashPromoViewSet(viewsets.ModelViewSet):
    queryset = FlashPromo.objects.all()
    serializer_class = FlashPromoSerializer

    def create(self, request, *args, **kwargs):
        serializer = FlashPromoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        store_product_id = serializer.validated_data.get("store_product")
        special_price = serializer.validated_data.get("special_price")
        user_segment_ids = serializer.validated_data.get("user_segments", [])
        start_time = timezone.now()

        try:
            store_product = StoreProduct.objects.select_related("store", "product").get(
                id=store_product_id
            )
        except StoreProduct.DoesNotExist:
            return Response(
                {"detail": "StoreProduct not found."}, status=status.HTTP_404_NOT_FOUND
            )

        # Check whether that product already has another active promotion (in any store).
        if FlashPromo.objects.filter(
            store_product__product=store_product.product,
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
            store_product=store_product,
            special_price=special_price,
            start_time=start_time,
            end_time=end_time,
            is_active=True,
        )
        flash_promo.user_segments.set(user_segment_ids)
        serializer = self.get_serializer(flash_promo)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
