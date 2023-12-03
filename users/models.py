from extensions import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone_number = db.Column(db.String(15), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    otp_secret = db.Column(db.String(16), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.phone_number}')"

    def get_id(self):
        return str(self.id)  # Ensure the ID is a string to satisfy
