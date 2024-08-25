from django.urls import path, include
from .views import *


urlpatterns = [
    path('user/', UserView.as_view(), name='user'),
    path('user/update/', UserUpdateView.as_view(), name='update-user'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
