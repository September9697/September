from django.db import models
from django.contrib.auth.models import User
from shop.models import Product

class Cart(models.Model):
	user=models.ForeignKey(User,related_name='cart')

	def __str__(self):
		return 'Cart {} of user {}'.format(self.id,self.user.id)

	def get_total_price(self):
		return sum(item.get_price() for item in self.items.all())


class CartItem(models.Model):
	cart=models.ForeignKey(Cart,related_name='items')
	item=models.ForeignKey(Product,related_name='carts')
	item_quantity=models.IntegerField(default=1)

	class Meta:
		ordering=('cart',)

	def __str__(self):
		return 'Product {} in cart {}'.format(self.item.id,self.id)

	def get_price(self):
		return self.item.price*self.item_quantity


