# Django testing  

## Описание
Тесты для двух проектов - сайта с новостями и комментариями (тестировал на pytest) и сайта - записной книжки (тесты на unittest)

## Используемые технологии:

- django
- pytest
- unittest

В проекте используется python 3.9

## Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/VladimirNagibin/django_testing.git
```

```
cd django_testing
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


В корень проекта нужно поместить файл .env  со значением SECRET_KEY= секретный ключ Django
____

**Владимир Нагибин** 

Github: [@VladimirNagibin](https://github.com/VladimirNagibin/)