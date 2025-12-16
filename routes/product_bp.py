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

# READ

# History
@product_bp.route('/product', methods=['GET'])
def get_all_products():
    """
    Lista todos os produtos.
    """
    # 1. Buscar todos os produtos
    products = Product.query.all()
    
    # 2. Serializar a lista usando ProductResponseSchema
    products_list = [
        ProductResponseSchema.model_validate(p).model_dump()
        for p in products
    ]

    return jsonify({"products": products_list}), 200

# One product
@product_bp.route('/product/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """
    Busca um produto pelo ID.
    """
    # 1. Buscar produto, retorna 404 se não encontrado
    product = Product.query.get_or_404(product_id)
    
    # 2. Serializar o objeto SQLAlchemy para o formato de resposta Pydantic/JSON
    response_data = ProductResponseSchema.model_validate(product).model_dump()

    return jsonify(response_data), 200

# UPDATE

# O ProductInputSchema pode ser re-utilizado para o update, 
# mas campos opcionais devem ser tratados com cautela se usar PUT (substituição completa).
# Para PATCH (atualização parcial), usaremos um esquema de entrada para update.
# Como seus schemas de entrada não usam Optional/None, vou usar a abordagem simples de PATCH.

@product_bp.route('/product/<int:product_id>', methods=['PATCH'])
def update_product(product_id):
    """
    Atualiza parcialmente um produto pelo ID (PATCH).
    Permite alterar nome, barcode ou user_id.
    """
    # 1. Buscar produto existente
    product = Product.query.get_or_404(product_id)
    
    try:
        # 2. Obter dados da requisição
        data = request.get_json()

        # 3. Validar apenas os campos presentes na requisição (reutilizando o schema)
        # Passar data para ProductInputSchema com o método model_validate_json para validar.
        # Aqui, a validação é um pouco mais complexa porque queremos apenas 
        # validar os campos *que vieram*. Uma abordagem Pydantic ideal é criar
        # um 'UpdateSchema' onde todos os campos são Optional.
        
        # **Simplificação (aplica as mudanças diretamente se a chave existir):**
        if 'name' in data:
            product.name = data['name']
        if 'barcode' in data:
            product.barcode = data['barcode']

        # Note: Eco_score não está no InputSchema, mas pode ser atualizado se você 
        # tiver um endpoint que o calcule ou o receba.
        # if 'certificates' in data:
        #    product.certificates = data['certificates']

        # 4. Commit da transação
        db.session.commit()

        # 5. Retornar resposta
        response_data = ProductResponseSchema.model_validate(product).model_dump()
        return jsonify({
            "message": "Produto atualizado com sucesso",
            "product": response_data
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

# DELETE

@product_bp.route('/product/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    """
    Deleta um produto pelo ID.
    """
    # 1. Buscar produto existente
    product = Product.query.get_or_404(product_id)

    try:
        # 2. Deletar e commitar
        db.session.delete(product)
        db.session.commit()
        return jsonify({"message": f"Produto ID {product_id} deletado com sucesso"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400