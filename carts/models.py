from django.db import models
from store.models import variation
from accounts.models import Account
# Create your models here.
class cart(models.Model):
    cart_id = models.CharField(max_length=250,blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.cart_id

from store.models import product


class cart_item(models.Model):
    user = models.ForeignKey(Account,on_delete=models.CASCADE ,null=True )
    product = models.ForeignKey(product,on_delete=models.CASCADE)
    variation = models.ManyToManyField(variation,blank=True)
    cart = models.ForeignKey(cart,on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def subtotal(self):
        return self.product.price*self.quantity

    def __unicode__(self):
        return self.product