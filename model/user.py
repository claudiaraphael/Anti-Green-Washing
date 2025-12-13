from extensions import db  # Importa a instância global do Flask-SQLAlchemy
from datetime import datetime
from sqlalchemy.orm import relationship


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now)  # SEM ()

    def __init__(self, username: str, email: str):
        self.username = username
        self.email = email

    def __repr__(self):
        return f'<User {self.username}>'
