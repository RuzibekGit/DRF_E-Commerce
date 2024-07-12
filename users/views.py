from rest_framework import generics, status
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from shared.utils import send_code_to_email
from users.models import UserModel, ConfirmationModel, CODE_VERIFIED
from rest_framework.permissions import AllowAny, IsAuthenticated

from users.serializers import (SignUpSerializer,
                               LoginSerializer,
                               LogoutSerializer)



# -------------------------- Registration -------------------------------
# region sign in
class SignUpCreateAPIView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = SignUpSerializer
    model = UserModel
# endregion


# -------------------------- Log In -------------------------------
# region log in
class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer

# endregion


# -------------------------- Log Out -------------------------------
# region log out
class LogOutView(APIView):
    serializer_class = LogoutSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        refresh = self.request.data['refresh']
        token = RefreshToken(token=refresh)
        token.blacklist()
        response = {
            "success": True,
            "message": "User logged out successfully"
        }
        return Response(response, status=status.HTTP_200_OK)
# endregion

# -------------------------- Verification -------------------------------
# region verification
class CodeVerifiedAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = self.request.user
        code = request.data.get('code')

        verification_code = ConfirmationModel.objects.filter(
            code=code, is_confirmed=False, user_id=user.id,
            expiration_time__gte=timezone.now()
        )
        if not verification_code.exists():
            response = {
                "success": False,
                "message": "Verification code is not valid"
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        ConfirmationModel.objects.update(is_confirmed=True)

        user.auth_status = CODE_VERIFIED
        user.save()

        response = {
            "success": True,
            "access_token": user.token()['access_token'],
            "auth_status": user.auth_status
        }
        return Response(response, status=status.HTTP_200_OK)
# endregion