"""
URL configuration for auth_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from django.contrib import admin
from authentications.views import (CustomTokenObtainPairView, protected_resource,
                                   OAuth2ProtectedResource, oauth2_callback, CustomTokenView)
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),  # Админ-панель
    path('', include('authentications.urls')),  # Подключение URL-маршрутов из приложения authentications
    # JWT endpoints
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),  # Получение пары JWT токенов
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Обновление JWT токена
    path('api/protected/', protected_resource, name='protected_resource'),  # Защищенный ресурс
    # OAuth2 endpoints
    path('oauth/token/', CustomTokenView.as_view(), name='token'),
    path('oauth/', include('oauth2_provider.urls', namespace='oauth2_provider')),  # URL-маршруты OAuth2 провайдера
    path('callback/', oauth2_callback, name='oauth2_callback'), # Callback URL для OAuth2
    path('api/oauth2-protected/', OAuth2ProtectedResource.as_view(), name='oauth2_protected_resource'),  # Защищенный OAuth2 ресурс
]
