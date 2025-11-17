import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Morpion:
    def __init__(self):
        self.grille = np.zeros((3,3), dtype=int)
        self.joueur = 'X'  # X commence
        self.joueur1 = "Joueur 1"
        self.joueur2 = "Joueur 2"

        self.root = tk.Tk()
        self.root.title("Jeu du Morpion")

        self.label_resultat = tk.Label(self.root, text=f"Tour de {self.joueur1}", font=("Arial",16))
        self.label_resultat.pack(pady=5)

        self.fig, self.ax = plt.subplots(figsize=(5,5))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack()
        self.canvas_widget.bind("<Button-1>", self.clic_canvas)

        # Centrer la fenêtre
        self.root.update_idletasks()
        self.root.eval('tk::PlaceWindow . center')

        # Fermeture propre
        self.root.protocol("WM_DELETE_WINDOW", self.fermer_fenetre)

        self.afficher_grille()
        self.root.mainloop()

    def afficher_grille(self):
        self.ax.clear()
        self.ax.axis('off')

        for i in range(1,3):
            self.ax.plot([i,i],[0,3],color='black', linewidth=3)
            self.ax.plot([0,3],[i,i],color='black', linewidth=3)

        for i in range(3):
            for j in range(3):
                if self.grille[i,j] == 1:
                    self.ax.text(j+0.5, i+0.5, 'X', fontsize=40, ha='center', va='center', color='blue')
                elif self.grille[i,j] == 2:
                    self.ax.text(j+0.5, i+0.5, 'O', fontsize=40, ha='center', va='center', color='red')

        self.ax.set_xlim(0,3)
        self.ax.set_ylim(0,3)
        self.ax.invert_yaxis()
        self.canvas.draw()

    def verifier_victoire(self, joueur):
        val = 1 if joueur == 'X' else 2
        for i in range(3):
            if np.all(self.grille[i,:]==val) or np.all(self.grille[:,i]==val):
                return True
        if np.all(np.diag(self.grille)==val) or np.all(np.diag(np.fliplr(self.grille))==val):
            return True
        return False

    def verifier_match_nul(self):
        return np.all(self.grille!=0)

    def clic_canvas(self, event):
        width, height = self.canvas_widget.winfo_width(), self.canvas_widget.winfo_height()
        x, y = event.x, event.y
        i = int(y / height * 3)
        j = int(x / width * 3)

        if self.grille[i,j]!=0:
            return

        self.grille[i,j] = 1 if self.joueur=='X' else 2
        self.afficher_grille()

        nom_joueur_courant = self.joueur1 if self.joueur=='X' else self.joueur2

        if self.verifier_victoire(self.joueur):
            self.label_resultat.config(text=f"{nom_joueur_courant} a gagné !")
            self.canvas_widget.unbind("<Button-1>")
        elif self.verifier_match_nul():
            self.label_resultat.config(text="Match nul !")
            self.canvas_widget.unbind("<Button-1>")
        else:
            self.joueur = 'O' if self.joueur=='X' else 'X'
            nom_joueur_suivant = self.joueur1 if self.joueur=='X' else self.joueur2
            self.label_resultat.config(text=f"Tour de {nom_joueur_suivant}")

    def fermer_fenetre(self):
        self.canvas_widget.destroy()
        plt.close(self.fig)
        self.root.destroy()

# --- Lancer le jeu ---
if __name__ == "__main__":
    Morpion()
