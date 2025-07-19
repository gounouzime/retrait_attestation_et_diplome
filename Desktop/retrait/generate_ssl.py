from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from datetime import datetime, timedelta

# Générer la clé privée
key = rsa.generate_private_key(public_exponent=65537, key_size=2048)

# Détails du certificat
subject = issuer = x509.Name([
    x509.NameAttribute(NameOID.COUNTRY_NAME, u"BJ"),
    x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"Natitingou"),
    x509.NameAttribute(NameOID.LOCALITY_NAME, u"Natitingou"),
    x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"Université de Natitingou"),
    x509.NameAttribute(NameOID.COMMON_NAME, u"localhost"),
])

cert = x509.CertificateBuilder().subject_name(subject).issuer_name(issuer).public_key(
    key.public_key()).serial_number(x509.random_serial_number()).not_valid_before(
    datetime.utcnow()).not_valid_after(
    datetime.utcnow() + timedelta(days=365)
).sign(key, hashes.SHA256())

# Enregistrer la clé privée
with open("key.pem", "wb") as f:
    f.write(key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    ))

# Enregistrer le certificat
with open("cert.pem", "wb") as f:
    f.write(cert.public_bytes(serialization.Encoding.PEM))

print("✅ Fichiers 'key.pem' et 'cert.pem' générés.")
