from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_wtf import CSRFProtect
from flask_mail import Mail
from flask_talisman import Talisman
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import logging
from logging.handlers import RotatingFileHandler
import os

# Ajouter cet import
from dotenv import load_dotenv

from app.config import Config

# Extensions globales
db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
csrf = CSRFProtect()
mail = Mail()
limiter = Limiter(key_func=get_remote_address, default_limits=["100 per minute"])

login.login_view = 'routes.connexion'

def create_app():
    # Charger le fichier .env (mettre le chemin selon ta structure)
    basedir = os.path.abspath(os.path.dirname(__file__))
    load_dotenv(os.path.join(basedir, '..', '.env'))  # .. car __init__.py est dans app/

    app = Flask(__name__)
    app.config.from_object(Config)

    # Vérification de la clé secrète
    if not app.config.get("SECRET_KEY"):
        app.config['SECRET_KEY'] = 'dev-secret-key-123'

    # Initialisation des extensions avec l'app Flask
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    csrf.init_app(app)
    mail.init_app(app)
    limiter.init_app(app)

    # Sécurisation HTTPS + headers HTTP sécurisés
    # Pour dev local sans HTTPS, mettre force_https=False
    Talisman(app, content_security_policy=None, force_https=True)

    # Import des modules internes
    from app import models
    from app.routes import routes
    app.register_blueprint(routes)

    # Chargement utilisateur flask-login
    @login.user_loader
    def load_user(user_id):
        return models.Utilisateur.query.get(int(user_id))

    # Logging avec rotation
    if not app.debug and not app.testing:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/app.log', maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('Application démarrée')

    return app
