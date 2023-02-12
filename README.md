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


## Авторы проекта
- Frontend [Яндекс.Практикум](https://practicum.yandex.ru/ "Яндекс.Практикум")
- Backend [VladisloveRus](https://github.com/VladisloveRus "Владислав Черепанов")
