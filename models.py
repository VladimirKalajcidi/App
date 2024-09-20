from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)



class Term(db.Model):
    __bind_key__ = 'maths_topics'
    __tablename__ = 'terms'
    
    id = db.Column(db.Integer, primary_key=True)
    maths_topic = db.Column(db.String(50), nullable=False)
    term = db.Column(db.String(100), nullable=False)
    definition = db.Column(db.Text, nullable=False)
    dependency_id = db.Column(db.Integer, ForeignKey('terms.id'), nullable=True)  # ForeignKey to itself

    # Self-referential relationship for the dependency term
    dependency = relationship('Term', remote_side=[id], backref='dependent_terms')

# Explanation:
# - The `dependency_id` column is now set as a ForeignKey that references the `id` of the same `terms` table.
# - The `nullable=True` allows for cases where no dependency may exist.