from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import CustomUserCreationForm
from .utils import custom_pagination
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


#--------------------------------------------------------------

def home(request):
    faculties = Faculty.objects.all()
    context = {'faculties':faculties}
    return render(request,'khneu_pub_app/home.html',context=context)    

def get_faculty(request,slug):
    specializations = Specialization.objects.filter(faculty__slug=slug)
    context = {'subjects':specializations}
    return render(request,'khneu_pub_app/subjects.html',context=context)

def get_specialization(request,slug):
    articles = Article.objects.filter(specialization__slug=slug)
    page = request.GET.get('page', 1)
    page_obj = custom_pagination(page,articles,2)
    context = {'subjects':page_obj}
    return render(request,'khneu_pub_app/subjects.html',context=context)

def get_article(request,slug):
    article = Article.objects.get(slug=slug)
    context = {'article':article}
    return render(request,'khneu_pub_app/article.html',context=context)

def search(request):
    if request.method == 'POST':
        search_query = request.POST['search_query']
        articles = Article.objects.filter(name__icontains = search_query)
        context = {'subjects':articles}
        return render(request,'khneu_pub_app/subjects.html',context = context)
    else:
        return redirect('home')



#Later
def get_about(request):
    return render(request,'khneu_pub_app/about.html')
def get_students(request):
    return render(request,'khneu_pub_app/subjects.html')
def get_teachers(request):
    return render(request,'khneu_pub_app/subjects.html')
def get_contacts(request):
    return render(request,'khneu_pub_app/contacts.html')
def get_specs(request):
    specs = Specialization.objects.all()
    context = {'subjects':specs}
    return render(request,'khneu_pub_app/subjects.html',context=context)