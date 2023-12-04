from flask import Blueprint, render_template, redirect, url_for, abort, request, flash

from cart.models import CartItem
from extensions import db
from flask_login import login_required, current_user

from main.models import ProductView

main_bp = Blueprint('main',
                    __name__,
                    template_folder='templates',
                    static_folder='static')


# @main_bp.route('/')
# # @login_required
# def home():
#     return render_template('home.html', user=current_user)
#
#
# from flask import render_template, redirect, url_for
# from app import app, db
# from app.models import Product


@main_bp.route('/')
def home():
    products = get_all_products()
    total_amount = 0
    # total_amount = calculate_total_amount(products)
    return render_template('home.html', products=products, total_amount=total_amount)


@main_bp.route('/add-to-cart/<int:product_id>')
@login_required
def add_to_cart(product_id):
    product = get_product_by_id(product_id)

    if not product:
        flash('Product not found.', 'error')
        return redirect(url_for('products.view_products'))

    # Check if the user is authenticated
    if current_user.is_authenticated:
        # Check if the product is already in the user's cart
        existing_item = CartItem.query.filter_by(user_id=current_user.id, product_id=product_id).first()

        cart_item = []
        if existing_item:
            existing_item.quantity += 1
        else:
            new_item = CartItem(user_id=current_user.id, product_id=product_id, quantity=1)
            db.session.add(new_item)

        db.session.commit()

        # To display items in cart.
        cart_list = CartItem.query.filter_by(user_id=current_user.id).all()
        for item in cart_list:
            product_info = get_product_by_id(item.product_id)
            view = ProductView()
            view.name = product_info['name']
            view.quantity = item.quantity
            view.price = product_info['price']
            view.total = item.quantity * product_info['price']
            cart_item.append(view)

        flash(f'{product["name"]} added to cart.', 'success')

        # Calculate the total and pass it to the template
        total_price = calculate_total_price(current_user.id)

        return render_template('home.html', products=get_all_products(), total_price=total_price, cart=cart_item)


@main_bp.route('/add/<int:product_id>')
def add(product_id):
    product = get_product_by_id(product_id)
    if product is None:
        abort(404)

    product['quantity'] += 1
    db.session.commit()
    return redirect(url_for('main.home'))


@main_bp.route('/remove/<int:product_id>')
def remove(product_id):
    product = get_product_by_id(product_id)
    if product is None:
        abort(404)

    if product.quantity > 0:
        product.quantity -= 1
        db.session.commit()
    return redirect(url_for('home'))


@main_bp.route('/checkout')
def checkout():
    if current_user.is_authenticated:
        # Check if the product is already in the user's cart
        cart_item = []

        # To display items in cart.
        cart_list = CartItem.query.filter_by(user_id=current_user.id).all()
        for item in cart_list:
            product_info = get_product_by_id(item.product_id)
            view = ProductView()
            view.name = product_info['name']
            view.quantity = item.quantity
            view.price = product_info['price']
            view.total = item.quantity * product_info['price']
            cart_item.append(view)

        # Calculate the total and pass it to the template
        total_price = calculate_total_price(current_user.id)

        return render_template('checkout.html', total_price=total_price, cart=cart_item)

    products = get_all_products()
    total_amount = 0
    # total_amount = calculate_total_amount(products)
    return render_template('home.html', products=products, total_amount=total_amount)


def calculate_total_amount(products):
    total_amount = sum(product.price * product.quantity for product in products)
    return total_amount


def calculate_total_price(user_id):
    # Calculate the total price based on the items in the user's cart
    cart_items = CartItem.query.filter_by(user_id=user_id).all()
    total_price = sum(item.quantity * get_product_by_id(item.product_id)['price'] for item in cart_items)
    return total_price


def get_all_products():
    # Replace this with your logic to fetch all products
    products = [
        {'id': 1, 'name': 'Apple', 'price': 4.00, },
        {'id': 2, 'name': 'Orange', 'price': 3.00, },
        {'id': 2, 'name': 'Banana',  'price': 2.00, },
        # Add more products as needed
    ]
    return products


def get_product_by_id(product_id):
    products = get_all_products()
    for item in products:
        print(item)
        if item['id'] == product_id:
            return item

    return None
