from datetime import datetime
import re
from email_validator import validate_email, EmailNotValidError

from flask import Blueprint, render_template, redirect, url_for, flash, request, session, send_from_directory, abort
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from sqlalchemy import func
from sqlalchemy.orm import joinedload
from app import db, csrf, mail
from werkzeug.security import generate_password_hash
from flask_mail import Message
import fitz  # PyMuPDF
import os
from functools import wraps

from app.models import Utilisateur, Admin, Demande, DocumentAdmin, MessageContact, EtudiantReference
from .forms import ConnexionForm, InscriptionForm, DemandeForm, ContactForm, MessageFormAdmin, ConfirmationForm, ReponseForm
from .config import Config

routes = Blueprint('routes', __name__)
UPLOAD_FOLDER = Config.UPLOAD_FOLDER

ALLOWED_EXTENSIONS = {'pdf'}

# ========== Fonction d'extraction du numéro quittance depuis un PDF ==========

def extraire_numero_quittance(chemin_pdf):
    try:
        import re
        import fitz  # PyMuPDF

        doc = fitz.open(chemin_pdf)
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()

        # Chercher "QT123456" ou "QX123456", etc.
        match = re.search(r"Q[A-Z]{0,2}\d{6,}", text)
        if match:
            return match.group(0)
    except Exception as e:
        print(f"Erreur extraction quittance : {e}")
    return None



# ========== Fonction de vérification des extensions ==========

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ========== Fonction de vérification des extensions ==========

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# ========== Décorateurs ==========

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('routes.connexion'))
        return f(*args, **kwargs)
    return decorated

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if session.get('role') != 'admin':
            flash("Accès administrateur requis.", "danger")
            return redirect(url_for('routes.connexion'))
        return f(*args, **kwargs)
    return decorated

def etudiant_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if session.get('role') != 'etudiant':
            flash("Accès étudiant requis.", "danger")
            return redirect(url_for('routes.connexion'))
        return f(*args, **kwargs)
    return decorated

# ========== Routes publiques ==========

@routes.route('/')
def accueil():
    return render_template('index.html')

@routes.route('/a_propos')
def a_propos():
    return render_template('a_propos.html')

@routes.route('/connexion', methods=['GET', 'POST'])
def connexion():
    form = ConnexionForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        utilisateur = Utilisateur.query.filter_by(email=email).first()
        if utilisateur and utilisateur.check_password(password):
            session['user_id'] = utilisateur.id
            session['role'] = utilisateur.role

            flash(f"Bienvenue {utilisateur.prenom.title()} !", "success")  # ✅ Ajout du message

            if utilisateur.role == 'admin':
                return redirect(url_for('routes.admin_dashboard'))
            else:
                return redirect(url_for('routes.etudiant_dashboard'))

        flash("Email ou mot de passe incorrect", "danger")
    return render_template('connexion.html', form=form)

@routes.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('routes.connexion'))

# ========== Tableau de bord étudiant ==========

@routes.route('/etudiant/dashboard')
@login_required
@etudiant_required
def etudiant_dashboard():
    user = Utilisateur.query.get(session['user_id'])
    demandes = Demande.query.filter_by(utilisateur_id=user.id).all()

    # Charger aussi la relation 'demande' dans documents pour éviter des requêtes supplémentaires dans le template
    documents = DocumentAdmin.query\
    .join(Demande, DocumentAdmin.demande_id == Demande.id)\
    .options(joinedload(DocumentAdmin.demande))\
    .filter(Demande.utilisateur_id == user.id)\
    .all()
    
    print(f"Documents récupérés ({len(documents)}):")
    for doc in documents:
        print(f"Document id={doc.id}, filename={doc.filename}, demande_id={doc.demande_id}")
        if doc.demande:
            print(f"  Demande id={doc.demande.id}, utilisateur_id={doc.demande.utilisateur_id}, type={doc.demande.type_demande}")
        else:
            print("  Pas de demande liée")
    
    return render_template('etudiant_dashboard.html', user=user, demandes=demandes, documents=documents)

@routes.route('/etudiant/demande', methods=['GET', 'POST'])
@login_required
@etudiant_required
def faire_demande():
    form = DemandeForm()
    if form.validate_on_submit():
        files = {
            'acte': form.fichier_acte_naissance.data,
            'carte': form.fichier_carte_etudiant.data,
            'releve': form.fichier_releve_notes.data,
            'demande': form.fichier_demande_au_doyen.data,
            'recu': form.recu.data,
            'piece': form.piece.data
        }

        timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
        filenames = {}
        paths = {}

        # Sauvegarde sécurisée des fichiers, avec contrôle si fichier manquant et extension autorisée
        for key, file in files.items():
            if not file:
                flash(f"Le fichier requis pour '{key}' est manquant.", "danger")
                return redirect(request.url)

            if not allowed_file(file.filename):
                flash(f"Le fichier '{file.filename}' pour '{key}' doit être au format PDF.", "danger")
                return redirect(request.url)

            filename = secure_filename(f"{timestamp}_{key}_{file.filename}")
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            try:
                file.save(file_path)
            except Exception as e:
                flash(f"Erreur lors de l'enregistrement du fichier {key}: {str(e)}", "danger")
                return redirect(request.url)
            filenames[key] = filename
            paths[key] = file_path

        # Extraction du numéro quittance dans le PDF reçu
        quittance_extraite = extraire_numero_quittance(paths['recu'])

        if not quittance_extraite:
            flash("Le numéro de quittance n’a pas pu être extrait du fichier PDF du reçu.", "danger")
            return redirect(request.url)

        if quittance_extraite != form.numero_quittance.data.strip():
            flash("Le numéro de quittance saisi ne correspond pas à celui présent dans le reçu PDF.", "danger")
            return redirect(request.url)

        # Vérifier si ce numéro est déjà utilisé
        deja_utilisee = Demande.query.filter_by(numero_quittance=quittance_extraite).first()
        if deja_utilisee:
            flash("Ce numéro de quittance a déjà été utilisé pour une autre demande.", "warning")
            return redirect(request.url)

        # Création et sauvegarde de la demande en base
        demande = Demande(
            type_demande=form.type_demande.data,
            fichier_acte_naissance=filenames['acte'],
            fichier_carte_etudiant=filenames['carte'],
            fichier_releve_notes=filenames['releve'],
            fichier_demande_au_doyen=filenames['demande'],
            fichier_recu=filenames['recu'],
            fichier_piece=filenames['piece'],
            numero_quittance=quittance_extraite,
            annee_scolaire=form.annee_scolaire.data,
            quittance_valide=True,
            statut='En attente',
            utilisateur_id=session['user_id']
        )

        db.session.add(demande)
        db.session.commit()

        flash("Votre demande a été envoyée avec succès. Elle sera examinée par l'administration. Vous serez notifié dès qu'une décision sera prise.", "success")
        return redirect(url_for('routes.etudiant_dashboard'))

    return render_template('demande_diplome.html', form=form)


# ========== Tableau de bord admin ==========

@routes.route('/admin/dashboard')
@login_required
@admin_required
def admin_dashboard():
    admin_user = Admin.query.get(session['user_id'])  # récupère l'admin connecté
    nb_non_lus = MessageContact.query.filter_by(lu_par_admin=False).count()
    return render_template('admin_dashboard.html', user=admin_user, nb_non_lus=nb_non_lus)

@routes.route('/admin/demandes')
@login_required
@admin_required
def admin_demandes():
    demandes = Demande.query.all()
    return render_template('admin_demandes.html', demandes=demandes)

@routes.route('/demande/modifier/<int:demande_id>', methods=['GET', 'POST'], endpoint='modifier_demande')
@login_required
def modifier_demande(demande_id):
    # Charger la demande précise de l'étudiant connecté
    demande = Demande.query.filter_by(id=demande_id, utilisateur_id=current_user.id).first_or_404()


    editable = demande.statut == 'Refusée'
    form = DemandeForm(obj=demande)

    if request.method == 'POST':
        if not editable:
            flash("Vous ne pouvez pas modifier cette demande.", "danger")
            return redirect(url_for('routes.faire_demande'))

        if form.validate_on_submit():
            form.populate_obj(demande)

            # Remettre le statut en attente après modification
            demande.statut = 'En attente'
            demande.raison_refus = None  # effacer la raison de refus

            # Gérer la sauvegarde des fichiers...

            db.session.commit()
            flash("Votre demande a été modifiée et renvoyée.", "success")
            return redirect(url_for('routes.faire_demande'))

    return render_template('demande_diplome.html', form=form, editable=editable, demande=demande)



@routes.route('/admin/upload/<int:demande_id>', methods=['POST'])
@login_required
@admin_required
def upload_document(demande_id):
    demande = Demande.query.get_or_404(demande_id)
    
    if demande.statut != 'Validée':
        flash("Impossible d'ajouter un document à une demande non validée.", "warning")
        return redirect(url_for('routes.admin_demandes'))

    fichier = request.files.get('document_admin')
    type_doc = request.form.get('type')

    if fichier and type_doc:
        if not allowed_file(fichier.filename):
            flash("Le fichier doit être au format PDF.", "danger")
            return redirect(url_for('routes.admin_demandes'))

        import time
        timestamp = time.strftime("%Y%m%d%H%M%S")
        nom_fichier = secure_filename(f"{timestamp}_{type_doc}_{fichier.filename}")
        fichier.save(os.path.join(UPLOAD_FOLDER, nom_fichier))

        etudiant = Utilisateur.query.get(demande.utilisateur_id)

        document = DocumentAdmin(
            type_document=type_doc,
            filename=nom_fichier,
            annee=demande.annee_scolaire,
            filiere=etudiant.filiere,
            demande_id=demande.id,
            # demande_id=demande.id si ce champ existe
        )
        db.session.add(document)
        db.session.commit()
        flash("Document uploadé avec succès.", "success")
    else:
        flash("Veuillez fournir un fichier et un type de document.", "danger")

    return redirect(url_for('routes.admin_demandes'))

@routes.route('/admin/etudiants')
@login_required
@admin_required
def liste_etudiants():
    etudiants = Utilisateur.query.filter_by(role='etudiant').all()
    return render_template('admin_etudiants.html', etudiants=etudiants)

@routes.route('/admin/etudiants/supprimer/<int:etudiant_id>', methods=['POST'])
@csrf.exempt
@login_required
@admin_required
def supprimer_etudiant(etudiant_id):
    etudiant = Utilisateur.query.get_or_404(etudiant_id)
    try:
        db.session.delete(etudiant)
        db.session.commit()
        flash('Étudiant supprimé avec succès.', 'success')
    except Exception as e:
        db.session.rollback()
        flash("Une erreur est survenue lors de la suppression.", "danger")
    return redirect(url_for('routes.liste_etudiants'))

# ========== Messagerie Admin ==========



# ========== Confirmation et inscription ==========

@routes.route('/confirmation', methods=['GET', 'POST'])
def confirmation():
    form = ConfirmationForm()

    if form.validate_on_submit():
        nom = form.nom.data.strip().lower()
        prenom = form.prenom.data.strip().lower()
        email = form.email.data.strip().lower()
        matricule = form.matricule.data.strip().upper()
        numero = form.numero.data.strip()
        password = form.password.data

        # Vérifier si l'étudiant existe dans EtudiantReference
        ref = EtudiantReference.query.filter(
            func.lower(EtudiantReference.nom) == nom,
            func.lower(EtudiantReference.prenom) == prenom,
            func.lower(EtudiantReference.email) == email,
            EtudiantReference.matricule == matricule
        ).first()

        if not ref:
            flash("Aucun étudiant correspondant trouvé. Veuillez vérifier vos informations.", "danger")
            return redirect(url_for('routes.confirmation'))

        # Vérifier s’il y a déjà un compte
        if Utilisateur.query.filter_by(email=ref.email).first():
            flash("Un compte est déjà associé à ces informations. Veuillez vous connecter.", "warning")
            return redirect(url_for('routes.connexion'))

        # Créer le compte utilisateur
        password_hash = generate_password_hash(password)

        nouvel_utilisateur = Utilisateur(
            nom=ref.nom,
            prenom=ref.prenom,
            email=ref.email,
            password_hash=password_hash,
            matricule=ref.matricule,
            numero=numero,
            annee=ref.annee,
            filiere=ref.filiere,
            role="etudiant"
        )

        db.session.add(nouvel_utilisateur)
        db.session.commit()

        flash("Confirmation réussie. Vous pouvez maintenant vous connecter.", "success")
        return redirect(url_for('routes.connexion'))

    return render_template('confirmation.html', form=form)

@routes.route('/contact_admin', methods=['GET', 'POST'])
@login_required
def contact_admin():
    user_id = session.get('user_id')
    user = Utilisateur.query.get(user_id)

    if not user:
        flash("Utilisateur introuvable. Veuillez vous reconnecter.", "danger")
        return redirect(url_for('routes.logout'))

    form = ContactForm()

    # ✅ On récupère bien uniquement les messages de l'étudiant connecté
    anciens_messages = MessageContact.query.filter(
        MessageContact.user_id == user.id
    ).order_by(MessageContact.date_envoi.desc()).all()

    if form.validate_on_submit():
        email_saisi = form.email.data.strip().lower()
        email_officiel = user.email.strip().lower()

        # Vérification que l'email saisi correspond au compte
        if email_saisi != email_officiel:
            flash("L'adresse email saisie ne correspond pas à votre compte.", "danger")
            return redirect(url_for('routes.contact_admin'))

        # Validation syntaxique de l'adresse
        try:
            validate_email(email_saisi)
        except EmailNotValidError:
            flash("Adresse e-mail invalide.", "danger")
            return redirect(url_for('routes.contact_admin'))

        # ✅ Enregistrement du message
        msg_obj = MessageContact(
            email=email_officiel,
            sujet=form.sujet.data.strip(),
            contenu=form.message.data.strip(),
            user_id=user.id
        )
        db.session.add(msg_obj)
        db.session.commit()

        # ✅ Notification admin
        admin_msg = Message(
            subject=form.sujet.data.strip(),
            sender=email_officiel,
            recipients=['gounouzime50@gmail.com'],
            reply_to=email_officiel
        )
        admin_msg.body = f"""
Nouveau message reçu :

Étudiant : {user.nom} {user.prenom}
Email    : {email_officiel}
Matricule: {user.matricule}

Sujet   : {form.sujet.data.strip()}

Message :
{form.message.data.strip()}
"""
        try:
            mail.send(admin_msg)
        except Exception:
            flash("Erreur lors de l'envoi de l'e-mail de notification.", "warning")

        flash("Message envoyé avec succès.", "success")
        return redirect(url_for('routes.contact_admin'))

    return render_template('contact.html', form=form, anciens_messages=anciens_messages)



@routes.route('/admin/repondre/<int:message_id>', methods=['POST'])
@login_required
@admin_required
def repondre_message(message_id):
    form = ReponseForm()

    if not form.validate_on_submit():
        flash("Veuillez saisir une réponse.", "danger")
        return redirect(url_for('routes.admin_messagerie'))

    message_origine = MessageContact.query.get_or_404(message_id)

    message_origine.reponse = form.reponse.data
    message_origine.date_reponse = datetime.utcnow()
    message_origine.lu_par_admin = True
    db.session.commit()

    try:
        msg = Message(
            subject=f"Réponse à votre message : {message_origine.sujet}",
            sender='admin@email.com',  # Remplace cette adresse par celle utilisée dans config
            recipients=[message_origine.email]
        )
        msg.body = form.reponse.data
        mail.send(msg)
        flash("Réponse envoyée avec succès.", "success")
    except Exception as e:
        flash(f"Erreur lors de l'envoi de l'e-mail : {str(e)}", "danger")

    return redirect(url_for('routes.admin_messagerie'))


@routes.route('/admin/messagerie')
@login_required
@admin_required
def admin_messagerie():
    messages = MessageContact.query.order_by(MessageContact.date_envoi.desc()).all()
    reponse_form = ReponseForm()
    return render_template('admin_messagerie.html', messages=messages, reponse_form=reponse_form)

@routes.route('/etudiant/message/supprimer/<int:message_id>', methods=['POST'])
@login_required
@etudiant_required
def supprimer_message_etudiant(message_id):
    message = MessageContact.query.get_or_404(message_id)
    if message.user_id != session['user_id']:
        flash("Action non autorisée.", "danger")
        return redirect(url_for('routes.contact_admin'))

    if message.reponse:
        flash("Ce message a déjà été répondu. Suppression impossible.", "warning")
        return redirect(url_for('routes.contact_admin'))

    try:
        db.session.delete(message)
        db.session.commit()
        flash("Message supprimé avec succès.", "success")
    except Exception:
        db.session.rollback()
        flash("Erreur lors de la suppression du message.", "danger")

    return redirect(url_for('routes.contact_admin'))


@routes.route('/admin/conversations')
@login_required
@admin_required
def liste_conversations():
    etudiants = Utilisateur.query \
        .join(MessageContact, MessageContact.user_id == Utilisateur.id) \
        .filter(Utilisateur.role == 'etudiant') \
        .distinct() \
        .all()
    return render_template('liste_conversation.html', etudiants=etudiants)

@routes.route('/admin/conversation/<int:user_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_conversation(user_id):
    etudiant = Utilisateur.query.get_or_404(user_id)
    messages = MessageContact.query \
        .filter_by(user_id=user_id) \
        .order_by(MessageContact.date_envoi.asc()) \
        .all()

    # Marquer comme lus
    for msg in messages:
        if not msg.lu_par_admin:
            msg.lu_par_admin = True
    db.session.commit()

    reponse_form = ReponseForm()

    if reponse_form.validate_on_submit():
        dernier_msg = messages[-1] if messages else None
        if dernier_msg:
            dernier_msg.reponse = reponse_form.reponse.data
            dernier_msg.date_reponse = datetime.utcnow()

            try:
                msg_email = Message(
                    subject=f"Réponse à votre message : {dernier_msg.sujet}",
                    sender='admin@email.com',
                    recipients=[etudiant.email],
                    body=reponse_form.reponse.data
                )
                mail.send(msg_email)
                db.session.commit()
                flash("Réponse envoyée avec succès.", "success")
            except Exception as e:
                flash(f"Erreur lors de l'envoi de l'e-mail : {str(e)}", "danger")

        return redirect(url_for('routes.admin_conversation', user_id=user_id))

    return render_template(
        'admin_messagerie.html',
        etudiant=etudiant,
        messages=messages,
        reponse_form=reponse_form
    )

@routes.route('/admin/message/supprimer/<int:message_id>', methods=['POST'])
@csrf.exempt 
@login_required
@admin_required
def supprimer_message(message_id):
    message = MessageContact.query.get_or_404(message_id)
    try:
        db.session.delete(message)
        db.session.commit()
        flash("Message supprimé avec succès.", "success")
    except Exception as e:
        db.session.rollback()
        flash("Une erreur est survenue lors de la suppression du message.", "danger")
    return redirect(request.referrer or url_for('routes.admin_messagerie'))


@routes.route('/uploads/<filename>')
@login_required
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


@routes.route('/telecharger/<filename>')
@login_required
def telecharger_fichier(filename):
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)





@routes.route('/admin/traiter_demande/<int:demande_id>', methods=['POST'])
@admin_required
def traiter_demande(demande_id):
    decision = request.form.get('decision')
    raison_refus = request.form.get('raison_refus')
    raison_perso = request.form.get('raison_personnalisee')

    demande = Demande.query.get_or_404(demande_id)

    if decision == 'valider':
        demande.statut = 'Validée'
        demande.raison_refus = None
        db.session.commit()
        flash("Demande validée. Vous pouvez maintenant uploader le diplôme.", "success")
        return redirect(url_for('routes.admin_demandes'))

    elif decision == 'refuser':
        # Si aucune raison n’est sélectionnée
        if not raison_refus:
            flash("Veuillez sélectionner une raison de refus.", "danger")
            return redirect(url_for('routes.admin_demandes'))

        # Si "autre" est sélectionnée mais aucun texte personnalisé n’est fourni
        if raison_refus == "autre":
            if not raison_perso or raison_perso.strip() == "":
                flash("Veuillez préciser la raison du refus.", "danger")
                return redirect(url_for('routes.admin_demandes'))
            demande.raison_refus = raison_perso
        else:
            demande.raison_refus = raison_refus

        demande.statut = 'Refusée'
        db.session.commit()
        flash("Demande refusée.", "warning")
        return redirect(url_for('routes.admin_demandes'))

    flash("Décision invalide.", "danger")
    return redirect(url_for('routes.admin_demandes'))


