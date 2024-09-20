import random
from flask import Flask, render_template, request, redirect, url_for, session, flash, send_file
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


@app.route('/manifest.json')
def serve_manifest():
    return send_file('manifest.json', mimetype='application/manifest+json')


@app.route('/sw.js')
def serve_sw():
    return send_file('sw.js', mimetype='application/javascript')


@app.route('/auth', methods=['GET', 'POST'])
def auth():
    if request.method == 'POST':
        # Handle signup
        if request.form.get('action') == 'signup':
            email = request.form['email']
            password = request.form['password']
            hashed_password = generate_password_hash(password)

            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                flash("Error: Email already exists.", "error")
                return redirect(url_for('auth'))

            new_user = User(email=email, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            flash("Account created successfully! You can log in now.", "success")
            return redirect(url_for('auth'))

        # Handle login
        if request.form.get('action') == 'login':
            email = request.form['email']
            password = request.form['password']
            user = User.query.filter_by(email=email).first()

            if user and check_password_hash(user.password, password):
                session['user_id'] = user.id
                return redirect(url_for('main'))
            flash('Invalid credentials', 'error')

    return render_template('auth.html')

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
