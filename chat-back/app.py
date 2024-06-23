from datetime import datetime, timedelta
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager, get_jwt_identity, jwt_required
from flask_uploads import UploadSet, configure_uploads, IMAGES


app = Flask(__name__)
CORS(app)
app.config.from_object('config.Config')


#config upload_img
app.config['UPLOADED_PHOTOS_DEST'] = 'uploads/images'
photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)


db = SQLAlchemy(app)
migrate = Migrate(app, db)

# jwt config 

jwt = JWTManager(app)

app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=2)


@jwt.unauthorized_loader
def unauthorized_response(callback):
    return jsonify({
        'msg': 'Missing Authorization Header'
    }), 401

@jwt.invalid_token_loader
def invalid_token_response(callback):
    return jsonify({
        'msg': 'Invalid Token'
    }), 422
    
    




## import of models
from models.users import User
from models.messages import Message

## import of blue print in routes
from routes.auth_route import auth_bp
from routes.messages_route import message_bp
from routes.users_route import users_bp

# registration of blueprint in app 

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(message_bp, url_prefix='/chat')
app.register_blueprint(users_bp, url_prefix='/user')

if __name__ == '__main__':
    app.run(debug=True)