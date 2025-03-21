from django.db import models
import os

class Category(models.Model):
    name = models.CharField(max_length=155)
    parent_category = models.ForeignKey("Category", null=True, blank=True, on_delete=models.SET_NULL)
    description = models.TextField(null=True, blank=True)
    
    def __str__(self) -> str:
        return self.name
   
   
class Properties(models.Model):
    categoty = models.ForeignKey(Category, on_delete=models.CASCADE) # typo category
    name = models.CharField(max_length=155)
    
    def __str__(self) -> str:
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=155)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.IntegerField()
    
    def inventory(self) -> int:
        return sum(item.inventory for item in self.items.all())

    def __str__(self) -> str:
        return f"{self.category} - {self.title}"
    
    def primery_image_alt_text (self) -> str: # typo primary
        primery_item = Item.objects.filter(product=self, is_primary=True).first()
        if primery_item:
            return primery_item.primery_image_alt_text()
        return None
    
    def primery_image_image_url (self) -> str:
        primery_item = Item.objects.filter(product=self, is_primary=True).first()
        if primery_item:
            return primery_item.primery_image_image_url()
        return None
    
   
class Item(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='items')
    name = models.CharField(max_length=255)
    inventory = models.IntegerField()
    is_primary = models.BooleanField(default=False)
    
    def __str__(self) -> str:
        return f"{self.product} - {self.name}"
    
    def primery_image_image_url(self) -> str:
        return ItemImage.objects.filter(item=self, is_primary=True).first().image_url() if ItemImage.objects.filter(item=self, is_primary=True).exists() else None
    
    def primery_image_alt_text(self) -> str:
        return ItemImage.objects.filter(item=self, is_primary=True).first().alt_text if ItemImage.objects.filter(item=self, is_primary=True).exists() else None
    

def upload_to(instance, filename):
    # Extract the original file extension
    ext = os.path.splitext(filename)[1]
    # Create a new filename: item-id_is-primary_timestamp
    is_primary = 'primary' if instance.is_primary else 'variant'
    timestamp = instance.id or 'new'  # Use ID if exists, else 'new' for new uploads
    new_filename = f"{instance.item.id}_{is_primary}_{timestamp}{ext}"
    return f'images/items/{instance.item.id}/{new_filename}'

class ItemImage(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='images')
    is_primary = models.BooleanField(default=False)
    image_file = models.ImageField(upload_to=upload_to)
    alt_text = models.CharField(max_length=255, blank=True)
    
    def __str__(self) -> str:
        return f"Image for {self.item.name}"
    
    def image_url(self):
        return self.image_file.url
    
    
class ItemProperties(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='properties')
    properties = models.ForeignKey(Properties, on_delete=models.CASCADE)
    value = models.CharField(max_length=155)
    
    