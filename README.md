#  Продуктовый помощник foodgram

Проект для обмена рецептами. 

## Технологии
- Python
- Django
- Postgres
- Docker

## Установка

- Скопируйте репозиторий.
```sh
git clone https://github.com/VladisloveRus/foodgram-project-react
```
- Для запуска установите вирутальное окружение и зависимости:
```sh
python -m venv venv
pip install -r requirements.txt 
```
- Создайте файл .env директории infra и заполните его по примеру:
```sh
DB_ENGINE=django.db.backends.postgresql
DB_NAME=[ИМЯ БД]
POSTGRES_USER=[ПОЛЬЗОВАТЕЛЬ БД]
POSTGRES_PASSWORD=[ПАРОЛЬ БД]
DB_HOST=db
DB_PORT=5432
SECRET_KEY=[СЕКРЕТНЫЙ КЛЮЧ]
ALLOWED_HOSTS= web localhost 127.0.0.1 [ВАШ ХОСТ]
```
- Выполните следующие команды:
```sh
cd infra
docker-compose up --build
```
- После запуска, откройте контейнер web и в нём выполните следующие команды
```sh
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --no-input
python manage.py add_ingredients
```
- Так же, в контейнере web, можно создать суперпользователя
```sh
python manage.py createsuperuser
```

## Сервер запущен по адресу [wolfi.onthewifi.com](http://wolfi.onthewifi.com/ "wolfi.onthewifi.com")
- Данные для входа в панель администратора
```sh
E-mail: Admin@mail.ru
Password: Administrator1586
```

## Авторы проекта
- Frontend [Яндекс.Практикум](https://practicum.yandex.ru/ "Яндекс.Практикум")
- Backend [VladisloveRus](https://github.com/VladisloveRus/ "Владислав Черепанов")
