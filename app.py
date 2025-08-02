# app.py

from flask import Flask, render_template, request, redirect, url_for, flash, send_file, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, current_user, logout_user, login_required
import io
import xhtml2pdf.pisa as pisa
from datetime import datetime
import os
from authlib.integrations.flask_client import OAuth

# --- APP CONFIGURATION ---
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_strong_secret_key'  # Change this to a random string
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

# --- GOOGLE OAUTH CONFIGURATION ---
oauth = OAuth(app)
oauth.register(
    name='google',
    client_id='YOUR_GOOGLE_CLIENT_ID',  # <-- REPLACE with your Client ID
    client_secret='YOUR_GOOGLE_CLIENT_SECRET',  # <-- REPLACE with your Client Secret
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    client_kwargs={'scope': 'openid email profile'},
    jwks_uri="https://www.googleapis.com/oauth2/v3/certs",
)

# --- DATABASE MODEL (updated to handle Google users) ---
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=True)
    google_id = db.Column(db.String(120), unique=True, nullable=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --- ROUTES ---
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(username=username, email=email, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html')

# --- NEW GOOGLE OAUTH ROUTES ---
@app.route('/login/google')
def login_google():
    redirect_uri = url_for('auth_google', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)

@app.route('/auth/google/callback')
def auth_google():
    token = oauth.google.authorize_access_token()
    user_info = oauth.google.get('userinfo').json()
    
    # Check if a user with this Google ID exists
    user = User.query.filter_by(google_id=user_info['id']).first()
    
    if not user:
        # Check if a user with this email already exists
        user = User.query.filter_by(email=user_info['email']).first()
        if user:
            # If so, link their Google ID to the existing account
            user.google_id = user_info['id']
            db.session.commit()
            flash('Your Google account has been linked to your existing account!', 'success')
        else:
            # Create a new user account
            user = User(
                google_id=user_info['id'],
                username=user_info['email'],  # Use email as username for new Google users
                email=user_info['email']
            )
            db.session.add(user)
            db.session.commit()
            flash('New account created with Google!', 'success')

    login_user(user)
    return redirect(url_for('home'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/convert', methods=['POST'])
@login_required
def convert():
    source_html = request.form.get('text_input', '')
    if not source_html.strip():
        flash('Please provide some text to convert.', 'warning')
        return redirect(url_for('home'))

    pdf_html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <style>
            body {{ font-family: 'Poppins', sans-serif; font-size: 12px; line-height: 1.6; padding: 20px; }}
            h1, h2, h3, h4, h5, h6 {{ font-family: 'Poppins', sans-serif; }}
        </style>
    </head>
    <body>
        {source_html}
    </body>
    </html>
    """
    result_file = io.BytesIO()
    pisa_status = pisa.CreatePDF(pdf_html, dest=result_file)

    if not pisa_status.err:
        result_file.seek(0)
        return send_file(
            result_file, 
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f'converted_text_{datetime.now().strftime("%Y%m%d%H%M%S")}.pdf'
        )
    
    flash('An error occurred during PDF conversion.', 'danger')
    return redirect(url_for('home'))

# --- MAIN ENTRY POINT ---
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)