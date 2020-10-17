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
    
