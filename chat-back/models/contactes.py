from app import db
from datetime import datetime

class Contacte(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    contact_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # Relation bidirectionnelle pour accéder facilement aux utilisateurs et à leurs contacts
    user = db.relationship('User', foreign_keys=[user_id], backref=db.backref('contacts_associations', cascade='all, delete-orphan'))
    contact = db.relationship('User', foreign_keys=[contact_id])

