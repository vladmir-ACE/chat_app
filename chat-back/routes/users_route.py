from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from app import db ,photos
from models.messages import Message
from models.users import User
from models.contactes import Contacte

users_bp = Blueprint('user', __name__)


#list of all user 

@users_bp.route('/all', methods=['GET'])
@jwt_required()
def all_user():
   
    users = User.query.all()

    return jsonify(
        {"data":[{
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'phone_number': user.phone_number
         } for user in users]
        }), 200
    


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
                "phone_number":user.phone_number,
                'img':photos.url(user.img)  if user.img else None
            }
        }),200
    else:
        jsonify({"msg":"user not found"}),404
    

# ad a user in contact table 

@users_bp.route('/contacte/add',methods=['POST'])
@jwt_required()
def save_contact():
    data=request.json
    current_user_identity = get_jwt_identity()
    user_id=current_user_identity['id']
    contact_id=data.get('contact_id')
    
    new_contacte= Contacte(user_id=user_id,contact_id=contact_id)
    db.session.add(new_contacte)
    db.session.commit()
    
    return jsonify({"msg": "contacte successfully add "}), 201

# delete  a user in contact table 
@users_bp.route('/contacte/delete',methods=['DELETE'])
@jwt_required()
def del_contact():
    data=request.json
    current_user_identity = get_jwt_identity()
    user_id=current_user_identity['id']
    contact_id=data.get('contact_id')
    
    new_contacte= Contacte(user_id=user_id,contact_id=contact_id)
    db.session.add(new_contacte)
    db.session.commit()
    
    return jsonify({"msg": "contacte successfully delete add "}), 201
    
    


    
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
        'phone_number': contact.phone_number,
        'img':photos.url(contact.img)  if contact.img else None
         } for contact in contacts]
        }), 200
    

# profile part 
@users_bp.route('/upload_image', methods=['POST'])
@jwt_required()
def upload_image():
    if 'img' not in request.files:
        return jsonify({"msg": "No file part"}), 400

    file = request.files['img']

    if file.filename == '':
        return jsonify({"msg": "No selected file"}), 400

    if file and file.filename:
        filename = photos.save(file)
        current_user_identity = get_jwt_identity()
        user = User.query.filter_by(username=current_user_identity['username']).first_or_404()
        user.img = filename
        db.session.commit()
        return jsonify({"data": {
             "img":photos.url(filename)
            }}), 200

    return jsonify({"msg": "Image upload failed"}), 400

# unknow contact who sent message 
@users_bp.route('/unknown_contacts', methods=['GET'])
@jwt_required()
def get_unknown_contacts():
    current_user_identity = get_jwt_identity()
    current_user = User.query.filter_by(id=current_user_identity['id']).first_or_404()

    # Récupérer les messages reçus par l'utilisateur courant
    received_messages = Message.query.filter_by(receiver_id=current_user.id).all()
    
    # Filtrer les utilisateurs qui ont envoyé des messages et ne sont pas dans les contacts
    unknown_senders = set()
    for message in received_messages:
        sender = User.query.get(message.sender_id)
        if not current_user.is_contact(sender):
            unknown_senders.add(sender)

    return jsonify(
        {"data": [{
            'id': sender.id,
            'username': sender.username,
            'email': sender.email,
            'phone_number': sender.phone_number,
            'img':sender.img if sender.img else None
        } for sender in unknown_senders]}
    ), 200