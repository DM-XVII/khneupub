import datetime
from django.test import TestCase,Client
from django.urls import reverse
from khneu_pub_app.models import *

class TestHomeView(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(email='testuser@gmail.com', password='testpassword')
        self.client = Client()
        self.url = reverse('home')
        
    def test_home_view_authenticated_user(self):
        self.faculty = Faculty.objects.create(name ='faculty',image ='media/faculty/123.jpg')
        
        self.img_url = self.faculty.image.url
        
        self.client.login(email ='testuser@gmail.com',password='testpassword')
        response = self.client.get(self.url)

        self.assertEqual(response.status_code,200) # success
        self.assertTemplateUsed(response,'khneu_pub_app/home.html') # correct template
        self.assertIn('faculties',response.context) # context is passed
        self.assertContains(response,f'src="{self.img_url}"') # img is rendered
        self.assertContains(response,self.faculty.name) # name is rendered

    def test_home_view_empty_queryset(self):
        self.client.login(email ='testuser@gmail.com',password='testpassword')
        response = self.client.get(self.url)

        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'khneu_pub_app/home.html')
        self.assertIn('faculties',response.context)

    def test_home_view_unauthenticated_user(self):
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code,302)
        self.assertRedirects(response,'/login/?next='+self.url)     


class TestGetFacultySpecializationArticle(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(email='testuser@gmail.com', password='testpassword')
        self.faculty = Faculty.objects.create(name ='faculty',image ='media/faculty/123.jpg')
        self.specialization = Specialization.objects.create(name ='specialization',image ='media/faculty/123.jpg',faculty = self.faculty)
        self.client = Client()
        self.faculty_url = reverse('faculty',kwargs={'slug':self.faculty.slug})
        self.specialization_url=reverse('specialization',kwargs={'slug':self.specialization.slug})
        self.article = Article.objects.create(name='article',description='desc',image='media/faculty/123.jpg',
                                              specialization=self.specialization,content='article content',
                                              created_by=self.user,upload_date=datetime.datetime.now())  
        self.article_url = reverse('article',kwargs={'slug':self.article.slug})
        
    def test_get_faculty_page_unauthenticated_user(self):
        response = self.client.get(self.faculty_url)

        self.assertEqual(response.status_code,302)
        self.assertRedirects(response,'/login/?next='+self.faculty_url)

    def test_faculty_page_authenticated_user(self):
        
        self.img_url = self.specialization.image.url
        self.client.login(email='testuser@gmail.com',password='testpassword')
        response = self.client.get(self.faculty_url)

        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'khneu_pub_app/subjects.html')
        self.assertIn('subjects',response.context) # context is passed
        self.assertContains(response,f'src="{self.img_url}"') # img is rendered
        self.assertContains(response,self.specialization.name) # name is rendered
    
    def test_faculty_page_with_invalid_slug(self):
        self.client.login(email='testuser@gmail.com',password='testpassword')
        response = self.client.get(reverse('faculty', kwargs={'slug': 'invalid-slug'}))

        self.assertEqual(response.status_code,404)

    def test_get_specialization_page_unauthenticated_user(self):
        response = self.client.get(self.specialization_url)

        self.assertEqual(response.status_code,302)
        self.assertRedirects(response,'/login/?next='+self.specialization_url)

    def test_specialization_page_authenticated_user(self):
         
        self.img_url = self.specialization.image.url
        self.client.login(email='testuser@gmail.com',password='testpassword')
        response = self.client.get(self.specialization_url)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'khneu_pub_app/subjects.html')
        self.assertIn('subjects',response.context) # context is passed

        self.assertContains(response,f'src="{self.img_url}"') # img is rendered
        self.assertContains(response,self.article.name) # name is rendered
    
    def test_specialization_page_with_invalid_slug(self):
        self.client.login(email='testuser@gmail.com',password='testpassword')
        response = self.client.get(reverse('specialization', kwargs={'slug': 'invalid-slug'}))

        self.assertEqual(response.status_code,404)


    def test_get_article_unauthenticated_user(self):
        response = self.client.get(self.article_url)

        self.assertEqual(response.status_code,302)
        self.assertRedirects(response,'/login/?next='+self.article_url)

    def test_get_article_authenticated_user(self):
        self.client.login(email='testuser@gmail.com',password='testpassword')
        response = self.client.get(self.article_url)

        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'khneu_pub_app/article.html')
        self.assertIn('article',response.context) 
        self.assertIn('is_favorited',response.context) 
        self.assertContains(response,f'src="{self.article.image.url}"') # img is rendered
        self.assertContains(response,self.article.content) # name is rendered
    
    def test_get_article_invalid_slug(self):
        self.client.login(email='testuser@gmail.com',password='testpassword')
        response = self.client.get(reverse('article',kwargs={'slug':'wrong-slug'}))
        self.assertEqual(response.status_code,404)

        

  

