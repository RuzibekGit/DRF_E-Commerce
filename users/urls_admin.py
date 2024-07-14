from django.urls import path
from users.views import (SignUpCreateAPIView,
                         CodeVerifiedAPIView,
                         LoginView,
                         LogOutView,
                         ResendVerifyCodeAPIView,
                         ForgetPasswordView,
                         UserUpdateAPIView)

from users.views_admin import AdminListView

app_name = 'admins'

urlpatterns = [
    path('users/', AdminListView.as_view(), name='users'),
    path('users/<int:pk>/', AdminListView.as_view(), name='about-user'),


]
