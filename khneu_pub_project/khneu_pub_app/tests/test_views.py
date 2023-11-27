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
    
    def test_add_to_favorite_toggle(self):
        self.client.login(email='testuser@gmail.com',password='testpassword')

        self.assertFalse(Favorite.objects.filter(user=self.user, article=self.article).exists())

        response = self.client.post(reverse('add_to_favorite', args=[self.article.slug]))

        self.assertTrue(Favorite.objects.filter(user=self.user, article=self.article).exists())

        response = self.client.post(reverse('add_to_favorite', args=[self.article.slug]))

        self.assertFalse(Favorite.objects.filter(user=self.user, article=self.article).exists())

    
    def test_add_to_favorite_nonexistent_article(self):
        self.client.login(email='testuser@gmail.com',password='testpassword')
        response = self.client.post(reverse('add_to_favorite', args=['nonexistent-article']))

        self.assertEqual(response.status_code, 404)

    def test_search_post(self):
        self.client.login(email='testuser@gmail.com',password='testpassword')
        response = self.client.post(reverse('search'), {'search_query': 'article'})

        self.assertEqual(response.status_code, 200)
        self.assertIn(self.article, response.context['subjects'])
        self.assertContains(response, 'article')
        self.assertNotContains(response, 'Another Article')

    def test_delete_article_post(self):
        self.client.login(email='testuser@gmail.com',password='testpassword')
        response = self.client.post(reverse('delete_article', args=[self.article.slug]))

        self.assertRedirects(response, reverse('home'))

        self.assertFalse(Article.objects.filter(slug=self.article.slug).exists())

    def test_delete_article_get(self):
        self.client.login(email='testuser@gmail.com',password='testpassword')
        response = self.client.get(reverse('delete_article', args=[self.article.slug]))
        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, 'khneu_pub_app/delete_article.html')

        self.assertEqual(response.context['article'], self.article)
    
    def test_get_students_view(self):
        self.client.login(email='testuser@gmail.com',password='testpassword')
        response = self.client.get(reverse('students'))


        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'khneu_pub_app/students_list.html')
        self.assertIn('specializations', response.context)
        self.assertIn('subjects', response.context)

    def test_post_request_with_specialization(self):
        self.client.login(email='testuser@gmail.com',password='testpassword')
        response = self.client.post(reverse('students'), {'specialization': self.specialization.id})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'khneu_pub_app/students_list.html')
        self.assertIn('specializations', response.context)
        self.assertIn('subjects', response.context)

    def test_post_request_without_specialization(self):
        self.client.login(email='testuser@gmail.com',password='testpassword')
        response = self.client.post(reverse('students'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'khneu_pub_app/students_list.html')
        self.assertIn('specializations', response.context)
        self.assertIn('subjects', response.context)




class GetUserProfileViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='testuser@example.com',
            password='testpassword',
            first_name='Test',
            last_name='User',
        )

        self.user_profile = UserProfile.objects.filter(user=self.user).first()

        if not self.user_profile:
            self.user_profile = UserProfile.objects.create(
                user=self.user,
                photo='images/profile_photo/test_photo.jpg',  
            )
        self.client = Client()
        self.client.login(email='testuser@example.com', password='testpassword')

    def test_get_user_profile_view(self):
        response = self.client.get(reverse('user_profile', args=[self.user.id]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'khneu_pub_app/student_profile.html')

        self.assertIn('student', response.context)

        self.assertIn('profile', response.context)
        self.assertContains(response, self.user.first_name)
        self.assertContains(response, self.user.last_name)

        self.assertContains(response, f'<img src="{self.user_profile.photo.url}"')

    def test_get_user_profile_view_with_invalid_pk(self):
        response = self.client.get(reverse('user_profile', args=[999]))
        self.assertEqual(response.status_code, 404)
  

class GetUserFavoriteListViewTest(TestCase):
    def setUp(self):
        self.faculty = Faculty.objects.create(name ='faculty',image ='media/faculty/123.jpg')
        self.specialization = Specialization.objects.create(name ='specialization',image ='media/faculty/123.jpg',faculty = self.faculty)
        self.user = get_user_model().objects.create_user(
            email='testuser@example.com',
            password='testpassword',
            first_name='Test',
            last_name='User',
        )

        # Create a client and log in the user
        self.client = Client()
        self.client.login(email='testuser@example.com', password='testpassword')

        # Create articles for testing
        self.article1 = Article.objects.create(name='article1',description='desc',image='media/faculty/123.jpg',
                                              specialization=self.specialization,content='article content',
                                              created_by=self.user,upload_date=datetime.datetime.now())  

        # Create favorites for the user
        self.favorite1 = Favorite.objects.create(user=self.user, article=self.article1)

    def test_get_user_favorite_list_view(self):
        # Send a GET request to the view
        response = self.client.get(reverse('user_favorite_list', args=[self.user.id]))

        # Check if the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check if the template used is correct
        self.assertTemplateUsed(response, 'khneu_pub_app/subjects.html')

        # Check if the 'subjects' variable is in the context
        self.assertIn('subjects', response.context)

        # Check if the rendered HTML contains the names of the favorite articles
        self.assertContains(response, self.article1.name)

class GetUserArticlesListViewTest(TestCase):
    def setUp(self):
        self.faculty = Faculty.objects.create(name ='faculty',image ='media/faculty/123.jpg')
        self.specialization = Specialization.objects.create(name ='specialization',image ='media/faculty/123.jpg',faculty = self.faculty)
        self.user = get_user_model().objects.create_user(
            email='testuser@example.com',
            password='testpassword',
            first_name='Test',
            last_name='User',
        )

        # Create a client and log in the user
        self.client = Client()
        self.client.login(email='testuser@example.com', password='testpassword')

        # Create articles for testing
        self.article1 = Article.objects.create(name='article1',description='desc',image='media/faculty/123.jpg',
                                              specialization=self.specialization,content='article content',
                                              created_by=self.user,upload_date=datetime.datetime.now())  

    def test_get_user_articles_list_view(self):
        # Send a GET request to the view
        response = self.client.get(reverse('user_articles_list', args=[self.user.id]))

        # Check if the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check if the template used is correct
        self.assertTemplateUsed(response, 'khneu_pub_app/subjects.html')

        # Check if the 'subjects' variable is in the context
        self.assertIn('subjects', response.context)

        # Check if the rendered HTML contains the names of the user's articles
        self.assertContains(response, self.article1.name)



