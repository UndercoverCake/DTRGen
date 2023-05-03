from django.urls import path
from . import views
	
urlpatterns = [
	path('', views.home, name="home"),
	path('adminpanel/', views.register, name="adminpanel"),
    path('change-password/<int:user_id>/', views.change_password, name='change-password'),
	path('preview/', views.preview, name="preview"),
    path('undergradPreview/', views.undergradpreview, name="undergradPreview"),
    path('gradPreview/', views.gradpreview, name="gradPreview"),
    path('login/', views.signin, name='login'),
    path('logout/', views.signout, name='logout'),
    path('form/', views.saveTimes, name="saveTimes"),
    path('deactivate-user/<int:user_id>/', views.deactivate_user, name='deactivate-user'),
    path('activate-user/<int:user_id>/', views.activate_user, name='activate-user'),
    path('adminpanel/search', views.searchBar, name='searchBar'),
]