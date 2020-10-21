from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('logout/', views.logout, name='logout'),
    path('accounts/login', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('account/', include('django.contrib.auth.urls')),
    path('user_profile/<username>/', views.user_profile, name='user_profile'),
    path('<post_id>/like', views.like, name='likePost'),
    path('<post_id>/comment', views.post_comment, name='comment'),
    path('search/', views.search_profile, name='search'),
    path('unfollow/<to_unfollow>', views.unfollow, name='unfollow'),
    path('follow/1<to_follow>', views.follow, name='follow'),
    path('profile/<username>/', views.profile, name='profile'),
]

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)