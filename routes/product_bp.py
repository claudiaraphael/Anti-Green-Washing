from flask import Blueprint, jsonify, request
from extensions import db
from model.product import Product
from schemas.product_schemas import ProductInputSchema, ProductResponseSchema

# Criar blueprint padrão do Flask
products_bp = Blueprint('products', __name__)


@products_bp.route('/products', methods=['POST'])
def create_product():
    """
    Cria um novo produto no banco de dados.
    """
    try:
        data = request.get_json()
        
        # Validar com Pydantic
        validated_data = ProductInputSchema(**data)
        
        # Criar instância do produto
        new_product = Product(
            name=validated_data.name,
            barcode=validated_data.barcode,
            date_inserted=None  # usa default
        )
        
        # Adicionar e commitar
        db.session.add(new_product)
        db.session.commit()
        
        # Retornar resposta
        return jsonify({
            "message": "Produto criado com sucesso",
            "product": {
                "id": new_product.id,
                "name": new_product.name,
                "barcode": new_product.barcode,
                "eco_score": new_product.eco_score,
                "date_inserted": new_product.date_inserted.isoformat() if new_product.date_inserted else None
            }
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400


@products_bp.route('/products', methods=['GET'])
def get_all_products():
    """
    Lista todos os produtos.
    """
    products = Product.query.all()
    return jsonify({
        "products": [
            {
                "id": p.id,
                "name": p.name,
                "barcode": p.barcode,
                "eco_score": p.eco_score,
                "date_inserted": p.date_inserted.isoformat() if p.date_inserted else None
            }
            for p in products
        ]
    }), 200


@products_bp.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """
    Busca um produto pelo ID.
    """
    product = Product.query.get_or_404(product_id)
    return jsonify({
        "id": product.id,
        "name": product.name,
        "barcode": product.barcode,
        "eco_score": product.eco_score,
        "date_inserted": product.date_inserted.isoformat() if product.date_inserted else None
    }), 200


@products_bp.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    """
    Deleta um produto pelo ID.
    """
    product = Product.query.get_or_404(product_id)
    
    try:
        db.session.delete(product)
        db.session.commit()
        return jsonify({"message": "Produto deletado com sucesso"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400