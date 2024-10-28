from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('', views.main_page, name='main'),  # Главная страница
    path('login/', views.user_login, name='login'),  # Страница входа
    path('register/', views.register, name='register'),  # Страница регистрации
    path('logout/', LogoutView.as_view(), name='logout'),  # Выход
]