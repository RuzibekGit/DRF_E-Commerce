from rest_framework import status
from rest_framework import generics
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated

from shared.pagination import CustomPagination
from users.models import MANAGER, ADMIN, ORDINARY_USER, NEW
from orders.models import OrderModel, OrderItem
from orders.serializers import OrderListSerializer, OrderDetailSerializer, OrderUpdateSerializer




class OrderListView(generics.ListAPIView):
    serializer_class = OrderListSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get(self, request, *args, **kwargs):
        user = self.request.user
        if user.auth_status == NEW: 
            response = {
                "success": False,
                "message": "You do not have permission to access"
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        
        if pk := self.kwargs.get('pk'):
            order = get_object_or_404(OrderModel, pk=pk)
            order_serializer = OrderListSerializer(order)
            order_items = OrderItem.objects.filter(order=order)
            order_items_serializer = OrderDetailSerializer(order_items, many=True)
            response = {
                    **order_serializer.data,
                    "order_items": order_items_serializer.data
                }
            return Response(response, status=status.HTTP_200_OK)
        
        return super().get(request, *args, **kwargs)

    def get_queryset(self):

        # -------------- search filter ---------------------
        queryset = OrderModel.objects.all()
        if q := self.request.GET.get('q'):
            queryset = queryset.filter(user__username__icontains=q)

        return queryset





class OrderStatusUpdateView(generics.UpdateAPIView):
    queryset = OrderModel.objects.all()
    serializer_class = OrderUpdateSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        order = self.get_object()
        if request.user.user_role != ADMIN:
            response = {
                "success": False,
                "message": "You do not have permission to access"
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = self.get_serializer(order, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            response = {
                "success": True,
                "message": "Order status updated successfully",
                "data": serializer.data
            }
            return Response(response, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)