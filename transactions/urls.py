from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    TransactionViewSet, StatusViewSet, TypeViewSet,
    CategoryViewSet, SubcategoryViewSet
)

router = DefaultRouter()
router.register(r'transactions', TransactionViewSet, basename='transaction')
router.register(r'statuses', StatusViewSet, basename='status')
router.register(r'types', TypeViewSet, basename='type')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'subcategories', SubcategoryViewSet, basename='subcategory')

urlpatterns = [
    path('', include(router.urls)),
]
