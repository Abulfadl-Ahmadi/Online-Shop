from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'properties', PropertiesViewSet)
router.register(r'products', ProductViewSet)
router.register(r'product-images', ItemImageViewSet)
router.register(r'item', ItemViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('product-perositories/', BulkItemPropertiesCreateView.as_view(), name='bulk-product-perositories-create'),
    # path('image-product/<str:id>', ProductImageView.as_view(), name='image-product'),
    # path('create-image-product/', ProductImageCreateView.as_view(), name='create-image-product')
    # path('products/', ProductListView.as_view(), name='products'),
]
