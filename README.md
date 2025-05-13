# Application Web Vulnérable pour TP Sécurité

Ce projet est une application web intentionnellement vulnérable créée dans le cadre d'un TP sur la sécurité web. Elle illustre différentes vulnérabilités courantes telles que les injections SQL, XSS, et d'autres failles de sécurité web.

## Vulnérabilités implémentées

L'application contient les vulnérabilités suivantes :

1. **Injection SQL** : La page de connexion ne sanitize pas les entrées utilisateur, permettant des injections SQL classiques.
2. **Cross-Site Scripting (XSS)** : La fonctionnalité de commentaire n'échappe pas les entrées utilisateur, rendant possible les attaques XSS.

## Structure du projet

- `vuln.py` : Application principale Flask
- `vulnerable.db` : Base de données SQLite contenant les utilisateurs
- `templates/` : Contient les fichiers HTML
  - `index.html` : Page de connexion
  - `comment.html` : Page de commentaires
- `static/` : Contient les fichiers CSS
  - `style.css` : Styles de base pour l'application

## Installation et exécution

1. Cloner ce dépôt :

```bash
git clone [URL_DU_REPO]
cd [NOM_DU_REPO]
```

2. Installer les dépendances (Flask) :

```bash
pip install flask
```

3. Exécuter l'application :

```bash
python vuln.py
```

4. Accéder à l'application dans votre navigateur :
   - `http://localhost:5000/login` - Page de connexion (vulnérable aux injections SQL)
   - `http://localhost:5000/comment` - Page de commentaires (vulnérable au XSS)

## Avertissement

Cette application est intentionnellement vulnérable et est conçue uniquement à des fins éducatives. **NE PAS** déployer cette application dans un environnement de production ou sur un serveur accessible publiquement.

## Exemples d'exploitation

### Injection SQL

Essayez d'entrer `' OR '1'='1` comme nom d'utilisateur et n'importe quoi comme mot de passe.

### XSS

Essayez d'entrer `<script>alert('XSS')</script>` comme commentaire.

## Contexte éducatif

Ce projet fait partie d'un TP sur les attaques web avancées, couvrant :

- Les injections SQL (classiques et en aveugle)
- Les failles d'inclusion de fichiers (LFI)
- Les failles d'upload de fichiers
- Les protections contre ces vulnérabilités
