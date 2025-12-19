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

# --- CRUD Operations ---
"""
ALGORITMO product_bp:
- escaneia codigo de barras (barcode)
- verifica (if) se ja esta na base de dados - funcao GET com o barcode
- se (if) o produto ja estiver, faz uma requisicao GET ao banco de dados
- (ELSE) se o produto nao estiver na base de dados, faz a requisicao GET pra api externa  OFF e retorna os dados em json (data)
- calcula o score baseado nos dados da json -> calculate_score()
- pega os dados em json e o score e cria um novo produto na base de dados com uma funcao POST
- salva o novo produto na base de dados
- retorna a resposta com os dados do produto e o score calculado
"""
# 1 - escaneia codigo de barras (barcode)
# essa parte vai rolar no javascript do frontend
# passa o barcode pro backend via requisicao POST no fetch

# 2 - verifica (if) se ja esta na base de dados - funcao GET com o barcode
if barcode in local database:
    # 3 - se (if) o produto ja estiver, faz uma requisicao GET ao banco de dados
    @product_bp.route('/product/<string:barcode>', methods=['GET'])
    @swag_from({})
    def get_product(barcode):
        existing_product = Product.query.filter_by(barcode=barcode).first()
        if existing_product:
            return jsonify({
                "message": "Product found in history",
                "product": ProductResponseSchema.model_validate(existing_product).model_dump()
            }), 200
