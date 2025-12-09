from flask import Flask, jsonify, request
from flasgger import Swagger, swag_from
from extensions import db
import json

# import blueprints
from routes.product import Product
from routes.comment import Comment
from routes.user import Users

def create_app(config_name='development'):
    app = Flask(__name__)

    # database config: db
    if config_name == 'testing':
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:' # SQLite em memória para testes (ISOLAMENTO!)
        app.config['TESTING'] = True
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///antigreenwashing.db' # # SQLite em arquivo (Desenvolvimento/Produção)
        
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app) # VINCULA o objeto 'db' ao App (com as configurações acima)

    with app.app_context():
        db.create_all()         # db.create_all() usa os modelos que foram importados acima (model.product, etc.)



    # Swagger configuration



    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)