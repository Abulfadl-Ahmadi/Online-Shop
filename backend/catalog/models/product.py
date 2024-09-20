from django.db import models

__all__ = ('Category', 'Properties', 'Product', 'ProductProperties')

class Category(models.Model):
    name = models.CharField(max_length=155)
    description = models.TextField()
    
    def __str__(self) -> str:
        return self.name
    
    
class Properties(models.Model):
    categoty = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=155)
    
    def __str__(self) -> str:
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=155)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.IntegerField()
    inventory = models.IntegerField()
    
    def __str__(self) -> str:
        return f"{self.title} - {self.category}"
    
class ProductProperties(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    properties = models.ForeignKey(Properties, on_delete=models.CASCADE)
    value = models.CharField(max_length=155)

    