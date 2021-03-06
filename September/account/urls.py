from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views
urlpatterns = [
	url(r'^login/$',views.user_login,name='login'), 
	url(r'^profile/$',views.profile_view,name='profile_view'),
	url(r'^logout/$',views.user_logout,name='logout'),
	url(r'^register/$',views.RegisterView.as_view(),name='register'),
	url(r'^changeprofile/$',views.ChangeProfile,name='changeprofile'),
]
