from django.contrib import admin
from orders.models import OrderModel, OrderItem



@admin.register(OrderModel)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'status', 'created_at']
    list_filter = ['created_at', 'status']



@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'price']
    search_fields = ['name']