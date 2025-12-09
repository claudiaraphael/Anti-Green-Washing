# ============================================
# ARQUIVO: app.py (ARQUIVO PRINCIPAL)
# ============================================

from flask import Flask
from flasgger import Swagger
from extensions import db

# Import dos blueprints
from routes.products import products_bp
from routes.comments import comments_bp
from routes.users import users_bp


def create_app():
    app = Flask(__name__)

    # Configurações
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///antigreenwashing.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inicializa extensões
    db.init_app(app)

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

    # ============================================
    # REGISTRA OS BLUEPRINTS
    # ============================================

    app.register_blueprint(products_bp, url_prefix='/api')
    app.register_blueprint(comments_bp, url_prefix='/api')
    app.register_blueprint(users_bp, url_prefix='/api')

    return app


if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True)
