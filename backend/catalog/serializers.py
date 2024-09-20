from rest_framework import serializers
from .models import ProductProperties, Product, Properties
from rest_framework import serializers
from .models import *

__all__ = (
    'CategorySerializer',
    'PropertiesSerializer',
    'ProductSerializer',
    'ProductProperties',
)

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        
class PropertiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Properties
        fields = '__all__'
        
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        


class ProductPropertiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductProperties
        fields = ['id', 'product', 'properties', 'value']


class BulkProductPropertiesSerializer(serializers.Serializer):
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    properties = serializers.ListField(
        child=serializers.DictField(child=serializers.CharField())
    )

    def create(self, validated_data):
        product = validated_data['product_id']
        properties_data = validated_data['properties']
        
        product_properties_instances = []
        for prop_data in properties_data:
            prop_id = prop_data.get('property_id')
            value = prop_data.get('value')

            # Fetch the property instance
            property_instance = Properties.objects.get(id=prop_id)

            # Create a new ProductProperties instance
            product_properties_instance = ProductProperties.objects.create(
                product=product,
                properties=property_instance,
                value=value
            )
            product_properties_instances.append(product_properties_instance)

        return product_properties_instances
        
        