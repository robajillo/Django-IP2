from django.test import TestCase
from django.contrib.auth.models import User
from .models import *
import datetime as dt

class TestProfile(TestCase):
    def setUp(self):
        self.user = User(username='charles')
        self.user.save()

        self.profile_test = Profile(id=2, name='image', profile_picture='default.jpg', bio='this is a test profile',
                                    user=self.user)

    def test_instance(self):
        self.assertTrue(isinstance(self.profile_test, Profile))

    def test_save_profile(self):
        self.profile_test.save_profile()
        after = Profile.objects.all()
        self.assertTrue(len(after) > 0)

class TestPost(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='testuser', password='12345')
        profile = Profile.objects.create(user=User, name='roba', bio='my bio', location='Kenya')
        self.post_test = Post(image='image.jpg',user=user, caption='this is a caption', name= 'Audi', created_date='2020-10-19 13:14:59+03', likes=8)

    def test_instance(self):
        self.assertTrue(isinstance(self.post_test, Post))

    def test_save_post(self):
        self.post_test.save_image()
        after = Post.objects.all()
        self.assertTrue(len(after) > 0)

    def test_delete_image(self):
        self.post_test.delete_image()
        images = Post.objects.all()
        self.assertTrue(len(images) == 0)

class FollowTestCase(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='testuser', password='12345')
        
        Follow.objects.create(follower=user, following=user)
        
        self.follower = Follow(follower=user)
        
    def test_instance(self):
        self.assertTrue(isinstance(self.follower,Follow))

class LikesTestCase(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='testuser', password='12345')
        profile = Profile.objects.create(user=User, name='roba', bio='my bio', location='Kenya')
        post = Post.objects.create(image='image.jpg',user=user, caption='this is a caption', name= 'Audi', created_date='2020-10-19 13:14:59+03', likes=8)
        
        Likes.objects.create(user=user, post=post)
        
        self.user = Likes(user=user)
        
    def test_instance(self):
        self.assertTrue(isinstance(self.user,Likes))
    