from flask import Blueprint, request, jsonify
from dotenv import load_dotenv
import requests
import os

load_dotenv()

openfoodfacts_bp = Blueprint('openfoodfacts', __name__)

# Environment variables
OFF_BASE = os.getenv('OFF_BASE', 'https://world.openfoodfacts.net')

# ROUTES

# get product by barcode
@openfoodfacts_bp.route('/openfoodfacts/product/<barcode>', methods=['GET'])
def get_product_by_barcode(barcode: str):
    """
    Fetch product from Open Food Facts by barcode
    """
    try:
        # Build correct URL replacing {barcode}
        url = f'{OFF_BASE}/api/v2/product/{barcode}'

        response = requests.get(url, timeout=10)
        response.raise_for_status()

        data = response.json()

        # Check if product was found
        if data.get('status') == 0:
            return jsonify({
                'error': 'Product not found',
                'barcode': barcode
            }), 404

        # Extract relevant data
        product = data.get('product', {})

        return jsonify({
            'barcode': barcode,
            'name': product.get('product_name', 'No name'),
            'brands': product.get('brands', ''),
            'categories': product.get('categories', ''),
            'ecoscore_grade': product.get('ecoscore_grade', ''),
            'labels': product.get('labels', ''),
            'image_url': product.get('image_url', ''),
            'raw_data': product  # complete data if needed
        }), 200

    except requests.exceptions.Timeout:
        return jsonify({'error': 'API request timeout'}), 504
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'API request error: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'Internal error: {str(e)}'}), 500

# get product by name


@openfoodfacts_bp.route('/openfoodfacts/product/', methods=['GET'])
def get_product_by_name(name: str):
    """
    Search products on Open Food Facts by name
    Query params: name (required), page (optional)
    """
    try:
        name = request.args.get('name')
        page = request.args.get('page', 1)

        if not name:
            return jsonify({'error': 'Parameter "name" is required'}), 400

        # Search parameters
        params = {
            'search_terms': name,
            'page': page,
            'page_size': 20,
            'json': 1
        }

        url = f'{OFF_BASE}/cgi/search.pl'
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()

        # Format results
        products = []
        for product in data.get('products', []):
            products.append({
                'barcode': product.get('code', ''),
                'name': product.get('product_name', 'No name'),
                'brands': product.get('brands', ''),
                'image_url': product.get('image_url', ''),
                'ecoscore_grade': product.get('ecoscore_grade', '')
            })

        return jsonify({
            'count': data.get('count', 0),
            'page': data.get('page', 1),
            'products': products
        }), 200

    except requests.exceptions.Timeout:
        return jsonify({'error': 'API request timeout'}), 504
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'API request error: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'Internal error: {str(e)}'}), 500


"""
JavaScript chama Flask
Flask chama Open Food Facts (GET/POST)
Flask processa dados
Flask retorna JSON pro JavaScript
JavaScript atualiza a tela
"""
