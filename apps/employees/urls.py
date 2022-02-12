from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
<<<<<<< HEAD
    path('game_1/', views.game_1),
    path('game_2/', views.game_2),
    path('game_3/', views.game_3),
    path('game_4/', views.game_4),
=======
    path('wordoftheday/', views.wordoftheday, name='wordoftheday'),
>>>>>>> regerogarc
]