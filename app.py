from flask import Flask, jsonify
from flask_cors import CORS
from flasgger import Swagger
from extensions import db

# import data models to create data base tables
from model.product import Product
from model.comment import Comment
from model.user import User


def create_app():
    """
    Creates and configures the Flask application, integrating OpenAPI 3.0.
    """

    # API Configuration (Metadata for OpenAPI)
    info = {
        'title': 'Anti Green Washing API',
        'version': '2.0',
        'description': 'Anti Green Washing API for product sustainability verification. The app scans products barcodes and takes data from the Open Food Facts API and returns data about sustainability certificates that brand has. The user can also add more data.',
    }

    # create flask application and initialize OpenAPI
    app = Flask(__name__)

    # Flask and SQLAlchemy Configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///antigreenwashing.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Swagger Config

    swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": 'apispec',
                "route": '/apispec.json',
                "rule_filter": lambda rule: True,
                "model_filter": lambda tag: True,
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/apidocs/"
    }

    swagger_template = {
        "info": {
            "title": "Anti Green Washing API",
            "description": "API para verificação de sustentabilidade de produtos. Escaneia códigos de barras e consulta dados do Open Food Facts para retornar certificações de sustentabilidade.",
            "version": "2.0",
            "contact": {
                "name": "API Support",
                "email": "seu-email@exemplo.com"
            }
        },
        "schemes": ["http"],
        "tags": [
            {
                "name": "Product",
                "description": "Operações relacionadas a produtos"
            },
            {
                "name": "User",
                "description": "Operações relacionadas a usuários"
            },
            {
                "name": "Comment",
                "description": "Operações relacionadas a comentários"
            }
        ]
    }

    # Inicializar Swagger
    Swagger(app, config=swagger_config, template=swagger_template)

    # db.init_app(app) initializes the SQLAlchemy database with the Flask app
    db.init_app(app)

    # CORS Configuration: connect front end to back end
    CORS(app, resources={
        r"/*": {
            "origins": ["http://127.0.0.1:5500", "http://localhost:5500", "http://127.0.0.1:5500/index.html"],
            "methods": ["GET", "POST", "PUT", "DELETE", "PATCH"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })

    # Database Initialization
    with app.app_context():
        db.create_all()

    # Route Registration (Blueprints)
    from routes.product_bp import product_bp
    from routes.user_bp import user_bp
    from routes.comment_bp import comment_bp

    app.register_blueprint(product_bp, url_prefix='/api')
    app.register_blueprint(comment_bp, url_prefix='/api')
    app.register_blueprint(user_bp, url_prefix='/api')

    # Simple test route
    @app.route('/')
    def home():
        return 'Anti Green Washing API v2.0'

    @app.route('/test')
    def test_route():
        return jsonify({"message": "API Funcionando com Flask-OpenAPI3!"})

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)
