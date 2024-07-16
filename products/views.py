from rest_framework import status
from rest_framework import generics
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.db.models.functions import Lower

from shared.pagination import CustomPagination
from products.models import ProductModel
from users.models import MANAGER, ADMIN, ORDINARY_USER, NEW
from users.views import return_error
from products.permissions import IsOwner
from products.serializers import (ProductAddSerializer,
                                  ProductUpdateSerializer,
                                  ProductListSerializer,
                                  ProductDetailSerializer)





# ----------------------- Product Add ------------------------------
# region product add
class ProductCreateAPIView(generics.CreateAPIView):
    queryset = ProductModel.objects.all()
    serializer_class = ProductAddSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user = request.user
        if user.user_role == MANAGER:  
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            response = {
                'status': True,
                'message': "Successfully new product added",
                'data': serializer.data
            }
            return Response(response, status=status.HTTP_201_CREATED)
        
        else:
            return return_error("You don't have permission")
            
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

# endregion




# ----------------------- Product Update ------------------------------
# region product update
class ProductUpdateAPIView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProductUpdateSerializer
    http_method_names = ['put', 'patch']

    def get_object(self):
        return ProductModel.objects.get(pk=self.kwargs['pk'])

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        custom_response = {
            'status': True,
            'message': "Product updated successfully",
            'data': response.data
        }
        return Response(custom_response, status=status.HTTP_202_ACCEPTED)

    def partial_update(self, request, *args, **kwargs):
        response = super().partial_update(request, *args, **kwargs)
        custom_response = {
            "success": True,
            "message": "Product updated successfully",
            'data': response.data
        }
        return Response(custom_response, status=status.HTTP_202_ACCEPTED)

# endregion




# ----------------------- Product Delete ------------------------------
# region product delete
class ProductDeleteAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        product = get_object_or_404(ProductModel, pk=pk)
        
        if not product:
            return return_error(message="Post does not found", http_request=status.HTTP_404_NOT_FOUND)
        if product.author != request.user:
            return return_error(message="You don't have permission", http_request=status.HTTP_403_FORBIDDEN)
            
        self.check_object_permissions(product.first(), request)
        product.delete()
        response = {
            "status": True,
            "message": "Successfully deleted"
        }
        return Response(response, status=status.HTTP_204_NO_CONTENT)

# endregion




# ----------------------- Product List ------------------------------
# region product list
class ProductListView(generics.ListAPIView):
    serializer_class = ProductListSerializer
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
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        
        if pk := self.kwargs.get('pk'):
            self.serializer_class = ProductDetailSerializer
            self.pagination_class = None
            return ProductModel.objects.filter(id=pk)
        
        # -------------- search filter ---------------------
        queryset = ProductModel.objects.all()
        if q := self.request.GET.get('q'):
            queryset = queryset.filter(name__icontains=q)

        # -------------- filter section --------------------
        if sort := self.request.GET.get('sort'):
            match sort:
                case 'price-lh':   queryset = queryset.order_by('sale_price')
                case 'price-hl':   queryset = queryset.order_by('-sale_price')
                case 'name-AZ':   queryset = queryset.order_by(Lower('name'))
                case 'name-ZA':   queryset = queryset.order_by(Lower('name').desc())

        return queryset
# endregion