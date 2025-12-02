from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
username = os.environ.get('DATABASE_USERNAME')
password = os.environ.get('DATABASE_PASSWORD')
host = os.environ.get('DATABASE_HOST')
db_name = os.environ.get('DATABASE_NAME')
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{username}:{password}@{host}/{db_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialisation des extensions
db = SQLAlchemy(app)
login_manager = LoginManager(app)

# Configuration de Flask-Login
login_manager.login_view = 'login'  # Vue vers laquelle rediriger si non connecté
login_manager.login_message = 'Veuillez vous connecter pour accéder à cette page.'
login_manager.login_message_category = 'info'

# Importations pour éviter les dépendances circulaires
# Ces imports doivent être APRÈS l'initialisation de 'app' et 'db'
from app import routes, models

# Configuration du user_loader pour Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return models.User.query.get(int(user_id))