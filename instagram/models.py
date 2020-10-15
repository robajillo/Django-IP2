from django.db import models
import datetime

class Post(models.Model):
    image = models.ImageField(blank=True,null=True)
    author = models.ForeignKey('auth.User',on_delete = models.CASCADE)
    caption = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    
