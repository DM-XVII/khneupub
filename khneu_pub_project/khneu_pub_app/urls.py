from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.custom_login, name='login'),
    path('', views.home, name='home'),
    path('faculty/<slug:slug>', views.get_faculty, name='faculty'),
    path('specialization/<slug:slug>', views.get_specialization, name='specialization'),
    path('article/<slug:slug>', views.get_article, name='article'),
]