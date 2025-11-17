import random

# Nombre à deviner
nombre_a_deviner = random.randint(1, 100)

# Nombre maximum de tentatives
max_tentatives = 10

print("=== Jeu de devinettes ===")
print(f"Devinez le nombre entre 1 et 100. Vous avez {max_tentatives} tentatives.\n")

# Boucle pour les tentatives
for tentative in range(1, max_tentatives + 1):
    try:
        guess = int(input(f"Tentative {tentative}: Entrez votre nombre : "))
    except ValueError:
        print("Veuillez entrer un nombre valide.\n")
        continue

    if guess < 1 or guess > 100:
        print("Le nombre doit être entre 1 et 100.\n")
        continue

    if guess < nombre_a_deviner:
        print("C'est plus grand.\n")
    elif guess > nombre_a_deviner:
        print("C'est plus petit.\n")
    else:
        print(f"🎉 Bravo ! Vous avez deviné le nombre {nombre_a_deviner} en {tentative} tentatives !")
        break
else:
    print(f"😢 Vous avez épuisé vos {max_tentatives} tentatives. Le nombre était {nombre_a_deviner}.")
