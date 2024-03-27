from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, get_user
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm, PostForm
from .models import Post

# Create your views here.
@login_required(login_url='/login')
def home(request):
    posts = Post.objects.all()
    
    if request.method == 'POST':
        post_id = request.POST.get('post-id')
        post = Post.objects.filter(id=post_id).first()
        if post and post.author == request.user:
            post.delete()
    
    return render(request, 'main/home.html', context={'posts': posts})

def sign_up(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/home')
    else:
        form = RegistrationForm()
    
    return render(request, 'registration/sign_up.html', context={'form': form})

@login_required(login_url='/login')
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            
            return redirect('/home')
    else:
        form = PostForm()
    
    return render(request, 'main/create_post.html', context={'form': form})