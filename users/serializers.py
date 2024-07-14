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

# ----------------------- SignUp ------------------------------
# region sign up
class SignUpSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(write_only=True, required=True)
    last_name = serializers.CharField(write_only=True, required=True)
    username = serializers.CharField(write_only=True, required=True)
    email = serializers.CharField(write_only=True, required=True)
    password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)

    uuid = serializers.IntegerField(read_only=True)
    auth_status = serializers.CharField(read_only=True, required=False)

    validation_error = dict()

    class Meta:
        model = UserModel
        fields = ['first_name', 'last_name', 'username','email', 'password', 'confirm_password','uuid', 'auth_status']


    # ------------------------------
    def create(self, validated_data):
        user = super(SignUpSerializer, self).create(validated_data)
        code = user.create_verify_code()

        send_code_to_email(user.email, code, name=user.first_name)
      
        user.save()
        return user
    
    # ------------------------------
    def validate(self, data):
        name      = data['first_name']
        last_name = data['last_name']    
        password  = data['password']
        confirm_password = data.get('confirm_password')

        if password != confirm_password:
            self.validation_error['password'] = "Passwords don't match"

        for check in [["First name", name, 'first_name'], ["Last name", last_name, 'last_name']]:
            if not check[1].isalpha():
                self.validation_error[check[2]] = f"{check[0]} is not a valid, please use only letters."
        
        if self.validation_error:
            raise_error(self.validation_error)
        
        data.pop('confirm_password')
        return data

    # ------------------------------
    def validate_username(self, username):
        self.validation_error = dict()

        if UserModel.objects.filter(username=username).exists():
            self.validation_error['username'] =  "Username already exists"
        return username

    
    # ------------------------------
    def validate_email(self, email):
        email = str(email).lower()
    
        if UserModel.objects.filter(email=email).exists():
            self.validation_error['email'] = 'Email already exists.'
            return email

        if not is_valid_email(email):
            self.validation_error['email'] = 'Please enter a valid email address.'
            return email

        try:
            mx_record = dns.resolver.query(email.split('@')[-1], 'MX')
            # TODO: write function to for mx_record
            
        except dns.resolver.NXDOMAIN:
            self.validation_error['email'] = "Please enter a valid email address."
        
        return email
    
    
    
    # ------------------------------
    def to_representation(self, instance):
        data = {
            'status': True,
            'message': "Successfully registered, code sent to you email. ",
            'access_token': instance.token()['access_token'],
            'auth_status': instance.auth_status
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





   