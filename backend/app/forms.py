from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Optional
from app.models import User


class SignupForm(FlaskForm):
    username = StringField('Nom d\'utilisateur',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Mot de passe', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirmer le mot de passe',
                                     validators=[DataRequired(), EqualTo('password',
                                                                         message='Les mots de passe doivent correspondre.')])
    submit = SubmitField('Créer le compte')

    def validate_username(self, username):
        """Vérifie si le nom d'utilisateur est déjà pris."""
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Ce nom d\'utilisateur est déjà pris.')

    def validate_email(self, email):
        """Vérifie si l'email est déjà pris."""
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Cet email est déjà utilisé.')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    remember = BooleanField('Se souvenir de moi')
    submit = SubmitField('Se connecter')


class MessageForm(FlaskForm):
    content = TextAreaField('Votre message', validators=[DataRequired(), Length(min=5, max=500)])

    # Champs optionnels pour l'utilisateur spécial (ID=2)
    first_name = StringField('Prénom (optionnel)', validators=[Optional(), Length(max=100)])
    last_name = StringField('Nom (optionnel)', validators=[Optional(), Length(max=100)])

    submit = SubmitField('Envoyer le message')