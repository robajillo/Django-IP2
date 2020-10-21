from django.db import models
import datetime
from django.utils import timezone
from django.contrib.auth.models import User
from django_currentuser.db.models import CurrentUserField
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid


class Post(models.Model):
   
    image = models.ImageField(upload_to='posts/')
    user = models.ForeignKey('Profile', on_delete = models.CASCADE,default='',related_name='posts')
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

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return f'{self.user.name} Post'


class Profile(models.Model):
    user =models.OneToOneField(User, on_delete=models.CASCADE,related_name='profile')
    profile_picture = models.ImageField(upload_to='images/')
    bio = models.TextField(max_length=500)
    name = models.CharField( max_length=120)
    location = models.CharField(max_length=60)

    def __str__(self):
        return self.bio
    
    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

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
class Comment(models.Model):
    comment = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='comments')
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.comment
    
    def save_comments(self):
        self.save()

    
    def delete_comment(self):
        self.delete()

    @classmethod
    def get_comments(cls, id):
        comment = cls.objects.filter(id=id).all()
        return comment

class Follow(models.Model):
    follower = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='following')
    followed = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='followers')

    def __str__(self):
        return f'{self.follower} Follow'


class Likes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_like')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_likes')

