from flask import Flask, jsonify, request
from flasgger import Swagger, swag_from
from extensions import db
import json

from model.product import Product
from model.comment import Comment
from model.user import User

def create_app(config_name='development'):
    app = Flask(__name__)

    # database config: db
    if config_name == 'testing':
        # SQLite em memória para testes (ISOLAMENTO!)
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['TESTING'] = True
    else:
        # SQLite em arquivo (Desenvolvimento/Produção)
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///antigreenwashing.db'

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # VINCULA o objeto 'db' ao App (com as configurações acima)
    db.init_app(app)

    with app.app_context():
        # db.create_all() usa os modelos que foram importados acima (model.product, etc.)
        db.create_all()

    # Swagger configuration

    if __name__ == '__main__':
        app = create_app()
        app.run(debug=True)

    return app




create_app()
   

@app.get('/')
def hello_world():
    return 'chill out vaporwave mix'