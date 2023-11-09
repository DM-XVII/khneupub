from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import CustomUserCreationForm

from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm

from .models import *
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'khneu_pub_app/register.html', {'form': form})

def custom_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            # Return an 'invalid login' error message.
            pass
    return render(request, 'khneu_pub_app/login.html')



def home(request):
    faculties = Faculty.objects.all()
    context = {'faculties':faculties}
    return render(request,'khneu_pub_app/home.html',context=context)

def specializations(request):
    specializations = Specialization.objects.all()
    context = {'specializations':specializations}
    return render(request,'khneu_pub_app/home.html',context=context)

