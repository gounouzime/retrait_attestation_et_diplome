from app import create_app, db
from app.models import EtudiantReference

app = create_app()

etudiants = [
        EtudiantReference(nom="GOUNOU", prenom="Zimé", email="gounouzime50@gmail.com", matricule="11170STI22", filiere="Mathematiques Informatiques", annee="2021-2022"),
        EtudiantReference(nom="SOHO", prenom="Fresnel", email="sohofresnelsimonyelihan@gmail.com", matricule="11186STI23", filiere="Mathematiques Informatiques", annee="2025-2026"),
        EtudiantReference(nom="KONE", prenom="Fatou", email="fatoukone@gmail.com", matricule="20200234", filiere="Physique Chimie", annee="2020-2021"),
        EtudiantReference(nom="DIALLO", prenom="Moussa", email="moussadiallo@gmail.com", matricule="20190321", filiere="SVT", annee="2019-2020"),
        EtudiantReference(nom="SOW", prenom="Aïcha", email="aichasow@gmail.com", matricule="20230456", filiere="Mathematiques Informatique", annee="2023-2024"),
    ]

with app.app_context():  # 🔁 CONTEXTE D'APPLICATION
    if not EtudiantReference.query.first():  # ✅ VÉRIFICATION ICI
        db.session.bulk_save_objects(etudiants)
        db.session.commit()
        print("✅ Étudiants insérés avec succès.")
    else:
        print("ℹ️ Étudiants déjà présents. Aucune insertion.")
