from django.contrib import admin
from .models import Cart,CartItem

admin.site.register(Cart)


class CartItemAdmin(admin.ModelAdmin):
	list_display=['id','item','cart']
admin.site.register(CartItem,CartItemAdmin)
