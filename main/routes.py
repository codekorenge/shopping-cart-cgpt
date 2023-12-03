from flask import Blueprint, render_template
from flask_login import login_required, current_user

main_bp = Blueprint('main',
                    __name__,
                    template_folder='templates',
                    static_folder='static')


@main_bp.route('/')
@login_required
def home():
    return render_template('home.html', user=current_user)
