from django.test import SimpleTestCase
from django.urls import reverse,resolve
from khneu_pub_app.views import *
class TestUrls(SimpleTestCase):

    def test_home_url_resolves(self):
        url = reverse('home')
        self.assertEquals(resolve(url).func,home)

    def test_register_url_resolves(self):
        url = reverse('register')
        self.assertEquals(resolve(url).func,register)
    
    def test_login_url_resolves(self):
        url = reverse('login')
        self.assertEquals(resolve(url).func,custom_login)
    
    def test_logout_url_resolves(self):
        url = reverse('logout')
        self.assertEquals(resolve(url).func,logout_view)
    
    def test_faculty_url_resolves(self):
        url = reverse('faculty',args=['some-slug'])
        self.assertEquals(resolve(url).func,get_faculty)
    
    def test_specialization_url_resolves(self):
        url = reverse('specialization',args=['some-slug'])
        self.assertEquals(resolve(url).func,get_specialization)
    
    def test_article_url_resolves(self):
        url = reverse('article',args=['some-slug'])
        self.assertEquals(resolve(url).func,get_article)
    
    def test_search_url_resolves(self):
        url = reverse('search')
        self.assertEquals(resolve(url).func,search)
    
    def test_create_article_url_resolves(self):
        url = reverse('create_article')
        self.assertEquals(resolve(url).func,create_article)
    
    def test_add_to_favorite_url_resolves(self):
        url = reverse('add_to_favorite',args=['some-slug'])
        self.assertEquals(resolve(url).func,add_to_favorite)
    
    def test_update_article_url_resolves(self):
        url = reverse('update_article',args=['some-slug'])
        self.assertEquals(resolve(url).func,update_article)
    
    def test_delete_article_url_resolves(self):
        url = reverse('delete_article',args=['some-slug'])
        self.assertEquals(resolve(url).func,delete_article)
    

    def test_user_profle_url_resolves(self):
        url = reverse('user_profile',args=[1])
        self.assertEquals(resolve(url).func,get_user_profile)
    
    def test_user_favorite_list_url_resolves(self):
        url = reverse('user_favorite_list',args=[1])
        self.assertEquals(resolve(url).func,get_user_favorite_list)
    
    def test_user_articles_list_url_resolves(self):
        url = reverse('user_articles_list',args=[1])
        self.assertEquals(resolve(url).func,get_user_articles_list)
    
    def test_about_url_resolves(self):
        url = reverse('about')
        self.assertEquals(resolve(url).func,get_about)
    
    def test_students_url_resolves(self):
        url = reverse('students')
        self.assertEquals(resolve(url).func,get_students)
    
    def test_specialization_list_url_resolves(self):
        url = reverse('specs')
        self.assertEquals(resolve(url).func,get_specs)
    
    def test_contacts_url_resolves(self):
        url = reverse('contacts')
        self.assertEquals(resolve(url).func,get_contacts)
    

    


    
    


    
    
    
    
    