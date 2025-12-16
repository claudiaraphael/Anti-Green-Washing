from app import app
import requests
import os

# import global variables
OFF_BARCODE = os.getenv('OFF_BARCODE')
OFF_PRODUCT = os.getenv('OFF_PRODUCT')


# ROUTES
# get product by barcode
@app.route('/product/<barcode>', methods=['GET'])
def get_product_by_barcode(barcode: str:
    URI = OFF_BARCODE
    response = requests.get(URI, **{'barcode': barcode})                      
    data = response.json()
    return data

# get product by name
@app.route('/product/', methods=['GET'])
def get_product_by_name(name: str):
    response = requests.get(OFF_BARCODE, **{'name': name, 'barcode': barcode})
    data = response.json()
    return data

"""
JavaScript chama Flask
Flask chama Open Food Facts (GET/POST)
Flask processa dados
Flask retorna JSON pro JavaScript
JavaScript atualiza a tela
"""