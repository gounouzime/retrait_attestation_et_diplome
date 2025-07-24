from app import db, create_app
from app.models import EtudiantReference

app = create_app()

with app.app_context():
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

    db.session.commit()
    print("Étudiants de référence ajoutés avec succès.")
