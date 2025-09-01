from rest_framework import serializers
from .models import StoreProduct


class StoreProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreProduct
        fields = ("id", "price", "stock", "store", "product")
