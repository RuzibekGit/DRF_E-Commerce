from rest_framework.views import APIView
from rest_framework import status
from rest_framework import generics
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated

from shared.pagination import CustomPagination
from cart.serializers import  CartItemSerializer, AddToCartSerializer, CheckoutSerializer
from cart.models import CartModel
from products.models import ProductModel
from orders.models import OrderItem, OrderModel

# ----------------------- Product List ------------------------------
# region product list

class CartListView(generics.ListAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        user = self.request.user
        return CartModel.objects.filter(user=user)

# endregion


class AddToCartView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = AddToCartSerializer(data=request.data)
        if serializer.is_valid():
            product = get_object_or_404(ProductModel, id=serializer.validated_data['product_id'])
            cart_item, created = CartModel.objects.get_or_create(
                user=request.user, product=product)
            cart_item.quantity += serializer.validated_data['quantity']
            cart_item.save()
            return Response({"success": True, "message": "Product added to cart"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class IncreaseCartItemView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        cart_item = get_object_or_404(CartModel, pk=pk, user=request.user)
        cart_item.quantity += 1
        cart_item.save()
        return Response({"success": True, "message": "Product quantity increased"}, status=status.HTTP_200_OK)


class DecreaseCartItemView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        cart_item = get_object_or_404(CartModel, pk=pk, user=request.user)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
            return Response({"success": True, "message": "Product quantity decreased"}, status=status.HTTP_200_OK)
        return Response({"success": False, "message": "Quantity cannot be less than 1"}, status=status.HTTP_400_BAD_REQUEST)


class RemoveCartItemView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        cart_item = get_object_or_404(CartModel, pk=pk, user=request.user)
        cart_item.delete()
        return Response({"success": True, "message": "Product removed from cart"}, status=status.HTTP_200_OK)


class CheckoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        serializer = CheckoutSerializer(data=request.data)
        if serializer.is_valid():
            cart_items = CartModel.objects.filter(user=request.user, id=pk)
            if not cart_items.exists():
                return Response({"success": False, "message": "Cart not found"}, status=status.HTTP_404_NOT_FOUND)

            order = OrderModel.objects.create(
                user=request.user,
                status='NEW',
                order_note='',
                first_name=request.user.first_name,
                last_name=request.user.last_name,
                email=request.user.email,
                phone=serializer.validated_data['phone_number']
            )

            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    name=item.product.name,
                    price=item.product.price,
                    photos=item.product.photos,
                    sale_price=item.product.sale_price
                )
                item.delete()

            return Response({"success": True, "message": "Order created successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
