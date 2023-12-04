from unittest import TestCase
import unittest
from flask_login import current_user

from app import create_app
from cart.models import CartItem
from extensions import db
from users.models import User


class TestRoutes(TestCase):
    def create_app(self):
        app = create_app(testing=True)
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        return app

    def setUp(self):
        db.create_all()
        user = User(username='test_user', password='test_password')
        db.session.add(user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_home_route_authenticated(self):
        with self.client:
            self.client.post('/login', data=dict(
                username='test_user',
                password='test_password'
            ), follow_redirects=True)
            response = self.client.get('/')

            self.assert200(response)
            self.assertIn(b'Welcome', response.data)

    def test_home_route_unauthenticated(self):
        response = self.client.get('/')
        self.assertRedirects(response, '/login')

    def test_add_to_cart_route(self):
        with self.client:
            self.client.post('/login', data=dict(
                username='test_user',
                password='test_password'
            ), follow_redirects=True)
            product_id = 1
            response = self.client.get(f'/add-to-cart/{product_id}')

            self.assert200(response)
            self.assertIn(b'added to cart', response.data)

            cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
            self.assertEqual(len(cart_items), 1)
            self.assertEqual(cart_items[0].quantity, 1)

    # Add more tests for other routes as needed


if __name__ == '__main__':
    unittest.main()
