from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, FileField, TextAreaField, EmailField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Regexp
from flask_wtf.file import FileAllowed, FileRequired

class ConnexionForm(FlaskForm):  # ✅ Hérite correctement, pas de désactivation CSRF
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    submit = SubmitField('Se connecter')

class InscriptionForm(FlaskForm):
    nom = StringField('Nom', validators=[DataRequired()])
    prenom = StringField('Prénom', validators=[DataRequired()])
    email = StringField('Email', validators=[
        DataRequired(),
        Email(),
        Regexp(r'^[\w\.-]+@gmail\.com$', message="L'email doit être une adresse Gmail valide.")
    ])
    numero = StringField('Numéro de téléphone', validators=[
        DataRequired(),
        Regexp(r'^\d{8}$', message="Le numéro doit comporter exactement 8 chiffres.")
    ])
    password = PasswordField('Mot de passe', validators=[
        DataRequired(),
        Length(min=8, message="Le mot de passe doit contenir au moins 8 caractères."),
        Regexp(r'.*[A-Z].*', message="Le mot de passe doit contenir au moins une majuscule."),
        Regexp(r'.*[a-z].*', message="Le mot de passe doit contenir au moins une minuscule."),
        Regexp(r'.*\d.*', message="Le mot de passe doit contenir au moins un chiffre."),
        Regexp(r'.*[\W_].*', message="Le mot de passe doit contenir un caractère spécial.")
    ])
    confirm_password = PasswordField('Confirmer le mot de passe', validators=[
        DataRequired(), EqualTo('password')
    ])
    matricule = StringField('Matricule', validators=[DataRequired()])
    annee = SelectField('Année', choices=[('L1', 'L1'), ('L2', 'L2'), ('L3', 'L3')], validators=[DataRequired()])
    filiere = SelectField('Filière', choices=[('MI', 'Math-Info'), ('PC', 'Physique-Chimie'), ('SVT', 'SVT')], validators=[DataRequired()])
    submit = SubmitField("S'inscrire")

class DemandeForm(FlaskForm):
    type_demande = SelectField(
        'Type de demande',
        choices=[
            ('attestation_diplome', 'Attestation de diplôme'),
            ('diplome', 'Diplôme de licence'),
            ('attestation_passage_3A', 'Attestation de passage en 3e année'),
            ('duplicata_attestation', 'Duplicata attestation de diplôme')
        ],
        validators=[DataRequired(message="Veuillez sélectionner un type de demande.")]
    )

    annee_scolaire = StringField(
        'Année scolaire',
        validators=[
            DataRequired(message="L’année scolaire est requise."),
            Regexp(r'^\d{4}-\d{4}$', message="Format attendu : AAAA-AAAA (ex. 2022-2023)")
        ]
    )

    numero_quittance = StringField(
        'Numéro de quittance',
        validators=[DataRequired(message="Le numéro de quittance est requis.")]
    )

    fichier_acte_naissance = FileField(
        'Acte de naissance (PDF)',
        validators=[
            FileRequired(message="Veuillez fournir l’acte de naissance."),
            FileAllowed(['pdf'], 'Seuls les fichiers PDF sont acceptés.')
        ]
    )

    fichier_carte_etudiant = FileField(
        'Carte d’étudiant (PDF)',
        validators=[
            FileRequired(message="Veuillez fournir la carte d’étudiant."),
            FileAllowed(['pdf'], 'Seuls les fichiers PDF sont acceptés.')
        ]
    )

    fichier_releve_notes = FileField(
        'Relevé de notes (PDF)',
        validators=[
            FileRequired(message="Veuillez fournir le relevé de notes."),
            FileAllowed(['pdf'], 'Seuls les fichiers PDF sont acceptés.')
        ]
    )

    fichier_demande_au_doyen = FileField(
        'Demande au doyen (PDF)',
        validators=[
            FileRequired(message="Veuillez fournir la demande adressée au doyen."),
            FileAllowed(['pdf'], 'Seuls les fichiers PDF sont acceptés.')
        ]
    )

    recu = FileField(
        'Reçu de paiement (PDF)',
        validators=[
            FileRequired(message="Veuillez fournir le reçu de paiement."),
            FileAllowed(['pdf'], 'Seuls les fichiers PDF sont acceptés.')
        ]
    )

    piece = FileField(
        'Autre document justificatif (PDF)',
        validators=[
            FileRequired(message="Veuillez fournir le document justificatif."),
            FileAllowed(['pdf'], 'Seuls les fichiers PDF sont acceptés.')
        ]
    )

    submit = SubmitField('Soumettre la demande')

class MessageForm(FlaskForm):
    matricule = StringField('Matricule', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    contenu = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('Envoyer')

class MessageFormAdmin(FlaskForm):
    contenu = TextAreaField('Votre réponse', validators=[DataRequired()])
    submit = SubmitField('Envoyer')


class ReponseForm(FlaskForm):
    reponse = TextAreaField('Réponse', validators=[DataRequired()])
    submit = SubmitField('Envoyer la réponse')



class ContactForm(FlaskForm):
    email = StringField('Votre adresse email', validators=[DataRequired(), Email()])
    sujet = StringField('Sujet', validators=[DataRequired()])
    message = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('Envoyer')


class ConfirmationForm(FlaskForm):
    nom = StringField("Nom", validators=[
        DataRequired(),
        Regexp(r"^[A-Za-zÀ-ÖØ-öø-ÿ' -]+$", message="Nom invalide.")
    ])

    prenom = StringField("Prénom", validators=[
        DataRequired(),
        Regexp(r"^[A-Za-zÀ-ÖØ-öø-ÿ' -]+$", message="Prénom invalide.")
    ])

    matricule = StringField("Matricule", validators=[
        DataRequired(),
        Regexp(r"^[0-9A-Za-z-]+$", message="Matricule invalide.")
    ])

    email = EmailField("Email", validators=[
        DataRequired(),
        Email(message="Adresse email invalide.")
    ])

    numero = StringField(
        "Numéro de téléphone",
        default="01",
        validators=[
            DataRequired(),
            Regexp(r"^01\d{8}$", message="Le numéro doit commencer par 01 et contenir 10 chiffres.")
        ],
        description="Commence par 01 et contient exactement 10 chiffres."
    )

    password = PasswordField(
        "Mot de passe",
        validators=[
            DataRequired(),
            Length(min=8, message="Le mot de passe doit contenir au moins 8 caractères."),
            Regexp(
                r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).*$",
                message="Le mot de passe doit contenir une majuscule, une minuscule, un chiffre et un caractère spécial."
            )
        ],
        description="Min. 8 caractères, avec majuscule, minuscule, chiffre, et caractère spécial."
    )

    confirm_password = PasswordField(
        "Confirmer le mot de passe",
        validators=[
            DataRequired(),
            EqualTo("password", message="Les mots de passe ne correspondent pas.")
        ]
    )

    submit = SubmitField("Valider mon identité")

class SuppressionForm(FlaskForm):
    submit = SubmitField('Supprimer') 