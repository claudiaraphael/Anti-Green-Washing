from flask import jsonify
from flask_cors import CORS
from extensions import db
from flask_openapi3 import OpenAPI

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
        'description': 'Anti Green Washing API for product sustainability verification',
    }

    # create flask application and initialize OpenAPI
    app = OpenAPI(__name__, info=info, doc_prefix='/api')

    # Flask and SQLAlchemy Configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///antigreenwashing.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # db.init_app(app) initializes the SQLAlchemy database with the Flask app
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

    # Route Registration (Blueprints)
    # CORRIGIDO: importar com 's' no final
    from routes.product_bp import products_bp
    from routes.user_bp import users_bp
    from routes.comment_bp import comments_bp

    # Registra os blueprints
    app.register_blueprint(products_bp, url_prefix='/api')
    app.register_blueprint(comments_bp, url_prefix='/api')
    app.register_blueprint(users_bp, url_prefix='/api')

    # Simple test route
    @app.route('/test')
    def test_route():
        """
        This test route does not use Pydantic, but OpenAPI3 documents it.
        """
        return jsonify({"message": "API Funcionando com Flask-OpenAPI3!"})

    return app


if __name__ == '__main__':
    # Create the application instance
    app = create_app()
    app.run(debug=True, port=5000)

# Swagger documentation will be available at: /api/swagger
# OpenAPI JSON specification will be at: /api/openapi.json