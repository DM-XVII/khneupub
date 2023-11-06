from django import forms
from .models import CustomUser,Specialization


class CustomUserCreationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    specialization = forms.ModelChoiceField(queryset=Specialization.objects.all())

    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'specialization',)  

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user