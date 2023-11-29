from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.custom_login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('faculty/<slug:slug>', views.get_faculty, name='faculty'),
    path('specialization/<slug:slug>', views.get_specialization, name='specialization'),
    path('article/<slug:slug>', views.get_article, name='article'),
    path('search/', views.search, name='search'),
    path('create_article/', views.create_article, name='create_article'),
    path('article/<slug:article_slug>/add_to_favorite/', views.add_to_favorite, name='add_to_favorite'),
    path('update_article/<slug:slug>/',views.update_article, name='update_article'),
    path('delete_article/<slug:slug>/', views.delete_article, name='delete_article'),
    path('user_profile/<int:pk>/', views.get_user_profile, name='user_profile'),
    path('edit_profile/<int:user_id>/', views.edit_profile, name='edit_profile'),
    path('user_favorite_list/<int:user_pk>/', views.get_user_favorite_list, name='user_favorite_list'),
    path('user_articles_list/<int:user_pk>/', views.get_user_articles_list, name='user_articles_list'),
    path('about/', views.get_about, name='about'),
    path('students/', views.get_students, name='students'),
    path('specs/', views.get_specs, name='specs'),
    #Later
    path('contacts/', views.get_contacts, name='contacts'),
]