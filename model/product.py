from extensions import db  # Importa o db globalmente definido
from datetime import datetime
from sqlalchemy.orm import relationship


class Product(db.Model):
    __tablename__ = 'product'

    id = db.Column("pk_product", db.Integer, primary_key=True)
    # removed unique because nomes podem se repetir, o barcode é o ID real
    name = db.Column(db.String(140))
    barcode = db.Column(db.String(50), unique=True)
    image_url = db.Column(db.String(255), nullable=True)
    date_inserted = db.Column(db.DateTime, default=datetime.now)

    # Truth Label Core Data
    score = db.Column(db.Float, nullable=True)
    nova_group = db.Column(db.Integer, nullable=True)  # Prioridade Média

    # Tags armazenadas como String (Text para não haver limite de caracteres)
    ingredients_analysis_tags = db.Column(
        db.Text, nullable=True)  # Prioridade Alta
    # Prioridade Alta
    labels_tags = db.Column(db.Text, nullable=True)
    allergens_tags = db.Column(
        db.Text, nullable=True)            # Prioridade Baixa
    additives_tags = db.Column(
        db.Text, nullable=True)            # Prioridade Média

    comments = db.relationship(
        "Comment", backref="product", lazy=True, cascade="all, delete-orphan")

    def __init__(self, name, barcode, score=None, image_url=None, nova_group=None,
                 ingredients_analysis_tags=None, labels_tags=None,
                 allergens_tags=None, additives_tags=None, date_inserted=None):
        self.name = name
        self.barcode = barcode
        self.score = score
        self.image_url = image_url
        self.nova_group = nova_group
        self.ingredients_analysis_tags = ingredients_analysis_tags
        self.labels_tags = labels_tags
        self.allergens_tags = allergens_tags
        self.additives_tags = additives_tags

        if date_inserted:
            self.date_inserted = date_inserted

    def __repr__(self):
        return f'<Product {self.name} - Score: {self.score}>'
