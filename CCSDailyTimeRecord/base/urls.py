from django.urls import path
from . import views
	
urlpatterns = [
	path('', views.home, name="home"),
	path('adminpanel/', views.adminpanel, name="adminpanel"),
	path('draft/', views.draft, name="draft"),
	path('form/', views.form, name="form"),
	path('login2/', views.login2, name="login2"),
	path('myprofile/', views.myprofile, name="myprofile"),
	path('preview/', views.preview, name="preview"),
]