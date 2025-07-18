import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'vraiclefsupersecrete123'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB

    # === Flask-Mail Config ===
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = "gounouzime50@gmail.com"  # remplace par ton adresse
    MAIL_PASSWORD = "vvzgziobfrjfktsr"          # remplace par ton mot de passe
    MAIL_DEFAULT_SENDER = MAIL_USERNAME 
