from sqlalchemy.orm import Session
from database.models.TaskModel import TaskModel
import datetime


class TaskModelDAL:
    def __init__(self, session: Session):
        self.session = session

    def create_task(self, title, description) -> TaskModel:
        """Функция создания и записи в базу данных новой задачи"""
        task = TaskModel(title=title, description=description)
        self.session.add(task)
        self.session.commit()
        return task

    def get_all_tasks(self):
        """Получение всех записей задач из базы данных в виде списка"""
        return self.session.query(TaskModel).filter(TaskModel.id is not None).all()

    def get_task_by_id(self, id) -> TaskModel:
        """Получение конкретной записи задачи из таблицы, поиск по полю id"""
        return self.session.query(TaskModel).filter(TaskModel.id == id).first()

    def update_task(self, id, title=None, description=None) -> TaskModel:
        """Обновление уже существующей записи в базе данных, поиск по полю id"""
        current = self.session.query(TaskModel).filter(TaskModel.id == id).first()
        if title is not None:
            current.title = title
        if description is not None:
            current.description = description
        current.updated_at = datetime.datetime.now()
        self.session.commit()
        return current

    def delete_task_by_id(self, id) -> None:
        """Удаление записи по полю id"""
        self.session.query(TaskModel).filter(TaskModel.id == id).delete()
        self.session.commit()
