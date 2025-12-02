from datetime import datetime
from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


# Le 'UserMixin' ajoute les propriétés requises par Flask-Login (is_authenticated, etc.)
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)

    # Relation : Un utilisateur peut avoir plusieurs messages
    messages = db.relationship('Message', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

    def set_password(self, password):
        """Crée un hash sécurisé pour le mot de passe."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Vérifie si le mot de passe fourni correspond au hash."""
        return check_password_hash(self.password_hash, password)


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # Champs spécifiques pour l'utilisateur spécial (ID=2)
    first_name = db.Column(db.String(100), nullable=True)
    last_name = db.Column(db.String(100), nullable=True)

    # Clé étrangère
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Message('{self.content[:20]}...', Auteur: {self.user_id})"