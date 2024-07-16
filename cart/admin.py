from django.contrib import admin

from cart.models import CartModel

@admin.register(CartModel)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'quantity', 'created_at']
    list_filter = ['created_at']
