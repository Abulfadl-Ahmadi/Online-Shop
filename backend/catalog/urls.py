from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, PropertiesViewSet, ProductViewSet, BulkProductPropertiesCreateView

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'properties', PropertiesViewSet)
router.register(r'products', ProductViewSet)

urlpatterns = [
    path('/', include(router.urls)),
    path('product-perositories/', BulkProductPropertiesCreateView.as_view(), name='bulk-product-perositories-create')
]
