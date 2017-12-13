from django.db import models
from django.contrib.auth.models import User
from shop.models import Product
from django.utils import timezone

class Comment(models.Model):
	user=models.ForeignKey(User,related_name='comments')
	product=models.ForeignKey(Product,related_name='comments')
	body=models.TextField()
	publish=models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering=('publish',)

	def __str__(self):
		return 'Comment by {} on {}'.format(self.user.username,self.product.name)

