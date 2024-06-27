### Проект Blogicum  

## Описание
Blogicum - 

## Используемые технологии:

- django
- SQLite
- Bootstrap

В проекте использовался python3.9

## Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/VladimirNagibin/api_yamdb.git
```

```
cd api_yamdb
```

Cоздать и активировать виртуальное окружение:

```
python -m venv venv
```

```
source venv/Scripts/activate
```

Установить пакетный менеджер и зависимости из файла requirements.txt:

```
python -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Выполнить миграции:

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

