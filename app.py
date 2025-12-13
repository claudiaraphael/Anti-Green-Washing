from flask import Flask
from flask_cors import CORS
from extensions import db
from flask_openapi3 import OpenAPI

# import data models to create data base tables
from model.product import Product
from model.comment import Comment
from model.user import User

from schemas import *
from routes import *

# Function Application Factory


def create_app():
    """
    Creates and configures the Flask application, integrating OpenAPI 3.0.

    """

    # 1. API Configuration (Metadata for OpenAPI)
    info = {
        'title': 'Anti Green Washing API',
        'version': '2.0',
        'description': 'Anti Green Washing API for product sustainability verification',
    }

    # create flask application and initialize OpenAPI
    # The OpenAPI object acts as the Flask application.
    app = OpenAPI(__name__, info=info, doc_prefix='/api')

    # Flask and SQLAlchemy Configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///antigreenwashing.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # db.init_app(app) initializes the SQLAAlchemy database with the Flask app
    db.init_app(app)

    # CORS Configuration: connect front end to back end
    CORS(app, resources={
        r"/api/*": {
            "origins": ["http://127.0.0.1:5500"],
            "methods": ["GET", "POST", "PUT", "DELETE", "PATCH"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })

    # Database Initialization
    with app.app_context():
        # Create tables if they do not exist
        db.create_all()


    # ============================================
    # CONFIGURAÇÃO DO FLASGGER (SÓ AQUI NO APP.PY)
    # ============================================

    swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": 'apispec',
                "route": '/apispec.json',
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/api/docs"
    }

    swagger_template = {
        "swagger": "2.0",
        "info": {
            "title": "API Anti-Greenwashing",
            "description": "API para verificação de sustentabilidade de produtos",
            "version": "1.0.0",
            "contact": {
                "email": "suporte@antigreenwashing.com"
            }
        },
        "basePath": "/",
        "schemes": ["http", "https"],
        "tags": [
            {"name": "Products", "description": "Operações com produtos"},
            {"name": "Comments", "description": "Operações com comentários"},
            {"name": "Users", "description": "Operações com usuários"}
        ]
    }

    Swagger(app, config=swagger_config, template=swagger_template)

    # Route Registration (Blueprints)
    # IMPORTAR BLUEPRINTS AQUI DENTRO DA FUNÇÃO
    from routes.product_bp import product_bp
    from routes.user_bp import user_bp
    from routes.comment_bp import comment_bp

    # ============================================
    # REGISTRA OS BLUEPRINTS
    # ============================================

    app.register_blueprint(product_bp, url_prefix='/api')
    app.register_blueprint(comment_bp, url_prefix='/api')
    app.register_blueprint(user_bp, url_prefix='/api')

    # Simple test route (Without Pydantic validation)
    @app.route('/test')
    def test_route():
        """
        This test route does not use Pydantic, but OpenAPI3 documents it.
        """
        return jsonify({"message": "API Funcionando com Flask-OpenAPI3!"})

    return app


# Main execution block
if __name__ == '__main__':
    # Create the application instance
    app = create_app()
    app.run(debug=True, port=5000)

# Swagger documentation will be available at: /api/swagger
# OpenAPI JSON specification will be at: /api/openapi.json
