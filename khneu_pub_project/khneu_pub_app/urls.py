from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.custom_login, name='login'),
    path('', views.home, name='home'),
    path('faculty/<slug:slug>', views.get_faculty, name='faculty'),
    path('specialization/<slug:slug>', views.get_specialization, name='specialization'),
    path('article/<slug:slug>', views.get_article, name='article'),
    path('search/>', views.search, name='search'),
    path('create_article/>', views.create_article, name='create_article'),
    path('article/<slug:article_slug>/add_to_favorite/', views.add_to_favorite, name='add_to_favorite'),


#Later
    path('about/', views.get_about, name='about'),
    path('students/', views.get_students, name='students'),
    path('teachers/', views.get_teachers, name='teachers'),
    path('specs/', views.get_specs, name='specs'),
    path('contacts/', views.get_contacts, name='contacts'),
]