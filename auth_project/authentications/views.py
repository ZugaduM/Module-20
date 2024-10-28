import base64

from django.shortcuts import render, redirect # Импорт функций для рендеринга страниц и перенаправления
from django.contrib.auth import login, authenticate # Импорт функций для аутентификации пользователей
from django.contrib import messages # Импорт для работы с сообщениями пользователю
from django.views.decorators.http import require_http_methods # Импорт декоратора для ограничения HTTP методов
from django.contrib.auth.models import User # Импорт модели пользователя Django
from django.http import JsonResponse # Импорт для JSON ответов
from rest_framework_simplejwt.views import TokenObtainPairView # Импорт базового класса для работы с JWT токенами
from rest_framework_simplejwt.authentication import JWTAuthentication # Импорт класса аутентификации JWT
from rest_framework.decorators import api_view, permission_classes # Импорт декораторов REST framework
from rest_framework.permissions import IsAuthenticated # Импорт класса разрешений для аутентифицированных пользователей
from rest_framework.response import Response # Импорт класса ответа REST framework
from oauth2_provider.views.generic import ProtectedResourceView # Импорт базового класса для OAuth2 защищенных ресурсов
from oauth2_provider.contrib.rest_framework import OAuth2Authentication # Импорт класса аутентификации OAuth2
from oauth2_provider.views import TokenView  # Базовый класс для создания токенов
from oauth2_provider.models import AccessToken, Application  # Модели для токенов и приложений OAuth2
from rest_framework.decorators import authentication_classes # Импорт декоратора для указания классов аутентификации
from .models import UserProfile # Импорт модели профиля пользователя


def main_page(request):
    # Отображение главной страницы приложения
    return render(request, 'mainpage.html')


def user_login(request):
    # Получение имени пользователя из POST запроса
    username = request.POST['username']
    # Получение пароля из POST запроса
    password = request.POST['password']
    # Получение метода аутентификации из POST запроса
    auth_method = request.POST['auth_method']

    # Проверка учетных данных пользователя
    user = authenticate(username=username, password=password)
    if user is not None:
        try:
            # Получение профиля пользователя из базы данных
            profile = UserProfile.objects.get(user=user)
            # Проверка соответствия метода аутентификации
            if profile.auth_method != auth_method:
                messages.error(request, f'This account uses {profile.auth_method} authentication method')
                return redirect('main')
        except UserProfile.DoesNotExist:
            # Обработка отсутствия профиля
            messages.error(request, 'User profile not found')
            return redirect('main')

        # Выполнение входа пользователя в систему
        login(request, user)
        # Отправка сообщения об успешном входе
        messages.success(request, f'Successfully logged in using {auth_method}')
    else:
        # Отправка сообщения о неверных учетных данных
        messages.error(request, 'Invalid credentials')

    # Перенаправление на главную страницу
    return redirect('main')


@require_http_methods(["POST"])
def register(request):
    # Получение данных регистрации из POST запроса
    username = request.POST['username']
    email = request.POST['email']
    password1 = request.POST['password1']
    password2 = request.POST['password2']
    auth_method = request.POST['auth_method']

    # Проверка совпадения паролей
    if password1 != password2:
        messages.error(request, 'Passwords do not match')
        return redirect('main')

    # Проверка существования пользователя с таким именем
    if User.objects.filter(username=username).exists():
        messages.error(request, 'Username already exists')
        return redirect('main')

    try:
        # Создание нового пользователя
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1
        )

        # Создание профиля пользователя
        UserProfile.objects.create(
            user=user,
            auth_method=auth_method
        )

        # Автоматический вход после регистрации
        login(request, user)
        # Отправка сообщения об успешной регистрации
        messages.success(request, 'Registration successful!')
        return redirect('main')

    except Exception as e:
        # Обработка ошибок при регистрации
        messages.error(request, f'Registration failed: {str(e)}')
        return redirect('main')


class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            # Получаем пользователя из запроса
            username = request.data.get('username')
            user = User.objects.get(username=username)

            try:
                profile = UserProfile.objects.get(user=user)
                if profile.auth_method != 'jwt':
                    return Response({'error': 'This account uses different authentication method'}, status=400)
            except UserProfile.DoesNotExist:
                return Response({'error': 'User profile not found'}, status=400)
        return response


class OAuth2ProtectedResource(ProtectedResourceView):
    def get(self, request, *args, **kwargs):
        try:
            # Проверка профиля пользователя
            profile = UserProfile.objects.get(user=request.user)
            # Проверка метода аутентификации
            if profile.auth_method != 'oauth':
                return JsonResponse({'error': 'This account uses different authentication method'}, status=400)
        except UserProfile.DoesNotExist:
            return JsonResponse({'error': 'User profile not found'}, status=400)

        # Возврат приветственного сообщения
        return JsonResponse({'message': f'Hello, {request.user.username}!'})


def oauth2_callback(request):
    # Получаем код авторизации из параметров запроса
    code = request.GET.get('code')
    # Получаем информацию об ошибке, если она есть
    error = request.GET.get('error')

    # Если есть ошибка, возвращаем информацию о ней
    if error:
        return JsonResponse({
            'error': error,
            'description': request.GET.get('error_description')
        })

    # Если ошибок нет, возвращаем полученный код авторизации
    return JsonResponse({'code': code})

class CustomTokenView(TokenView):
    def create_token_response(self, request):
        response = super().create_token_response(request)
        # Получаем client_id из заголовка Authorization
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        client_id = base64.b64decode(auth_header.split(' ')[1]).decode().split(':')[0]
        # Привязываем токен к пользователю
        token = AccessToken.objects.latest('created')
        token.user = Application.objects.get(client_id=client_id).user
        token.save()
        return response

# Защищенный ресурс
@api_view(['GET'])
@authentication_classes([OAuth2Authentication, JWTAuthentication])
@permission_classes([IsAuthenticated])
def protected_resource(request):
    # Возврат защищенного ресурса для аутентифицированных пользователей
    return Response({'message': f'Hello, {request.user.username}!'})