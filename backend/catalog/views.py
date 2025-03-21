from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import UpdateAPIView, CreateAPIView, ListAPIView, get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import *
from .serializers import *


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    # Restrict write access (create, update, delete) to admin users only
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAdminUser]
        else:
            self.permission_classes = [AllowAny]

        return super().get_permissions()


class PropertiesViewSet(viewsets.ModelViewSet):
    queryset = Properties.objects.all()
    serializer_class = PropertiesSerializer

    def get_permissions(self):
        # if self.action in ['create', 'update', 'partial_update', 'destroy']:
        #     self.permission_classes = [IsAdminUser]
        # else:
        #     self.permission_classes = [AllowAny]
        self.permission_classes = [AllowAny]
        return super().get_permissions()


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.prefetch_related('items__images', 'items__properties')
    # permission_classes = [IsAuthenticatedOrReadOnly]

    def get_permissions(self):
        # if self.action in ['create', 'update', 'partial_update', 'destroy']:
        #     self.permission_classes = [IsAdminUser]
        # else:
        #     self.permission_classes = [AllowAny]
        self.permission_classes = [AllowAny]
        return super().get_permissions()
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ProductListSerializer
        return ProductDetailSerializer
    
class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.prefetch_related('images', 'properties')
    # permission_classes = [IsAuthenticatedOrReadOnly]

    def get_permissions(self):
        # if self.action in ['create', 'update', 'partial_update', 'destroy']:
        #     self.permission_classes = [IsAdminUser]
        # else:
        #     self.permission_classes = [AllowAny]
        self.permission_classes = [AllowAny]
        return super().get_permissions()
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ItemSerializer
        return ItemCreateSerializer
    

class BulkItemPropertiesCreateView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly] # should be IsAdminUser
    def post(self, request, *args, **kwargs):
        serializer = BulkItemPropertiesSerializer(data=request.data)
        if serializer.is_valid():
            item_properties = serializer.save()
            return Response({"success": "ItemProperties created successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ItemImageViewSet(viewsets.ModelViewSet):
    # permission_classes = (AllowAny, )
    queryset = ItemImage.objects.all()
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAdminUser]
        else:
            self.permission_classes = [AllowAny]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == 'list':
            return ItemImageDetailSerializer
        return ItemImageCreateSerializer
