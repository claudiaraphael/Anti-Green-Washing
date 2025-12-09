from extensions import db # Importa a instância global do Flask-SQLAlchemy
from datetime import datetime
from sqlalchemy.orm import relationship
from typing import Union

# Agora herda de db.Model 
class User(db.Model): 
    __tablename__ = 'user' # Padrão é minúsculo

    # Usando db.Column e db.Integer/String/DateTime
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now())
    
    # Usando db.relationship
    products = db.relationship("Product", back_populates="owner")
    comments = db.relationship("Comment", back_populates="author")
    
    def __repr__(self):
        return f'<User {self.username}>'