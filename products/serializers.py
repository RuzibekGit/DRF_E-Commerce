from django.contrib.auth import authenticate
from django.core.validators import FileExtensionValidator
from django.db.models import Q

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

import re
import dns.resolver

from shared.utils import send_code_to_email
from users.models import UserModel, PHOTO, NEW, DONE, CODE_VERIFIED

from products.models import ProductModel



def is_valid_email(email):
    pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
    return re.match(pattern, email) is not None


def raise_error(message="Validation error!"):
    response = {
        "success": False,
        "message": message
    }
    raise serializers.ValidationError(detail=response)

# ----------------------- Product Add ------------------------------
# region product add
class ProductAddSerializer(serializers.ModelSerializer):
    # first_name = serializers.CharField(write_only=True, required=True)
    # last_name = serializers.CharField(write_only=True, required=True)
    # username = serializers.CharField(write_only=True, required=True)
    # email = serializers.CharField(write_only=True, required=True)
    # password = serializers.CharField(write_only=True, required=True)
    # confirm_password = serializers.CharField(write_only=True, required=True)

    # uuid = serializers.IntegerField(read_only=True)
    # auth_status = serializers.CharField(read_only=True, required=False)

    validation_error = dict()

    class Meta:
        model = ProductModel
        fields = ['name', 'price', 'photos', 'description', 'quantity']


    # # ------------------------------
    # def create(self, validated_data):
    #     product = super(ProductAddSerializer, self).create(validated_data)
        
      
    #     product.save()
    #     return product
    
    # ------------------------------
    def validate(self, data):
        validation_error = dict()

        
        return data
    
    
    
    # ------------------------------
    def to_representation(self, instance):
        data = {
            'status': True,
            'message': "Successfully new product added ",
            'data': instance
            }
       
        return data
# endregion



# ----------------------- Login ------------------------------
# region login
class LoginSerializer(TokenObtainPairSerializer):
    def __init__(self, *args, **kwargs):
        super(LoginSerializer, self).__init__(*args, **kwargs)
        self.fields['userinput'] = serializers.CharField(max_length=128)
        self.fields['username'] = serializers.CharField(read_only=True)


    def validate(self, attrs):
        userinput = attrs.get('userinput')

        if is_valid_email(userinput):
            user = UserModel.objects.filter(email=userinput).first()
        elif userinput.startswith('+'):
            user = UserModel.objects.filter(phone_number=userinput).first()
        else:
            user = UserModel.objects.filter(username=userinput).first()

        if user is None:
            raise_error("Invalid username or password")

        auth_user = authenticate(
            username=user.username, 
            password=attrs['password']
        )
        
        if auth_user is None:
            raise_error("Invalid username or password")

        response = {
            "success": True,
            "access_token": auth_user.token()['access_token'],
            "refresh_token": auth_user.token()['refresh_token']
        }
        return response
# endregion


# ----------------------- LogIn ------------------------------
# region login
class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()
# endregion


# ----------------------- Forgot Password ------------------------------
# region forgot password
class ForgetPasswordSerializer(serializers.Serializer):
    email = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        email = attrs.get('email')
        user = UserModel.objects.filter(email=email)
        
        if not email:
            raise_error("Email is required")

        if not user.exists():
            raise_error("User not found")
        elif UserModel.objects.filter(email=email, auth_status=NEW).exists():
            raise_error(message="The user’s verification is still pending.")

        attrs["user"] = user.first()
        return attrs
# endregion


# ----------------------- Update User ------------------------------
# region update
class UpdateUserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(write_only=True, required=True)
    last_name = serializers.CharField(write_only=True, required=True)
    username = serializers.CharField(write_only=True, required=True)


    class Meta:
        model = UserModel
        fields = ['first_name', 'last_name', 'username']


    # ------------------------------
    def validate(self, data):
        validation_error = dict()

        fullname = []
        if (name := data.get('first_name')) and not name.isalpha():
            validation_error["first_name"] = f"First name is not a valid, please use only letters."

        if (last := data.get('last_name')) and not last.isalpha():
            validation_error["last_name"] = f"Last name is not a valid, please use only letters."

        if (user := data.get("username")) and UserModel.objects.filter(username=user).exists():
            validation_error["username"] = "Username already exists"

        
        if validation_error:
            raise_error(validation_error)

        return data

    
    # ------------------------------
    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.save()

        return instance
# endregion


# ----------------------- Update Avatar ------------------------------
# region avatar
class UpdateAvatarSerializer(serializers.Serializer):
    photo = serializers.ImageField(validators=[FileExtensionValidator(allowed_extensions=[
        'jpg', 'jpeg', 'png', 'heic'
    ])])

    def update(self, instance, validated_data):
        photo = validated_data.get('photo')
        if photo:
            instance.avatar = photo
            instance.auth_status = PHOTO
            instance.save()
        return instance
# endregion





   