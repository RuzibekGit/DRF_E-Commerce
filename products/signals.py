from django.db.models import Avg
from django.db.models.signals import pre_save
from django.dispatch import receiver

from products.models import ProductModel

# ----------------------------------- Sale Price -------------------------------------------
@receiver(pre_save, sender=ProductModel)
def product_update_price( instance, **kwargs):
    # For calculate sale price
    price, disc = instance.price, instance.discount
    instance.sale_price = price - (disc * price / 100) if disc else price
    



    
