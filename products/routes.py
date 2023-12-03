from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from extensions import db
from users.models import User
from cart.models import CartItem
from utils.utils import get_product_by_id

products_bp = Blueprint('products',
                        __name__,
                        template_folder='templates',
                        static_folder='static')


@products_bp.route('/view-products')
@login_required
def view_products():
    products = [
        {'id': 1, 'name': 'Product 1', 'price': 19.99},
        {'id': 2, 'name': 'Product 2', 'price': 29.99},
        # Add more products as needed
    ]

    return render_template('view_products.html', products=products)


@products_bp.route('/add-to-cart/<int:product_id>', methods=['GET', 'POST'])
@login_required
def add_to_cart(product_id):
    if request.method == 'POST':
        product = get_product_by_id(product_id)

        if not product:
            flash('Product not found.', 'error')
            return redirect(url_for('products.view_products'))

        # Check if the user is authenticated
        if current_user.is_authenticated:
            # Check if the product is already in the user's cart
            existing_item = CartItem.query.filter_by(user_id=current_user.id, product_id=product_id).first()

            if existing_item:
                existing_item.quantity += 1
            else:
                new_item = CartItem(user_id=current_user.id, product_id=product_id, quantity=1)
                db.session.add(new_item)

            db.session.commit()

            flash(f'{product["name"]} added to cart.', 'success')

            # Calculate the total and pass it to the template
            total_price = calculate_total_price(current_user.id)
            return render_template('view_products.html', products=get_all_products(), total_price=total_price)

        flash('User not authenticated.', 'error')
        return redirect(url_for('products.view_products'))

    # Handle GET request if needed (e.g., redirect to the product details page)
    return redirect(url_for('products.view_products'))


def calculate_total_price(user_id):
    # Calculate the total price based on the items in the user's cart
    cart_items = CartItem.query.filter_by(user_id=user_id).all()
    total_price = sum(item.quantity * get_product_by_id(item.product_id)['price'] for item in cart_items)
    return total_price


def get_all_products():
    # Replace this with your logic to fetch all products
    products = [
        {'id': 1, 'name': 'Product 1', 'price': 19.99},
        {'id': 2, 'name': 'Product 2', 'price': 29.99},
        # Add more products as needed
    ]
    return products

#
# def get_product_by_id(product_id):
#     # Replace this with your actual logic to fetch product details from the database
#     products = [
#         {'id': 1, 'name': 'Product 1', 'price': 19.99},
#         {'id': 2, 'name': 'Product 2', 'price': 29.99},
#         # Add more products as needed
#     ]
#
#     return next((product for product in products if product['id'] == product_id), None)
