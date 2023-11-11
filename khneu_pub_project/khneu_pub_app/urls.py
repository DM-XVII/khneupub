from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.custom_login, name='login'),
    path('', views.home, name='home'),
    path('faculty/<slug:slug>', views.get_faculty, name='faculty'),
    path('specialization/<slug:slug>', views.get_specialization, name='specialization'),
    path('article/<slug:slug>', views.get_article, name='article'),


#Later
    path('about/', views.get_about, name='about'),
    path('students/', views.get_students, name='students'),
    path('teachers/', views.get_teachers, name='teachers'),
    path('specs/', views.get_specs, name='specs'),
    path('contacts/', views.get_contacts, name='contacts'),
]