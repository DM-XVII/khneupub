from django.test import TestCase
from khneu_pub_app.models import *
from django.urls import reverse

class ModelTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(email='testuser@gmail.com', password='testpassword')
        self.faculty = Faculty.objects.create(name='Computer Science', image='images/faculty/123.jpg')
        self.specialization = Specialization.objects.create(
            name='Web Development',
            faculty=self.faculty,
            image='path/to/image.jpg'        
        )
        self.article = Article.objects.create(
            name='Django Testing',
            description='A comprehensive guide to testing in Django',
            image='images/faculty/123.jpg',
            specialization=self.specialization,
            slug='django-testing',
            content='Lorem ipsum dolor sit amet.',
            created_by=self.user,
            upload_date=timezone.now()
        )
        self.favorite = Favorite.objects.create(user=self.user, article=self.article)

    def test_faculty_creation(self):
        self.assertEqual(self.faculty.name, 'Computer Science')
        self.assertIsNotNone(self.faculty.image)
        self.assertEqual(self.faculty.slug,'computer-science')
        self.assertEqual(self.faculty.get_absolute_url(), reverse('faculty', kwargs={'slug': self.faculty.slug}))
        self.assertEqual(self.faculty.__str__(), self.faculty.name)

    def test_faculty_ordering(self):
        faculty2 = Faculty.objects.create(
            name='Database Management',
            image='images/faculty/123.jpg'
        )
        self.assertLess(self.faculty.pk, faculty2.pk)

    def test_specialization_creation(self):
        self.assertEqual(self.specialization.name, 'Web Development')
        self.assertEqual(self.specialization.faculty, self.faculty)
        self.assertEqual(self.specialization.slug,'web-development')
        self.assertIsNotNone(self.specialization.image)
        self.assertEqual(self.specialization.get_absolute_url(), reverse('specialization', kwargs={'slug': self.specialization.slug}))
        self.assertEqual(self.specialization.__str__(), self.specialization.name)

    def test_specialization_ordering(self):
        specialization2 = Specialization.objects.create(
            name='Database Management',
            faculty=self.faculty,
            image='images/faculty/123.jpg'
        )
        self.assertLess(self.specialization.pk, specialization2.pk)
 
    def test_article_creation(self):
        self.assertEqual(self.article.name, 'Django Testing')
        self.assertIsNotNone(self.article.image)
        self.assertEqual(self.article.slug,'django-testing')
        self.assertEqual(self.article.get_absolute_url(), reverse('article', kwargs={'slug': self.article.slug}))
        self.assertEqual(self.article.__str__(), self.article.name)


    def test_favorite_model_creation(self):
        self.assertEqual(self.favorite.article,self.article)
        self.assertEqual(self.favorite.user,self.user)
        self.assertEqual(self.favorite.__str__(), f"favorite article of {self.user.last_name} {self.user.first_name}")

