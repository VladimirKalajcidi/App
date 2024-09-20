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

        # Check if the email already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            # Email already exists, handle accordingly (e.g., show an error message)
            return "Error: Email already exists.", 400  # or render a template with an error message

        # Create a new user if email doesn't exist
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
        return 'Invalid credentials'
    return render_template('login.html')

@app.route('/main')
def main():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('main.html')

@app.route('/random_term/<topic>')
def random_term(topic):
    with app.app_context():
        terms = Term.query.filter_by(maths_topic=topic).all()
        if terms:
            selected_term = random.choice(terms)
            # Fetch the dependent term using its dependency_id
            dependency_id = selected_term.dependency_id
            dependency_term = Term.query.filter_by(id=dependency_id).first() if dependency_id != -1 else None
            
            return render_template('term.html', term=selected_term, dependency_term=dependency_term)
        
        return "No terms available for this topic.", 404


@app.route('/new_term/<topic>', methods=['POST'])
def new_term(topic):
    with app.app_context():
        terms = Term.query.filter_by(maths_topic=topic).all()
        selected_term = random.choice(terms) if terms else None
        return render_template('term.html', term=selected_term) if selected_term else "No terms available for this topic.", 404


@app.route('/term/<int:term_id>')
def show_term(term_id):
    term = Term.query.get_or_404(term_id)
    dependency_term = Term.query.get(term.dependency_id) if term.dependency_id else None
    print(f"Term: {term.term}, Dependency ID: {term.dependency_id}, Dependency Term: {dependency_term.term if dependency_term else 'None'}")
    return render_template('term_combined.html', term=term, dependency_term=dependency_term)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

if __name__ == '__main__':
    app.run(debug=True)
