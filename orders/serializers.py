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







# ----------------------- Order List ------------------------------
# region order list


class OrderListSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = OrderModel
        fields = ['id', 'user', 'status', 'order_note', 'first_name']

    def get_user(self, obj):
        return obj.user.first_name

# endregion


# ----------------------- Order Detail ------------------------------
# region order detail
class OrderDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderModel
        fields =   ['id', 'user', 'status', 'order_note',  'first_name', 'last_name', 'email', 'phone']
# endregion


# ----------------------- Order Items ------------------------------
# region order items 
class OrderDetailSerializer(serializers.ModelSerializer):
    order = serializers.SerializerMethodField()
    product = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'product', 'name', 'price', 'photos', 'sale_price']

    def get_order(self, obj):
        return obj.order.first_name
    
    def get_product(self, obj):
        return obj.product.name
# endregion


# ----------------------- Order Update ------------------------------
# region order update
class OrderUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderModel
        fields = ['id', 'status']
# endregion
