### Проект Blogicum  

## Описание
Blogicum - сайт для публикаций постов, для которых определены категории и опционально расположение. Зарегистрированные пользователи могут комментировать чужие посты. 

## Используемые технологии:

- django
- SQLite
- Bootstrap

В проекте используется python 3.9

## Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/VladimirNagibin/django_sprint4.git
```

```
cd django_sprint4
```

Cоздать и активировать виртуальное окружение:

```
python3.9 -m venv venv
```

```
source venv/bin/activate
```

Установить пакетный менеджер и зависимости из файла requirements.txt:

```
pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Перейти в рабочую папку и выполнить миграции:

```
cd blogicum/
```

```
python manage.py migrate
```

Загрузить тестовые данные:

```
python manage.py loaddata db.json
```

Запустить проект:

```
python manage.py runserver
```

В корень проекта нужно поместить файл .env  со значением SECRET_KEY= секретный ключ Django

Сайт будет доступен по адресу http://127.0.0.1:8000/

____

**Владимир Нагибин** 

Github: [@VladimirNagibin](https://github.com/VladimirNagibin/)
