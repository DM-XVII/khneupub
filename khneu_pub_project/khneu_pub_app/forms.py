from typing import Any
from django import forms
from .models import CustomUser,Specialization,Article,UserProfile


class CustomUserCreationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    specialization = forms.ModelChoiceField(queryset=Specialization.objects.all())

    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'specialization',)  
    
    def clean(self) -> dict[str, Any]:
        cleaned_data=super().clean()

        first_name = cleaned_data.get('first_name')
        if any(char.isdigit() for char in first_name):
            self.add_error('first_name','Ім\'я не може містити цифри')

        last_name = cleaned_data.get('last_name')
        if any(char.isdigit() for char in last_name):
            self.add_error('last_name','Прізвище не може містити цифри')

        email = cleaned_data.get('email')
        if CustomUser.objects.filter(email__iexact=email).exists():
            self.add_error('email', 'Цей email вже використовуються')
        

        password = cleaned_data.get('password') 
        if len(password) < 8:
            self.add_error('password','Пароль повинен складатися не менш ніж з 8 символів')
        
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
    
class ArticleCreationForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ('name','description','image','specialization','content')
    
    def clean(self) -> dict[str, Any]:
        cleaned_data=super().clean()
        desc = cleaned_data.get('description')
        if not desc:
            self.errors['description'].clear()
            self.add_error('description','Заповніть будь ласка опис публікації')

        content = cleaned_data.get('content')
        if not content:
            self.errors['content'].clear()
            self.add_error('content','Заповніть будь ласка контент публікації')

        return cleaned_data


class EditCustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name','specialization']

class EditUserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['photo']