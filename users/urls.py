from django.urls import path
from users.views import (SignUpCreateAPIView,
                         CodeVerifiedAPIView,
                         LoginView,
                         LogOutView,
                         ResendVerifyCodeAPIView,
                         ForgetPasswordView,
                         UserUpdateAPIView)

from users.views_admin import AdminListView

app_name = 'users'

urlpatterns = [
    path('register/', SignUpCreateAPIView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogOutView.as_view(), name='logout'),
    path('verify/', CodeVerifiedAPIView.as_view(), name='verify'),
    path('verify/resend/', ResendVerifyCodeAPIView.as_view(), name='verify-resend'),
    path('forget/password/', ForgetPasswordView.as_view(), name='forget-password'),
    path('update/', UserUpdateAPIView.as_view(), name='update'),
    # path('refresh/token/', RefreshTokenView.as_view(), name='refresh'),
    # path('update/avatar/', UpdateAvatarAPIView.as_view(), name='update-avatar'),

]
