# setup_data.py

from app import create_app, db
from app.models import Utilisateur, EtudiantReference, ReferenceQuittance
import os

app = create_app()

def ajouter_admin():
    ancien = Utilisateur.query.filter_by(email='gounouzime50@gmail.com').first()
    if ancien:
        db.session.delete(ancien)
        db.session.commit()
        print("Ancien administrateur supprimé.")

    admin = Utilisateur(
        nom='GOUNOU',
        prenom='Zimé',
        email='gounouzime50@gmail.com',
        matricule='ADMIN002',
        annee='',
        filiere='',
        role='admin'
    )
    admin.set_password('admin456')
    db.session.add(admin)
    db.session.commit()
    print("✅ Nouvel administrateur ajouté.")


def ajouter_etudiants_reference():
    etudiants = [
        EtudiantReference(nom="SOHO", prenom="Fresnel", email="sohofresnelsimonyelihan@gmail.com", matricule="11186STI23", filiere="Mathematiques Informatique", annee="2025-2026"),
        EtudiantReference(nom="KONE", prenom="Fatou", email="fatoukone@gmail.com", matricule="20200234", filiere="Physique Chimie", annee="2020-2021"),
        EtudiantReference(nom="DIALLO", prenom="Moussa", email="moussadiallo@gmail.com", matricule="20190321", filiere="SVT", annee="2019-2020"),
        EtudiantReference(nom="SOW", prenom="Aïcha", email="aichasow@gmail.com", matricule="20230456", filiere="Mathematiques Informatique", annee="2023-2024"),
        EtudiantReference(nom="HOUNTONDJI", prenom="Michel", email="hountonmichel@gmail.com", matricule="11109STII23", filiere="Mathematiques Informatique", annee="2021-2022"),
        EtudiantReference(nom="AGOSSOU", prenom="Grégoire", email="aggossou@gmail.com", matricule="20230401", filiere="SVT", annee="2023-2024"),
        EtudiantReference(nom="EMINNEM", prenom="Marchall", email="eminem@gmail.com", matricule="20230567", filiere="Physique Chimie", annee="2019-2020"),
        EtudiantReference(nom="AKODEGNON", prenom="Crepin", email="crepin@gmail.com", matricule="20230756", filiere="Mathematiques Informatique", annee="2018-2019"),
        EtudiantReference(nom="LAMAR", prenom="Kendrick", email="kendrick@gmail.com", matricule="20233356", filiere="Mathematiques Informatique", annee="2023-2024"),
    ]

    ajout = 0
    for etu in etudiants:
        if not EtudiantReference.query.filter_by(matricule=etu.matricule).first():
            db.session.add(etu)
            ajout += 1
    db.session.commit()
    print(f"✅ {ajout} étudiants de référence ajoutés.")


def ajouter_quittances():
    path = os.path.join(os.path.dirname(__file__), "quittances.txt")
    if not os.path.exists(path):
        print("❌ Fichier quittances.txt introuvable.")
        return

    with open(path, "r") as f:
        lignes = [ligne.strip() for ligne in f if ligne.strip()]

    ajout = 0
    for numero in lignes:
        if not ReferenceQuittance.query.filter_by(numero=numero).first():
            rq = ReferenceQuittance(numero=numero)
            db.session.add(rq)
            ajout += 1
    db.session.commit()
    print(f"✅ {ajout} numéros de quittance ajoutés.")


def main():
    with app.app_context():
        db.create_all()
        ajouter_admin()
        ajouter_etudiants_reference()
        ajouter_quittances()
        print("🎉 Données initiales importées avec succès.")


if __name__ == "__main__":
    main()
