from django.urls import path
from .views import UserProductsView, ProductView

urlpatterns = [
    path('products/', UserProductsView.as_view(), name='user-products'),
    path('product/<int:pk>/', ProductView.as_view(), name='product'),
]