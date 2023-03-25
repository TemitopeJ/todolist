from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('manage', views.manage, name='manage'),
    path('logout', views.logout, name='logout'),
    path('delete/<str:num>', views.delete, name='delete')
]