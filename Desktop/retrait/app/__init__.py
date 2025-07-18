from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_wtf import CSRFProtect
from flask_mail import Mail
from app.config import Config

# Initialisations globales des extensions
db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
csrf = CSRFProtect()
mail = Mail()

login.login_view = 'routes.connexion'  # Redirection si @login_required

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Assure-toi que la clé secrète est bien dans Config aussi
    if not app.config.get("SECRET_KEY"):
        app.config['SECRET_KEY'] = 'dev-secret-key-123'  # fallback pour développement

    # Initialisation des extensions avec l'app Flask
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    csrf.init_app(app)        # ✅ Protection CSRF activée
    mail.init_app(app)

    # Importation des modèles et routes
    from app import models
    from app.routes import routes
    app.register_blueprint(routes)

    # Chargement de l'utilisateur pour flask-login
    @login.user_loader
    def load_user(user_id):
        return models.Utilisateur.query.get(int(user_id))

    return app
