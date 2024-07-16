from django.contrib.auth import authenticate
from django.core.validators import FileExtensionValidator
from django.db.models import Q

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

import re
import dns.resolver

from shared.utils import send_code_to_email
from users.models import UserModel, PHOTO, MANAGER

from products.models import ProductModel
from users.serializers import UserSerializer



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
    author = UserSerializer(read_only=True)

    class Meta:
        model = ProductModel
        fields = ['name', 'price', 'photos', 'description', 'quantity', 'author']

# 
# endregion




# ----------------------- Update Products ------------------------------
# region update
class ProductUpdateSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = ProductModel
        fields = ['name', 'price', 'photos', 'description', 'quantity', 'author']


    # ------------------------------
    def validate(self, attrs):
        user = self.context['request'].user
        if user.user_role != MANAGER:
            raise_error("You don't have permission")
        if self.instance.author != user:
            raise_error("You don't have permission to change this product")


        validation_error = dict()
        # -------- Price ---------
        try:
            attrs['price'] = float(attrs.get('price'))
        except:
            validation_error['price'] = f"Price is not a valid"
        # -------- Quantity ---------
        try:
            attrs['quantity'] = int(attrs.get('quantity'))
        except:
            validation_error['quantity'] = f"Quantity is not a valid"

        if (name := attrs.get('name')) and len(name) < 5:
            validation_error['name'] = f"Name is not a valid"

        if validation_error:
            raise_error(validation_error)

        return attrs
        
    # ------------------------------
    def update(self, instance, validated_data):
    
        instance.name = validated_data.get('name', instance.name)
        instance.price = validated_data.get('price', instance.price)
        instance.photos = validated_data.get('photos', instance.photos)
        instance.description = validated_data.get('description', instance.description)
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.author = self.context['request'].user
        instance.save()
        return instance

# endregion




# ----------------------- Product List ------------------------------
# region product list
class ProductListSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductModel
        fields =  ['id', 'name', 'price', 'photos', 'author']
# endregion


# ----------------------- Product Detail ------------------------------
# region product detail
class ProductDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductModel
        fields =  ['id', 'name', 'price', 'sale_price', 'photos', 'description', 'quantity', 'author']
# endregion


   