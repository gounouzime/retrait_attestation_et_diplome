# wsgi.py

from app import create_app, db
from setup_data import ajouter_admin, ajouter_etudiants_reference, ajouter_quittances

app = create_app()

with app.app_context():
    db.create_all()
    ajouter_admin()
    ajouter_etudiants_reference()
    ajouter_quittances()
