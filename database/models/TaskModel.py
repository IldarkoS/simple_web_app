from werkzeug.routing import ValidationError
from extensions import db
import datetime
from sqlalchemy.orm import validates


class TaskModel(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now())

    """Две функции валидации, одна для поля title, вторая для поля description:
    - поля не могут быть пустыми
    - тип данных только string
    - ограничение по количеству символов
    """
    @validates('title')
    def validate_title(self, key, title):
        if not title:
            raise ValidationError('Title cannot be empty')
        if not isinstance(title, str):
            raise ValidationError('Title must be a string')
        if len(title) > 250:
            raise ValidationError('Title must be less than 250 characters')
        return title

    @validates('description')
    def validate_description(self, key, description):
        if not description:
            raise ValidationError('Description cannot be empty')
        if not isinstance(description, str):
            raise ValidationError('Description must be a string')
        if len(description) > 2**16 - 1:
            raise ValidationError('Description must be smaller')
        return description
