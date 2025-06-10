from app import db, create_app
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = create_app()

with app.app_context():
    db.create_all()
    print("✅ Tables créées avec succès dans la base de données.")



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(80), nullable=False)
    prenom = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)  # email doit être unique
    password = db.Column(db.String(200), nullable=False)  # on stocke souvent des mots de passe hashés (donc plus longs)
    confirm_password = db.Column(db.String(200), nullable=False)  # mais en vrai on ne stocke pas ce champ !
    matricule = db.Column(db.String(80), unique=True, nullable=False)  # chaque étudiant a un matricule unique
    annee = db.Column(db.String(10), nullable=False)
    filiere = db.Column(db.String(80), nullable=False)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Crée toutes les tables définies par les modèles
    app.run(debug=True)
