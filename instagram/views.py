from django.shortcuts import render, redirect,get_object_or_404
from . models import *
from django.contrib.auth.decorators import login_required
from .models import Post, Comment, Profile, Follow
from django.contrib.auth.models import User
from .forms import *
from django.contrib.auth import login, authenticate
from django.contrib.auth import logout as django_logout
from django.http import HttpResponseRedirect, JsonResponse,HttpResponse, Http404
from django.conf import settings 
from .email import send_welcome_email
from django.urls import reverse
from django.db import transaction


def login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect(request,'/')
    
    return render(request, '/django_registration/login.html')
        
@login_required
def logout(request):
    django_logout(request)
    return  HttpResponseRedirect('index')

def index(request):
    try:        
        post = Post.objects.all()
        users = User.objects.exclude(id=request.user.id)
        
    except DoesNotExist:
        raise Http404()
    return render(request,'index.html',{'post':post, 'users':users})


@login_required(login_url='login')
def profile(request, username):
    user=get_object_or_404(User,username=username)
    post = Post.objects.filter(user=request.user)
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        prof_form = UpdateUserProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and prof_form.is_valid():
            user_form.save()
            prof_form.save()
            return HttpResponseRedirect(request.path_info)
    else:
        user_form = UpdateUserForm(instance=request.user)
        prof_form = UpdateUserProfileForm(instance=request.user.profile)
    params = {
        'user_form': user_form,
        'prof_form': prof_form,
        'post': post,
        'user':user,

    }
    return render(request, 'profile.html', params)


@login_required(login_url='login')
def search_profile(request):
    if 'search_user' in request.GET and request.GET['search_user']:
        name = request.GET.get("search_user")
        results = Profile.search_profile(name)
        print(results)
        message = f'name'
        params = {
            'results': results,
            'message': message
        }
        return render(request, 'search.html', params)
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

@login_required
def single_post(request,post_id):
    post = get_object_or_404(Post, id=post_id)
    user = request.user
    comments = Comment.objects.filter(post=post).order_by('-created_date')
    
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.user = user
            data.post = post
            data.save()
            return HttpResponseRedirect(reverse('singlePost', args=[post_id]))
            
        else:
            form = CommentForm()
    
    return render(request, 'single_post.html', {'post':post, 'form':CommentForm, 'comments':comments})    

def unfollow(request, to_unfollow):
    if request.method == 'GET':
        user_profile2 = Profile.objects.get(pk=to_unfollow)
        unfollow_d = Follow.objects.filter(follower=request.user.profile, followed=user_profile2)
        unfollow_d.delete()
        return redirect('user_profile', user_profile2.user.username)


@login_required
def follow(request, username):
    user = request.user
    folllowing = get_object_or_404(User, username=username)
    
    try:
        f, created = Follow.objects.get_or_create(follower=user, following=folllowing)
        
        if int(option) == 0:
            f.delete()
            Stream.objects.filter(following=folllowing, user=user).all().delete()
            
        else:
            posts = Post.objects.all().filter(user=folllowing)[:10]
            
            with transaction.atomic():
                for post in posts:
                    stream = Stream(post=post, user=user, date=post.date, following=folllowing)
                    stream.save()
                    
        return HttpResponseRedirect(reverse('profile'))
    except User.DoesNotExist:
        return HttpResponseRedirect(reverse('profile'))      




