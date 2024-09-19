from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_db():
    from app import app
    with app.app_context():
        db.create_all()