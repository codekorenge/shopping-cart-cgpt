# utils/utils.py
def get_product_by_id(product_id):
    # Replace this with your actual logic to fetch product details from your database
    products = [
        {'id': 1, 'name': 'Product 1', 'price': 19.99},
        {'id': 2, 'name': 'Product 2', 'price': 29.99},
        # Add more products as needed
    ]
    return next((product for product in products if product['id'] == product_id), None)