from extensions import db
from datetime import datetime


class Comment(db.Model):
    __tablename__ = 'comment'

    id = db.Column("pk_comment", db.Integer, primary_key=True)
    text = db.Column(db.String(500))
    author = db.Column(db.String(80))
    n_estrela = db.Column(db.Integer)
    date_inserted = db.Column(db.DateTime, default=datetime.now)  # SEM ()

    # Foreign Key
    product_id = db.Column(db.Integer, db.ForeignKey(
        'product.pk_product'), nullable=False)

    def __init__(self, author: str, text: str, n_estrela: int = 0):
        self.author = author
        self.text = text
        self.n_estrela = n_estrela

    def __repr__(self):
        return f'<Comment by {self.author}>'
