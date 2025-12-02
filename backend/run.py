import os
from app import app, db
from app.models import User
from sqlalchemy.exc import OperationalError
from werkzeug.security import generate_password_hash  # <--- IMPORTATION CLÉ
import time

# --- Logique d'initialisation de l'application ---

MAX_RETRIES = 10
RETRY_DELAY = 5  # secondes

print("Démarrage du script d'initialisation...")

for i in range(MAX_RETRIES):
    try:
        # Pousse un contexte d'application
        with app.app_context():

            # 1. Crée toutes les tables si elles n'existent pas
            print("Tentative de création des tables (db.create_all())...")
            db.create_all()
            print("Tables vérifiées/créées.")

            # 2. Logique de "Seeding" :
            # Vérifie si l'utilisateur admin (ID=1) n'existe pas
            if User.query.get(1) is None:
                print("Création de l'utilisateur Admin (ID=1)...")
                # Génère le hash pour 'admin123'
                admin_hash = generate_password_hash("admin123", method="scrypt")

                admin_user = User(
                    id=1,
                    username='admin',
                    email='admin@carnet.com',
                    password_hash=admin_hash,
                    is_admin=True
                )
                db.session.add(admin_user)
                print("Utilisateur Admin ajouté à la session.")

            # Vérifie si l'utilisateur spécial (ID=2) n'existe pas
            if User.query.get(2) is None:
                print("Création de l'utilisateur Spécial (ID=2)...")
                # Génère le hash pour 'special123'
                special_hash = generate_password_hash("special123", method="scrypt")

                special_user = User(
                    id=2,
                    username='special',
                    email='special@carnet.com',
                    password_hash=special_hash,
                    is_admin=False
                )
                db.session.add(special_user)
                print("Utilisateur Spécial ajouté à la session.")

            # 3. Commit les nouveaux utilisateurs (s'il y en a)
            db.session.commit()
            print("Commit de la session de seeding effectué.")

            # 4. S'assure que le prochain ID auto-incrémenté est correct
            try:
                max_id = db.session.execute(db.text('SELECT MAX(id) FROM user')).scalar() or 0
                next_id = max_id + 1
                db.session.execute(db.text(f'ALTER TABLE user AUTO_INCREMENT = {next_id};'))
                db.session.commit()
                print(f"AUTO_INCREMENT pour la table 'user' mis à {next_id}.")
            except Exception as e:
                print(f"Avertissement lors de la mise à jour de AUTO_INCREMENT: {e}")
                db.session.rollback()

            print("Initialisation de la base de données terminée avec succès.")
            break

    except OperationalError as e:
        print(f"Échec de la connexion à la DB (Tentative {i + 1}/{MAX_RETRIES}): {e}")
        if i == MAX_RETRIES - 1:
            print("Échec final de l'initialisation de la DB.")
            raise e
        print(f"Nouvelle tentative dans {RETRY_DELAY} secondes...")
        time.sleep(RETRY_DELAY)

    except Exception as e:
        print(f"Erreur inattendue lors de l'initialisation: {e}")
        if i == MAX_RETRIES - 1:
            raise e
        print(f"Nouvelle tentative dans {RETRY_DELAY} secondes...")
        time.sleep(RETRY_DELAY)

# --- Point d'entrée pour le débogage local ---
if __name__ == '__main__':
    print("Lancement en mode débogage local...")
    app.run(debug=True, host='0.0.0.0')