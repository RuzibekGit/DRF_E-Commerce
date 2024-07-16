from django.urls import path
from orders.views import OrderListView, OrderStatusUpdateView



app_name = 'orders'

urlpatterns = [
    path('', OrderListView.as_view(), name='order-list'),
    path('<int:pk>/detail/', OrderListView.as_view(), name='order-detail'),
    path('<int:pk>/update-status/', OrderStatusUpdateView.as_view(), name='order-status-update'),
    

]
