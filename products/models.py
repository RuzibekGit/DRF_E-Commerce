from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from shared.models import BaseModel
from users.models import UserModel




# --------------------------------------- Products ----------------------------------------------------------
# region products
class ProductModel(BaseModel):
    name = models.CharField(max_length=255, db_index=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    photos = models.ImageField(upload_to='products', default="products/images.png")
    description = models.TextField()
    quantity = models.IntegerField(default=0)

    discount = models.PositiveSmallIntegerField(default=0, validators=[MaxValueValidator(100), MinValueValidator(0)])
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    author = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='products')


    def __str__(self) -> str:
        return self.name
    
    
    def get_related_products(self):
        return ProductModel.objects.filter(author__in=self.author.all()).exclude(pk=self.pk).distinct()


    class Meta:
        verbose_name = 'product'
        verbose_name_plural = 'products'

# endregion
