from django.conf.urls import url
from . import views

urlpatterns=[
	url(r'^create/(?P<item_id>\d+)/$',views.create_comment,name='create'),
]