from django.urls import path
from . import views

urlpatterns = [
    path('about/', views.about, name='about'),
    path('login/', views.loginpage, name='login'),
    path('logout/', views.log_out, name='logout'),
    path('registration/', views.registration, name='registration'),
    path('', views.home, name='home'),
    path('room/<str:pk>/', views.room, name='room'),
    path('profile/<str:pk>/', views.user_profile, name='profile'),
    path('create-room/', views.createroom, name='create-room'),
    path('update-room/<str:pk>/', views.updateroom, name='update-room'),
    path('del-room/<str:pk>/', views.delroom, name='del-room'),
]
