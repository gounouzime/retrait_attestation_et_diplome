from app import create_app, db
from app.models import Utilisateur

app = create_app()

with app.app_context():
    # Supprimer l'utilisateur existant avec le même email s'il existe
    ancien = Utilisateur.query.filter_by(email='gounouzime50@gmail.com').first()
    if ancien:
        db.session.delete(ancien)
        db.session.commit()
        print("Ancien utilisateur supprimé.")

    # Créer le nouvel admin
    nouvel_admin = Utilisateur(
        nom='GOUNOU',
        prenom='Zimé',
        email='gounouzime50@gmail.com',
        matricule='ADMIN002',
        annee='',
        filiere='',
        role='admin'
    )
    nouvel_admin.set_password('admin456')  # Définis un mot de passe sécurisé

    db.session.add(nouvel_admin)
    db.session.commit()
    print("Nouvel administrateur ajouté avec succès.")
