from django.db import models
import datetime
from django.utils import timezone
from django.contrib.auth.models import User

class Post(models.Model):
    image = models.ImageField(upload_to='images/')
    user = models.ForeignKey('Profile', on_delete = models.CASCADE,default='')
    caption = models.CharField(max_length=250)
    name = models.CharField(max_length=250, default='')
    created_date = models.DateTimeField(default=timezone.now)
    likes = models.ManyToManyField(User, related_name='likes' )

    def __str__(self):
        return f'{self.user.name} Post'
    
class Profile(models.Model):
    user =models.CharField(max_length=255)
    profile_picture = models.ImageField(upload_to='images/')
    bio = models.TextField(max_length=500, default="My Bio")
    name = models.CharField( max_length=120)
    location = models.CharField(max_length=60)

    def __str__(self):
        return f'{self.user.username} Profile'

    def save_profile(self):
        self.user

    def delete_profile(self):
        self.delete()

    @classmethod
    def search_profile(cls, name):
        return cls.objects.filter(user__username__icontains=name).all()

class Comment(models.Model):
    comment = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='comments')
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.user.name} Post'

class Follow(models.Model):
    follower = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='following')
    followed = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='followers')

    def __str__(self):
        return f'{self.follower} Follow'