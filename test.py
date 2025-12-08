from flask import Flask, jsonify, request
from flasgger import Swagger, swag_from
import json

app = Flask(__name__)

# Swagger configuration
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
        "title": "Product Management API",
        "description": "API for user registration and product management with external API integration",
        "version": "1.0.0",
        "contact": {
            "name": "Your Name",
            "email": "your.email@example.com"
        }
    },
    "securityDefinitions": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "JWT Authorization header using the Bearer scheme. Example: 'Bearer {token}'"
        }
    },
    "tags": [
        {
            "name": "Users",
            "description": "User management endpoints"
        },
        {
            "name": "Products",
            "description": "Product management endpoints"
        }
    ]
}

swagger = Swagger(app, config=swagger_config, template=swagger_template)

# In-memory databases (replace with actual database)
users_db = []
products_db = []
user_id_counter = 1
product_id_counter = 1


# JSON specs for each endpoint
register_user_spec = {
    "tags": ["Users"],
    "summary": "Register a new user",
    "description": "Creates a new user account in the system",
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "type": "object",
                "required": ["username", "email", "password"],
                "properties": {
                    "username": {
                        "type": "string",
                        "example": "john_doe",
                        "minLength": 3,
                        "maxLength": 50
                    },
                    "email": {
                        "type": "string",
                        "format": "email",
                        "example": "john@example.com"
                    },
                    "password": {
                        "type": "string",
                        "format": "password",
                        "example": "SecurePass123!",
                        "minLength": 8
                    },
                    "full_name": {
                        "type": "string",
                        "example": "John Doe"
                    }
                }
            }
        }
    ],
    "responses": {
        "201": {
            "description": "User registered successfully",
            "schema": {
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                        "example": "User registered successfully"
                    },
                    "user": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "integer", "example": 1},
                            "username": {"type": "string", "example": "john_doe"},
                            "email": {"type": "string", "example": "john@example.com"},
                            "full_name": {"type": "string", "example": "John Doe"}
                        }
                    }
                }
            }
        },
        "400": {
            "description": "Invalid input or user already exists",
            "schema": {
                "type": "object",
                "properties": {
                    "error": {"type": "string", "example": "Username already exists"}
                }
            }
        }
    }
}

add_product_spec = {
    "tags": ["Products"],
    "summary": "Add a new product",
    "description": "Creates a new product in the local database",
    "security": [{"Bearer": []}],
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "type": "object",
                "required": ["name", "price", "category"],
                "properties": {
                    "name": {
                        "type": "string",
                        "example": "Gaming Laptop"
                    },
                    "description": {
                        "type": "string",
                        "example": "High-performance gaming laptop with RTX 4080"
                    },
                    "price": {
                        "type": "number",
                        "format": "float",
                        "example": 1499.99,
                        "minimum": 0
                    },
                    "category": {
                        "type": "string",
                        "example": "Electronics"
                    },
                    "stock_quantity": {
                        "type": "integer",
                        "example": 50,
                        "minimum": 0
                    },
                    "sku": {
                        "type": "string",
                        "example": "LAPTOP-001"
                    }
                }
            }
        }
    ],
    "responses": {
        "201": {
            "description": "Product created successfully",
            "schema": {
                "type": "object",
                "properties": {
                    "message": {"type": "string", "example": "Product added successfully"},
                    "product": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "integer", "example": 1},
                            "name": {"type": "string", "example": "Gaming Laptop"},
                            "price": {"type": "number", "example": 1499.99},
                            "category": {"type": "string", "example": "Electronics"}
                        }
                    }
                }
            }
        },
        "400": {"description": "Invalid input"},
        "401": {"description": "Unauthorized - missing or invalid token"}
    }
}

get_product_spec = {
    "tags": ["Products"],
    "summary": "Retrieve product data",
    "description": "Gets product from local database or external API if not found locally. Use 'source' query param to force external API lookup.",
    "parameters": [
        {
            "name": "product_id",
            "in": "path",
            "type": "integer",
            "required": True,
            "description": "The product ID"
        },
        {
            "name": "source",
            "in": "query",
            "type": "string",
            "required": False,
            "enum": ["local", "external", "auto"],
            "default": "auto",
            "description": "Data source: 'local' (database only), 'external' (API only), or 'auto' (try local first, then external)"
        }
    ],
    "responses": {
        "200": {
            "description": "Product found",
            "schema": {
                "type": "object",
                "properties": {
                    "product": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "integer", "example": 1},
                            "name": {"type": "string", "example": "Gaming Laptop"},
                            "description": {"type": "string"},
                            "price": {"type": "number", "example": 1499.99},
                            "category": {"type": "string", "example": "Electronics"},
                            "stock_quantity": {"type": "integer", "example": 50},
                            "sku": {"type": "string", "example": "LAPTOP-001"}
                        }
                    },
                    "source": {
                        "type": "string",
                        "enum": ["local_database", "external_api"],
                        "example": "local_database"
                    }
                }
            }
        },
        "404": {
            "description": "Product not found",
            "schema": {
                "type": "object",
                "properties": {
                    "error": {"type": "string", "example": "Product not found in database or external API"}
                }
            }
        }
    }
}

update_product_spec = {
    "tags": ["Products"],
    "summary": "Update product information",
    "description": "Updates an existing product in the local database",
    "security": [{"Bearer": []}],
    "parameters": [
        {
            "name": "product_id",
            "in": "path",
            "type": "integer",
            "required": True,
            "description": "The product ID to update"
        },
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {
                    "name": {"type": "string", "example": "Updated Gaming Laptop"},
                    "description": {"type": "string"},
                    "price": {"type": "number", "example": 1399.99},
                    "category": {"type": "string"},
                    "stock_quantity": {"type": "integer", "example": 45},
                    "sku": {"type": "string"}
                },
                "description": "All fields are optional. Only provided fields will be updated."
            }
        }
    ],
    "responses": {
        "200": {
            "description": "Product updated successfully",
            "schema": {
                "type": "object",
                "properties": {
                    "message": {"type": "string", "example": "Product updated successfully"},
                    "product": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "integer"},
                            "name": {"type": "string"},
                            "price": {"type": "number"},
                            "category": {"type": "string"}
                        }
                    }
                }
            }
        },
        "404": {"description": "Product not found"},
        "401": {"description": "Unauthorized"}
    }
}

delete_product_spec = {
    "tags": ["Products"],
    "summary": "Delete a product",
    "description": "Removes a product from the local database",
    "security": [{"Bearer": []}],
    "parameters": [
        {
            "name": "product_id",
            "in": "path",
            "type": "integer",
            "required": True,
            "description": "The product ID to delete"
        }
    ],
    "responses": {
        "200": {
            "description": "Product deleted successfully",
            "schema": {
                "type": "object",
                "properties": {
                    "message": {"type": "string", "example": "Product deleted successfully"},
                    "deleted_product_id": {"type": "integer", "example": 1}
                }
            }
        },
        "404": {
            "description": "Product not found",
            "schema": {
                "type": "object",
                "properties": {
                    "error": {"type": "string", "example": "Product not found"}
                }
            }
        },
        "401": {"description": "Unauthorized"}
    }
}


# Routes with JSON specs applied via decorator
@app.route('/api/register', methods=['POST'])
@swag_from(register_user_spec)
def register_user():
    """Register a new user"""
    global user_id_counter
    
    data = request.get_json()
    
    # Validation
    if not data or not all(k in data for k in ['username', 'email', 'password']):
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Check if user exists
    if any(u['username'] == data['username'] for u in users_db):
        return jsonify({'error': 'Username already exists'}), 400
    
    if any(u['email'] == data['email'] for u in users_db):
        return jsonify({'error': 'Email already exists'}), 400
    
    # Create user (in production, hash the password!)
    user = {
        'id': user_id_counter,
        'username': data['username'],
        'email': data['email'],
        'full_name': data.get('full_name', '')
    }
    users_db.append(user)
    user_id_counter += 1
    
    return jsonify({
        'message': 'User registered successfully',
        'user': user
    }), 201


@app.route('/api/products', methods=['POST'])
@swag_from(add_product_spec)
def add_product():
    """Add a new product to the database"""
    global product_id_counter
    
    data = request.get_json()
    
    # Validation
    if not data or not all(k in data for k in ['name', 'price', 'category']):
        return jsonify({'error': 'Missing required fields: name, price, category'}), 400
    
    if data['price'] < 0:
        return jsonify({'error': 'Price must be positive'}), 400
    
    # Create product
    product = {
        'id': product_id_counter,
        'name': data['name'],
        'description': data.get('description', ''),
        'price': data['price'],
        'category': data['category'],
        'stock_quantity': data.get('stock_quantity', 0),
        'sku': data.get('sku', f'PROD-{product_id_counter:05d}')
    }
    products_db.append(product)
    product_id_counter += 1
    
    return jsonify({
        'message': 'Product added successfully',
        'product': product
    }), 201


@app.route('/api/products/<int:product_id>', methods=['GET'])
@swag_from(get_product_spec)
def get_product(product_id):
    """
    Retrieve product from local database or external API
    
    This endpoint implements a smart lookup strategy:
    1. If source='local' or 'auto': Check local database first
    2. If not found and source='auto' or 'external': Query external API
    3. If found in external API, optionally cache it locally
    """
    source = request.args.get('source', 'auto')
    
    # Try local database first (unless explicitly requesting external only)
    if source in ['local', 'auto']:
        product = next((p for p in products_db if p['id'] == product_id), None)
        if product:
            return jsonify({
                'product': product,
                'source': 'local_database'
            }), 200
        
        # If source is 'local' only and not found, return 404
        if source == 'local':
            return jsonify({'error': 'Product not found in local database'}), 404
    
    # Try external API (if source is 'external' or 'auto' and not found locally)
    if source in ['external', 'auto']:
        # TODO: Replace this with your actual external API call
        # Example: response = requests.get(f'https://api.example.com/products/{product_id}')
        
        # Simulated external API response
        external_product = fetch_from_external_api(product_id)
        
        if external_product:
            # Optionally cache it locally for future requests
            # external_product['id'] = product_id  # Ensure ID matches
            # products_db.append(external_product)
            
            return jsonify({
                'product': external_product,
                'source': 'external_api'
            }), 200
    
    return jsonify({'error': 'Product not found in database or external API'}), 404


def fetch_from_external_api(product_id):
    """
    Simulates fetching from an external API
    
    In production, replace this with actual API call:
    
    import requests
    
    def fetch_from_external_api(product_id):
        try:
            response = requests.get(
                f'https://api.example.com/products/{product_id}',
                headers={'Authorization': 'Bearer YOUR_API_KEY'},
                timeout=5
            )
            if response.status_code == 200:
                return response.json()
            return None
        except requests.exceptions.RequestException as e:
            print(f'External API error: {e}')
            return None
    """
    # Simulated external data
    if product_id == 999:  # Mock external product
        return {
            'id': product_id,
            'name': 'External Product',
            'description': 'Product from external API',
            'price': 99.99,
            'category': 'External',
            'stock_quantity': 100,
            'sku': 'EXT-999'
        }
    return None


@app.route('/api/products/<int:product_id>', methods=['PUT'])
@swag_from(update_product_spec)
def update_product(product_id):
    """Update product information in local database"""
    data = request.get_json()
    
    # Find product
    product = next((p for p in products_db if p['id'] == product_id), None)
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    
    # Update fields (only if provided)
    if 'name' in data:
        product['name'] = data['name']
    if 'description' in data:
        product['description'] = data['description']
    if 'price' in data:
        if data['price'] < 0:
            return jsonify({'error': 'Price must be positive'}), 400
        product['price'] = data['price']
    if 'category' in data:
        product['category'] = data['category']
    if 'stock_quantity' in data:
        if data['stock_quantity'] < 0:
            return jsonify({'error': 'Stock quantity must be non-negative'}), 400
        product['stock_quantity'] = data['stock_quantity']
    if 'sku' in data:
        product['sku'] = data['sku']
    
    return jsonify({
        'message': 'Product updated successfully',
        'product': product
    }), 200


@app.route('/api/products/<int:product_id>', methods=['DELETE'])
@swag_from(delete_product_spec)
def delete_product(product_id):
    """Delete product from local database"""
    global products_db
    
    # Find product
    product = next((p for p in products_db if p['id'] == product_id), None)
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    
    # Remove from database
    products_db = [p for p in products_db if p['id'] != product_id]
    
    return jsonify({
        'message': 'Product deleted successfully',
        'deleted_product_id': product_id
    }), 200


# Optional: List all products endpoint
@app.route('/api/products', methods=['GET'])
def list_products():
    """
    List all products
    ---
    tags:
      - Products
    responses:
      200:
        description: List of all products
        schema:
          type: object
          properties:
            products:
              type: array
              items:
                type: object
            count:
              type: integer
    """
    return jsonify({
        'products': products_db,
        'count': len(products_db)
    }), 200


if __name__ == '__main__':
    # Add some sample data for testing
    users_db.append({
        'id': 1,
        'username': 'testuser',
        'email': 'test@example.com',
        'full_name': 'Test User'
    })
    user_id_counter = 2
    
    products_db.append({
        'id': 1,
        'name': 'Sample Laptop',
        'description': 'A sample product',
        'price': 999.99,
        'category': 'Electronics',
        'stock_quantity': 10,
        'sku': 'PROD-00001'
    })
    product_id_counter = 2
    
    print("\n" + "="*60)
    print("🚀 Flask API Server Starting...")
    print("="*60)
    print(f"📖 Swagger UI: http://localhost:5000/apidocs/")
    print(f"📋 API Spec: http://localhost:5000/apispec.json")
    print("="*60 + "\n")
    
    app.run(debug=True, port=5000)