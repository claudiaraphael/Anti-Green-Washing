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
