from app import create_app

app = create_app()

if __name__ == '__main__':
    # Activation du HTTPS avec les certificats générés
    app.run(debug=True, ssl_context=('cert.pem', 'key.pem'),host='0.0.0.0')
 def init_admin():
    from app.models import Utilisateur
    with app.app_context():
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
            print("Administrateur créé.")

init_admin()
