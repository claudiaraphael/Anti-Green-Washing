from flask import Blueprint, jsonify, request
from flasgger import swag_from
from extensions import db
from model.product import Product
from schemas.product_schemas import ProductInputSchema, ProductResponseSchema
import requests

# score ccalculator
from scripts.score_calculator import calculate_score


# Blueprint definition
product_bp = Blueprint('product', __name__)

# --- CRUD Operations ---

# CREATE (Scan & Save)


@product_bp.route('/product', methods=['POST'])
@swag_from({
    'tags': ['Product'],
    'summary': 'Scan and create a new product',
    'description': 'Receives a barcode, consults Open Food Facts, calculates score, and saves.',
    'parameters': [
        {
            'in': 'body',
            'name': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'required': ['barcode'],
                'properties': {
                    'barcode': {'type': 'string', 'example': '7891234567890'}
                }
            }
        }
    ],
    'responses': {
        201: {'description': 'Product analyzed and saved successfully'},
        404: {'description': 'Product not found in Open Food Facts'}
    }
})
def create_product():
    try:
        data = request.get_json()
        validated_data = ProductInputSchema(**data)
        barcode = validated_data.barcode

        # 1. Fetch from external API
        off_url = f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json"
        response = requests.get(off_url, timeout=10)
        product_data = response.json()

        if product_data.get("status") == 0:
            return jsonify({"error": "Product not found"}), 404

        off_info = product_data.get("product", {})

        # 2. Extract raw data for scoring
        nova = off_info.get("nova_groups")
        ing_tags = off_info.get("ingredients_analysis_tags", [])
        lab_tags = off_info.get("labels_tags", [])
        add_tags = off_info.get("additives_tags", [])

        # 3. CALCULATE THE SCORE using your script
        final_score = calculate_score(
            nova_group=nova,
            ingredients_tags=ing_tags,
            labels_tags=lab_tags,
            additives_tags=",".join(add_tags)
        )

        # 4. Save to Database
        new_product = Product(
            name=off_info.get("product_name", "Unknown Product"),
            barcode=barcode,
            image_url=off_info.get("image_front_url"),
            nova_group=nova,
            ingredients_analysis_tags=",".join(ing_tags),
            labels_tags=",".join(lab_tags),
            allergens_tags=",".join(off_info.get("allergens_tags", [])),
            additives_tags=",".join(add_tags),
            score=final_score  # Saved in the DB!
        )

        db.session.add(new_product)
        db.session.commit()

        # 5. Return the result
        return jsonify({
            "message": "Product scanned and saved successfully",
            "product": ProductResponseSchema.model_validate(new_product).model_dump()
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Internal error: {str(e)}"}), 400

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

        response_data = ProductResponseSchema.model_validate(
            product).model_dump()
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
