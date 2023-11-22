from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from autoslug import AutoSlugField
from ckeditor.fields import RichTextField
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

class Faculty(models.Model):
    name = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from ='name',unique=True)
    image = models.ImageField(upload_to='images/faculty/')

    def get_absolute_url(self):
        return reverse('faculty',kwargs={'slug':self.slug})

    def __str__(self):
        return self.name
 
class Specialization(models.Model):
    name = models.CharField(max_length=255)
    faculty = models.ForeignKey('Faculty',on_delete=models.CASCADE)
    slug = AutoSlugField(populate_from ='name',unique=True)
    image = models.ImageField(upload_to='images/specialization/')

    def get_absolute_url(self):
        return reverse('specialization',kwargs={'slug':self.slug})


    def __str__(self):
        return self.name 
    
class Article(models.Model):
    name = models.CharField(max_length=255)
    description = RichTextField(config_name ='description_ckeditor')
    image = models.ImageField(upload_to='images/article/')
    specialization = models.ForeignKey('Specialization',on_delete=models.CASCADE)
    slug = AutoSlugField(populate_from ='name',unique=True)
    content = RichTextField(config_name = 'content_ckeditor')
    created_by = models.ForeignKey('CustomUser',on_delete=models.CASCADE)
    upload_date = models.DateTimeField()

    def get_absolute_url(self):
        return reverse('article',kwargs={'slug':self.slug})

    def __str__(self):
        return self.name 
    
class Favorite(models.Model):
    user = models.ForeignKey('CustomUser',on_delete=models.CASCADE)
    article = models.ForeignKey('Article',on_delete=models.CASCADE)

    def __str__(self):
        return f"favorite article of {self.user.last_name} {self.user.first_name}"





#Custom registration
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30,default='')
    last_name = models.CharField(max_length=30,default='')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    specialization = models.ForeignKey(Specialization, on_delete=models.CASCADE, null=True, blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    def get_absolute_url(self):
        return reverse('user_profile',kwargs={'pk':self.pk})

class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser,on_delete=models.CASCADE,related_name='profile')
    photo = models.ImageField(upload_to='images/profile_photo', default='images/profile_photo/default_photo.png')

    def __str__(self):
        return f"profile of {self.user.last_name} {self.user.first_name}"
