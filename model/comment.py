from extensions import db 
from datetime import datetime

class Comment(db.Model):
    __tablename__ = 'comment'

    id = db.Column("pk_comment", db.Integer, primary_key=True)
    text = db.Column(db.String(500))
    author = db.Column(db.String(80))
    n_estrela = db.Column(db.Integer)
    date_inserted = db.Column(db.DateTime, default=datetime.now())
    
    # Correção: O campo que armazena a chave estrangeira (FK) é geralmente nomeado com '_id'
    # Ele usa db.ForeignKey e aponta para 'tablename.column_name'
    product_id = db.Column(db.Integer, db.ForeignKey('product.pk_product'), nullable=False)
    
    # Relação: Permite acessar o objeto Product a partir do Comment
    product = db.relationship("Product", backref=db.backref('comments_list', lazy=True))


    def __init__(self, author: str, text: str, n_estrela: int = 0):
        self.author = author
        self.text = text
        self.n_estrela = n_estrela
        if date_inserted:
            self.date_inserted = date_inserted

    def __repr__(self):
        return f'<Comment by {self.author}>'