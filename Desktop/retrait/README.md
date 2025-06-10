 
Single-database configuration for Flask.
# 🎓 Système de Gestion des Demandes de Retrait d’Attestation et de Diplôme

## 📌 Description du projet

Ce projet est une application web développée avec **Flask**, **HTML**, **CSS** et **SQLAlchemy**, permettant aux étudiants d’effectuer des **demandes de retrait d’attestation ou de diplôme** de manière numérique.

Les fonctionnalités principales incluent :
- Authentification sécurisée pour les étudiants enregistrés.
- Soumission de demandes avec des pièces justificatives obligatoires (au format PDF).
- Validation automatique du **numéro de quittance bancaire**.
- Tableau de bord administrateur pour valider ou refuser les demandes.
- Téléchargement du diplôme ou attestation par l’étudiant une fois validée.
- Système de **messagerie privée** entre l’administrateur et les étudiants.

## 🧑‍🎓 Fonctionnalités pour les étudiants

- ✅ Accès restreint uniquement aux étudiants inscrits dans la base de données.
- 📝 Formulaire d'inscription sécurisé.
- 🔐 Connexion et accès au tableau de bord personnel.
- 📄 Faire une demande de :
  - Attestation de diplôme
  - Diplôme de licence
  - Attestation de duplicata de diplôme
  - Attestation de passage en 3e année
- 📤 Téléversement de documents justificatifs.
- 🔎 Vérification du **numéro de quittance** via la base de la banque :
  - Rejet si le numéro n’existe pas ou a déjà été utilisé.
- 📥 Téléchargement du document validé.
- 📬 Envoi de message à l’administrateur.

## 🛠️ Fonctionnalités pour l’administrateur

- 👁️ Visualisation de toutes les demandes soumises.
- 📂 Accès aux documents fournis par les étudiants.
- ❌ Refus de la demande avec indication obligatoire d’une raison.
- ✅ Validation de la demande et envoi du diplôme final.
- 📧 Réponse aux messages des étudiants.
- 🔔 Notification des nouveaux messages.

## 💻 Technologies utilisées

- [x] Flask (framework backend Python)
- [x] HTML / CSS (interfaces utilisateurs)
- [x] SQLAlchemy (ORM pour la base de données)
- [x] Environnement virtuel Python (`venv`)

## 🚀 Lancement de l'application

1. Cloner le dépôt ou copier les fichiers dans un dossier.
2. Créer un environnement virtuel :

```bash
python -m venv venv
Activer l’environnement virtuel :

Sur Windows :

bash
Copier
Modifier
venv\Scripts\activate
Sur macOS/Linux :

bash
Copier
Modifier
source venv/bin/activate
Installer les dépendances :

bash
Copier
Modifier
pip install -r requirements.txt
Lancer le serveur Flask :

bash
Copier
Modifier
flask run
Ouvrir le lien affiché dans le navigateur, généralement :
http://127.0.0.1:5000

🗂️ Organisation des fichiers
bash
Copier
Modifier
/retrait
│
├── app.py / routes.py         # Fichier principal de l’application Flask
├── templates/                 # Fichiers HTML
├── static/                    # Fichiers CSS et autres ressources statiques
├── models.py                  # Modèles SQLAlchemy
├── README.md                  # Ce fichier
├── requirements.txt           # Bibliothèques Python requises
📧 Contact
Pour toute question, veuillez contacter l’administrateur via le système de messagerie intégré ou par email.

Contribution
Les contributions sont les bienvenues !
Merci de forker le projet et de proposer une pull request.

Licence
Ce projet est sous licence MIT.
Voir le fichier LICENSE pour plus de détails.

Contact
Pour toute question ou suggestion, vous pouvez me contacter à :
gounouzime50@gmail.com

Développé par [GOUNOU Zimé]
Faculté des Sciences et Techniques de Natitingou

