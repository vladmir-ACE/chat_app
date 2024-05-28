from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required
from app import db
from models.messages import Message
from models.users import User

message_bp = Blueprint('chat', __name__)

@message_bp.route('/send_message', methods=['POST'])
@jwt_required()
def send_message():
    data = request.get_json()
    sender_id = data.get('sender_id')
    receiver_id = data.get('receiver_id')
    content = data.get('content')

    new_message = Message(sender_id=sender_id, receiver_id=receiver_id, content=content)

    db.session.add(new_message)
    db.session.commit()

    return jsonify({"msg": "Message sent successfully"}), 201


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
