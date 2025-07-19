from app import create_app

app = create_app()

if __name__ == '__main__':
    # Activation du HTTPS avec les certificats générés
    app.run(debug=True, ssl_context=('cert.pem', 'key.pem'),host='0.0.0.0')
