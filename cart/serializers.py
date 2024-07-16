from django.contrib.auth import authenticate
from django.core.validators import FileExtensionValidator
from django.db.models import Q

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

import re
import dns.resolver
from rest_framework import serializers

from shared.utils import send_code_to_email
from users.models import UserModel, PHOTO, MANAGER

from products.models import ProductModel
from users.serializers import UserSerializer
from orders.models import OrderModel, OrderItem

from cart.models import CartModel




# ----------------------- Order Items ------------------------------
# region order items 
class CartItemSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='product.name')
    price = serializers.DecimalField(source='product.price', max_digits=10, decimal_places=2)
    photo = serializers.ImageField(source='product.photos')
    description = serializers.CharField(source='product.description')

    class Meta:
        model = CartModel
        fields = ['id', 'name', 'price', 'photo', 'description', 'quantity']
# endregion




class AddToCartSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField()


class CheckoutSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=20)
    address = serializers.CharField(max_length=255)
