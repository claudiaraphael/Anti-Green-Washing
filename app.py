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
    app = OpenAPI(__name__, info=info)

    # Flask and SQLAlchemy Configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///antigreenwashing.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # db.init_app(app) initializes the SQLAlchemy database with the Flask app
    db.init_app(app)

    # CORS Configuration: connect front end to back end
    CORS(app, resources={
        r"/*": {
            "origins": ["http://127.0.0.1:5500", "http://localhost:5500"],
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
    @app.route('/test')
    def test_route():
        return jsonify({"message": "API Funcionando com Flask-OpenAPI3!"})

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)
