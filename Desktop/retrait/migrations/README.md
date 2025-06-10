Single-database configuration for Flask.
# Système de Gestion des Demandes de Retrait d'Attestation et Diplôme

## Description

Ce projet est une application web développée avec **Flask**, **HTML**, et **CSS** destinée à faciliter la gestion des demandes de retrait d'attestation et de diplôme pour la Faculté des Sciences et Techniques de Natitingou.

L'application permet aux étudiants de soumettre leurs demandes en ligne, aux administrateurs de valider ou refuser ces demandes, et d'envoyer les documents correspondants une fois la demande validée. Un système de messagerie intégré permet la communication entre étudiants et administrateurs.

---

## Fonctionnalités principales

- Soumission en ligne des demandes d'attestation ou de diplôme par les étudiants.
- Upload de pièces justificatives (fichiers PDF uniquement).
- Validation ou refus des demandes par l’administrateur avec motifs de refus.
- Upload des documents validés pour mise à disposition aux étudiants.
- Suivi du statut des demandes côté étudiant.
- Système de messagerie privé entre étudiants et administrateurs.
- Tableau de bord admin avec gestion simplifiée des demandes et des messages.

---

## Technologies utilisées

- **Python 3.x** avec le framework **Flask**
- **HTML5**, **CSS3** pour les interfaces utilisateurs
- **SQLite** (ou autre base de données) pour le stockage des données
- Gestion des fichiers uploadés côté serveur

---

## Installation

1. Clonez ce dépôt :

   ```bash
   git clone <URL_DU_DEPOT>
   cd nom_du_projet
Créez un environnement virtuel Python :

bash
Copier
Modifier
python -m venv venv
source venv/bin/activate  # Sur Windows : venv\Scripts\activate
Installez les dépendances :

bash
Copier
Modifier
pip install -r requirements.txt
Lancez l’application :

bash
Copier
Modifier
flask run
Ouvrez votre navigateur à l’adresse :

cpp
Copier
Modifier
http://127.0.0.1:5000
Utilisation
Étudiants : s’inscrire, se connecter, soumettre une demande, suivre son statut, consulter les documents validés, et envoyer des messages.

Administrateurs : se connecter, gérer les demandes (valider/refuser), uploader les documents validés, répondre aux messages des étudiants.

Structure du projet
routes.py : gestion des routes Flask.

templates/ : fichiers HTML.

static/ : fichiers CSS, JavaScript, images.

uploads/ : dossier pour stocker les fichiers uploadés.

models.py (optionnel) : définition des modèles de données.

Contribution
Les contributions sont les bienvenues !
Merci de forker le projet et de proposer une pull request.

Licence
Ce projet est sous licence MIT.
Voir le fichier LICENSE pour plus de détails.

Contact
Pour toute question ou suggestion, vous pouvez me contacter à :
votre.email@example.com

Développé par [GOUNOU Zimé]
Faculté des Sciences et Techniques de Natitingou

