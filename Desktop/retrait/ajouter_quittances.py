from app import create_app, db
from app.models import ReferenceQuittance

app = create_app()

with app.app_context():
    with open("quittances.txt", "r") as f:
        lignes = f.readlines()
        numeros = [ligne.strip() for ligne in lignes if ligne.strip()]

        for numero in numeros:
            # Vérifier si le numéro existe déjà avant d'ajouter
            exists = ReferenceQuittance.query.filter_by(numero=numero).first()
            if not exists:
                rq = ReferenceQuittance(numero=numero)
                db.session.add(rq)

        db.session.commit()
    print("Numéros ajoutés avec succès.")
