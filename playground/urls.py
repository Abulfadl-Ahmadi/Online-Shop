from django.urls import URLPattern, path
from .views import *

urlpatterns = [
    path('welcome/', welcome),
    path('products/', products),
]
