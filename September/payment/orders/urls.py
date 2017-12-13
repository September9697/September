from django.conf.urls import url
from . import views

urlpatterns=[
	url(r'^create/$',views.order_create,name='order_create'),
	url(r'^admin/order/(?P<order_id>\d+)/$',views.admin_order_detail,name='admin_order_detail'),
	url(r'^orderlist/$',views.order_list,name='order_list'),
	url(r'^(?P<id>\d+)/$',views.order_detail,name='order_detail'),
	url(r'^verify/(?P<order_id>\d+)/$',views.VerifyOrder,name='verify'),
]