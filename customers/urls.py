from django.urls import path
from .views import UserCustomersView, CustomersView, user_customers_view, detail_customers, create_customers_view, update_customers, delete_customers

urlpatterns = [
    path('customers/', UserCustomersView.as_view(), name='user_customers_api'),
    path('customers/<int:pk>/', CustomersView.as_view(), name='customers_api'),
    # path('user/customers/', UserCustomersView.as_view(), name='user_customers'),
    path('customers/create/', create_customers_view, name='create_customers_view'),
    path('users/customers/', user_customers_view, name='user_customers_view'),
    path('customers/detail/<int:pk>/', detail_customers, name='customers_detail_view'),
    path('customers/update/<int:pk>/', update_customers, name='update_customers_view'),
    path('customers/delete/<int:pk>/', delete_customers, name='delete_customers_view'),
]