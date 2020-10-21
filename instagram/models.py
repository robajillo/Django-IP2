from django.db import models
import datetime
from django.utils import timezone
from django.contrib.auth.models import User
from django_currentuser.db.models import CurrentUserField
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid


class Profile(models.Model):
    user =models.OneToOneField(User, on_delete=models.CASCADE,related_name='profile')
    profile_picture = models.ImageField(upload_to='images/')
    bio = models.TextField(max_length=500)
    name = models.CharField( max_length=120)
    location = models.CharField(max_length=60)

    
    
    

    def save_image(self):
        self.save()

    def save_profile(self):
        self.save()
        
    def delete_image(self):
        self.delete()
    
    def delete_profile(self):
        self.delete()

    @classmethod
    def search_profile(cls, name):
        return cls.objects.filter(user__username__icontains=name).all()


class Post(models.Model):
   
    image = models.ImageField(upload_to='posts/')
    user = models.ForeignKey(User, on_delete = models.CASCADE,default='',related_name='user_post')
    profile = models.ForeignKey('Profile', on_delete = models.CASCADE,default='',related_name='user_profile')
    caption = models.CharField(max_length=250)
    name = models.CharField(max_length=250, default='')
    created_date = models.DateTimeField(default=timezone.now)
    likes = models.IntegerField(default=0)


    class Meta:
        ordering = ["-pk"]

    def get_absolute_url(self):
        return f"/post/{self.id}"

    @property
    def get_all_comments(self):
        return self.comments.all()

    def save_image(self):
        self.save()
    
    def save_post(self):
        self.save()

    def delete_image(self):
        self.delete()

    
    def __str__(self):
        return self.caption



class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower',default='')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following',default='')

class Likes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_like')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_likes')

class Stream(models.Model):
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='stream_following',default='')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    date = models.DateTimeField()
    
    def add_post(sender,instance,*args,**kwargs):
        post = instance
        user = post.user
        followers = Follow.objects.all().filter(following=user)
        
        for follower in followers:
            stream = Stream(post=post, user=follower.follower, date=post.date, following=user)
            stream.save()

class Comment(models.Model):
    comment = models.TextField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_comment')
    created_date = models.DateTimeField(default=timezone.now)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_comment')
            
post_save.connect(Stream.add_post, sender=Post)
    