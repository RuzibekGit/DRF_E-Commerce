from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from shared.models import BaseModel
from users.models import UserModel
from products.models import ProductModel

NEW, IN_THE_WAY, DELIVERED, CANCELED = "NEW", "IN_THE_WAY", "DELIVERED", "CANCELED"



class OrderModel(BaseModel):
    STATUES = (
        (NEW, NEW),
        (IN_THE_WAY, IN_THE_WAY),
        (DELIVERED, DELIVERED),
        (CANCELED, CANCELED)
    )

    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(max_length=128, choices=STATUES, default=NEW)
    order_note = models.CharField(max_length=600, null=True)

    first_name  = models.CharField(max_length=20, null=True, blank=True)
    last_name   = models.CharField(max_length=20, null=True, blank=True)
    email       = models.EmailField(null=True)
    phone       = models.CharField(max_length=50, null=True, blank=True)




    def __str__(self):
        return self.first_name
    

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'


class OrderItem(models.Model):
    order = models.ForeignKey(OrderModel, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(ProductModel, on_delete=models.SET_NULL, related_name='orders', null=True,)

    name = models.CharField(max_length=255, db_index=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    photos = models.ImageField(upload_to='products', default="products/images.png")

    sale_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    def get_related_products(self):
        return ProductModel.objects.filter(order__in=self.order.all()).exclude(pk=self.pk).distinct()

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'Order Item'
        verbose_name_plural = 'Order Items'