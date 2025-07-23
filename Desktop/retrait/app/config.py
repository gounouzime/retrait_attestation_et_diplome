import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
# Charge le fichier .env à la racine du projet (un niveau au-dessus de app/)
load_dotenv(os.path.join(basedir, '..', '.env'))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'vraiclefsupersecrete123'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    UPLOAD_FOLDER = os.path.join(basedir, 'static', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB

    # Flask-Mail Config - chargement depuis .env ou fallback
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.gmail.com'
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'True').lower() in ['true', '1', 't']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = MAIL_USERNAME

    # Sécurité cookies
    SESSION_COOKIE_SECURE = True          # cookie envoyé uniquement sur HTTPS
    SESSION_COOKIE_HTTPONLY = True        # pas accessible via JS (XSS)
    SESSION_COOKIE_SAMESITE = 'Lax'       # limite fuite cookie cross-site

    REMEMBER_COOKIE_SECURE = True
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_SAMESITE = 'Lax'

    # Debug / Testing
    DEBUG = False    # ne pas afficher erreurs détaillées en prod
    TESTING = False
    
    MAX_CONTENT_LENGTH = 32 * 1024 * 1024  # 32 Mo
 
