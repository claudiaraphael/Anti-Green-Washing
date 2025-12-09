from flask import Flask, jsonify, request
from flasgger import Swagger, swag_from
from extensions import db
import json

# import blueprints
from routes.products import products
from routes.comments import comments
from routes.users import users

def create_app():
    app = Flask(__name__)

    # config
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///antigreenwashing.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # Swagger configuration
    


    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True)