import os
from datetime import datetime
import pandas as pd
from utils import hash_password, verify_password
from pathlib import Path

class Database:
    def __init__(self, db_dir=None, file_name="users.csv"):
        self.db_dir = Path(db_dir) if db_dir else Path(__file__).parent / "database"
        self.file_path = self.db_dir / file_name
        self.users_df = pd.DataFrame()
        self.__check_database()
        self.load_users()

    def __check_database(self):
        self.db_dir.mkdir(parents=True, exist_ok=True)

        if not self.file_path.exists():
            data = {
                "username": "admin",
                "password": "admin",
                "email": "admin@example.com",
                "admin": True
            }
            self.users_df = self.add_user(data)

    def _create_user_dataframe(self, username, password, email="", admin=False):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data = {
            "username": [username],
            "password": [hash_password(password)],
            "email": [email],
            "admin": [admin],
            "created_at": [timestamp],
            "updated_at": [timestamp]
        }
        return pd.DataFrame(data)

    def load_users(self):
        if self.file_path.exists():
            self.users_df = pd.read_csv(self.file_path)
        return self.users_df
    
    def save_users(self):
        self.db_dir.mkdir(parents=True, exist_ok=True)
        self.users_df.to_csv(self.file_path, index=False)

    def authenticate_user(self, username: str, password: str):
        """
        Authentifie un utilisateur en vérifiant son nom d'utilisateur et son mot de passe.
        
        Args:
            username (str): Le nom d'utilisateur à authentifier.
            password (str): Le mot de passe fourni pour l'authentification.
            
        Returns:
            tuple: (dictionnaire utilisateur, message d'erreur)
                - Si authentification réussie : (utilisateur, None)
                - Si échec : (None, message d'erreur)
        """
        try:
            # Filtrer le DataFrame pour trouver la ligne correspondant au nom d'utilisateur fourni
            user_rows = self.users_df[self.users_df['username'] == username]

            # Vérifier si aucun utilisateur n'a été trouvé
            if user_rows.empty:
                raise ValueError(f"Aucun utilisateur avec le nom d'utilisateur '{username}' trouvé !")

            # Vérifier s'il y a plusieurs utilisateurs avec le même nom d'utilisateur
            if len(user_rows) > 1:
                raise ValueError(f"Erreur : plusieurs utilisateurs avec le nom d'utilisateur '{username}' trouvés !")

            # Récupérer le mot de passe stocké pour l'utilisateur trouvé
            stored_password = user_rows['password'].values[0]

            # Vérifier si le mot de passe fourni correspond au mot de passe stocké
            if verify_password(password, stored_password):
                # Si le mot de passe est correct, convertir la ligne utilisateur en dictionnaire
                current_user = user_rows.to_dict(orient='records')[0]
                return current_user, None  # Authentification réussie

            # Si le mot de passe est incorrect
            return None, "Mot de passe incorrect"

        except ValueError as e:
            # Capturer et retourner les erreurs liées à l'utilisateur (non trouvé ou doublons)
            return None, str(e)

    def add_user(self, data):
        try:
            new_user_df = self._create_user_dataframe(**data)
            self.users_df = pd.concat([self.users_df, new_user_df], ignore_index=True)
            self.save_users()
            return True, None
        except Exception as e:
            return False, f"{type(e).__name__}: {str(e)}"

    def user_exists(self, username: str) -> tuple[bool, str | None]:
        """
        Vérifie si un utilisateur existe déjà dans le DataFrame et qu'il est unique.

        Args:
            username (str): le nom d'utilisateur à vérifier

        Returns:
            tuple[bool, str | None]:
                - (True, None) si l'utilisateur existe et est unique
                - (False, None) si l'utilisateur n'existe pas
                - (False, message_erreur) si doublons ou exception
        """
        try:
            user_rows = self.users_df[self.users_df['username'] == username]

            if user_rows.empty:
                return False, None
            elif len(user_rows) > 1:
                return False, f"Plusieurs utilisateurs trouvés avec le nom '{username}'"
            else:
                return True, None

        except Exception as e:
            return False, str(e)

    def authenticate_user(self, username: str, password: str):
        try:
            user_rows = self.users_df[self.users_df['username'] == username]
            
            if user_rows.empty:
                return None, f"Aucun utilisateur avec le nom d'utilisateur '{username}' trouvé !"
            if len(user_rows) > 1:
                return None, f"Erreur : plusieurs utilisateurs avec le nom d'utilisateur '{username}' trouvés !"
            
            stored_password = user_rows['password'].values[0]
            if verify_password(password, stored_password):
                current_user = user_rows.to_dict(orient='records')[0]
                return current_user, None
            return None, "Mot de passe incorrect"

        except Exception as e:
            return None, f"{type(e).__name__}: {str(e)}"
    
    def delete_user(self, username: str):
        try:
            # Recharger les utilisateurs
            self.load_users()

            # Vérifier que l'utilisateur existe
            if username not in self.users_df['username'].values:
                return False, f"L'utilisateur '{username}' n'existe pas."

            # Supprimer l'utilisateur
            self.users_df = self.users_df[self.users_df['username'] != username]

            # Sauvegarder
            self.save_users()

            return True, None

        except Exception as e:
            return False, f"{type(e).__name__}: {str(e)}"

    def update_user(self, new_data: dict):
        try:
            # Recharger les utilisateurs
            self.load_users()

            # Trouver l'index de l'utilisateur
            idx_list = self.users_df.index[self.users_df['username'] == new_data['username']].tolist()

            idx = idx_list[0]

            # Mettre à jour le mot de passe si présent
            if 'password' in new_data and new_data['password']:
                self.users_df.at[idx, 'password'] = hash_password(new_data['password'])

            # Mettre à jour l'email si présent
            if 'email' in new_data and new_data['email']:
                self.users_df.at[idx, 'email'] = new_data['email']

            # Mettre à jour la date de modification
            self.users_df.at[idx, 'updated_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Sauvegarder le CSV
            self.save_users()

            return True, None

        except Exception as e:
            return False, f"{type(e).__name__}: {str(e)}"