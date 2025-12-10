from flask import Flask, jsonify
from flask_cors import CORS
from extensions import db
from flask_openapi3 import OpenAPI 

# import data models to create data base tables
from model.product import Product
from model.comment import Comment
from model.user import User


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
    
    # CREATE FLASK APPLICATION AND INITIALIZE OpenAPI
    # The OpenAPI object acts as the Flask application.
    app = OpenAPI(__name__, info=info, doc_prefix='/api')
    
    # 2. Flask and SQLAlchemy Configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///antigreenwashing.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # 3. Extensions Initialization
    db.init_app(app)
    
    # CORS Configuration: connect front end to back end
    CORS(app, resources={
        r"/api/*": {
            "origins": ["http://127.0.0.1:5500"],
            "methods": ["GET", "POST", "PUT", "DELETE"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })

    # 4. Database Initialization
    with app.app_context():
        # Create tables if they do not exist
        db.create_all()

    # 5. Route Registration (Blueprints) - Next Step
    # Flask-OpenAPI3 uses Blueprints to organize routes.
    # Example: from routes.product import product_bp
    # app.register_api(product_bp)

    # Simple test route (Without Pydantic validation)
    @app.get('/test')
    def test_route():
        """
        This test route does not use Pydantic, but OpenAPI3 documents it.
        """
        return jsonify({"message": "API Funcionando com Flask-OpenAPI3!"})

    # Swagger documentation will be available at: /api/swagger
    # OpenAPI JSON specification will be at: /api/openapi.json
    
    return app

# Main execution block
if __name__ == '__main__':
    # Create the application instance
    app = create_app()
    app.run(debug=True, port=5000)