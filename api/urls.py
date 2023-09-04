from  rest_framework.routers import DefaultRouter
from django.urls import path ,include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.urls import re_path
from blog.views import PostViewSet
from django.urls import path
from users.views import *


urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='register_user'),
    path('login-with-otp/',LoginWithOTP.as_view(),  name='login-with-otp'),
    path('validate-otp/', ValidateOTP.as_view(), name='validate-otp'),
    path('edit-info/<int:pk>/', EditView.as_view(), name='edit_user'),
    path('change_password/<int:pk>/', ChangePasswordView.as_view(), name='auth_change_password'),
]

blog_router = DefaultRouter()
blog_router.register('post', PostViewSet)
urlpatterns += blog_router.urls
