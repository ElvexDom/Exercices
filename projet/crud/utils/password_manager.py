import bcrypt

class PasswordManager:
    """
    Classe pour gérer le hash des mots de passe et la vérification.
    """

    @staticmethod
    def hash_password(password: str) -> str:
        """
        Hash un mot de passe en utilisant bcrypt.
        Renvoie le hash sous forme de chaîne.
        """
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    @staticmethod
    def verify_password(password: str, hashed: str) -> bool:
        """
        Vérifie qu'un mot de passe correspond à un hash.
        Renvoie True si correct, False sinon.
        """
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
