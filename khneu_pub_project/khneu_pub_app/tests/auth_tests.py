from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from khneu_pub_app.models import Faculty,Specialization
class AuthenticationTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')

    def test_register_view(self):
        self.faculty = Faculty.objects.create(name ='faculty',image ='media/faculty/123.jpg')
        self.specialization = Specialization.objects.create(name ='specialization',image ='media/faculty/123.jpg',faculty = self.faculty)
        response = self.client.post(self.register_url, {
            'first_name': 'John',
            'last_name': 'Doe',
            'specialization': self.specialization.id,  
            'email': 'john.doe@example.com',
            'password': 'secure_password',
        })
        
        self.assertEqual(response.status_code, 302)  


    def test_login_view(self):
        # Test logging in with valid credentials
        user = get_user_model().objects.create_user(
            email='john.doe@example.com',
            password='secure_password'
        )
        response = self.client.post(self.login_url, {
            'email': 'john.doe@example.com',
            'password': 'secure_password',
        })
        self.assertEqual(response.status_code, 302)  # Expect a redirect
        self.assertRedirects(response, reverse('home'))

        # Check if the user is now authenticated
        self.assertTrue(response.client.session['_auth_user_id'])

    def test_logout_view(self):
        # Test logging out
        user = get_user_model().objects.create_user(
            email='john.doe@example.com',
            password='secure_password'
        )
        self.client.login(email='john.doe@example.com', password='secure_password')
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, 302)  # Expect a redirect
        self.assertRedirects(response, reverse('login'))

        # Check if the user is now logged out
        self.assertFalse(response.client.session.get('_auth_user_id'))

    # Add more test cases as needed
