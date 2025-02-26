from flask import Flask, jsonify, send_file, request
import requests
from io import BytesIO


app = Flask(__name__)

products = []
next_id = 1

@app.route('/products', methods=['GET'])
def get_products():
    return jsonify(products)

@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = next((p for p in products if p['id'] == product_id), None)
    if product is not None:
        return jsonify(product)
    else:
        return jsonify({'error': 'Product not found'}), 404

@app.route('/products', methods=['POST'])
def add_product():
    global next_id
    data = request.json
    new_product = {
        'id': next_id,
        'name': data['name'],
        'description': data['description'],
        'icon' : data['icon']
    }
    products.append(new_product)
    next_id += 1
    return jsonify(new_product), 201

@app.route('/product/<int:product_id>/icon', methods=['GET'])
def get_product_icon(product_id):
    product = next((p for p in products if p['id'] == product_id), None)
    if product is not None and 'icon' in product:
        icon_url = product['icon']
        response = requests.get(icon_url)

        if response.status_code == 200:
            return send_file(BytesIO(response.content), mimetype='image/jpeg')
        else:
            return jsonify({'error': 'Failed to retrieve icon'}), response.status_code

    else:
        return jsonify({'error': 'Product or icon not found'}), 404


@app.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    product = next((p for p in products if p['id'] == product_id), None)
    if product is not None:
        data = request.json
        product['name'] = data.get('name', product['name'])
        product['description'] = data.get('description', product['description'])
        return jsonify(product)
    else:
        return jsonify({'error': 'Product not found'}), 404

@app.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    global products
    products = [p for p in products if p['id'] != product_id]
    return jsonify({'message': 'Product deleted'}), 204

if __name__ == '__main__':
    app.run(debug=True)