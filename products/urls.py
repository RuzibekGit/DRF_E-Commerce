from django.urls import path

from products.views import (ProductCreateAPIView, 
                            ProductUpdateAPIView, 
                            ProductDeleteAPIView,
                            ProductListView)

app_name = 'products'

urlpatterns = [
    path('add/', ProductCreateAPIView.as_view(), name='product-add'),
    path('<int:pk>/update/', ProductUpdateAPIView.as_view(), name='product-update'),
    path('<int:pk>/delete/', ProductDeleteAPIView.as_view(), name='product-delete'),
    path('list/', ProductListView.as_view(), name='product-list'),
    path('<int:pk>/detail/', ProductListView.as_view(), name='product-detail'),


]
