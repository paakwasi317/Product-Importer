from rest_framework import serializers
from workflow.models import Products


class ProductSerializer(serializers.ModelSerializer):

    """
        overriding create method to over-write duplicate products with same sku
    """
    def create(self, validated_data):
        product = Products.objects.filter(sku=validated_data.get('sku')).first()
        if not product:
            instance = Products.objects.create(**validated_data)
            print("-------created--------")
        else:
            instance = super(ProductSerializer, self).update(product, validated_data)
            print("-------updated--------")
        return instance

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
