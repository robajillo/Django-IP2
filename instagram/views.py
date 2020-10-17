from django.shortcuts import render, redirect
from . models import Post
from django.contrib.auth.decorators import login_required
from .models import Post, Comment, Profile, Follow
from django.contrib.auth.models import User

