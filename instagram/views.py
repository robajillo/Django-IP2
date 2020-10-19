from django.shortcuts import render, redirect,get_object_or_404
from . models import *
from django.contrib.auth.decorators import login_required
from .models import Post, Comment, Profile, Follow
from django.contrib.auth.models import User
from .forms import SignUpForm,PostForm,UpdateUserForm, UpdateUserProfileForm, CommentForm
from django.contrib.auth import login, authenticate
from django.http import HttpResponseRedirect, JsonResponse,HttpResponse, Http404
from django.conf import settings 
from .email import send_welcome_email
from django.urls import reverse



def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


def index(request):
    try:        
        post = Post.objects.all()
        users = User.objects.exclude(id=request.user.id)
        
    except DoesNotExist:
        raise Http404()
    return render(request,'index.html',{'post':post, 'users':users})


@login_required(login_url='login')
def profile(request, username):
    images = request.user.profile.posts.all()
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateUserProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return HttpResponseRedirect(request.path_info)
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateUserProfileForm(instance=request.user.profile)
    
    return render(request, 'profile.html')

@login_required(login_url='login')
def user_profile(request, username):
    user_prof = get_object_or_404(User, username=username)
    if request.user == user_prof:
        return redirect('profile', username=request.user.username)
    user_posts = user_prof.profile.posts.all()
    
    followers = Follow.objects.filter(followed=user_prof.profile)
    follow_status = None
    for follower in followers:
        if request.user.profile == follower.follower:
            follow_status = True
        else:
            follow_status = False
    
    return render(request, 'userprofile.html')

@login_required(login_url='login')
def search_profile(request):
    if 'search_user' in request.GET and request.GET['search_user']:
        name = request.GET.get("search_user")
        results = Profile.search_profile(name)
        message = f'name'
        
        return render(request, 'search.html')
    else:
        message = "You haven't searched for any image category"
    return render(request, 'search.html', {'message': message})


@login_required
def like(request,post_id):
    user = request.user
    post = Post.objects.get(id=post_id)
    current_likes = post.likes
    
    liked = Likes.objects.filter(user=user, post=post).count()
    
    if not liked:
        like = Likes.objects.create(user=user,post=post)
        
        current_likes = current_likes + 1
        
    else:
        Likes.objects.filter(user=user,post=post).delete()
        current_likes = current_likes - 1
        
    post.likes = current_likes
    post.save() 
    
    return HttpResponseRedirect(reverse('index'))       

@login_required(login_url='login')
def post_comment(request,image_id):
    current_user=request.user
    post = Post.objects.all()
    profile_user = User.objects.get(username=current_user)
    comments = Comment.objects.all()
    print(comments)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.comment_user = current_user
            comment.save()

            print(comments)


        return redirect('index')
    else:
        form = CommentForm()

    return HttpResponseRedirect(reverse('index'))