from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from app import db
from hashlib import sha256
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin 

class Utilisateur(db.Model, UserMixin):
    __tablename__ = 'utilisateurs'

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    prenom = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='etudiant')
    matricule = db.Column(db.String(20))
    numero = db.Column(db.String(20))
    annee = db.Column(db.String(10))
    filiere = db.Column(db.String(100))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<Utilisateur {self.email}>"


class Demande(db.Model):
    __tablename__ = 'demandes'

    id = db.Column(db.Integer, primary_key=True)
    type_demande = db.Column(db.String(50), nullable=True)
    fichier_acte_naissance = db.Column(db.String(200), nullable=True)
    fichier_carte_etudiant = db.Column(db.String(200), nullable=True)
    fichier_releve_notes = db.Column(db.String(200), nullable=True)
    fichier_demande_au_doyen = db.Column(db.String(200), nullable=True)
    fichier_recu = db.Column(db.String(200), nullable=True)
    fichier_piece = db.Column(db.String(200), nullable=True)
    numero_quittance = db.Column(db.String(50), nullable=True)
    quittance_valide = db.Column(db.Boolean, default=True)
    annee_scolaire = db.Column(db.String(20), nullable=True)
    date_demande = db.Column(db.DateTime, default=datetime.utcnow)
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)
    statut = db.Column(db.String(20), default='En attente')
    raison_refus = db.Column(db.String(255))

    utilisateur_id = db.Column(db.Integer, db.ForeignKey('utilisateurs.id'), nullable=True)
    utilisateur = db.relationship(
        "Utilisateur",
        backref=db.backref("documents_admin", overlaps="demandes"),
        overlaps="demandes"
    )

    documents_admin = db.relationship(
        'DocumentAdmin',
        back_populates='demande',
        lazy=True,
        overlaps="demandes"
    )

    def statut_affichage(self):
        return {
            "En attente": "🕒 En attente",
            "Validée": "✅ Validée",
            "Refusée": f"❌ Refusée ({self.raison_refus})"
        }.get(self.statut, self.statut)


class DocumentAdmin(db.Model):
    __tablename__ = 'documents_admin'

    id = db.Column(db.Integer, primary_key=True)
    type_document = db.Column(db.String(100), nullable=False)
    filename = db.Column(db.String(150), nullable=False)
    annee = db.Column(db.String(10), nullable=True)
    filiere = db.Column(db.String(100), nullable=True)
    date_upload = db.Column(db.DateTime, default=datetime.utcnow)
    hash_document = db.Column(db.String(64), unique=True, nullable=True) 
    qr_code_path = db.Column(db.String(255))  # ✅ si tu veux le chemin du fichier avec QR

    demande_id = db.Column(db.Integer, db.ForeignKey('demandes.id'), nullable=True)

    demande = db.relationship("Demande", back_populates="documents_admin")


class Admin(db.Model):
    __tablename__ = 'admins'

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    prenom = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class MessageContact(db.Model):
    __tablename__ = 'messages_contact'

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100))
    email = db.Column(db.String(120))
    sujet = db.Column(db.String(200))
    contenu = db.Column(db.Text)
    date_envoi = db.Column(db.DateTime, default=datetime.utcnow)
    reponse = db.Column(db.Text, nullable=True)
    date_reponse = db.Column(db.DateTime, nullable=True)
    lu_par_admin = db.Column(db.Boolean, default=False)
    visible_admin = db.Column(db.Boolean, default=True)

    user_id = db.Column(db.Integer, db.ForeignKey('utilisateurs.id'), nullable=False)
    utilisateur = db.relationship('Utilisateur', backref='messages_contact')


class EtudiantReference(db.Model):
    __tablename__ = 'etudiants_reference'

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    prenom = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    matricule = db.Column(db.String(20), unique=True, nullable=False)
    numero = db.Column(db.String(20))
    annee = db.Column(db.String(10))
    filiere = db.Column(db.String(100))
    compte_active = db.Column(db.Boolean, default=False)


class ResultatAcademique(db.Model):
    __tablename__ = 'resultats_academiques'

    id = db.Column(db.Integer, primary_key=True)
    matricule = db.Column(db.String(20), nullable=False)
    annee_scolaire = db.Column(db.String(20), nullable=False)
    niveau = db.Column(db.String(10), nullable=False)
    valide = db.Column(db.Boolean, default=False)


class ReferenceQuittance(db.Model):
    __tablename__ = 'references_quittances'

    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.String(100), unique=True, nullable=False)

    def __repr__(self):
        return f"<ReferenceQuittance {self.numero}>"
