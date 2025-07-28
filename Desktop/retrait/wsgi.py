# wsgi.py

from app import create_app, db

app = create_app()

# Création automatique des tables à chaque démarrage si elles n'existent pas
with app.app_context():
    db.create_all()
