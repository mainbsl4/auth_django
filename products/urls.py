from django.urls import path
from .views import UserProductsView, ProductView, user_products_view, detail_product, create_product_view, update_product, delete_product

urlpatterns = [
    path('products/', UserProductsView.as_view(), name='user_products_api'),
    path('product/<int:pk>/', ProductView.as_view(), name='product_api'),
    # path('user/products/', UserProductsView.as_view(), name='user_products'),
    path('product/create/', create_product_view, name='create_product_view'),
    path('users/products/', user_products_view, name='user_products_view'),
    path('product/detail/<int:pk>/', detail_product, name='product_detail_view'),
    path('product/update/<int:pk>/', update_product, name='update_product_view'),
    path('product/delete/<int:pk>/', delete_product, name='delete_product_view'),
]