from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from flask_socketio import emit, join_room, leave_room
import socketio
from app import db
from models.messages import Message
from models.users import User

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