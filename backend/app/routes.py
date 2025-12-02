from flask import render_template, url_for, flash, redirect
from app import app, db
from app.forms import SignupForm, LoginForm, MessageForm
from app.models import User, Message
from flask_login import login_user, current_user, logout_user, login_required


# --- Routes d'Authentification ---

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = SignupForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        # Par défaut, is_admin est False
        db.session.add(user)
        db.session.commit()
        flash('Votre compte a été créé ! Vous pouvez maintenant vous connecter.', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html', title='Créer un compte', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            flash('Connexion réussie !', 'success')
            return redirect(url_for('index'))
        else:
            flash('Échec de la connexion. Veuillez vérifier l\'email et le mot de passe.', 'danger')
    return render_template('login.html', title='Se connecter', form=form)


@app.route("/logout")
def logout():
    logout_user()
    flash('Vous avez été déconnecté.', 'info')
    return redirect(url_for('login'))


# --- Route Principale (Carnet de bienvenue) ---

@app.route("/", methods=['GET', 'POST'])
@app.route("/index", methods=['GET', 'POST'])
@login_required
def index():
    form = MessageForm()

    # --- Logique de Soumission (POST) ---
    if form.validate_on_submit():
        # Cas 1 : Utilisateur Spécial (ID=2)
        if current_user.id == 2:
            msg = Message(content=form.content.data,
                          author=current_user,
                          first_name=form.first_name.data,
                          last_name=form.last_name.data)
            db.session.add(msg)
            db.session.commit()
            flash('Votre message a été envoyé !', 'success')

        # Cas 2 : Utilisateur Normal (ni admin, ni ID=2)
        elif not current_user.is_admin:
            if not current_user.messages:  # Vérifie s'il n'a pas déjà posté
                msg = Message(content=form.content.data, author=current_user)
                db.session.add(msg)
                db.session.commit()
                flash('Votre message a été envoyé !', 'success')
            else:
                flash('Vous avez déjà envoyé un message.', 'warning')

        # Cas 3 : Administrateur (tente de poster)
        else:
            flash('Les administrateurs ne peuvent pas poster de messages.', 'info')

        return redirect(url_for('index'))  # Redirige pour éviter double soumission

    # --- Logique d'Affichage (GET) ---

    # 1. Déterminer quels messages afficher
    messages_to_display = []
    if current_user.is_admin:
        # L'admin voit TOUT
        messages_to_display = Message.query.order_by(Message.created_at.desc()).all()
    elif current_user.id == 2:
        # L'utilisateur spécial (ID=2) ne voit RIEN
        messages_to_display = []
    else:
        # L'utilisateur normal ne voit QUE les siens
        messages_to_display = current_user.messages  # Utilise la relation

    # 2. Déterminer si le formulaire doit être affiché
    show_form = False
    if current_user.id == 2:
        # L'utilisateur spécial voit TOUJOURS le formulaire
        show_form = True
    elif not current_user.is_admin and not current_user.messages:
        # L'utilisateur normal voit le formulaire SEULEMENT s'il n'a pas posté
        show_form = True

    return render_template('index.html',
                           title='Carnet de Bienvenue',
                           form=form,
                           messages=messages_to_display,
                           show_form=show_form)


@app.route("/delete_message/<int:message_id>", methods=['POST'])
@login_required
def delete_message(message_id):
    # 1. Sécurité : Vérifier si l'utilisateur est un admin
    if not current_user.is_admin:
        flash('Cette action est réservée aux administrateurs.', 'danger')
        return redirect(url_for('index'))

    # 2. Trouver le message ou renvoyer une erreur 404 s'il n'existe pas
    message_to_delete = Message.query.get_or_404(message_id)

    # 3. Supprimer le message de la base de données
    db.session.delete(message_to_delete)
    db.session.commit()

    flash('Le message a été supprimé avec succès.', 'success')
    return redirect(url_for('index'))