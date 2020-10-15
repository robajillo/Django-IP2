from django.db import models

class Post(models.Model):
    image = models.ImageField(blank=true,null=true)
    author = models.ForeignKey('auth.User',on_delete = models.CASCADE)
    caption = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    
