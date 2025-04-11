from rest_framework import viewsets, permissions
from .models import Transaction, Status, Type, Category, Subcategory
from .serializers import (
    TransactionSerializer, StatusSerializer, TypeSerializer,
    CategorySerializer, SubcategorySerializer
)


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class BaseOwnerViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        return self.model.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class TransactionViewSet(BaseOwnerViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    model = Transaction

class StatusViewSet(BaseOwnerViewSet):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
    model = Status

class TypeViewSet(BaseOwnerViewSet):
    queryset = Type.objects.all()
    serializer_class = TypeSerializer
    model = Type

class CategoryViewSet(BaseOwnerViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    model = Category

class SubcategoryViewSet(BaseOwnerViewSet):
    queryset = Subcategory.objects.all()
    serializer_class = SubcategorySerializer
    model = Subcategory
