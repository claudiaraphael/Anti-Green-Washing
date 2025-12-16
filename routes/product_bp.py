from flask import Blueprint, jsonify, request
from extensions import db
from model.product import Product
from schemas.product_schemas import ProductInputSchema, ProductResponseSchema

# Criar blueprint padrão do Flask
product_bp = Blueprint('product', __name__)

# CRUD
# Create


@product_bp.route('/product', methods=['POST'])
def create_product():
    """
    Creates a new product in the database

    Uses Kwargs to transfer data.

    It's commonly used in APIs with Flask when you want flexibility in parameters without having to explicitly define them.

    Creates an instance of the SQLAlchemy Product model. The model_dump(exclude_unset=True) converts the validated Pydantic object back to a dictionary, excluding fields that weren't set in the request. The ** unpacks the dictionary as named arguments.

    Converts the SQLAlchemy `new_product` object to the Pydantic `ProductResponseSchema` (validating the response structure) and then transforms it into a dictionary with `model_dump()`.

    Returns JSON with success message and product data, with HTTP status 201 (Created).

    If any error occurs (Pydantic validation, database error, etc.), rolls back any pending changes in the SQLAlchemy session.

    Returns formatted error as JSON with status 400 (Bad Request).

    Flow summary: receives JSON → validates with Pydantic → creates SQLAlchemy model → saves to database → formats response with Pydantic → returns JSON.

    """
    try:
        # 1. obtain data (pydantic)
        data = request.get_json()

        # validate data according to the schema (pydantic)
        validated_data = ProductInputSchema(**data)
        # if there is something wrong, it raises an exception

        # 2. Create instance of the SQLAlchemy model
        # **kwargs facilitates trasnfering all the key-value pairs
        # **kwargs = dicionario de argumentos nomeados
        new_product = Product(**validated_data.model_dump(exclude_unset=True))

        # 3. Persist in the data base
        # adds new product to staging area (sqlalchemy) - not yet saved
        db.session.add(new_product)

        db.session.commit()  # executes SQL: INSERT in the data base, persisting the

        # 4. Return Response - using ProductResponseSchema
        response_data = ProductResponseSchema.model_validate(
            new_product).model_dump()

        return jsonify({
            "message": "Produto criado com sucesso",
            "product": response_data
        }), 201

    except Exception as e:
        db.session.rollback()
        # If Pydantic validation fails (e.g., missing field), the error is caught here.
        return jsonify({"error": str(e)}), 400
