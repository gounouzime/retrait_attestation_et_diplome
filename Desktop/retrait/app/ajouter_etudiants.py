from app import app, db
from models import EtudiantReference

with app.app_context():
    etudiants = [
        EtudiantReference(nom="SOHO", prenom="Fresnel", email="sohofresnelsimonyelihan@gmail.com", matricule="11186STI23", filiere="Mathematiques Informatique", annee="2025-2026"),
        EtudiantReference(nom="KONE", prenom="Fatou", email="fatoukone@gmail.com", matricule="20200234", filiere="Physique Chimie", annee="2020-2021"),
        EtudiantReference(nom="DIALLO", prenom="Moussa", email="moussadiallo@gmail.com", matricule="20190321", filiere="SVT", annee="2019-2020"),
        EtudiantReference(nom="SOW", prenom="Aïcha", email="aichasow@gmail.com", matricule="20230456", filiere="Mathematiques Informatique", annee="2023-2024"),
    ]

    db.session.bulk_save_objects(etudiants)
    db.session.commit()
    print("Étudiants de référence ajoutés avec succès.")
