from flask import Blueprint, jsonify, request
from flasgger import swag_from
from extensions import db
from model.product import Product
from schemas.product_schemas import ProductInputSchema, ProductResponseSchema
import requests

# Blueprint definition
product_bp = Blueprint('product', __name__)

# --- CRUD Operations ---

# CREATE (Scan & Save)
@product_bp.route('api/product', methods=['POST'])
@swag_from({
    'tags': ['Product'],
    'summary': 'Scan and create a new product',
    'description': 'Receives a barcode, consults Open Food Facts, and saves the product to the local history.',
    'parameters': [
        {
            'in': 'body',
            'name': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'required': ['barcode'],
                'properties': {
                    'barcode': {'type': 'string', 'example': '7891234567890'},
                    'user_id': {'type': 'integer', 'example': 1}
                }
            }
        }
    ],
    'responses': {
        201: {
            'description': 'Product scanned and saved successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string'},
                    'product': {'type': 'object'}
                }
            }
        },
        400: {'description': 'Validation error or invalid barcode'},
        404: {'description': 'Product not found in the Global Database'},
        502: {'description': 'Error communicating with the external API'}
    }
})
def create_product():
    """
    Workflow: Receive barcode -> Query Open Food Facts -> Extract Tags & Image -> Save to SQLite.
    """
    try:
        # 1. Obtain and validate barcode via Pydantic
        data = request.get_json()
        validated_data = ProductInputSchema(**data)
        barcode = validated_data.barcode

        # 2. Call Open Food Facts API
        off_url = f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json"
        try:
            response = requests.get(off_url, timeout=10)
            response.raise_for_status()
        except requests.exceptions.RequestException:
            return jsonify({"error": "Failed to connect to Open Food Facts"}), 502

        product_data = response.json()

        # Status 0 means the product was not found
        if product_data.get("status") == 0:
            return jsonify({"error": "Product not found in the global database"}), 404

        # 3. Extract data from the external API
        off_info = product_data.get("product", {})

        # Mapping to Product model
        name = off_info.get("product_name", "Unknown Product")
        image_url = off_info.get("image_front_url")
        nova_group = off_info.get("nova_groups")

        # Tag processing (converting lists to comma-separated strings for SQLite Text field)
        ingredients_tags = ",".join(off_info.get("ingredients_analysis_tags", []))
        labels_tags = ",".join(off_info.get("labels_tags", []))
        allergens_tags = ",".join(off_info.get("allergens_tags", []))
        additives_tags = ",".join(off_info.get("additives_tags", []))

        # 4. Create SQLAlchemy Model Instance
        # Score starts at 0.0 until the score function is implemented
        new_product = Product(
            name=name,
            barcode=barcode,
            image_url=image_url,
            nova_group=nova_group,
            ingredients_analysis_tags=ingredients_tags,
            labels_tags=labels_tags,
            allergens_tags=allergens_tags,
            additives_tags=additives_tags,
            score=0.0
        )

        # 5. Persist in Database
        db.session.add(new_product)
        db.session.commit()

        # 6. Serialize response via Pydantic
        response_data = ProductResponseSchema.model_validate(new_product).model_dump()

        return jsonify({
            "message": "Product scanned and saved successfully",
            "product": response_data
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Internal error: {str(e)}"}), 400


# READ (History)
@product_bp.route('/product', methods=['GET'])
@swag_from({
    'tags': ['Product'],
    'summary': 'List product history',
    'description': 'Returns a list of all scanned products, including scores and images.',
    'responses': {
        200: {
            'description': 'List of products retrieved successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'products': {
                        'type': 'array',
                        'items': {'$ref': '#/definitions/ProductResponse'}
                    }
                }
            }
        }
    }
})
def get_all_products():
    """
    Lists all products saved in the local database.
    """
    # Order by insertion date (newest first)
    products = Product.query.order_by(Product.date_inserted.desc()).all()

    # Pydantic processes the list including tags, image_url, and score
    products_list = [
        ProductResponseSchema.model_validate(p).model_dump()
        for p in products
    ]

    return jsonify({"products": products_list}), 200


# READ (Single Product)
@product_bp.route('/product/<int:product_id>', methods=['GET'])
@swag_from({
    'tags': ['Product'],
    'summary': 'View product details',
    'description': 'Returns all details of a specific product from the local database.',
    'responses': {
        200: {'description': 'Product data found'},
        404: {'description': 'Product not found in history'}
    }
})
def get_product(product_id):
    product = Product.query.get_or_404(product_id)
    response_data = ProductResponseSchema.model_validate(product).model_dump()
    return jsonify(response_data), 200


# UPDATE
@product_bp.route('/product/<int:product_id>', methods=['PATCH'])
@swag_from({
    'tags': ['Product'],
    'summary': 'Update local product',
    'description': 'Updates the name or barcode of a product in the history.',
    'parameters': [
        {
            'in': 'path',
            'name': 'product_id',
            'type': 'integer',
            'required': True,
            'description': 'Product ID'
        },
        {
            'in': 'body',
            'name': 'body',
            'schema': {
                'type': 'object',
                'properties': {
                    'name': {'type': 'string', 'example': 'New Name'},
                    'barcode': {'type': 'string', 'example': '123456789'}
                }
            }
        }
    ],
    'responses': {
        200: {'description': 'Product updated successfully'},
        404: {'description': 'Product not found'}
    }
})
def update_product(product_id):
    product = Product.query.get_or_404(product_id)

    try:
        data = request.get_json()

        if 'name' in data:
            product.name = data['name']

        if 'barcode' in data:
            product.barcode = data['barcode']

        db.session.commit()

        response_data = ProductResponseSchema.model_validate(product).model_dump()
        return jsonify({
            "message": "Product updated successfully",
            "product": response_data
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400


# DELETE
@product_bp.route('/product/<int:product_id>', methods=['DELETE'])
@swag_from({
    'tags': ['Product'],
    'summary': 'Remove from history',
    'description': 'Permanently deletes a product from the local database.',
    'responses': {
        200: {'description': 'Removed successfully'},
        404: {'description': 'Not found'}
    }
})
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)

    try:
        db.session.delete(product)
        db.session.commit()
        return jsonify({"message": f"Product {product_id} removed from history"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400