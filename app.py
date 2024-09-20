import random
from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Term

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_BINDS'] = {
    'maths_topics': 'sqlite:///../helpers/math_topics.db'  # Bind for maths_topics database
}
app.config['SECRET_KEY'] = "\x0b\xaf2\xdd\xeaAZ\xa2\xe4\xdb\x06"

db.init_app(app)

# Initialize the database
with app.app_context():
    db.create_all()

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        hashed_password = generate_password_hash(password)

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return "Error: Email already exists.", 400

        new_user = User(email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            return redirect(url_for('main'))
        return 'Invalid credentials', 401
    return render_template('login.html')

@app.route('/main')
def main():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('main.html')


@app.route('/random_term/<topic>', methods=['GET'])
def random_term(topic):
    # Fetch random term based on the topic
    terms = Term.query.filter_by(maths_topic=topic).all()
    selected_term = random.choice(terms) if terms else None
    return render_template('term.html', term=selected_term, dependency_term=None)


@app.route('/show_dependency/<int:term_id>', methods=['GET'])
def show_dependency(term_id):
    # Fetch the main term and its dependency term
    term = Term.query.get_or_404(term_id)
    dependency_term = None
    
    if term.dependency_id != -1:
        dependency_term = Term.query.get(term.dependency_id)
        
    return render_template('term.html', term=term, dependency_term=dependency_term)

if __name__ == '__main__':
    app.run(debug=True)
