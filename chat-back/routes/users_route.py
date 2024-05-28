from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from app import db
from models.messages import Message
from models.users import User
from models.contactes import Contacte

users_bp = Blueprint('user', __name__)

# search a user by username or email 
@users_bp.route('/search', methods=['POST'])
@jwt_required()
def search():
    data=request.json
    search=data.get('search')
    user = User.query.filter((User.username==search) | (User.email==search)).first()
   
    if user:
        return jsonify({
            "user":{
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "phone_number":user.phone_number
            }
        }),200
    else:
        jsonify({"msg":"user not found"}),404
    

# ad a user in contact table 

@users_bp.route('/contacte/add',methods=['POST'])
def save_contact():
    data=request.json
    user_id=data.get('user_id')
    contact_id=data.get('contact_id')
    
    new_contacte= Contacte(user_id=user_id,contact_id=contact_id)
    db.session.add(new_contacte)
    db.session.commit()
    
    return jsonify({"msg": "contacte successfully add "}), 201
    
    
@users_bp.route('/contactes', methods=['GET'])
@jwt_required()
def get_contacts():
    current_user_identity = get_jwt_identity()
    current_user = User.query.filter_by(username=current_user_identity['username']).first_or_404()

    contacts = current_user.contacts.all()

    return jsonify(
        {"data":[{
        'id': contact.id,
        'username': contact.username,
        'email': contact.email,
        'phone_number': contact.phone_number
         } for contact in contacts]
        }), 200
    
