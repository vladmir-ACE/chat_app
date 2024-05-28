import os

class Config:
    SECRET_KEY ='your_secret_key'
    SQLALCHEMY_DATABASE_URI = 'mysql://root:@localhost/chat_app'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'your_jwt_secret_key'
