from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('<post_id>/like', views.like, name='likePost'),
    path('<post_id>', views.single_post, name='singlePost'),
    path('search/', views.search_profile, name='search'),
    path('profile/<username>/follow/', views.follow, name='follow'),
    path('profile/<username>/', views.profile, name='profile'),
    path('logout/', views.logout, name='logout'),
    path('accounts/login', views.login, name='login'),
]

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)