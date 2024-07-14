from django.contrib.auth import authenticate
from django.core.validators import FileExtensionValidator
from django.db.models import Q

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

import re
import dns.resolver

from shared.utils import send_code_to_email
from users.models import UserModel, PHOTO, NEW, DONE, CODE_VERIFIED



def is_valid_email(email):
    pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
    return re.match(pattern, email) is not None


def raise_error(message="Validation error!"):
    response = {
        "success": False,
        "message": message
    }
    raise serializers.ValidationError(detail=response)



# ----------------------- Users List ------------------------------
# region users list
class UserListSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserModel
        fields = ['id', 'first_name', 'last_name',
                  'username', 'email', 'auth_status', 'user_role']
# endregion


# ----------------------- About User ------------------------------
# region user
class AboutUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserModel
        fields = ['id', 'first_name', 'last_name',
                  'username', 'email', 'phone_number', 'bio', 'created_at', 'updated_at', 'last_login',  'auth_status', 'user_role']
# endregion



    

   