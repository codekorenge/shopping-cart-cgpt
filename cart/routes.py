from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from extensions import db
from cart.models import CartItem
from utils.utils import get_product_by_id

cart_bp = Blueprint('cart', __name__,
                    template_folder='templates',
                    static_folder='static')


@cart_bp.route('/view-cart')
@login_required
def view_cart():
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    total_price = calculate_total_price(current_user.id)

    return render_template('view_cart.html', cart_items=cart_items, total_price=total_price,
                           get_product_by_id=get_product_by_id)


@cart_bp.route('/remove-from-cart/<int:item_id>')
@login_required
def remove_from_cart(item_id):
    item = CartItem.query.get(item_id)

    if not item:
        flash('Item not found.', 'error')
    elif item.user_id != current_user.id:
        flash('You do not have permission to remove this item.', 'error')
    else:
        db.session.delete(item)
        db.session.commit()
        flash('Item removed from cart.', 'success')

    return redirect(url_for('cart.view_cart'))


def calculate_total_price(user_id):
    # Calculate the total price based on the items in the user's cart
    cart_items = CartItem.query.filter_by(user_id=user_id).all()
    total_price = sum(item.quantity * get_product_by_id(item.product_id)['price'] for item in cart_items)
    return total_price
