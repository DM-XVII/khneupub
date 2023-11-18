from typing import Any
from django import forms
from .models import CustomUser,Specialization,Article


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
