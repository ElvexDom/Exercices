import random

# Choix possibles
choix_possibles = ["pierre", "feuille", "ciseaux"]

# Scores : joueur et ordinateur
score_joueur = 0
score_ordi = 0

def determiner_gagnant(joueur, ordinateur):
    if joueur == ordinateur:
        return "égalité"
    elif (joueur == "pierre" and ordinateur == "ciseaux") \
         or (joueur == "feuille" and ordinateur == "pierre") \
         or (joueur == "ciseaux" and ordinateur == "feuille"):
        return "joueur"
    else:
        return "ordinateur"

print("=== Jeu Pierre - Feuille - Ciseaux ===")
print("Premier à 3 victoires gagne la partie.\n")

# Boucle de jeu jusqu'à 3 victoires
while score_joueur < 3 and score_ordi < 3:

    joueur = input("Votre choix (pierre / feuille / ciseaux) : ").lower()

    if joueur not in choix_possibles:
        print("Choix invalide, réessayez.\n")
        continue

    ordinateur = random.choice(choix_possibles)
    print(f"L'ordinateur a choisi : {ordinateur}")

    resultat = determiner_gagnant(joueur, ordinateur)

    if resultat == "joueur":
        print("Vous gagnez cette manche !\n")
        score_joueur += 1
    elif resultat == "ordinateur":
        print("L'ordinateur gagne cette manche !\n")
        score_ordi += 1
    else:
        print("Égalité.\n")

    print(f"Score actuel – Vous : {score_joueur} | Ordinateur : {score_ordi}\n")

# Résultat final
print("=== Fin du jeu ===")
if score_joueur == 3:
    print("🎉 Vous avez gagné la partie !")
else:
    print("🤖 L'ordinateur a gagné la partie !")
