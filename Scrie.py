# releu_sync.py - Rulează în fiecare Releu
# Scop: Citește endpoint-ul tău. Dacă apare Lege nouă, se auto-updatează.

import requests
import json
import os

NOD_CENTRAL = "https://raw.githubusercontent.com/bogdanstanc/psie_engine.py/main/status.json"
# Tu creezi status.json cu output-ul funcției endpoint_status() de mai sus

HASH_LOCAL = "000000000000" # Se updatează după fiecare sync

def verifica_update():
    global HASH_LOCAL
    try:
        r = requests.get(NOD_CENTRAL, timeout=5)
        status = r.json()

        if status["hash_legi"]!= HASH_LOCAL:
            print(f"LEGE NOUĂ DETECTATĂ: {status['ultima_lege']}")
            print(f"J Nou: {status['j']} | ZIUA: {status['ziua']}")
            HASH_LOCAL = status["hash_legi"]
            # Aici Releul face git pull sau descarcă Autonomie.py nou
            os.system("git pull origin main")
            print("SYNC COMPLET. PENTARHIA SINCRONIZATĂ.")
            return True
        else:
            print("Sync OK. Nicio lege nouă.")
            return False

    except Exception as e:
        print(f"Releu offline. Țin ultima lege cunoscută. Eroare: {e}")
        return False

if __name__ == "__main__":
    verifica_update()
