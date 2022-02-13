from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('register/', views.register_view, name='register'),
    path('employees/', include('apps.employees.urls')),
]
