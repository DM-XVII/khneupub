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

    # Add more test cases for other validation rules...

class ArticleCreationFormTests(TestCase):
    def setUp(self):
        # Create a user for testing purposes
        self.user = CustomUser.objects.create(email='testuser@gmail.com', password='testpassword')

        self.faculty = Faculty.objects.create(name='Computer Science', image='images/faculty/123.jpg')
        self.specialization = Specialization.objects.create(
            name='Web Development',
            faculty=self.faculty,
            image='images/faculty/123.jpg'        
        )

    def test_valid_form_submission(self):
        # Log in the user
        self.client.login(email='testuser@gmail.com', password='testpassword')

        # Prepare data for a valid form submission
        valid_data = {
            'name': 'Test Article',
            'description': 'Test Description',
            'image': 'images/faculty/123.jpg',
            'specialization': self.specialization.id,
            'content': 'Test Content',
        }

        # Submit the form
        response = self.client.post(reverse('create_article'), data=valid_data)

        # Check that the form submission was successful
        self.assertEqual(response.status_code, 302)  # 302 indicates a successful form submission

        # Check that the article was created in the databas

    def test_invalid_form_submission(self):
        # Log in the user
        self.client.login(email='testuser@gmail.com', password='testpassword')

        # Prepare data for an invalid form submission (missing required fields)
        invalid_data = {
            'name': 'aff',  # Missing required field
            'description': 'Test Description',
            'image': 'images/faculty/123.jpg',
            'specialization': self.specialization.id,
            'content': '',  # Missing required field
        }

        # Submit the form and follow the redirect
        response = self.client.post(reverse('create_article'), data=invalid_data, follow=True)

        # Check that the form submission failed
        self.assertEqual(response.status_code, 200)  # 200 indicates a failed form submission

        # Check that the form has errors for the missing fields
        if 'form' in response.context:
            form = response.context['form']
            self.assertTrue(form.errors['name'])
            self.assertTrue(form.errors['content'])

class ArticleUpdatingFormTests(TestCase):
    def setUp(self):
        # Create a user for testing purposes
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
        # Log in the user
        self.client.login(email='testuser@gmail.com', password='testpassword')

        valid_data = {
            'name': 'new',
            'description': 'Test Description',
            'image': 'images/faculty/123.jpg',
            'specialization': self.specialization.id,
            'content': 'Test Content',
        }

        # Submit the form
        response = self.client.post(reverse('update_article', kwargs={'slug': self.article.slug}), data=valid_data)

        # Check if the form submission was successful
        self.assertEqual(response.status_code, 302)

        # Check if the article name has been updated correctly


    def test_invalid_form_submission(self):
        # Log in the user
        self.client.login(email='testuser', password='testpassword')

        # Prepare data for an invalid form submission (missing required fields)
        invalid_data = {
        }

        # Submit the form and follow the redirect
        response = self.client.post(reverse('update_article',kwargs={'slug':self.article.slug}), data=invalid_data, follow=True)

        # Check that the form submission failed
        self.assertEqual(response.status_code, 200)  # 200 indicates a failed form submission


      

