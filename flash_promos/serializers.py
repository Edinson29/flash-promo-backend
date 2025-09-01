# serializers.py
from rest_framework import serializers
from .models import FlashPromo
from users.models import UserSegment
from stores.models import StoreProduct
from django.utils import timezone


class FlashPromoSerializer(serializers.ModelSerializer):
    user_segments = serializers.PrimaryKeyRelatedField(
        queryset=UserSegment.objects.all(),
        many=True,
    )

    class Meta:
        model = FlashPromo
        fields = (
            "id",
            "title",
            "store_product",
            "special_price",
            "start_time",
            "end_time",
            "user_segments",
        )

    def validate(self, data):
        start_time = data.get("start_time")
        end_time = data.get("end_time")
        special_price = data.get("special_price")
        store_product = data.get("store_product")

        if start_time and end_time:
            if start_time.date() != end_time.date():
                raise serializers.ValidationError(
                    "start_time and end_time must be the same day."
                )
            if start_time >= end_time:
                raise serializers.ValidationError(
                    "start_time can't be major or equal than end_time."
                )

        if store_product and special_price:
            if float(special_price) >= float(store_product.price):
                raise serializers.ValidationError(
                    "special_price must be less than the product's price."
                )
        return data
