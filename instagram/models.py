from django.db import models
import datetime
from django.utils import timezone

class Post(models.Model):
    image = models.ImageField(blank=True,null=True)
    user = models.ForeignKey('Profile',on_delete = models.CASCADE,related_name='posts')
    caption = models.CharField(max_length=250, blank=True)
    name = models.CharField(max_length=250, blank=True)
    created_date = models.DateTimeField(default=timezone.now)
    likes = models.ManyToManyField(User, related_name='likes', blank=True, )

    def __str__(self):
        return f'{self.user.name} Post'
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_picture = models.ImageField(blank=True,null=True)
    bio = models.TextField(max_length=500, default="My Bio", blank=True)
    name = models.CharField(blank=True, max_length=120)
    location = models.CharField(max_length=60, blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'
