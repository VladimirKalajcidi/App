import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from config import Config

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize SQLALCHEMY database
db = SQLAlchemy(app)

# Create table for users if it doesn't exist
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

from app import app

# Route for user authentication
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get user credentials from form data
        email = request.form['email']
        password = request.form['password']

        # Query database to retrieve user's hashed password (for demonstration purposes only)
        user = User.query.filter_by(email=email).first()

        if user and password == user.password:
            return 'Login successful!'
        else:
            return 'Invalid credentials'

    # Render login form
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Get user credentials from form data
        email = request.form['email']
        password = request.form['password']

        # Query database to check if email is already taken
        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            return 'Email already taken!'

        # Insert new user into database
        new_user = User(email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        return 'Signup successful!'

    # Render signup form
    return render_template('signup.html')

if __name__ == '__main__':
    app.run(debug=True)

create_db()
