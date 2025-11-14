# Environnement virtuel Python

Ce projet utilise **Python 3.11.9**.

Un environnement virtuel permet d'isoler les dépendances d'un projet Python pour éviter les conflits avec d'autres projets ou l'installation globale.

---

## 1. Création et activation de l'environnement virtuel

### Windows

```bash
# Crée un environnement virtuel nommé ".venv"
python -m venv .venv

# Active l'environnement virtuel
.venv\Scripts\activate
```

### Mac / Linux

```bash
# Crée un environnement virtuel nommé ".venv"
python -m venv .venv

# Active l'environnement virtuel
source .venv/bin/activate
```

> Une fois activé, le nom de l'environnement apparaît au début de votre terminal, par exemple `(.venv)`.

---

## 2. Gérer les dépendances

### Générer un fichier `requirements.txt`

```bash
# Liste toutes les librairies installées avec leurs versions
pip freeze > requirements.txt
```

### Installer depuis un fichier `requirements.txt`

```bash
# Installe toutes les dépendances listées
pip install -r requirements.txt
```

---

## 3. Conseils pratiques

* Toujours **activer l'environnement** avant d'installer des paquets.
* Avant de partager un projet ou de le versionner, mettez à jour `requirements.txt` avec `pip freeze`.
* Pour **désactiver l'environnement** :

```bash
deactivate
```
