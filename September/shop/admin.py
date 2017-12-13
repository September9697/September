from django.contrib import admin
from .models import Category,Product

class CategoryAdmin(admin.ModelAdmin):
	list_display=['name','slug']
	# 使用 prepopulated_fields 属性来指定那些要使用其他字段来自动赋值的字段
	prepopulated_fields = {'slug': ('name',)}
admin.site.register(Category,CategoryAdmin)

class ProductAdmin(admin.ModelAdmin):
	list_display=['name','slug','price','stock','available','created','updated']
	list_filter=['available','created','updated']
	# list_editable 属性来设置可被编辑的字段，
	# 并且这些字段都在管理站点的列表页被列出。这样可以让你一次编辑多行
	# 任何在 list_editable 的字段也必须在 list_display 中，因为只有这样被展示的字段才可以被编辑。
	list_editable=['price','stock','available']
	prepopulated_fields={'slug':('name',)}
admin.site.register(Product,ProductAdmin)