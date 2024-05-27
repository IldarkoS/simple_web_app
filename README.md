# TODO app
Веб-приложение, написанное с использованием Flask. Выбранная база данных: MySQL.

Сделана валидация, а также документация ('/swagger')

## Реализованы методы:
1. Создание задачи:
- Метод: POST
- URL: /tasks
- Параметры запроса: JSON-объект с полями title (строка) и description (строка, опционально).
- Ответ: JSON-объект с полями id, title, description, created_at, updated_at.

2. Получение списка задач:
- Метод: GET
- URL: /tasks
- Ответ: JSON-список задач, где каждая задача представляет собой JSON-объект с полями id, title, description, created_at, updated_at.

3. Получение информации о задаче:
- Метод: GET
- URL: /tasks/<id>
- Ответ: JSON-объект с полями id, title, description, created_at, updated_at.

4. Обновление задачи:
- Метод: PUT
- URL: /tasks/<id>
- Параметры запроса: JSON-объект с полями title (строка, опционально) и description (строка, опционально).
- Ответ: JSON-объект с полями id, title, description, created_at, updated_at.

5. Удаление задачи:
- Метод: DELETE
- URL: /tasks/<id>
- Ответ: Сообщение об успешном удалении.

## Запуск:

- Создать базу MySQL с именем 'tasks'
- Поменять example.env на .env и поменять данные, если это нужно

python -m venv venv

source venv/bin/activate

pip install -r requirements.txt

python main.py

Приложение будет доступно по - http://localhost:5000/

## Запуск тестов

python tests.py