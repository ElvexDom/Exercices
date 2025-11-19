import pandas as pd
from utils import Screen
from .database import Database

class UserAuth:
    """Classe pour gérer le hash des mots de passe et la connexion des utilisateurs."""

    def __init__(self):
        self.currentUser = None
        self.db = Database()
        self.screen = Screen()

    def login(self):
        """Récupération des identifiants depuis l'interface et connexion"""
        username, password = self.screen.login()
        self.currentUser, error = self.db.authenticate_user(username, password)
        if self.currentUser and not error:
            if self.currentUser.get('admin'):
                self.navigate()
            else:
                self.read_all()
        else:
            self.screen.show_message(error)

    def navigate(self):
        choix = self.screen.menu()
        match choix:
            case "1":
                self.read_all()
            case "2":
                self.create()
            case "3":
                self.update()
            case "4":
                self.delete()
            case "5":
                return
        return self.navigate()

    def read_all(self):
        df_display = self.db.load_users().to_dict(orient='records')
        users_display = [user for user in df_display if user.get('username') != self.currentUser['username']]
        self.screen.afficher_users(users_display)
        return

    def create(self):
        """
        Crée un nouvel utilisateur après saisie et vérification.
        Affiche les messages et demande d'appuyer sur Entrée pour continuer.
        """
        user_data, error_data = self.screen.askUserData("création")
        message = None

        if error_data:
            message = error_data
        elif not user_data:
            message = "Aucune donnée utilisateur fournie."
        else:
            username = user_data.get("username")
            existing_user, error_user = self.db.user_exists(username)

            if error_user:
                message = error_user
            elif existing_user:
                message = "Utilisateur '{username}' déjà existant."
            else:
                creation_success, creation_error = self.db.add_user(user_data)
                if creation_success:
                    message = f"Utilisateur '{username}' créé avec succès !"
                else:
                    message = creation_error

        self.screen.show_message(message)
        
    def delete(self):
        """
        Supprime un utilisateur après saisie et vérification.
        Affiche les messages et demande d'appuyer sur Entrée pour continuer.
        """
        user_data, error = self.screen.askUserData("suppression")  # user_data est un dict {"username": ...}
        message = None

        if error:
            message = error
        elif not user_data or "username" not in user_data:
            message = "Aucun nom d'utilisateur fourni."
        else:
            username = user_data.get("username")
            existing_user, error_user = self.db.user_exists(username)

            if error_user:
                message = error_user
            elif not existing_user:
                message = f"Utilisateur '{username}' non existant."
            else:
                deletion_success, deletion_error = self.db.delete_user(username)
                if deletion_success:
                    message = f"Utilisateur '{username}' supprimé avec succès !"
                else:
                    message = deletion_error

        self.screen.show_message(message)

    def update(self):
        """
        Met à jour un utilisateur après saisie et vérification.
        Affiche les messages et demande d'appuyer sur Entrée pour continuer.
        """
        user_data, error = self.screen.askUserData("modification")
        message = None

        if error:
            message = error
        elif not user_data or "username" not in user_data:
            message = "Aucune donnée utilisateur fournie."
        else:
            username = user_data["username"]
            existing_user, error_user = self.db.user_exists(username)

            if error_user:
                message = error_user
            elif not existing_user:
                message = f"Utilisateur '{username}' n'existe pas."
            else:
                update_success, update_error = self.db.update_user(user_data)
                if update_success:
                    message = f"Utilisateur '{username}' mis à jour avec succès !"
                else:
                    message = update_error

        self.screen.show_message(message)
