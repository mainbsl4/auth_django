# from django.urls import path

# urlpatterns = [

# ]



from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterUserView, signup_view, signin_view

from django.urls import path
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('user/signin/', TokenObtainPairView.as_view(), name='signin_api'),
    path('user/signup/', RegisterUserView.as_view(), name='signup_api'),
    path('user/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('signin/', signin_view, name='signin_view'),
    path('signup/', signup_view, name='signup_view'),
    path('logout/', LogoutView.as_view(next_page='signin_view'), name='logout'),
]