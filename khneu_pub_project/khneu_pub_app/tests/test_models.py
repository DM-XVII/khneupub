from django.test import TestCase
from khneu_pub_app.models import *
from django.urls import reverse

class FacultyModelTest(TestCase):
    def setUp(self):
        self.faculty = Faculty.objects.create(name='Computer Science', image='images/faculty/123.jpg')

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

class SpecializationModelTest(TestCase):
    def setUp(self):
        self.faculty = Faculty.objects.create(name='Computer Science', image='path/to/image.jpg')
        self.specialization = Specialization.objects.create(
            name='Web Development',
            faculty=self.faculty,
            image='path/to/image.jpg'        
        )
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


