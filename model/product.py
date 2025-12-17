from extensions import db  # Importa o db globalmente definido
from datetime import datetime
from sqlalchemy.orm import relationship


class Product(db.Model):
    __tablename__ = 'product'

    id = db.Column("pk_product", db.Integer, primary_key=True)
    name = db.Column(db.String(140)) # removed unique because nomes podem se repetir, o barcode é o ID real
    barcode = db.Column(db.String(50), unique=True)
    image_url = db.Column(db.String(255), nullable=True)
    date_inserted = db.Column(db.DateTime, default=datetime.now)

    # Truth Label Core Data
    score = db.Column(db.Float, nullable=True)

    comments = db.relationship("Comment", backref="product", lazy=True)
    nova_group = db.Column(db.Integer, nullable=True) # Prioridade Média

    def __init__(self, name: str, barcode: str, date_inserted=None):
        self.name = name
        self.barcode = barcode
        if date_inserted:
            self.date_inserted = date_inserted

    def __repr__(self):
        return f'<Product {self.name}>'
