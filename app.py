from flask import Flask
from extensions import db, login_manager
from main.routes import main_bp
from users.routes import user_bp
from products.routes import products_bp
from cart.routes import cart_bp


def create_app():
    app = Flask(__name__)
    app.config[
        'SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # You can change this to another database like MySQL or
    # PostgreSQL
    app.config['SECRET_KEY'] = 'your_secret_key'  # Change this to a secure random key for production
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        db.create_all()

    app.register_blueprint(main_bp, url_prefix='/')
    app.register_blueprint(user_bp, url_prefix='/users')
    app.register_blueprint(products_bp, url_prefix='/products')
    app.register_blueprint(cart_bp, url_prefix='/cart')

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
