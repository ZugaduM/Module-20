from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

"""
Файл маршрутов приложения.

Создан специально для разделения маршрутов проекта и приложения.
Файл маршрутов проекта содержит общие базовые маршруты.
А в каждом создаваемом приложении указываются собственные маршруты.

Таким образом каждый из файлов маршрутов остается легко читаемым и понятным.
"""

urlpatterns = [
    path('', views.main_page, name='main'),
    path('login/', views.user_login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
]