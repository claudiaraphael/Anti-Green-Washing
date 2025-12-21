from flask import Blueprint, jsonify, request
from flasgger import swag_from
from extensions import db
from model.product import Product
from schemas.product_schemas import ProductInputSchema, ProductResponseSchema
import requests

# score calculator
from scripts.score_calculator import calculate_score


# Blueprint definition
product_bp = Blueprint('product', __name__)


# ========== FUNÇÕES AUXILIARES (HELPERS) ==========

def buscar_produto_no_db(barcode):
    """
    Busca um produto no banco de dados local pelo código de barras.

    Args:
        barcode (str): Código de barras do produto

    Returns:
        Product | None: Objeto Product se encontrado, None caso contrário
    """
    return Product.query.filter_by(barcode=barcode).first()


def buscar_produto_na_off(barcode):
    """
    Busca um produto na API do Open Food Facts.

    Args:
        barcode (str): Código de barras do produto

    Returns:
        dict | None: Dados do produto se encontrado, None caso contrário
    """
    off_url = f"https://br.openfoodfacts.net/api/v2/product/{barcode}"

    try:
        response = requests.get(off_url, timeout=10)
        product_data = response.json()

        if product_data.get("status") == 0:
            return None

        return product_data.get("product")

    except requests.exceptions.RequestException as e:
        print(f"Erro ao consultar OFF: {e}")
        return None


def criar_e_salvar_produto(barcode, off_data):
    """
    Cria um novo produto a partir dos dados da OFF, calcula o score e salva no DB.

    Args:
        barcode (str): Código de barras do produto
        off_data (dict): Dados retornados pela API do Open Food Facts

    Returns:
        Product: Objeto Product salvo no banco de dados
    """
    # Extrai dados para cálculo do score
    nova = off_data.get("nova_groups")
    ing_tags = off_data.get("ingredients_analysis_tags", [])
    lab_tags = off_data.get("labels_tags", [])
    add_tags = off_data.get("additives_tags", [])

    # Calcula o score
    final_score = calculate_score(
        off_data,
        nova_group=off_data.get('nova_group'),
        ingredients_tags=off_data.get('ing_tags'),
        labels_tags=lab_tags,
        additives_tags=",".join(add_tags)
    )

    # Cria o objeto Product
    novo_produto = Product(
        name=off_data.get("product_name", "Unknown Product"),
        barcode=barcode,
        image_url=off_data.get(
            "image_front_url") or off_data.get("image_front_url"),
        nova_group=nova,
        ingredients_analysis_tags=",".join(ing_tags),
        labels_tags=",".join(lab_tags),
        allergens_tags=",".join(off_data.get("allergens_tags", [])),
        additives_tags=",".join(add_tags),
        score=final_score
    )

    # Salva no banco de dados
    db.session.add(novo_produto)
    db.session.commit()

    return novo_produto


# ========== ROTAS ==========

# SCAN: Escaneia código de barras e retorna/cria produto
@product_bp.route('/product/scan', methods=['POST'])
@swag_from({
    'tags': ['Product'],
    'summary': 'Scan barcode and get product',
    'description': 'Receives a barcode, checks local DB, fetches from OFF if needed, calculates score and saves.',
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
        200: {'description': 'Product found in local database'},
        201: {'description': 'Product fetched from OFF and saved'},
        404: {'description': 'Product not found in OFF'},
        400: {'description': 'Invalid request'}
    }
})
def scan_product():
    """
    Rota principal de scan:
    1. Verifica se produto existe no DB local
    2. Se não existe, busca na API do Open Food Facts
    3. Calcula score e salva no DB
    4. Retorna os dados do produto
    """
    try:
        data = request.get_json()
        validated_data = ProductInputSchema(**data)
        barcode = validated_data.barcode

        # Passo 1: Verifica no banco de dados local
        produto_existente = buscar_produto_no_db(barcode)

        if produto_existente:
            return jsonify({
                "message": "Product found in history",
                "product": ProductResponseSchema.model_validate(produto_existente).model_dump()
            }), 200

        # Passo 2: Busca na API externa
        off_data = buscar_produto_na_off(barcode)

        if not off_data:
            return jsonify({"error": "Product not found in Open Food Facts"}), 404

        # Passo 3: Cria e salva o produto
        novo_produto = criar_e_salvar_produto(barcode, off_data)

        # Passo 4: Retorna o resultado
        return jsonify({
            "message": "Product scanned and saved successfully",
            "product": ProductResponseSchema.model_validate(novo_produto).model_dump()
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Internal error: {str(e)}"}), 400


# GET: Busca produto no histórico (por ID, nome ou barcode)
@product_bp.route('/product', methods=['GET'])
@swag_from({
    'tags': ['Product'],
    'summary': 'Search product in history',
    'description': 'Search for a product in local database using ID, name, or barcode.',
    'parameters': [
        {'name': 'id', 'in': 'query', 'type': 'integer', 'description': 'Product ID'},
        {'name': 'name', 'in': 'query', 'type': 'string',
            'description': 'Product Name'},
        {'name': 'barcode', 'in': 'query', 'type': 'string',
            'description': 'Product Barcode'}
    ],
    'responses': {
        200: {'description': 'Product found'},
        400: {'description': 'Provide at least one search parameter'},
        404: {'description': 'Product not found in history'}
    }
})
def get_product():
    """
    Busca um produto no histórico local.
    Aceita ID, nome ou barcode como parâmetro de busca.
    """
    product_id = request.args.get('id')
    name = request.args.get('name')
    barcode = request.args.get('barcode')

    query = Product.query

    if product_id:
        product = query.get(product_id)
    elif barcode:
        product = query.filter_by(barcode=barcode).first()
    elif name:
        product = query.filter(Product.name.ilike(f"%{name}%")).first()
    else:
        return jsonify({"error": "Provide id, name, or barcode"}), 400

    if not product:
        return jsonify({"error": "Product not found"}), 404

    response_data = ProductResponseSchema.model_validate(product).model_dump()
    return jsonify(response_data), 200


# UPDATE: Atualiza dados de um produto
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
    """
    Atualiza nome ou barcode de um produto existente.
    """
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


# DELETE: Remove produto do histórico
@product_bp.route('/product/delete', methods=['DELETE'])
@swag_from({
    'tags': ['Product'],
    'summary': 'Remove a product from history',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'barcode': {'type': 'string'}
                }
            }
        }
    ],
    'responses': {
        200: {'description': 'Product deleted successfully'},
        404: {'description': 'Product not found'}
    }
})
def delete_product():
    data = request.get_json()
    barcode = data.get('barcode')

    # Busca o produto no banco
    product = Product.query.filter_by(barcode=barcode).first()

    if not product:
        return jsonify({"error": "Produto não encontrado no histórico"}), 404

    try:
        db.session.delete(product)
        db.session.commit()
        return jsonify({"message": "Produto removido com sucesso"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Erro ao deletar: {str(e)}"}), 500

# LIST: Lista todos os produtos no histórico


@product_bp.route('/products-list', methods=['GET'])
@swag_from({
    'tags': ['Product'],
    'summary': 'List all products in history',
    'description': 'Retrieves a list of all products stored in the local database history.',
    'responses': {
        200: {'description': 'List of products retrieved successfully'}
    }
})
def list_products():
    products = Product.query.all()
    response_data = [ProductResponseSchema.model_validate(
        prod).model_dump() for prod in products]
    return jsonify(response_data), 200
