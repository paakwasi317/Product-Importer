from rest_framework import serializers
from workflow.models import Products


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = [
            'id',
            'uuid',
            'name',
            'sku',
            'active',
            'description',
            'created_at',
            'updated_at'
        ]
