from django.conf.urls import url
from . import views

urlpatterns=[
    url(r'^add/(?P<product_id>\d+)/$',views.cart_add,name='cart_add'),
    url(r'^remove/(?P<product_id>\d+)/$',views.cart_remove,name='cart_remove'),
    url(r'^$',views.cart_detail,name='cart_detail'),
    url(r'^checkout/$',views.checkout,name='checkout'),
    url(r'^change/(?P<product_id>\d+)/$',views.cart_change_num,name='cart_change_num'),
]