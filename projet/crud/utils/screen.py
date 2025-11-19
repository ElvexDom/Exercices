import os

class Screen:
    def clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def login(self):
        self.clear()
                
        print("=" * 50)
        print("       Connexion à l'application       ".center(50))
        print("=" * 50)
        
        username = input("Nom d'utilisateur : ")
        password = input("Mot de passe     : ")
        
        return username, password

    def menu(self):
        while True:
            self.clear()
                    
            # Affichage de l'encadré
            print("=" * 73)
            print("MENU PRINCIPAL".center(73))
            print("=" * 73)
            print("\n[1] Lire     [2] Créer     [3] Modifier     [4] Supprimer     [5] Quitter\n")
            print("=" * 73)
            
            # Saisie du choix
            choix = input("Entrez le numéro du choix : ").strip()
            
            if choix in map(str, range(1, 6)):
                return choix
            

    def _collectUserInput(self, action: str, display_text: str):
        # méthode privée, accessible uniquement depuis la classe
        match action:
            case "création":
                # Saisie obligatoire
                while True:
                    self.clear()
                    print(display_text)
                    password = input("Mot de passe      : ").strip()
                    if password:
                        display_text += f"\nMot de passe      : {password}"
                        break

                while True:
                    self.clear()
                    print(display_text)
                    email = input("Email             : ").strip()
                    if email:
                        break

                data = {"password": password, "email": email}

            case "modification":
                # Saisie libre (pas obligatoire)
                password = input("Mot de passe (vide = inchangé) : ").strip()
                email = input("Email (vide = inchangé)        : ").strip()
                data = {}
                if password:
                    data.update({"password": password})
                if email:
                    data.update({"email": email})
        return data

    def afficher_users(self, users):
        """
        Affiche les utilisateurs sur une seule ligne par utilisateur,
        avec des colonnes de largeur fixe de 25 caractères.
        """
        self.clear()
        print("=" * 100)
        print("=== Liste des utilisateurs ===".center(100))
        print("=" * 100 + "\n")

        if not users:
            print("Aucun utilisateur à afficher.".center(100))
            print("\n" + "=" * 100 + "\n")
            input("\nAppuyez sur Entrée pour continuer...")
            return

        # Largeur fixe pour toutes les colonnes
        col_width = 25

        # En-tête
        print(f"{'Username'.ljust(col_width)}{'Email'.ljust(col_width)}{'Créé le'.ljust(col_width)}{'Modifié le'.ljust(col_width)}")
        print("-" * (col_width * 4))

        # Affichage des utilisateurs
        for user in users:
            print(
                f"{str(user.get('username','')).ljust(col_width)}"
                f"{str(user.get('email','')).ljust(col_width)}"
                f"{str(user.get('created_at','')).ljust(col_width)}"
                f"{str(user.get('updated_at','')).ljust(col_width)}"
            )

        print("=" * (col_width * 4))
        input("Appuyez sur Entrée pour continuer...")


    def askUserData(self, action: str):
        try:
            username = ""
            while username.strip() == "":
                self.clear()
                display_text = ""
                width = 60
                display_text += "=" * width + "\n" + f"=== {action.capitalize()} d'un utilisateur ===".center(width) + "\n" + "=" * width + "\n"
                print(display_text)
                username = input("Nom d'utilisateur : ").strip()
                data = {"username": username}
                display_text += f"Nom d'utilisateur : {username}"

            match action:
                case "création":
                    # Saisie obligatoire
                    while True:
                        self.clear()
                        print(display_text)
                        password = input("Mot de passe      : ").strip()
                        if password:
                            display_text += f"\nMot de passe      : {password}"
                            break

                    while True:
                        self.clear()
                        print(display_text)
                        email = input("Email             : ").strip()
                        if email:
                            break

                    data.update({"password": password, "email": email})

                case "modification":
                    # Saisie libre (pas obligatoire)
                    password = input("Mot de passe (vide = inchangé) : ").strip()
                    email = input("Email (vide = inchangé)        : ").strip()
                    if password:
                        data.update({"password": password})
                    if email:
                        data.update({"email": email})

            while True:
                self.clear()
                confirmation = input(f"Confirmer la {action} de l'utilisateur '{username}' ? (o/n) : ").strip().lower()
                if confirmation == "o":
                    self.clear()
                    return data, None
                elif confirmation == "n":
                    return None, None
                else:
                    print("Réponse invalide, veuillez entrer 'o' ou 'n'.")

        except Exception as e:
            return None, str(e)


    def show_message(self, message: str):
        self.clear()
        # Largeur totale de l'encadrement
        width = max(50, len(message) + 10)  # au moins 50 caractères ou un peu plus que le message

        # Ligne du dessus
        print("!" * width)

        # Ligne vide avec bordures
        print("!" + " " * (width - 2) + "!")

        # Ligne du message centré
        print("!" + message.center(width - 2) + "!")

        # Ligne vide avec bordures
        print("!" + " " * (width - 2) + "!")

        # Ligne du dessous
        print("!" * width)
        input("Appuyez sur Entrée pour continuer...")