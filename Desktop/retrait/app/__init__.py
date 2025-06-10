from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_wtf import CSRFProtect
from flask_mail import Mail
from app.config import Config

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
csrf = CSRFProtect()
mail = Mail()  # <-- Ajouté

login.login_view = 'routes.connexion'

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    csrf.init_app(app)
    mail.init_app(app)  # <-- Initialisation Mail

    from app import models
    from app.routes import routes

    app.register_blueprint(routes)

    @login.user_loader
    def load_user(user_id):
        return models.Utilisateur.query.get(int(user_id))

    return app
