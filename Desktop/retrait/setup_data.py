from flask_migrate import upgrade
from app import create_app, db
from app.models import Utilisateur, EtudiantReference, ReferenceQuittance

app = create_app()

with app.app_context():
    try:
        # 1. Appliquer les migrations
        upgrade()
        print("✅ Migration effectuée avec succès.")

        # 2. Suppression ancien administrateur s'il existe
        email_admin = "gounouzime50@gmail.com"
        ancien_admin = Utilisateur.query.filter_by(email=email_admin).first()
        if ancien_admin:
            db.session.delete(ancien_admin)
            db.session.commit()
            print("🗑️ Ancien administrateur supprimé.")

        # 3. Création du nouvel administrateur
        admin = Utilisateur(
            nom="GOUNOU",
            prenom="Zimé",
            email=email_admin,
            matricule="ADMIN002",
            annee="",
            filiere="",
            role="admin"
        )
        admin.set_password("admin456")
        db.session.add(admin)
        print("👤 Nouvel administrateur ajouté.")

        # 4. Étudiants de référence
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

        for etu in etudiants:
            exist = EtudiantReference.query.filter_by(matricule=etu.matricule).first()
            if not exist:
                db.session.add(etu)
                print(f"👨‍🎓 Ajouté : {etu.nom} {etu.prenom}")
            else:
                print(f"✅ Étudiant déjà existant : {etu.matricule}")

        # 5. Références quittances
        quittances = [
            ReferenceQuittance(numero="Q-2023-001"),
            ReferenceQuittance(numero="Q-2023-002"),
            ReferenceQuittance(numero="Q-2023-003"),
        ]

        for q in quittances:
            exist = ReferenceQuittance.query.filter_by(numero=q.numero).first()
            if not exist:
                db.session.add(q)
                print(f"💸 Ajouté quittance : {q.numero}")
            else:
                print(f"✅ Quittance déjà existante : {q.numero}")

        # 6. Commit final
        db.session.commit()
        print("🎉 Toutes les données ont été ajoutées avec succès.")

    except Exception as e:
        db.session.rollback()
        print(f"❌ Erreur lors de l'ajout des données : {e}")
