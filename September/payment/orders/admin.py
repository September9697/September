from django.contrib import admin
from .models import Order,OrderItem
from django.http import HttpResponse
from django.core.urlresolvers import reverse
import csv
import datetime

def export_to_csv(modeladmin,request,queryset):
	opts=modeladmin.model._meta
	# 创建一个HttpResponse实例包含一个定制text/csv内容类型来告诉浏览器这个响应需要处理为一个CSV文件
	response=HttpResponse(content_type='text/csv')
	# 添加一个Content-Disposition头来指示这个HTTP响应包含一个附件。
	response['Content-Disposition']='attachment; \ filename={}.csv'.format(opts.verbose_name)
	# 创建一个CSV writer对象，该对象将会被写入response对象。
	writer=csv.writer(response)
	# 使用模型_meta选项的get_fields()方法动态的获取model字段，排除一对多和多对多的关系
	fields=[field for field in opts.get_fields() if not field.many_to_many and not field.one_to_many]
	# 编写一个包含字段名的头行
	writer.writerow([field.verbose_name for field in fields])
	# 迭代查询集，并把查询集返回的每一个对象写入行
	for obj in queryset:
		data_row=[]
		for field in fields:
			value=getattr(obj,field.name)
			# 格式化datetime对象，因为这个给csv的输出值必须是字符串
			if isinstance(value,datetime.datetime):
				value=value.strftime('%d%m%Y')
			data_row.append(value)
		writer.writerow(data_row)
	return response
# 通过给这个函数设置一个short_description属性，定制这个操作在模板上的显示名
export_to_csv.short_description='Export to CSV'

def order_detail(obj):
	return '<a href="{}">View</a>'.format(
        reverse('orders:admin_order_detail', args=[obj.id]))
order_detail.allow_tags=True

class OrderItemInline(admin.TabularInline):
	model=OrderItem
	raw_id_fields=['product']

class OrderAdmin(admin.ModelAdmin):
	list_display=['id','first_name','last_name','email','address','postal_code',
				'city','paid','created','updated','userid','verified',order_detail]
	list_filter=['paid','created','updated']
	inlines=[OrderItemInline]
	actions = [export_to_csv]
admin.site.register(Order,OrderAdmin)


class OrderItemAdmin(admin.ModelAdmin):
	list_display=['id','order','product','commented']
admin.site.register(OrderItem,OrderItemAdmin)