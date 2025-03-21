from rest_framework import serializers
from .models import *

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        
class PropertiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Properties
        fields = '__all__'
    
class ItemImageDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemImage
        fields = ('item', 'is_primary', 'alt_text', 'image_url')
        
class ItemImageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemImage
        fields = ('item', 'is_primary', 'alt_text', 'image_file')
        

class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id',
            'title',
            'category',
            'price',
            'inventory',
            'primery_image_alt_text',
            'primery_image_image_url',
        ]
    


class ItemPropertiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemProperties
        fields = ['id', 'item', 'properties', 'value']


class BulkItemPropertiesSerializer(serializers.Serializer):
    item_id = serializers.PrimaryKeyRelatedField(queryset=Item.objects.all())
    properties = serializers.ListField(
        child=serializers.DictField(child=serializers.CharField())
    )

    def validate_properties(self, value):
        """
        Validate the 'properties' list to ensure each dictionary has required keys
        and valid data.
        """
        if not value:  # Check if the list is empty
            raise serializers.ValidationError("The 'properties' list cannot be empty.")

        for prop in value:
            # Ensure required keys exist
            if 'property_id' not in prop or 'value' not in prop:
                raise serializers.ValidationError(
                    "Each property must have 'property_id' and 'value' keys."
                )
            
            # Optional: Validate property_id is an integer
            try:
                prop_id = int(prop['property_id'])
                if prop_id <= 0:
                    raise ValueError
            except (ValueError, TypeError):
                raise serializers.ValidationError(
                    f"Invalid 'property_id': {prop['property_id']} must be a positive integer."
                )
            
            # Optional: Validate value is non-empty
            if not prop['value'].strip():
                raise serializers.ValidationError(
                    f"Value for property_id {prop['property_id']} cannot be empty."
                )

        return value

    def create(self, validated_data):
        item = validated_data['item_id']
        properties_data = validated_data['properties']
        
        item_properties_instances = []
        for prop_data in properties_data:
            prop_id = prop_data.get('property_id')
            value = prop_data.get('value')
            try:
                # Fetch the property instance
                property_instance = Properties.objects.get(id=prop_id)

                # Create a new ItemProperties instance
                item_properties_instance = ItemProperties.objects.create(
                    item=item,
                    properties=property_instance,
                    value=value
                )
                item_properties_instances.append(item_properties_instance)
            except Properties.DoesNotExist:
                raise serializers.ValidationError(f"Property with id {prop_id} does not exist.")

        return item_properties_instances
        
      
      
class ItemSerializer(serializers.ModelSerializer):
    images = ItemImageDetailSerializer(many=True)
    properties = ItemPropertiesSerializer(many=True)
    class Meta:
        model = Item
        fields = [
            'product',
            'name',
            'inventory',
            'images',
            'primery_image_image_url',
            'primery_image_alt_text',
            'properties'
        ]

class ItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = [
            "product",
            "name",
            "inventory",
            "is_primary",
        ]


class ProductDetailSerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True, read_only=True)
    class Meta:
        model = Product
        fields = [
            'title',
            'category',
            'price',
            'items',
            'primery_image_image_url',
            'primery_image_alt_text',
        ]
        