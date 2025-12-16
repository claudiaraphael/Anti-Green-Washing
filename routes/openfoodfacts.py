from app import app
import os

# import global variables
OFF_BARCODE = os.getenv('OFF_BARCODE')
OFF_PRODUCT = os.getenv('OFF_PRODUCT')

# get product by barcode
@app.route('/product/<barcode>', methods=['GET'])
def get_product_by_barcode(barcode: str) -> str:
    response = OFF_BARCODE.format(barcode=barcode)
    return response
