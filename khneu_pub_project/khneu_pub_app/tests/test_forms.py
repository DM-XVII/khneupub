from django.test import TestCase
from django.urls import reverse
from khneu_pub_app.forms import CustomUserCreationForm, ArticleCreationForm
from khneu_pub_app.models import Specialization, CustomUser, Article,Faculty
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files import File
class CustomUserCreationFormTest(TestCase):
    def setUp(self):
        self.faculty = Faculty.objects.create(name='Computer Science', image='images/faculty/123.jpg')
        self.specialization = Specialization.objects.create(
            name='Web Development',
            faculty=self.faculty,
            image='images/faculty/123.jpg'        
        )

    def test_valid_form(self):
        data = {
            'email': 'test@example.com',
            'first_name': 'John',
            'last_name': 'Doe',
            'specialization': self.specialization.id,
            'password': 'securepassword',
        }
        form = CustomUserCreationForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_first_name_with_digit(self):
        data = {
            'email': 'test@example.com',
            'first_name': 'John123',
            'last_name': 'Doe',
            'specialization': self.specialization.id,
            'password': 'securepassword',
        }
        form = CustomUserCreationForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('first_name', form.errors)


class ArticleCreationFormTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(email='testuser@gmail.com', password='testpassword')

        self.faculty = Faculty.objects.create(name='Computer Science', image='images/faculty/123.jpg')
        self.specialization = Specialization.objects.create(
            name='Web Development',
            faculty=self.faculty,
            image='images/faculty/123.jpg'        
        )

    def test_valid_form_submission(self):
        self.client.login(email='testuser@gmail.com', password='testpassword')

        valid_data = {
            'name': 'Test Article',
            'description': 'Test Description',
            'image': 'images/faculty/123.jpg',
            'specialization': self.specialization.id,
            'content': 'Test Content',
        }

    
        response = self.client.post(reverse('create_article'), data=valid_data)

        
        self.assertEqual(response.status_code, 302)  

       

    def test_invalid_form_submission(self):
       
        self.client.login(email='testuser@gmail.com', password='testpassword')

      
        invalid_data = {
            'name': 'aff', 
            'description': 'Test Description',
            'image': 'images/faculty/123.jpg',
            'specialization': self.specialization.id,
            'content': '',  
        }

        response = self.client.post(reverse('create_article'), data=invalid_data, follow=True)

        self.assertEqual(response.status_code, 200)  

        if 'form' in response.context:
            form = response.context['form']
            self.assertTrue(form.errors['name'])
            self.assertTrue(form.errors['content'])

class ArticleUpdatingFormTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(email='testuser', password='testpassword')

        self.faculty = Faculty.objects.create(name='Computer Science', image='images/faculty/123.jpg')
        self.specialization = Specialization.objects.create(
            name='Web Development',
            faculty=self.faculty,
            image='images/faculty/123.jpg'        
        )
        self.article =Article.objects.create(
            name='Test Article',
            description= 'Test Description',
            image= 'images/faculty/123.jpg',
            specialization= self.specialization,
            content= 'Test Content',
            created_by =self.user
        )

    def test_valid_form_submission(self):
        self.client.login(email='testuser@gmail.com', password='testpassword')

        valid_data = {
            'name': 'new',
            'description': 'Test Description',
            'image': 'images/faculty/123.jpg',
            'specialization': self.specialization.id,
            'content': 'Test Content',
        }

        response = self.client.post(reverse('update_article', kwargs={'slug': self.article.slug}), data=valid_data)

        self.assertEqual(response.status_code, 302)



    def test_invalid_form_submission(self):
        self.client.login(email='testuser', password='testpassword')

        invalid_data = {
        }

        response = self.client.post(reverse('update_article',kwargs={'slug':self.article.slug}), data=invalid_data, follow=True)

        self.assertEqual(response.status_code, 200)  

      

