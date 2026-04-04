from django.db import models


# Create your models here.

class Cart(models.Model):
    cart_id=models.CharField(max_length=100,blank=True)
    date_added=models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table='Cart'
        ordering=['date_added']

    def __str__(self):
        return self.cart_id



class CartItem(models.Model):
    product=models.ForeignKey('goods.Product',on_delete=models.DO_NOTHING)
    cart=models.ForeignKey(Cart,on_delete=models.DO_NOTHING)
    quantity=models.IntegerField()
    is_active=models.BooleanField(default=True)

    class Meta:
        db_table='CartItem'

    def sub_total(self):
        return self.product.price * self.quantity


    def __str__(self):
        return self.product