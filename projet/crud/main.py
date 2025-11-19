from user_management import UserAuth

class System:
    def __init__(self):
        self.auth = UserAuth()
        pass

    def start(self):
        """Lance le système."""
        self.auth.login()


# Point d'entrée
if __name__ == "__main__":
    system = System()
    system.start()
