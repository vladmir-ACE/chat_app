from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from flask_socketio import emit, join_room, leave_room
import socketio
from app import db,photos
from models.messages import Message
from models.users import User
from models.poste import Poste

message_bp = Blueprint('chat', __name__)

@message_bp.route('/send_message', methods=['POST'])
@jwt_required()
def send_message():
    current_user_identity = get_jwt_identity()
    data = request.get_json()
    sender_id = current_user_identity['id']
    receiver_id = data.get('receiver_id')
    content = data.get('content')

    new_message = Message(sender_id=sender_id, receiver_id=receiver_id, content=content)

    db.session.add(new_message)
    db.session.commit()
    
    

    return jsonify({"msg": "Message sent successfully"}), 201


#soket io config :




@message_bp.route('/received_messages/<int:user_id>', methods=['GET'])
@jwt_required()
def received_messages(user_id):
    user = User.query.get_or_404(user_id)
    messages = Message.query.filter_by(receiver_id=user.id).all()
    

    return jsonify(
        {"data":[{
        'id': message.id,
        'content': message.content,
        'timestamp': message.timestamp,
        'sender_id': message.sender_id
    } for message in messages]}), 200


@message_bp.route('/messages', methods=['GET'])
@jwt_required()
def all():
    
    messages = Message.query.all()
    

    return jsonify(
        {"data":[{
        'id': message.id,
        'content': message.content,
        'timestamp': message.timestamp,
        'sender_id': message.sender_id,
        'receiver_id':message.receiver_id
    } for message in messages]}), 200
    
    
#delete Message 

@message_bp.route('/delete_messages/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_message(id):
    try:
        message = Message.query.get(id)
        if not message:
            return jsonify({"message":"Le message n\'existe pas"}),404
        db.session.delete(message)
        db.session.commit()
        return jsonify({"message": "sucess dellete "}),200   
    except Exception as e:
        db.session.rollback()
        return jsonify({"message":str(e)}),500    
    
    

    
    
    
 #list des message envoye par le user connecté a un autre user 
@message_bp.route('/messages/send_to/<int:user_id>', methods=['GET'])
@jwt_required()
def messages_send_to(user_id):
    #id du user connecté
    current_user_identity = get_jwt_identity()
    user_connected = current_user_identity['id']
    
    #user a qui le message est envoyer 
    user = User.query.get_or_404(user_id)
    
    # list des message envoyé a cet user 
    messages = Message.query.filter_by(receiver_id=user.id,sender_id=user_connected).all()
    

    return jsonify(
        {"data":[{
        'id': message.id,
        'content': message.content,
        'timestamp': message.timestamp,
        'sender_id': message.sender_id,
        'receiver_id':message.receiver_id
    } for message in messages]}), 200
    
     #list des message envoye par le user connecté a un autre user 
@message_bp.route('/messages/recieve_to/<int:user_id>', methods=['GET'])
@jwt_required()
def recieve_to(user_id):
    #id du user connecté
    current_user_identity = get_jwt_identity()
    user_connected = current_user_identity['id']
    
    #user a qui le message est recus 
    user = User.query.get_or_404(user_id)
    
    # list des message recu de cet user 
    messages = Message.query.filter_by(receiver_id=user_connected,sender_id=user.id).all()
    

    return jsonify(
        {"data":[{
        'id': message.id,
        'content': message.content,
        'timestamp': message.timestamp,
        'sender_id': message.sender_id,
        'receiver_id':message.receiver_id
    } for message in messages]}), 200
    
    
    
#post enpoint 
# add a post     
@message_bp.route('/add_post', methods=['POST'])
@jwt_required()
def addPost():
    current_user_identity = get_jwt_identity()
    data = request.get_json()
    sender_id = current_user_identity['id']  
    content = data.get('content')
    
    # Convertir le contenu en bytes
    content_bytes = content.encode('utf-8')

    new_poste = Poste(sender_id=sender_id,  content=content_bytes)

    db.session.add(new_poste)
    db.session.commit()
    

    return jsonify({"msg": "Message sent successfully"}), 201


#list of post 

@message_bp.route('/liste_poste', methods=['GET'])
@jwt_required()
def all_poste():
    
    postes = Poste.query.all()
    
    return jsonify(
        {"data":[{
        'id': poste.id,
        'content': poste.content.decode('utf-8'),
        'timestamp': poste.timestamp,
        'sender_id': poste.sender_id,
    } for poste in postes]}), 200
    
#post des contactes 
@message_bp.route('/contacts_posts', methods=['GET'])
@jwt_required()
def contacts_posts():
    current_user_identity = get_jwt_identity()
    current_user = User.query.get(current_user_identity['id'])
    
    if not current_user:
        return jsonify({"msg": "User not found"}), 404
    
    # Récupérer les contacts de l'utilisateur connecté
    contacts = current_user.contacts.all()
    contact_ids = [contact.id for contact in contacts]
    
    # Récupérer les posts des contacts
    contacts_posts = Poste.query.filter(Poste.sender_id.in_(contact_ids)).all()
    
    # Construire la réponse JSON
    posts_data = [
        {
            'id': post.id,
            'content': post.content.decode('utf-8'),
            'timestamp': post.timestamp,
            'contact': {
                'id': post.sender.id,
                'username': post.sender.username,
                'phone_number': post.sender.phone_number,
                'email': post.sender.email,
                'img': photos.url(post.sender.img) if post.sender.img else None
            }
        }
        for post in contacts_posts
    ]
    
    return jsonify({"data": posts_data}), 200

# own post 
@message_bp.route('/own_post', methods=['GET'])
@jwt_required()
def own_posts():
    current_user_identity = get_jwt_identity()
    current_user = User.query.get(current_user_identity['id'])
    
    if not current_user:
        return jsonify({"msg": "User not found"}), 404
    
    # post du user conecter 
    postes=Poste.query.filter(Poste.sender_id==current_user.id)
    
   
    # Construire la réponse JSON
    posts_data = [
        {
            'id': post.id,
            'content': post.content.decode('utf-8'),
            'timestamp': post.timestamp,
            'contact': {
                'id': post.sender.id,
                'username': post.sender.username,
                'phone_number': post.sender.phone_number,
                'email': post.sender.email,
                'img': photos.url(post.sender.img) if post.sender.img else None
            }
        }
        for post in postes
    ]
    
    return jsonify({"data": posts_data}), 200

#delete a post 
@message_bp.route('/delete_post/<int:id>', methods=['DELETE'])
@jwt_required()
def deletePost(id):
    try:
        poste=Poste.query.get(id)
        if not poste:
            return jsonify({"message":"Le Poste n\'existe pas"}),404
        db.session.delete(poste)
        db.session.commit()
        return jsonify({"message": "sucess dellete "}),200   
    except Exception as e:
        db.session.rollback()
        return jsonify({"message":str(e)}),500    

