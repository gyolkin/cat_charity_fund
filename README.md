# Фонд помощи кошкам на FastAPI
[![Version_of_Python](https://img.shields.io/badge/Python-3.10-blue?style=flat&logo=python&logoColor=white)](#)
[![Version_of_FastAPI](https://img.shields.io/badge/FastAPI-0.78-cyan?style=flat&logo=fastapi&logoColor=white)](#)
[![Version_of_Pydantic](https://img.shields.io/badge/Pydantic-1.9-pink?style=flat&logo=pydantic&logoColor=white)](#)
[![Version_of_SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-1.4-red?style=flat&logoColor=white)](#)

## Описание
«QRKot» — это API благотворительного фонда помощи кошкам, построенное на FastAPI. Любой пользователь может видеть список всех целей, включая требуемые и уже внесенные суммы. Зарегистрированные пользователи могут отправлять пожертвования и просматривать список своих пожертвований. Администраторы сайта (суперюзеры) могут создавать и редактировать цели, получать информацию о всех пожертвованиях. Если создана новая цель, а в базе были «свободные» (не распределённые по проектам) пожертвования — они автоматически инвестироуются в новую цель. То же касается и создания пожертвований: если в момент пожертвования есть открытые проекты, эти пожертвования автоматически зачисляются на их счета.

## Технологический стек
- Python
- FastAPI
- Pydantic
- SQLAlchemy
- Alembic

В работе также используются вспомогательные библиотеки, например, [FastAPI Users](https://github.com/fastapi-users/fastapi-users).

## Запуск на локальном компьютере
Перед запуском рекомендуется настроить проект по шаблону .env.example. Файл с переменными окружения .env нужно расположить в корне проекта. Далее создать и активировать виртуальное окружение:
```
python -m venv venv
. venv/scripts/activate
```
Установить зависимости:
```
pip install -r requirements.txt
```
Применить миграции:
```
alembic upgrade head
```
При необходимости создать в базе данных администратора. Далее запустить проект:
```
uvicorn app.main:app
```
Интерактивная документация к API (Swagger UI) будет доступна по адресу, заданному в переменной окружения **SET_DOCS_URL**.
