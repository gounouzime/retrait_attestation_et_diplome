from app import create_app, db
from app.models import Utilisateur
from flask_migrate import upgrade

app = create_app()

def init_admin():
    with app.app_context():
        # Exécuter les migrations
        upgrade()
        print("✅ Migration effectuée avec succès.")

        # Vérifier s’il y a déjà un admin
        if not Utilisateur.query.filter_by(email='gounouzime50@gmail.com').first():
            admin = Utilisateur(
                nom='GOUNOU',
                prenom='Zimé',
                email='gounouzime50@gmail.com',
                matricule='ADMIN002',
                role='admin'
            )
            admin.set_password('admin456')
            db.session.add(admin)
            db.session.commit()
            print("✅ Administrateur créé.")
        else:
            print("ℹ️ Administrateur déjà existant.")

if __name__ == '__main__':
    init_admin()
    app.run(debug=True, host='0.0.0.0', port=10000)
