import random
import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class JeuPendu:
    def __init__(self):
        # --- Configuration du jeu ---
        self.liste_mots = ["python", "ordinateur", "hangman", "variable", "fonction"]
        self.mot_a_deviner = random.choice(self.liste_mots)
        self.mot_masque = ["_" for _ in self.mot_a_deviner]
        self.nb_erreurs = 0
        self.tentatives_max = 6
        self.lettres_devinees = []

        # --- Création de la fenêtre Tkinter ---
        self.root, self.fig, self.ax, self.canvas_widget = self.creer_fenetre()

        # --- Affichage initial du pendu ---
        self.afficher_pendu()

        # --- Lancement de la boucle principale ---
        self.root.mainloop()

    # --- Création de la fenêtre Tkinter ---
    def creer_fenetre(self):
        root = tk.Tk()
        root.title("Jeu du Pendu")

        # Frame pour le pendu
        frame_plot = tk.Frame(root)
        frame_plot.pack(pady=10)

        # Figure Matplotlib
        fig, ax = plt.subplots(figsize=(4, 6))
        canvas = FigureCanvasTkAgg(fig, master=frame_plot)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack()

        # Centrer la fenêtre
        root.update_idletasks()
        root.eval('tk::PlaceWindow . center')

        # Gestion propre de la fermeture
        root.protocol("WM_DELETE_WINDOW", lambda: (
            canvas_widget.destroy(),
            plt.close(fig),
            root.destroy()
        ))

        # --- Bind clavier pour capturer les lettres ---
        root.bind("<Key>", self.gestion_touche)

        # Stocker les objets pour les utiliser dans les méthodes
        self.fig = fig
        self.ax = ax
        self.canvas = canvas
        self.canvas_widget = canvas_widget

        return root, fig, ax, canvas_widget

    # --- Gestion des touches clavier ---
    def gestion_touche(self, event):
        lettre = event.char.lower()
        if lettre.isalpha():
            self.valider_lettre(lettre)

    # --- Affichage du pendu ---
    def afficher_pendu(self):
        self.ax.clear()

        # Potence
        self.ax.plot([0, 1], [0, 0], 'k')       # Base
        self.ax.plot([0.5, 0.5], [0, 1], 'k')   # Poteau vertical
        self.ax.plot([0.5, 1], [1, 1], 'k')     # Barre horizontale
        self.ax.plot([1, 1], [1, 0.8], 'k')     # Corde

        # Corps du pendu
        if self.nb_erreurs > 0:
            self.ax.add_patch(mpatches.Circle((1, 0.75), 0.05, fill=False, color='k'))  # Tête
        if self.nb_erreurs > 1:
            self.ax.add_patch(mpatches.FancyArrowPatch((1, 0.7), (1, 0.5), arrowstyle='-'))  # Corps
        if self.nb_erreurs > 2:
            self.ax.add_patch(mpatches.FancyArrowPatch((1, 0.65), (0.9, 0.6), arrowstyle='-'))  # Bras gauche
        if self.nb_erreurs > 3:
            self.ax.add_patch(mpatches.FancyArrowPatch((1, 0.65), (1.1, 0.6), arrowstyle='-'))  # Bras droit
        if self.nb_erreurs > 4:
            self.ax.add_patch(mpatches.FancyArrowPatch((1, 0.5), (0.9, 0.3), arrowstyle='-'))  # Jambe gauche
        if self.nb_erreurs > 5:
            self.ax.add_patch(mpatches.FancyArrowPatch((1, 0.5), (1.1, 0.3), arrowstyle='-'))  # Jambe droite

        # Mot masqué
        mot_affiche = " ".join(self.mot_masque)
        self.ax.text(0.5, 1.15, mot_affiche, fontsize=16, ha='center', fontfamily='monospace')

        self.ax.axis('off')
        self.ax.set_xlim(-0.2, 1.4)
        self.ax.set_ylim(-0.2, 1.3)
        self.canvas.draw()

    # --- Validation d'une lettre ---
    def valider_lettre(self, lettre):
        if lettre in self.lettres_devinees:
            messagebox.showinfo("Info", f"Vous avez déjà deviné '{lettre}'")
            return

        self.lettres_devinees.append(lettre)

        if lettre in self.mot_a_deviner:
            for i, l in enumerate(self.mot_a_deviner):
                if l == lettre:
                    self.mot_masque[i] = lettre
        else:
            self.nb_erreurs += 1

        self.afficher_pendu()
        self.verifier_fin_partie()

    # --- Vérification fin de partie ---
    def verifier_fin_partie(self):
        if "_" not in self.mot_masque:
            messagebox.showinfo("Félicitations", f"Vous avez trouvé le mot : {self.mot_a_deviner}")
            self.reinitialiser_jeu()
        elif self.nb_erreurs >= self.tentatives_max:
            messagebox.showinfo("Game Over", f"Le mot était : {self.mot_a_deviner}")
            self.reinitialiser_jeu()

    # --- Réinitialiser le jeu ---
    def reinitialiser_jeu(self):
        self.mot_a_deviner = random.choice(self.liste_mots)
        self.mot_masque = ["_" for _ in self.mot_a_deviner]
        self.nb_erreurs = 0
        self.lettres_devinees = []
        self.afficher_pendu()

# --- Lancer le jeu ---
if __name__ == "__main__":
    JeuPendu()
