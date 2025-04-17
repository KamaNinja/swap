<h2>Установка.</h2>

<p>Скачай репозиторий командой:</p>

```
git clone https://github.com/KamaNinja/swap.git
```

<br>
<p>Установи зависимости командой:</p>

```
pip install -r requirements.txt
```
<br>

<p>Создай БД в PostgreSQL.</p>
<br>

<p>В settings.py в переменной DATABASES установи свои значения NAME, USER и PASSWORD.</p>

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_db_name',
        'HOST': 'localhost',
        'PORT': '5432',
        'USER': 'your_user_name',
        'PASSWORD': 'your_password'
    }
}
```
<br>

<p>Сделай миграции:</p>

```
python3 manage.py makemigrations

python3 manage.py migrate
```
<br>

<p>перейди в shell:</p>

```
python3 manage.py shell
```

<p>и выполни следующий код:</p>

```
from django.contrib.auth.models import User
for i in range(1, 6):
    username = f"user{i}"
    password = f"user{i}"
    User.objects.create_user(username=username, password=password)
```
<p>Потом выйди из shell и выполнм команду:</p>

```
python3 manage.py loaddata ads_fixture_with_random_images.json
```

<p>Данные загружены! Можешь запускать сервер</p>

```
python3 manage.py runserver
```

<p>Имена пользователей: user1, user2, user3, user4, user5</p>
<p>Пароли: user1, user2, user3, user4, user5</p>
Удачи!)

