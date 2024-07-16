from django.contrib import admin

from products.models import ProductModel


@admin.register(ProductModel)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'quantity', 'created_at']
    search_fields = ['color', 'author']
    list_filter = ['author', 'created_at']
    # inlines = ['']
    readonly_fields = ['sale_price']
