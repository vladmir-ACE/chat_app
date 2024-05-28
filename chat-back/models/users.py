from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from models.contactes import Contacte



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    phone_number = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(256), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    
    #list od reciev and send messages
    sent_messages = db.relationship('Message', foreign_keys='Message.sender_id', backref='sender', lazy=True)
    received_messages = db.relationship('Message', foreign_keys='Message.receiver_id', backref='receiver', lazy=True)


    contacts = db.relationship('User', secondary='contacte', 
                               primaryjoin=(Contacte.user_id == id),
                               secondaryjoin=(Contacte.contact_id == id),
                               backref=db.backref('user_contacts', lazy='dynamic'), lazy='dynamic')
    

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        print(f"Password hash set for {self.username}: {self.password_hash}")  # Ajout pour débogage

    def check_pass(self, password):
        result = check_password_hash(self.password_hash, password)
        print(f"Checking password for {self.username}: {result}")  # Ajout pour débogage
        return result
    
    
    
    def add_contact(self, contact):
        if not self.is_contact(contact):
            self.contacts.append(contact)

    def remove_contact(self, contact):
        if self.is_contact(contact):
            self.contacts.remove(contact)

    def is_contact(self, contact):
        return self.contacts.filter(Contacte.contact_id == contact.id).count() > 0