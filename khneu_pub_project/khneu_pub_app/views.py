from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import login, authenticate,logout
from .forms import CustomUserCreationForm
from .utils import custom_pagination
from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib import messages
from .forms import CustomUserCreationForm,ArticleCreationForm,EditCustomUserForm,EditUserProfileForm
from django.contrib.auth.decorators import login_required
from .models import *

def register(request): #TESTED
    if not request.user.is_authenticated:
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
    else:
        return redirect('home')

def custom_login(request): #TESTED
    if not request.user.is_authenticated:
        if request.method == 'POST':
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Email або пароль містить помилку')
        return render(request, 'khneu_pub_app/login.html')
    else:
        return redirect('home')

@login_required 
def logout_view(request): #TESTED
    if request.method == 'POST':
        logout(request)
        return redirect('login')

    return render(request,'khneu_pub_app/logout.html')

@login_required
def home(request): #TESTED
    faculties = Faculty.objects.all()
    context = {'faculties':faculties}
    return render(request,'khneu_pub_app/home.html',context=context)    
@login_required
def get_faculty(request,slug): #TESTED
    faculty = get_object_or_404(Faculty,slug=slug)
    specializations = Specialization.objects.filter(faculty=faculty)
    context = {'subjects':specializations}
    return render(request,'khneu_pub_app/subjects.html',context=context)
@login_required
def get_specialization(request, slug): #TESTED
    specialization = get_object_or_404(Specialization,slug=slug)
    articles = Article.objects.filter(specialization=specialization).order_by('upload_date')
    page = request.GET.get('page')
    subjects = custom_pagination(page, articles, 2)
    context = {'subjects': subjects}
    return render(request, 'khneu_pub_app/subjects.html', context=context)
@login_required
def get_article(request,slug): #TESTED
    article = get_object_or_404(Article,slug=slug)
    is_favorited = Favorite.objects.filter(user=request.user, article=article).exists()
    context = {'article':article,
               'is_favorited':is_favorited,
               }
    return render(request,'khneu_pub_app/article.html',context=context)

@login_required
def create_article(request): #TESTED
    if request.method == 'POST':
        form = ArticleCreationForm(request.POST, request.FILES)
        
        if form.is_valid():
            form.instance.created_by = request.user
            form.instance.upload_date = timezone.now()
            
            form.save()
            return redirect('home')  
    else:
        form = ArticleCreationForm()
    
    return render(request, 'khneu_pub_app/create_article.html', {'form': form})

@login_required
def update_article(request,slug): #TESTED
    article = get_object_or_404(Article,slug=slug)
    if request.method =='POST':
        form = ArticleCreationForm(request.POST,request.FILES,instance=article)
        if form.is_valid():
            form.save()
            return redirect('article', slug=article.slug)
    else:
        form =ArticleCreationForm(instance=article)
    return render(request,'khneu_pub_app/update_article.html',{'form':form,'article':article})


@login_required
def search(request): #TESTED
    if request.method == 'POST':
        search_query = request.POST['search_query']
        articles = Article.objects.filter(name__icontains = search_query)
        context = {'subjects':articles}
        return render(request,'khneu_pub_app/subjects.html',context = context)
    else:
        return redirect('home')


@login_required
def add_to_favorite(request, article_slug): #TESTED
    article = get_object_or_404(Article, slug=article_slug)

    # Check if the article is already in the user's favorites
    favorite_qs = Favorite.objects.filter(user=request.user, article=article)
    if favorite_qs.exists():

        favorite_qs.delete()
    else:
        favorite = Favorite(user=request.user, article=article)
        favorite.save()

    return redirect('article', slug=article_slug)

@login_required
def delete_article(request, slug): #TESTED
    article = get_object_or_404(Article, slug=slug)

    if request.method == 'POST':
        article.delete()
        return redirect('home')  

    return render(request, 'khneu_pub_app/delete_article.html', {'article': article})


@login_required
def get_students(request):#TESTED
    specializations = Specialization.objects.all()

    if request.method == 'POST':
        specialization_id = request.POST.get('specialization', None)

        if specialization_id:
            students = CustomUser.objects.filter(is_staff=False, specialization_id=specialization_id).order_by('pk')
            
        else:
            students = CustomUser.objects.filter(is_staff=False).order_by('pk')
    else:
        students = CustomUser.objects.filter(is_staff=False).order_by('pk')

    page = request.GET.get('page')
    subjects = custom_pagination(page, students, 1)
    context = {'subjects': subjects, 'specializations': specializations}
    return render(request, 'khneu_pub_app/students_list.html', context=context)


def get_user_profile(request,pk): #TESTED
    student = get_object_or_404(CustomUser,pk=pk)
    profile = UserProfile.objects.get(user=student)
    context = {'student':student,
               'profile':profile}
    return render(request, 'khneu_pub_app/student_profile.html', context=context)


def edit_profile(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)

    if request.method == 'POST':
        user_form = EditCustomUserForm(request.POST, instance=user)
        profile_form = EditUserProfileForm(request.POST, request.FILES, instance=user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('user_profile', pk=user.id)
    else:
        user_form = EditCustomUserForm(instance=user)
        profile_form = EditUserProfileForm(instance=user.profile)

    return render(
        request,
        'khneu_pub_app/edit_profile.html',
        {'user_form': user_form, 'profile_form': profile_form, 'user': user}
    )
def get_user_favorite_list(request, user_pk): #TESTED
    favorites = Favorite.objects.filter(user=user_pk)
    
    articles = [favorite.article for favorite in favorites]
    
    page = request.GET.get('page')
    paginated_articles = custom_pagination(page, articles, 1)
    
    context = {'subjects': paginated_articles}
    
    return render(request, 'khneu_pub_app/subjects.html', context=context)


def get_user_articles_list(request,user_pk): #TESTED
    articles = Article.objects.filter(created_by = user_pk).order_by('pk')

    page = request.GET.get('page')
    paginated_articles = custom_pagination(page, articles, 1)
    context = {'subjects': paginated_articles}
    
    return render(request, 'khneu_pub_app/subjects.html', context=context)

def get_about(request): #TESTED
    return render(request,'khneu_pub_app/about.html')


def get_contacts(request): #TESTED
    return render(request,'khneu_pub_app/contacts.html')

@login_required #TESTED
def get_specs(request):
    specs = Specialization.objects.all()
    context = {'subjects':specs}
    return render(request,'khneu_pub_app/subjects.html',context=context)


