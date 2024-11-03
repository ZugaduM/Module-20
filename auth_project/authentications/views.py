import base64

from django.shortcuts import render, redirect                 # Импорт функций для рендеринга страниц и перенаправления
from django.contrib.auth import login, authenticate           # Импорт функций для аутентификации пользователей
from django.contrib import messages                           # Импорт для работы с сообщениями пользователю
from django.views.decorators.http import require_http_methods # Импорт декоратора для ограничения HTTP методов
from django.contrib.auth.models import User                   # Импорт модели пользователя Django
from django.http import JsonResponse                          # Импорт для JSON ответов
from rest_framework_simplejwt.views import TokenObtainPairView # Импорт базового класса для работы с JWT токенами
from rest_framework_simplejwt.authentication import JWTAuthentication # Импорт класса аутентификации JWT
from rest_framework.decorators import api_view, permission_classes # Импорт декораторов REST framework
from rest_framework.permissions import IsAuthenticated        # Импорт класса разрешений для аутентифицированных пользователей
from rest_framework.response import Response                  # Импорт класса ответа REST framework
from oauth2_provider.views.generic import ProtectedResourceView # Импорт базового класса для OAuth2 защищенных ресурсов
from oauth2_provider.contrib.rest_framework import OAuth2Authentication # Импорт класса аутентификации OAuth2
from oauth2_provider.views import TokenView                   # Базовый класс для создания токенов
from oauth2_provider.models import AccessToken, Application   # Модели для токенов и приложений OAuth2
from rest_framework.decorators import authentication_classes  # Импорт декоратора для указания классов аутентификации
from .models import UserProfile                               # Импорт модели профиля пользователя


def main_page(request):
    """
    Метод отображения главной страницы принимающий запрос (request)
    и перенаправляющий на mainpage.html

    :param request:
    :return render:
    """
    return render(request, 'mainpage.html')


def user_login(request):
    """
    Метод обрабатывающий пользовательский запрос, содержащий данные для входа.
    Для повышения безопасности используется POST-запрос, содержащий:
    username, password и auth_method.

    После получения данные сверяются с теми, что хранятся в базе.
    В случае ошибок:
        1. неправильно выбран метод аутентификации
        пользователь видит сообщение и происходит перенаправление на главную страницу (форму аутентификации)

        2. пользователь с введенными данными не существует
        срабатывает исключение, пользователь увидит соответствующее сообщение

    В ином случае пользователь входит в систему.

    :param request:
    :return render:
    """
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
    """
    Метод регистрации новых пользователей.

    Применяется декоратор @require_http_methods(["POST"]) для указания системе использовать только POST запросы.
    Получаем от пользователя данные:
        username
        email
        password1
        password2
        auth_method
    Два поля password исключают возможность ошибки в последовательности введенного пароль.
    Поле auth_method нужно для выбора соответствующего метода аутентификации и авторизации
    и последующей проверки его при входе. Если при попытке входа будет указан неправильный auth_method
    пользователь не сможет войти.

    В блоке try except пробуем создать нового пользователя. Если пользователь с введенными данными
    уже есть в базе сработает исключение и пользователь увидит сообщение с соответствующей ошибкой.

    В ином случае профиль успешно создастся и сработает блок автоматического входа login(request, user)

    :param request:
    :return redirect:
    """
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
    """
    Класс JSON WEB TOKEN.
    1. Наследует базовую функциональность создания JWT токенов от TokenObtainPairView
    2. Переопределяет метод post(), который:
        Сначала выполняет стандартную логику создания токена
        Проверяет успешность создания токена (status_code == 200)
        Получает пользователя по username из запроса
        Проверяет профиль пользователя на соответствие методу аутентификации JWT

    3. Класс возвращает JWT токен при успешной аутентификации, либо ошибку 400 если
    неправильно выбран метод аутентификации либо пользователь не найден.
    """
    def post(self, request, *args, **kwargs):
        """
        :param request:
        :param args:
        :param kwargs:
        :return response:
        """
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
    """
        Класс OAuth2ProtectedResource для защиты ресурсов.
        Наследуется от ProtectedResourceView, что обеспечивает базовую OAuth2 защиту.

        1. Реализует GET-метод, который:
            Проверяет существование профиля пользователя
            Валидирует правильность метода аутентификации (должен быть OAuth)
            Возвращает приветственное сообщение для авторизованного пользователя.

        При успешной аутентификации пользователь получит приветственное сообщение,
        а при неверном методе аутентификации или отсутствии профиля - соответствующее сообщение об ошибке.
        """
    def get(self, request, *args, **kwargs):
        """
        :param request:
        :param args:
        :param kwargs:
        :return JsonResponse:
        """
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
    """
    Метод обработки ответов OAuth2 сервера авторизации.

    Обработка успешной авторизации:
        # При успешной авторизации возвращает код авторизации
        return JsonResponse({'code': code})

    Обработка ошибок:
        # При наличии ошибки возвращает детали ошибки
        return JsonResponse({
            'error': error,
            'description': request.GET.get('error_description')
        })

    Данный callback используется в процессе OAuth2 авторизации:
        Принимает redirect от сервера авторизации
        Извлекает код авторизации или информацию об ошибке из URL параметров
        Возвращает результат в формате JSON

    :param request:
    :return JsonResponse:
    """

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
    """
    Класс CustomTokenView наследуемый от TokenView.

    1. Наследует базовую функциональность создания токена от TokenView

    2. Переопределяет метод create_token_response для добавления дополнительной логики:
        Извлекает client_id из заголовка Authorization, который приходит в Base64-encoded формате
        Декодирует client_id из Base64
        Находит последний созданный токен доступа
        Связывает токен с пользователем, который соответствует данному client_id
        Сохраняет обновленный токен
    """
    def create_token_response(self, request):
        """
        :param request:
        :return response:
        """
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
    """
    Защищенный API endpoint с многоуровневой аутентификацией.
        1. Декоратор @api_view(['GET']) указывает, что это REST endpoint, который принимает только GET-запросы
        2. Декоратор @authentication_classes определяет два метода аутентификации:
            OAuth2Authentication
            JWTAuthentication

        3. Декоратор @permission_classes([IsAuthenticated]) гарантирует, что доступ получат только
        аутентифицированные пользователи

        4. Функция возвращает персонализированное приветствие с именем пользователя

    :param request:
    :return Response:
    """
    # Возврат защищенного ресурса для аутентифицированных пользователей
    return Response({'message': f'Hello, {request.user.username}!'})
