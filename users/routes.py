from flask import Blueprint, flash, session, request, render_template, url_for, redirect
from flask_login import current_user, login_user, logout_user

from extensions import db, login_manager
from users.models import User
import pyotp

user_bp = Blueprint('user',
                    __name__,
                    template_folder='templates',
                    static_folder='static')


@user_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        phone_number = request.form['phone_number']
        password = request.form['password']

        # Check if the username or email is already taken
        existing_user = User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first()

        if existing_user:
            flash('Username or email is already taken. Please choose a different one.', 'error')
            return redirect(url_for('user.register'))

        # Create a new user
        new_user = User(username=username, email=email, phone_number=phone_number, password=password, otp_secret='')

        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('user.login'))

    return render_template('register.html')


@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and password == user.password:
            # Login successful, generate and send OTP
            otp_secret = pyotp.random_base32()
            session['otp_secret'] = otp_secret
            # To retrieve later.
            session['username'] = username
            session['id'] = user.id

            totp = pyotp.TOTP(otp_secret)
            otp = totp.now()
            print(f"Generated OTP: {otp}")

            # Here, you would typically send the OTP to the user's email.
            # For simplicity, we'll just print it here.
            print(f"Your one-time password is: {otp}")

            flash('One-time password sent to your email.', 'info')

            return redirect(url_for('user.validate_otp'))

        else:
            flash('Login failed. Please check your username and password.', 'error')

    return render_template('login.html')


@user_bp.route('/validate_otp', methods=['GET', 'POST'])
def validate_otp():
    if 'otp_secret' not in session:
        flash('Invalid access. Please log in again.', 'error')
        return redirect(url_for('user.login'))

    if request.method == 'POST':
        user_otp = request.form['otp']
        print(f"Entered OTP: {user_otp}")

        totp = pyotp.TOTP(session['otp_secret'])
        if totp.verify(user_otp):
            # OTP validation successful, log the user in
            username = session['username']
            user = User.query.filter_by(username=username).first()
            login_user(user)
            session.pop('otp_secret', None)  # Clear the OTP secret from the session
            flash('Login successful!', 'success')

            # Here, you would typically log the user in using Flask-Login.
            # For simplicity, we'll just print a message.
            print(f"User '{current_user.username}' logged in.")

            return redirect(url_for('main.home'))

        else:
            flash('Invalid OTP. Please try again.', 'error')

    return render_template('validate_otp.html')


@user_bp.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
