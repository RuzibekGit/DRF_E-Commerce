from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated

from products.serializers import ProductAddSerializer


class ProductCreateAPIView(generics.CreateAPIView):
    serializer_class = ProductAddSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
