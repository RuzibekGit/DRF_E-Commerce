from rest_framework import generics, status
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from shared.utils import send_code_to_email
from users.models import UserModel, ConfirmationModel, CODE_VERIFIED, ADMIN
from rest_framework.permissions import AllowAny, IsAuthenticated

from admin.serializers import (UserListSerializer,
                               AboutUserSerializer)

from shared.pagination import CustomPagination


class AdminListView(generics.ListAPIView):
    serializer_class = UserListSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get(self, request, *args, **kwargs):
        user = self.request.user
        if not user.user_role == ADMIN:
            response = {
                "success": False,
                "message": "You do not have permission to access"
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        if pk := self.kwargs.get('pk'):
            self.serializer_class = AboutUserSerializer
            self.pagination_class = None
            return UserModel.objects.filter(id=pk)
        return UserModel.objects.all()
