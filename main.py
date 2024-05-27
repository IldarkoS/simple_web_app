from flask import Flask, request, render_template
from extensions import db
from database.DAL import TaskModelDAL
import config
import json
from flask_swagger_ui import get_swaggerui_blueprint


def create_app() -> Flask:
    """Функция создания приложения"""
    app = Flask(__name__)
    app.config['SECRET_KEY'] = config.APP_SECRET_KEY
    connect_to_database(app=app)
    return app


def connect_to_database(app) -> None:
    """Функция подключения к базе данных"""
    app.config['SQLALCHEMY_DATABASE_URI'] = \
        f"mysql+pymysql://{config.DATABASE_USER}:{config.DATABASE_PASSWORD}@{config.DATABASE_HOST}/{config.DATABASE_NAME}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app=app)

    with app.app_context():
        db.create_all()


app = create_app()


@app.route('/')
def view_form():
    return render_template('index.html')


@app.route('/tasks', methods=['GET'])
def get_tasks() -> dict:
    """Получить список всех задач"""
    if request.method == 'GET':
        with app.app_context():
            answer = {"tasks": []}
            tasks = TaskModelDAL.TaskModelDAL(db.session).get_all_tasks()
            for each_task in tasks:
                answer['tasks'].append(
                    {
                        "id": each_task.id,
                        "title": each_task.title,
                        "description": each_task.description,
                        "created_at": each_task.created_at,
                        "updated_at": each_task.updated_at
                    }
                )
            return answer


@app.route('/tasks', methods=['POST'])
def create_task() -> dict:
    """Создание задачи"""
    if request.method == 'POST':
        data = request.get_json()
        try:
            title = data['title']
            description = data['description']
            with app.app_context():
                task = TaskModelDAL.TaskModelDAL(db.session).create_task(title=title, description=description)
                return {
                    "id": task.id,
                    "title": task.title,
                    "description": task.description,
                    "created_at": task.created_at,
                    "updated_at": task.updated_at
                }
        except Exception as e:
            return {
                f"ERROR": f"posting failed - {e}"
            }


@app.route('/tasks/<int:id>', methods=['GET'])
def get_task(id) -> dict:
    """Получить конкретную задачу"""
    if request.method == 'GET':
        with app.app_context():
            try:
                task = TaskModelDAL.TaskModelDAL(db.session).get_task_by_id(id=id)
                if task:
                    return {
                        "id": task.id,
                        "title": task.title,
                        "description": task.description,
                        "created_at": task.created_at,
                        "updated_at": task.updated_at
                    }
                else:
                    return {
                        "ERROR": f"task with id = {id} does not exist"
                    }
            except Exception as e:
                return {
                    f"ERROR": f"task_{id} get failed - {e}"
                }


@app.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id) -> dict:
    """Обновить конкретную задачу"""
    if request.method == 'PUT':
        data = request.get_json()
        title = data['title']
        description = data['description']
        with app.app_context():
            try:
                updated_task = TaskModelDAL.TaskModelDAL(db.session).update_task(id=id, title=title,
                                                                                 description=description)
                return {
                    "id": updated_task.id,
                    "title": updated_task.title,
                    "description": updated_task.description,
                    "created_at": updated_task.created_at,
                    "updated_at": updated_task.updated_at
                }
            except Exception as e:
                return {
                    f"ERROR": f"task with id = {id} does not exist"
                }


@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id) -> dict:
    """Удалить конкретную задачу"""
    if request.method == 'DELETE':
        with app.app_context():
            try:
                TaskModelDAL.TaskModelDAL(db.session).delete_task_by_id(id=id)
                return {
                    "task_id": "succesfully deleted"
                }
            except Exception as e:
                return {
                    f"ERROR": f"task_{id} delete failed - {e}"
                }


"""создание документации с помощью swagger-ui"""
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "TODO app"
    }
)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)

if __name__ == "__main__":
    app.run(debug=True)
