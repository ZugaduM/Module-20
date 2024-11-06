<img src="https://androidinsider.ru/wp-content/uploads/2020/05/end_to_end-750x439.jpg" align="center" alt="Authentications">

![GitHub last commit](https://img.shields.io/github/last-commit/zugadum/module-20)
![GitHub repo size](https://img.shields.io/github/repo-size/zugadum/module-20)
![GitHub Repo stars](https://img.shields.io/github/stars/zugadum/module-20)
![GitHub watchers](https://img.shields.io/github/watchers/zugadum/module-20)
![GitHub followers](https://img.shields.io/github/followers/zugadum)
![Static Badge](https://img.shields.io/badge/e--mail%3A-zugadum%40gmail.com-blue?link=mailto:zugadum@gmail.com)

# Анализ и сравнение различных методов аутентификации и авторизации в веб-приложениях: OAuth, JWT и session-based authentication

## Оглавление
- [Введение](#intro)
- [Конечные точки аутентификации](#end_points)
- [Термины и определения](#terms)
- [Структура проекта](#struct)
- [Анализ методов аутентификации](#analisis)
- [Заключение](#result)
- [Идеи по модернизации](#ideas)
- [Приложение 1. Пример файловой структуры проекта](#add_1)
- [Приложение 2. Список необходимых библиотек](#add_2)

## <img src="https://github.com/user-attachments/assets/0a965a32-a89b-4cbd-9e52-eb61f242a3f1" width="48"> <a id='intro'>Введение</a>
Целью данной работы является знакомство с каждым из представленных методов с последующей их реализацией, а также анализ документации и сбор данных для возможности определения достоинств и недостатков.

Для анализа и сравнения каждого из выбранных методов был создан одностраничный проект на базе Django. На единственной странице которого, отображается форма аутентификации или регистрации (в зависимости от того, что необходимо пользователю). Для создания более приятного интерфейса был использован инструментарий [Bootstrap](https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/) версии 5.1.3, который включает в себя различные CSS и HTML-шаблоны оформления.

## <img src="https://github.com/user-attachments/assets/05457dc6-4d76-463b-92cb-d57548134a4e" width="48"> <a id='end_points'>Конечные точки аутентификации</a>
  - **Session-based**
      * Вход: `POST /login/`
      * Защищенный ресурс: `GET /profile/`
  - **OAuth2**
      * Генерация токена: `POST /oauth/token/`
      * Защищенный ресурс: `GET /api/oauth2-protected/`
  - **JWT**
      * Генерация токена: `POST /api/token/`
      * Обновление токена: `POST /api/token/refresh/`
      * Защищенный ресурс: `GET /api/protected/`

## <img src="https://github.com/user-attachments/assets/9b01a7ad-5146-46b8-91ff-72db872fe160" width="48"> <a id='terms'>Термины и определения</a>
<table>
  <tr>
    <td><b>Регистрация</b></td>
    <td>это процесс передачи персональных данных пользователя, на основании которых, пользователь сможет получить доступ к определенным возможностям веб-сайта, в соответствии с его уровнем доступа. При регистрации создаётся личный кабинет (профиль или запись), через который пользователь может, например, смотреть фильмы, заказывать товары и отслеживать их обработку, а также просматривать историю своих запросов и многое другое</td>
  </tr>
  <tr>
    <td><b>Аутентификация</b></td>
    <td>процедура проверки подлинности введённых пользователем данных. В процессе аутентификации пользователь передает серверу данные для входа, чаще используется комбинация логин и пароль. В качестве логина может выступать различная информация, например, адрес электронной почты, а паролем чаще выступает комбинация из цифр, букв (в различном регистре) и специализированных символов</td>
  </tr>
  <tr>
    <td><b>Авторизация</b></td>
    <td>процесс предоставления прав доступа к различным возможностям и областям веб-сайта на основании присвоенных учетной записи прав (или уровня) доступа. Процесс авторизации происходит строго после процедуры аутентификации и может повторяться при каждом обращении пользователя к той или иной области (возможности) веб-сайта. Так же пользователь в процессе авторизации может получить доступ на определенное время. Для этой цели могут быть использованы сессионные ключи, либо токены</td>
  <tr>
    <td><b>Токен</b></td>
    <td>или ключ, это идентификатор, который используется для представления доступа к различным возможностям и областям веб-сайта. Токен может быть представлен в виде последовательности букв и цифр, а также в виде физического носителя (чаще в виде подключаемого usb устройства)</td>
</table>

## <img src="https://github.com/user-attachments/assets/a3c23b42-afdf-48e7-9a86-825aaa174d68" width="48"> <a id='struct'>Структура проекта</a>
### Проект включает в себя следующие ключевые компоненты:
### 1. Форма аутентификации
Данная страница отображает базовый (<a href="https://github.com/ZugaduM/Module-20/blob/main/auth_project/templates/base.html">base.html</a>) шаблон, который дополняется блоками из шаблона страницы аутентификации (<a href="https://github.com/ZugaduM/Module-20/blob/main/auth_project/templates/mainpage.html">mainpage.html</a>).
На Рисунке 1 показано в каком виде пользователю представляется страница.
На Главной (Домашней) странице отображается название сайта или приложения (Authentications), а также форма аутентификация, в которой можно:
  - Выбрать метод (session-based authentication, JWT или OAuth);
  -	Ввести имя пользователя (username) и пароль (password);
  -	Кнопка (Login) для передачи на сервер введенной информации с последующей ее проверкой;
  -	Текстовая ссылка (Register) для перехода к форме регистрации.
![image](https://github.com/user-attachments/assets/54fd9546-a0bf-42f3-945b-77c574981743)
*Рисунок 1. Форма аутентификации*

### 2. Форма регистрации
Данная страница отображает базовый ((<a href="https://github.com/ZugaduM/Module-20/blob/main/auth_project/templates/base.html">base.html</a>)) шаблон, который дополняется блоками из шаблона страницы аутентификации (<a href="https://github.com/ZugaduM/Module-20/blob/main/auth_project/templates/mainpage.html">mainpage.html</a>).
На Рисунке 2 показано в каком виде пользователю представляется страница.
На Главной (Домашней) странице отображается название сайта или приложения (Authentications), а также форма регистрации, в которой можно:
  -	Выбрать метод (session-based authentication, JWT или OAuth);
  -	Ввести данные для регистрации такие как имя пользователя (username), адрес электронной почты (email), пароль (поля password и confirm password);
  -	Кнопка (Register) для передачи на сервер введенной информации с последующей ее проверкой на наличие использования ранее (в случае если пользователь с такими данными уже зарегистрирован);
  -	Текстовая ссылка (Back to Login) для возврата к форме аутентификации.
![image](https://github.com/user-attachments/assets/d1fb893d-16e4-4c67-bdb0-312fbf6d81d4)
*Рисунок 2. Форма регистрации*

### 3. Шаблоны страниц
*base.html* – базовый шаблон, в котором подключается инструментарий Bootstrap, а также CSS стиль оформления границ форм. На основании данного шаблона разрабатывается шаблон аутентификации. 
*mainpage.html* – главная (домашняя) страница, с формами аутентификации и регистрации.

### 3. Структура базы данных
После миграции получаем следующую структуру, отображенную на Рисунке 3.
![image](https://github.com/user-attachments/assets/24354348-f4ab-43ac-9ee8-63d8458375db)
*Рисунок 3. Структура базы данных*

## <img src="https://github.com/user-attachments/assets/b8c35cb4-585e-4223-bc9c-f3c1da27d842" width="48"> <a id='analisis'>Анализ методов аутентификации</a>
### 1. Session-based authentication
Session-based authentication - это классический и надёжный метод аутентификации.
Для тестирования данного метода создадим нового пользователя admin. Процесс ввода регистрационных данных показан на Рисунке 4:
![image](https://github.com/user-attachments/assets/aa9e24cf-318f-40c1-a3ec-cdf78c02d082)
*Рисунок 4. Форма регистрации с введенными учетными данными*

Принцип работы данного метода построен на процессе аутентификации, при котором:
  -	Пользователь вводит логин и пароль;
  -	Сервер проверяет учетные данные;
  -	При успехе создаётся сессия с уникальным ID;
  -	ID сессии сохраняется в cookie браузера.

После отправке данных на сервер и успешной проверки на совпадения пользователь попадает в свой профиль, раздел или заданную администратором область сайта (приложения). Пример входа показан на Рисунке 5.
![image](https://github.com/user-attachments/assets/fb26834d-6baa-4b40-b9fd-816c9ef8d315)
*Рисунок 5. Успешная аутентификация*

При реализации данного метода сессионные данные хранятся на сервере, в cookie хранится только ID сессии, так же можно хранить дополнительные данные пользователя (например, пользовательские настройки, состояние корзины и прочее). Пример cookie показан на Рисунке 6.
![image](https://github.com/user-attachments/assets/8020ddc1-a46f-4834-9ba8-bafe1973e8bb)
*Рисунок 6. Пример сохраняемых cookie*

К преимуществам данного метода можно отнести:
  -	Простоту реализации;
  -	Доступность «из коробки», так как он является встроенным в Django по умолчанию;
  -	Легкость в отзыве сессии;
  -	Хорошая безопасность так как имеет защиту от XSS и CSRF атак.
К недостаткам можно отнести:
  -	Масштабируемость, так как требуется хранение сессий на сервере, что при большом количестве пользователей будет сильно влиять на память сервера;
  -	Производительность, так как при каждом запросе необходимо обращаться к базе данных или хранилищу сессий;
  -	Безопасность, так как присутствует риск атак через перехват сессии, возможность CSRF атак без правильной защиты, необходимость правильной конфигурации cookies.

### 2. JWT (JSON Web Token)
JWT - это JSON объект, который определен в открытом стандарте RFC 7519.
Для тестирования данного метода создадим нового пользователя admin2 и укажем метод аутентификации JWT как это показано на Рисунке 7.
![image](https://github.com/user-attachments/assets/3303c98e-3dcb-43c4-8b18-3074bf60aa83)
*Рисунок 7. Создаем пользователя для тестирования метода JWT*

Принцип работы данного метода построен на процессе аутентификации, при котором:
  -	Сперва пользователь заходит на сервер аутентификации с помощью аутентификационного ключа, которым может быть пара логин/пароль, либо Google ключ, либо ключ от учетной записи стороннего сервиса;
  -	Сервер генерирует JWT токен (строка в формате header.payload.signature) и отправляет его пользователю. Header - содержит информацию о том, как должна вычисляться JWT подпись. Payload - это полезные данные, которые хранятся внутри JWT (например, user_id). Signature электронная подпись, которая формируется особым образом;
  -	Когда пользователь делает запрос к API приложения, он добавляет к нему полученный ранее JWT;
  -	Когда пользователь делает API запрос, приложение может проверить по переданному с запросом JWT является ли пользователь тем, за кого себя выдает.
Чтобы показать как работает данный метод воспользуемся предусмотренным в REST framework API. Для этого перейдем по ссылке http://127.0.0.1:8000/api/token/.
Результат показан на Рисунке 8.
![image](https://github.com/user-attachments/assets/a9df9c9e-f205-4bbb-be30-4c516ecbd6d7)
*Рисунок 8. REST framework API*

Для получения JWT токена отправим POST запрос с именем пользователя и паролем, в случае ошибки получим предусмотренные нами сообщения. Результат представлен на Рисунках 9 и 10.
![image](https://github.com/user-attachments/assets/bac7cd43-14a1-4ebc-aec9-016ec79ea303)
*Рисунок 9. JWT токен*
![image](https://github.com/user-attachments/assets/76f28b62-e0ff-46dc-ab79-33d5e4791318)
*Рисунок 10. Результат запроса с неправильными данными*

Теперь для проверки аутентификационных данных воспользуемся утилитой CURL и отправим GET запрос на сервер используя access token. В результате мы должны будем получить доступ к следующему участку кода:
```python
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
```
*views.py*

Наш запрос будет иметь вид:

curl -H “Authorization: Bearer «access_token» http://localhost:8000/api/protected/
В результате мы получим ответ в формате строки со следующим содержанием «Hello, admin2!». Выполнение запроса показано на Рисунке 11.
![image](https://github.com/user-attachments/assets/b5ed0ecd-946d-45b7-909e-c3404f9ee95e)
*Рисунок 11. Результат запроса защищенной области используя JWT токен*

К преимуществам данного метода можно отнести:
  -	Не требует хранения на сервере;
  -	Отлично масштабируется;
  -	Работает на разных доменах;
  -	Идеален для REST API.
Из недостатков данного метода можно выделить:
  -	Объем передаваемых данных. Чем больше данных будет указано в payload, тем больше будет размер ключа;
  -	Низкая гарантия безопасности. Так как при создании JWT токена применяется только кодирование и подписание, но отсутствует шифрование – такой подход не дает гарантии защиты чувствительных данных;
  -	Нельзя отозвать отдельный токен до истечения срока;
  -	Токен хранится на клиенте.

### 3. OAuth 2
OAuth 2 - протокол авторизации (не аутентификации), позволяющий выдать одному сервису (приложению) права на доступ к ресурсам пользователя на другом сервисе. Протокол избавляет от необходимости доверять приложению логин и пароль, а также позволяет выдавать ограниченный набор прав, а не все сразу.
Для тестирования данного метода создадим нового пользователя admin3 как это было показано ранее. Далее для проверки метода авторизации OAuth2 перейдем в admin-панель Django, как это показано на Рисунке 12.
![image](https://github.com/user-attachments/assets/f58bb77e-de1b-40dc-9193-bfdfe4084303)
*Рисунок 12. Администраторская панель Django*

Для проверки метода необходимо создать клиентское приложение, получить токен и отправить запрос на сервер, используя токен. В результате пользователь получит доступ к защищенной области вебсайта (приложения). Для этого создадим запись в Applications (Django OAuth Toolkit) как это показано на Рисунках 13.1 и 13.2.

![image](https://github.com/user-attachments/assets/a1016c11-79a7-4e3c-bbab-1b93b8ad7b37)
*Рисунок 13.1. Настройка клиентского приложения (начало)*

![image](https://github.com/user-attachments/assets/e794cd18-b126-42c4-811b-a1d5910dddf0)
*Рисунок 13.2. Настройка клиентского приложения (продолжение)*

Далее для получаем токен. Для этого отправляем POST запрос используя CURL:
`curl -X POST http://localhost:8000/oauth/token/ -u "client_id:client_secret" -d "grant_type=client_credentials"`
И в результате, который отображен на Рисунке 13, видим токен.

![image](https://github.com/user-attachments/assets/7967f58e-9339-4da8-bbc3-1ad21b7c5d0e)
*Рисунок 13. Получаем OAut2h токен*

Теперь используя полученный токен, можно обратимся к защищенной области веб-сайта (приложения). Пример ответа сервера показан на Рисунке 17.

![image](https://github.com/user-attachments/assets/ad1ef5ff-7e10-4cda-a3e3-02652f6b381a)
*Рисунок 17 Ответ от сервера на запрос с использованием токена*

К преимуществам данного метода можно отнести:
  -	Упрощенная интеграция;
  -	Повышенная безопасность;
  -	Гибкая настройка прав;
  -	Поддержка мобильных приложений;
  -	Возможность обновления токенов.
Из недостатков данного метода можно выделить:
  -	Сложность реализации. Так как метод требует тщательного планирования архитектуры, правильной настройки безопасности и имеет сложную обработка ошибок;
  -	Требует отдельного сервера авторизации;
  -	Поскольку данный метод еще развивается, отсутствует устоявшаяся спецификация в следствии чего при выпуске очередного обновления может сильно меняться, что приводит усложнению технической поддержки;
  -	Безопасность. Так как метод во многом основана на SSL, это сильно упрощает жизнь разработчикам, но требует дополнительных вычислительных ресурсов и администрирования. Это может быть существенным вопросом в высоко нагруженных проектах.

## <img src="https://github.com/user-attachments/assets/bc9ea987-d107-419e-954b-b436411c48d0" width="48"> <a id='result'>Заключение</a>
Основываясь на представленном анализе выбранных методов аутентификации и авторизации, можно сделать следующий вывод:
  -	Session-based: идеален для классических веб-приложений;
  -	JWT: отличный выбор для современных API и мобильных приложений;
  -	OAuth2: лучшее решение для сложных систем с множественной интеграцией.

## <img src="https://github.com/user-attachments/assets/8130e651-545f-4a05-9626-a4c5e61247c7" width="48"> <a id='ideas'>Идеи по модернизации</a>
В качестве модернизации и улучшения функционала приложения можно выделить некоторые позиции, например:
  -	Добавить отображении cookie в профиле пользователя, использующего метод Session-based authentication;
  -	В форме аутентификации добавить кнопки авторизации сторонними ресурсами, такими как Google, GitHub;
  -	Добавить форму и механизм восстановления пароля учетной записи путем генерации уникальной ссылки;
  -	Добавить в профили пользователей функционал управления cookie (например, удаление), генерацию и перевыпуск токенов для методов JWT и OAuth2.

## <a id='add_1'>Приложение 1. Пример файловой структуры проекта</a>
![image](https://github.com/user-attachments/assets/b87c67b1-1433-46e5-8978-97bb58401dad)

## <a id='add_2'>Приложение 2. Список необходимых библиотек</a>
- asgiref==3.8.1
- certifi==2024.8.30
- cffi==1.17.1
- charset-normalizer==3.4.0
- cryptography==43.0.3
- Django==5.1.2
- django-oauth-toolkit==3.0.1
- djangorestframework==3.15.2
- djangorestframework-simplejwt==5.3.1
- idna==3.10
- jwcrypto==1.5.6
- oauthlib==3.2.2
- pycparser==2.22
- PyJWT==2.9.0
- requests==2.32.3
- sqlparse==0.5.1
- typing_extensions==4.12.2
- tzdata==2024.2
- urllib3==2.2.3

[![Top Langs](https://github-readme-stats.vercel.app/api/top-langs/?username=zugadum&layout=compact)](https://github.com/anuraghazra/github-readme-stats)
<h3 align="left">Я использую:</h3>
<p align="left"> <a href="https://www.arduino.cc/" target="_blank" rel="noreferrer"> <img src="https://cdn.worldvectorlogo.com/logos/arduino-1.svg" alt="arduino" width="40" height="40"/> </a> <a href="https://www.blender.org/" target="_blank" rel="noreferrer"> <img src="https://download.blender.org/branding/community/blender_community_badge_white.svg" alt="blender" width="40" height="40"/> </a> <a href="https://www.w3schools.com/cpp/" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/cplusplus/cplusplus-original.svg" alt="cplusplus" width="40" height="40"/> </a> <a href="https://www.djangoproject.com/" target="_blank" rel="noreferrer"> <img src="https://cdn.worldvectorlogo.com/logos/django.svg" alt="django" width="40" height="40"/> </a> <a href="https://git-scm.com/" target="_blank" rel="noreferrer"> <img src="https://www.vectorlogo.zone/logos/git-scm/git-scm-icon.svg" alt="git" width="40" height="40"/> </a> <a href="https://www.w3.org/html/" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/html5/html5-original-wordmark.svg" alt="html5" width="40" height="40"/> </a> <a href="https://developer.mozilla.org/en-US/docs/Web/JavaScript" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/javascript/javascript-original.svg" alt="javascript" width="40" height="40"/> </a> <a href="https://www.linux.org/" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/linux/linux-original.svg" alt="linux" width="40" height="40"/> </a> <a href="https://www.postgresql.org" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/postgresql/postgresql-original-wordmark.svg" alt="postgresql" width="40" height="40"/> </a> <a href="https://www.python.org" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" alt="python" width="40" height="40"/> </a> <a href="https://www.qt.io/" target="_blank" rel="noreferrer"> <img src="https://upload.wikimedia.org/wikipedia/commons/0/0b/Qt_logo_2016.svg" alt="qt" width="40" height="40"/> </a> <a href="https://www.sketch.com/" target="_blank" rel="noreferrer"> <img src="https://www.vectorlogo.zone/logos/sketchapp/sketchapp-icon.svg" alt="sketch" width="40" height="40"/> </a> <a href="https://www.sqlite.org/" target="_blank" rel="noreferrer"> <img src="https://www.vectorlogo.zone/logos/sqlite/sqlite-icon.svg" alt="sqlite" width="40" height="40"/> </a> </p>
