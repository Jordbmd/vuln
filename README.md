# Application Web Vulnérable pour TP Sécurité

Ce projet contient une application web intentionnellement vulnérable et une collection de scripts de test de sécurité développés dans le cadre d'un TP sur les attaques web avancées. Ces outils permettent de démontrer et de tester différentes vulnérabilités de sécurité web courantes.

## Contenu du projet

Le projet est divisé en deux parties principales :

1. **Application vulnérable** - Une application Flask comportant diverses vulnérabilités
2. **Scripts de test de sécurité** - Une collection d'outils pour détecter et exploiter des vulnérabilités

## Application Vulnérable

L'application Flask démontre plusieurs vulnérabilités courantes :

- **Injection SQL** dans la page de connexion (/login)
- **Cross-Site Scripting (XSS)** dans la page de commentaires (/comment)

### Structure du projet

- `vuln.py` : Application principale Flask
- `vulnerable.db` : Base de données SQLite contenant les utilisateurs
- `templates/` : Contient les fichiers HTML
  - `index.html` : Page de connexion
  - `comment.html` : Page de commentaires
- `static/` : Contient les fichiers CSS
  - `style.css` : Styles de base pour l'application

### Installation et exécution

1. Installer les dépendances :

```bash
pip install -r requirements.txt
```

2. Exécuter l'application :

```bash
python vuln.py
```

3. Accéder à l'application dans votre navigateur :
   - `http://localhost:5000/login` - Page de connexion (vulnérable aux injections SQL)
   - `http://localhost:5000/comment` - Page de commentaires (vulnérable au XSS)

## Scripts de Test de Sécurité

### Prérequis

- Python 3.6+
- Module `requests` (`pip install requests`)

Pour activer l'environnement Python :

```bash
python-env
```

### Scripts disponibles

#### Injection SQL

1. **sqli_classic.py** - Test d'injections SQL classiques

   ```bash
   python sqli_classic.py [URL]
   # Exemple : python sqli_classic.py http://localhost:5000
   ```

   Ce script teste différentes charges utiles (payloads) d'injection SQL classiques, incluant :

   - Bypasses d'authentification (`' OR '1'='1`)
   - Commentaires SQL pour tronquer les requêtes (`--`, `#`)
   - Injections UNION pour extraire des données
   - Tests de privilèges et limitations

2. **blind_sqli.py** - Test d'injections SQL en aveugle basées sur le temps (time-based)

   ```bash
   python blind_sqli.py [URL]
   # Exemple : python blind_sqli.py http://localhost:5000
   ```

   Ce script détecte les vulnérabilités d'injection SQL en aveugle en mesurant les délais de réponse du serveur. Il utilise des techniques comme `SLEEP()` pour introduire des délais conditionnels.

3. **blind_sqli_improved.py** - Test d'injections SQL en aveugle basées sur les valeurs booléennes
   ```bash
   python blind_sqli_improved.py [URL]
   # Exemple : python blind_sqli_improved.py http://localhost:5000
   ```
   Version améliorée qui utilise des tests booléens (true/false) pour extraire progressivement des informations de la base de données. Compatible avec SQLite, cette version peut :
   - Compter le nombre de tables dans la base de données
   - Identifier le nom des tables
   - Extraire les noms d'utilisateurs et mots de passe

#### Inclusion de Fichiers Locaux (LFI)

4. **lfi_tester.py** - Test de vulnérabilités LFI

   ```bash
   python lfi_tester.py [URL] [paramètre]
   # Exemple : python lfi_tester.py http://localhost:5000/app page
   ```

   Ce script teste une variété de techniques pour exploiter les vulnérabilités d'inclusion de fichiers :

   - Traversée de répertoire (../, ../../, etc.)
   - Utilisation du null byte (%00)
   - Encodage URL et double encodage
   - Contournement de filtres

   Il recherche des fichiers sensibles couramment ciblés sur Linux et Windows.

#### Upload de Fichiers

5. **upload_tester.py** - Test de vulnérabilités d'upload de fichiers
   ```bash
   python upload_tester.py [URL] [champ_formulaire]
   # Exemple : python upload_tester.py http://localhost:5000/upload file
   ```
   Ce script teste des techniques avancées pour contourner les restrictions d'upload :
   - Manipulation des extensions de fichier (double extension, extensions inhabituelles)
   - Falsification des types MIME
   - Upload de webshells (PHP, ASP, JSP)
   - Utilisation d'en-têtes de fichiers trompeurs (GIF89a)

## Exemples d'exploitation

### Injection SQL

```
' OR '1'='1
admin' --
' UNION SELECT 1,2,3 --
```

### XSS

```
<script>alert('XSS')</script>
<img src="x" onerror="alert('XSS')">
```

## Contexte éducatif

Ce projet fait partie d'un TP sur les attaques web avancées, couvrant :

- Les injections SQL (classiques et en aveugle)
- Les failles d'inclusion de fichiers (LFI)
- Les failles d'upload de fichiers
- Les protections contre ces vulnérabilités

## Avertissement

Cette application est intentionnellement vulnérable et conçue uniquement à des fins éducatives. **NE PAS** déployer cette application dans un environnement de production ou sur un serveur accessible publiquement.

Ces scripts sont fournis à des fins éducatives et pour tester des applications dont vous avez l'autorisation de tester. **NE PAS** utiliser ces scripts contre des sites web sans autorisation explicite.
