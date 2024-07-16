from django.db import models

from shared.models import BaseModel
from users.models import UserModel
from products.models import ProductModel


class CartModel(BaseModel):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name="product_cart")
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE, related_name="cart")
    quantity = models.IntegerField(default=1)

    def get_related_products(self):
        return CartModel.objects.filter(user__in=self.user.all()).exclude(pk=self.pk).distinct()
    
    def __str__(self) -> str:
        return self.user.first_name

    class Meta:
        verbose_name = 'Cart'
        verbose_name_plural = 'Carts'